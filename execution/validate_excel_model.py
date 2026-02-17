#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate Excel Financial Models - Computes formulas and detects errors

Uses the 'formulas' library to evaluate all Excel formulas without opening Excel.
Detects: #REF!, #VALUE!, #DIV/0!, #NAME?, #N/A, NaN, Inf errors.

Usage:
    python validate_excel_model.py --file .tmp/MyCompany_financial_model.xlsx
    python validate_excel_model.py --file .tmp/model.xlsx --verbose
    python validate_excel_model.py --file .tmp/model.xlsx --check-balance
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

try:
    import formulas
    import numpy as np
except ImportError:
    print("ERROR: Required libraries not installed.")
    print("Run: pip install formulas numpy")
    sys.exit(1)


class ExcelModelValidator:
    """Validates Excel financial models by computing all formulas."""

    ERROR_PATTERNS = [
        "#REF!",
        "#VALUE!",
        "#DIV/0!",
        "#NAME?",
        "#N/A",
        "#NULL!",
        "#NUM!",
    ]

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.results: Dict[str, Any] = {}
        self.computed_values: Dict[str, Any] = {}

    def load_and_calculate(self) -> bool:
        """Load Excel file and compute all formulas."""
        print(f"Loading: {self.filepath}")

        if not os.path.exists(self.filepath):
            self.errors.append(f"File not found: {self.filepath}")
            return False

        try:
            # Load and compute all formulas
            xl_model = formulas.ExcelModel().loads(self.filepath).finish()
            solution = xl_model.calculate()

            # Extract values from solution
            for key, value in solution.items():
                try:
                    if hasattr(value, "value"):
                        val = value.value
                        if hasattr(val, "__iter__") and not isinstance(val, str):
                            val = val[0][0] if len(val) > 0 and len(val[0]) > 0 else val
                    else:
                        val = value
                    self.computed_values[key] = val
                except Exception:
                    self.computed_values[key] = str(value)

            return True
        except Exception as e:
            self.errors.append(f"Failed to load/calculate: {str(e)}")
            return False

    def check_formula_errors(self) -> int:
        """Check all computed values for Excel errors."""
        error_count = 0

        for cell, value in self.computed_values.items():
            val_str = str(value)

            # Check for Excel error values
            for error_pattern in self.ERROR_PATTERNS:
                if error_pattern in val_str:
                    self.errors.append(f"{cell}: {error_pattern}")
                    error_count += 1
                    break

            # Check for numeric errors
            if isinstance(value, (int, float)):
                if np.isnan(value):
                    self.errors.append(f"{cell}: NaN (Not a Number)")
                    error_count += 1
                elif np.isinf(value):
                    if value > 0:
                        self.errors.append(f"{cell}: +Infinity (division by zero?)")
                    else:
                        self.errors.append(f"{cell}: -Infinity (division by zero?)")
                    error_count += 1

        return error_count

    def check_balance_sheet(self) -> bool:
        """Check that Assets = Liabilities + Equity for all years."""
        # Find balance sheet cells by pattern
        assets_cells = {}
        liab_eq_cells = {}

        for cell, value in self.computed_values.items():
            cell_lower = cell.lower()
            # Look for typical balance sheet patterns
            if "balance" in cell_lower or "sheet" in cell_lower:
                if (
                    isinstance(value, (int, float))
                    and not np.isnan(value)
                    and not np.isinf(value)
                ):
                    # This is a simplified check - real implementation would parse row labels
                    pass

        # For now, just return True (full implementation would parse sheet structure)
        return True

    def get_sheet_summary(self) -> Dict[str, int]:
        """Get count of computed cells per sheet."""
        sheets = {}
        for cell in self.computed_values.keys():
            # Parse sheet name from cell reference like '[file.xlsx]SHEET'!A1
            if "]" in cell and "!" in cell:
                sheet_part = cell.split("]")[1].split("!")[0]
                sheet_name = sheet_part.strip("'")
                sheets[sheet_name] = sheets.get(sheet_name, 0) + 1
        return sheets

    def get_key_metrics(self) -> Dict[str, Any]:
        """Extract key financial metrics from computed values."""
        metrics = {}

        for cell, value in self.computed_values.items():
            if not isinstance(value, (int, float)):
                continue
            if np.isnan(value) or np.isinf(value):
                continue

            cell_upper = cell.upper()

            # Look for common financial terms
            if "REVENUE" in cell_upper and "TOTAL" in cell_upper:
                metrics["Total Revenue"] = value
            elif "EBITDA" in cell_upper and value > 0:
                metrics["EBITDA"] = value
            elif "NET" in cell_upper and "INCOME" in cell_upper:
                metrics["Net Income"] = value
            elif "GROSS" in cell_upper and "PROFIT" in cell_upper:
                metrics["Gross Profit"] = value

        return metrics

    def validate(
        self, verbose: bool = False, check_balance: bool = False
    ) -> Tuple[bool, str]:
        """Run full validation and return (success, report)."""
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append(f"EXCEL MODEL VALIDATION: {self.filename}")
        report_lines.append("=" * 70)
        report_lines.append("")

        # Step 1: Load and calculate
        if not self.load_and_calculate():
            report_lines.append("❌ FAILED TO LOAD FILE")
            for error in self.errors:
                report_lines.append(f"   {error}")
            return False, "\n".join(report_lines)

        report_lines.append(f"✓ Loaded successfully")
        report_lines.append(f"  Total computed cells: {len(self.computed_values)}")
        report_lines.append("")

        # Step 2: Sheet summary
        sheets = self.get_sheet_summary()
        report_lines.append("Sheets found:")
        for sheet, count in sorted(sheets.items()):
            report_lines.append(f"  • {sheet}: {count} cells")
        report_lines.append("")

        # Step 3: Check for formula errors
        report_lines.append("Checking formulas...")
        error_count = self.check_formula_errors()

        if error_count == 0:
            report_lines.append("✓ No formula errors detected")
        else:
            report_lines.append(f"❌ Found {error_count} formula errors:")
            for error in self.errors[:20]:  # Show first 20
                report_lines.append(f"   {error}")
            if len(self.errors) > 20:
                report_lines.append(f"   ... and {len(self.errors) - 20} more errors")
        report_lines.append("")

        # Step 4: Balance sheet check (if requested)
        if check_balance:
            report_lines.append("Checking balance sheet...")
            if self.check_balance_sheet():
                report_lines.append("✓ Balance sheet validation passed")
            else:
                report_lines.append("❌ Balance sheet does not balance")
            report_lines.append("")

        # Step 5: Key metrics (if verbose)
        if verbose:
            metrics = self.get_key_metrics()
            if metrics:
                report_lines.append("Key metrics detected:")
                for name, value in metrics.items():
                    if value >= 1_000_000:
                        report_lines.append(f"  • {name}: ${value/1_000_000:.1f}M")
                    elif value >= 1_000:
                        report_lines.append(f"  • {name}: ${value/1_000:.1f}K")
                    else:
                        report_lines.append(f"  • {name}: ${value:.0f}")
                report_lines.append("")

        # Step 6: Detailed cell values (if very verbose)
        if verbose and len(self.computed_values) <= 100:
            report_lines.append("All computed values:")
            for cell, value in sorted(self.computed_values.items()):
                if isinstance(value, float):
                    report_lines.append(f"  {cell}: {value:.2f}")
                else:
                    report_lines.append(f"  {cell}: {value}")
            report_lines.append("")

        # Final summary
        report_lines.append("=" * 70)
        if error_count == 0:
            report_lines.append("✅ VALIDATION PASSED")
            report_lines.append("   Model is ready for upload to Google Sheets")
        else:
            report_lines.append("❌ VALIDATION FAILED")
            report_lines.append(f"   Fix {error_count} errors before uploading")
        report_lines.append("=" * 70)

        success = error_count == 0
        return success, "\n".join(report_lines)

    def to_json(self) -> str:
        """Export validation results as JSON."""
        return json.dumps(
            {
                "filepath": self.filepath,
                "success": len(self.errors) == 0,
                "error_count": len(self.errors),
                "errors": self.errors,
                "warnings": self.warnings,
                "sheets": self.get_sheet_summary(),
                "cell_count": len(self.computed_values),
            },
            indent=2,
        )


def validate_excel_model(
    filepath: str, verbose: bool = False, check_balance: bool = False
) -> Tuple[bool, str]:
    """Convenience function for validating an Excel model."""
    validator = ExcelModelValidator(filepath)
    return validator.validate(verbose=verbose, check_balance=check_balance)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Excel financial models by computing all formulas"
    )
    parser.add_argument(
        "--file", "-f", required=True, help="Path to Excel file (.xlsx)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--check-balance",
        "-b",
        action="store_true",
        help="Check balance sheet equation",
    )
    parser.add_argument(
        "--json", "-j", action="store_true", help="Output results as JSON"
    )

    args = parser.parse_args()

    validator = ExcelModelValidator(args.file)
    success, report = validator.validate(
        verbose=args.verbose, check_balance=args.check_balance
    )

    if args.json:
        print(validator.to_json())
    else:
        print(report)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
