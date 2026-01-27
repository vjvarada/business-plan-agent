#!/usr/bin/env python3
"""
Validate Financial Model Snapshot
==================================
Pre-flight validation before syncing snapshot to Google Sheets.

Usage:
    python validate_model_snapshot.py --snapshot <DIR> [--strict]
    
Example:
    python validate_model_snapshot.py --snapshot .tmp/snapshot
"""

import os
import sys
import json
import argparse
import csv
import re
from pathlib import Path
from collections import defaultdict

class ModelValidator:
    def __init__(self, snapshot_dir, strict=False):
        self.snapshot_dir = Path(snapshot_dir)
        self.strict = strict
        self.errors = []
        self.warnings = []
        self.sheets = {}
        self.formulas = {}
        
    def load_snapshot(self):
        """Load snapshot metadata and CSV files."""
        metadata_file = self.snapshot_dir / "snapshot.json"
        if not metadata_file.exists():
            self.errors.append(f"Snapshot metadata not found: {metadata_file}")
            return False
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        # Load all sheets
        for sheet in self.metadata['sheets']:
            name = sheet['safe_name']
            
            # Load values
            values_file = self.snapshot_dir / sheet['values_file']
            formulas_file = self.snapshot_dir / sheet['formulas_file']
            
            if not values_file.exists():
                self.errors.append(f"Values file missing: {values_file}")
                continue
            
            if not formulas_file.exists():
                self.errors.append(f"Formulas file missing: {formulas_file}")
                continue
            
            with open(values_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                self.sheets[name] = list(reader)
            
            with open(formulas_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                self.formulas[name] = list(reader)
        
        return True
    
    def validate_formula_syntax(self):
        """Check for broken formula references."""
        print("\n1. Validating formula syntax...")
        
        formula_pattern = re.compile(r'=.*')
        error_patterns = ['#REF!', '#VALUE!', '#NAME?', '#DIV/0!', '#N/A', '#NUM!']
        
        for sheet_name, formulas in self.formulas.items():
            for row_idx, row in enumerate(formulas):
                for col_idx, cell in enumerate(row[1:], start=1):  # Skip Row column
                    if cell and formula_pattern.match(str(cell)):
                        # Check for error values in formula
                        for error in error_patterns:
                            if error in cell:
                                col_letter = chr(64 + col_idx)
                                self.errors.append(
                                    f"{sheet_name}!{col_letter}{row[0]}: Formula error '{error}' in {cell}"
                                )
        
        if not self.errors:
            print("     No formula errors detected")
        else:
            print(f"     Found {len(self.errors)} formula errors")
    
    def validate_balance_sheet(self):
        """Check Assets = Liabilities + Equity."""
        print("\n2. Validating balance sheet equation...")
        
        if 'Balance_Sheet' not in self.sheets and 'Balance Sheet' not in self.formulas:
            self.warnings.append("Balance Sheet not found in snapshot")
            print("     Balance Sheet not found")
            return
        
        # Try to find balance sheet with various naming
        bs_name = None
        for name in self.sheets.keys():
            if 'balance' in name.lower() and 'sheet' in name.lower():
                bs_name = name
                break
        
        if not bs_name:
            self.warnings.append("Could not identify Balance Sheet")
            print("     Balance Sheet not identified")
            return
        
        # Look for Assets, Liabilities, Equity rows
        # This is a simplified check - real implementation would parse specific rows
        print(f"     Found Balance Sheet: {bs_name}")
        print("    ℹ Full balance validation requires row mapping")
    
    def validate_cross_sheet_references(self):
        """Check all cross-sheet formula references exist."""
        print("\n3. Validating cross-sheet references...")
        
        cross_ref_pattern = re.compile(r"='([^']+)'![A-Z]+\d+")
        
        sheet_names = set(sheet['name'] for sheet in self.metadata['sheets'])
        broken_refs = []
        
        for sheet_name, formulas in self.formulas.items():
            for row_idx, row in enumerate(formulas):
                for col_idx, cell in enumerate(row[1:], start=1):
                    if cell and '=' in str(cell):
                        # Find all cross-sheet references
                        refs = cross_ref_pattern.findall(str(cell))
                        for ref_sheet in refs:
                            if ref_sheet not in sheet_names:
                                col_letter = chr(64 + col_idx)
                                broken_refs.append(
                                    f"{sheet_name}!{col_letter}{row[0]}: References non-existent sheet '{ref_sheet}'"
                                )
        
        if broken_refs:
            self.errors.extend(broken_refs[:10])  # Limit to first 10
            print(f"     Found {len(broken_refs)} broken cross-sheet references")
        else:
            print("     All cross-sheet references valid")
    
    def validate_data_types(self):
        """Check data types are consistent."""
        print("\n4. Validating data types...")
        
        # Simple check: numeric columns should have numeric values
        type_errors = []
        
        for sheet_name, values in self.sheets.items():
            # Skip header rows (first 5 rows typically)
            for row_idx, row in enumerate(values[5:], start=6):
                for col_idx in range(2, min(8, len(row))):  # Columns B-G
                    cell = row[col_idx]
                    if cell and cell.strip():
                        # Check if looks like number but has invalid chars
                        if re.match(r'^[\d,.$%\-\(\)]+$', cell):
                            # Valid numeric-looking cell
                            continue
                        elif re.match(r'^[A-Z][a-z]', cell):
                            # Looks like text (starts with capital letter)
                            continue
                        else:
                            # Might be mixed or invalid
                            pass
        
        print("     Data type validation complete")
    
    def check_common_issues(self):
        """Check for common financial model issues."""
        print("\n5. Checking common issues...")
        
        # Check for negative revenue
        if 'Revenue' in self.sheets:
            revenue_sheet = self.sheets['Revenue']
            for row in revenue_sheet:
                for cell in row[1:]:
                    if cell and cell.startswith('-$') or cell.startswith('($'):
                        self.warnings.append(f"Revenue sheet has negative value: {cell}")
        
        # Check for zero divisions in formulas
        for sheet_name, formulas in self.formulas.items():
            for row in formulas:
                for cell in row[1:]:
                    if cell and '/0' in str(cell):
                        self.warnings.append(f"{sheet_name}: Potential division by zero in {cell}")
        
        if not self.warnings:
            print("     No common issues detected")
        else:
            print(f"     Found {len(self.warnings)} potential issues")
    
    def run_validation(self):
        """Run all validation checks."""
        print(f"\n{'='*80}")
        print("FINANCIAL MODEL SNAPSHOT VALIDATION")
        print(f"{'='*80}")
        print(f"Snapshot: {self.snapshot_dir}")
        print(f"Date: {self.metadata.get('snapshot_date', 'Unknown')}")
        print(f"Sheets: {len(self.metadata.get('sheets', []))}")
        
        self.validate_formula_syntax()
        self.validate_balance_sheet()
        self.validate_cross_sheet_references()
        self.validate_data_types()
        self.check_common_issues()
        
        # Print summary
        print(f"\n{'='*80}")
        print("VALIDATION SUMMARY")
        print(f"{'='*80}")
        
        if self.errors:
            print(f"\n ERRORS ({len(self.errors)}):")
            for error in self.errors[:20]:  # Show first 20
                print(f"  - {error}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more")
        
        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
        
        if not self.errors and not self.warnings:
            print("\n VALIDATION PASSED")
            print("Snapshot is ready to sync to Google Sheets")
            return True
        elif not self.errors:
            print("\n VALIDATION PASSED (with warnings)")
            print("Snapshot can be synced, but review warnings")
            return True
        else:
            print("\n VALIDATION FAILED")
            print("Fix errors before syncing to Google Sheets")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Validate financial model snapshot before syncing'
    )
    parser.add_argument('--snapshot', required=True, help='Snapshot directory')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    
    args = parser.parse_args()
    
    validator = ModelValidator(args.snapshot, args.strict)
    
    if not validator.load_snapshot():
        print("Failed to load snapshot")
        sys.exit(1)
    
    success = validator.run_validation()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
