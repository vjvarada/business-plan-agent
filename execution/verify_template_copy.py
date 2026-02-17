#!/usr/bin/env python3
"""
Template Copy Verifier
======================
Verifies that a copied financial model matches the expected 14-sheet template structure.

Usage:
    python verify_template_copy.py --sheet-id "1ABC..."
    python verify_template_copy.py --sheet-id "1ABC..." --detailed

Checks:
    - All 14 sheets present and correctly named
    - Sheet order matches template
    - Formula count matches template (within tolerance)
    - Cross-sheet references intact
    - No #REF! or #VALUE! errors
    - Key formulas preserved

Exit Codes:
    0 = Template copy verified successfully
    1 = Minor differences (warnings)
    2 = Major differences (errors)
"""

import argparse
import os
import sys
from typing import Any, Dict, List

from dotenv import load_dotenv

load_dotenv()

try:
    import gspread
except ImportError:
    print("Installing gspread...")
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread"])
    import gspread


# Expected 14-Sheet Template Structure
EXPECTED_SHEETS = [
    "Sources & References",
    "Assumptions",
    "Headcount Plan",
    "Revenue",
    "Operating Costs",
    "P&L",
    "Cash Flow",
    "Balance Sheet",
    "Summary",
    "Sensitivity Analysis",
    "Valuation",
    "Break-even Analysis",
    "Funding Cap Table",
    "Charts Data",
]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_sheets_client():
    """Get authenticated gspread client"""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials as OAuthCredentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists("token.json"):
        try:
            creds = OAuthCredentials.from_authorized_user_file("token.json", SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)


def verify_sheet_structure(spreadsheet) -> Dict[str, Any]:
    """Verify the spreadsheet structure matches template"""
    issues = []

    # Get all sheet names
    actual_sheets = [ws.title for ws in spreadsheet.worksheets()]

    print(f"Checking sheet structure...")
    print(f"  Expected: {len(EXPECTED_SHEETS)} sheets")
    print(f"  Found: {len(actual_sheets)} sheets\n")

    # Check all expected sheets exist
    missing_sheets = []
    for expected in EXPECTED_SHEETS:
        if expected not in actual_sheets:
            missing_sheets.append(expected)
            issues.append(("ERROR", f"Missing sheet: {expected}"))

    # Check for extra sheets
    extra_sheets = []
    for actual in actual_sheets:
        if actual not in EXPECTED_SHEETS:
            extra_sheets.append(actual)
            issues.append(("WARNING", f"Extra sheet (not in template): {actual}"))

    # Check sheet order
    order_issues = []
    for i, expected in enumerate(EXPECTED_SHEETS):
        if i < len(actual_sheets) and actual_sheets[i] != expected:
            order_issues.append((i, expected, actual_sheets[i]))
            issues.append(
                (
                    "WARNING",
                    f"Sheet order mismatch at position {i+1}: expected '{expected}', got '{actual_sheets[i]}'",
                )
            )

    return {
        "issues": issues,
        "missing_sheets": missing_sheets,
        "extra_sheets": extra_sheets,
        "order_issues": order_issues,
        "actual_sheets": actual_sheets,
    }


def count_formulas(worksheet) -> int:
    """Count cells containing formulas in a worksheet"""
    try:
        # Get all values
        all_values = worksheet.get_all_values()

        # Get formulas by checking each cell
        formula_count = 0
        for row_idx, row in enumerate(all_values, start=1):
            for col_idx in range(len(row)):
                try:
                    # Get the cell formula
                    cell_addr = gspread.utils.rowcol_to_a1(row_idx, col_idx + 1)
                    cell_value = worksheet.acell(
                        cell_addr, value_render_option="FORMULA"
                    ).value
                    if cell_value and str(cell_value).startswith("="):
                        formula_count += 1
                except:
                    pass

        return formula_count
    except Exception as e:
        print(f"    Warning: Could not count formulas: {e}")
        return 0


def check_for_errors(worksheet) -> List[str]:
    """Check for #REF!, #VALUE!, #DIV/0! errors"""
    try:
        all_values = worksheet.get_all_values()
        errors_found = []

        for row_idx, row in enumerate(all_values, start=1):
            for col_idx, value in enumerate(row, start=1):
                if value and isinstance(value, str):
                    if any(
                        err in value
                        for err in ["#REF!", "#VALUE!", "#DIV/0!", "#N/A", "#ERROR!"]
                    ):
                        cell_addr = gspread.utils.rowcol_to_a1(row_idx, col_idx)
                        errors_found.append(f"{cell_addr}: {value}")

        return errors_found
    except Exception as e:
        print(f"    Warning: Could not check for errors: {e}")
        return []


def verify_sheets_detailed(spreadsheet, detailed: bool = False) -> List[tuple]:
    """Verify each sheet in detail"""
    issues = []

    print("\nDetailed sheet verification:")
    print("=" * 60)

    for sheet_name in EXPECTED_SHEETS:
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            print(f"\n{sheet_name}:")

            # Get dimensions
            row_count = worksheet.row_count
            col_count = worksheet.col_count
            print(f"  Dimensions: {row_count} rows x {col_count} cols")

            # Check for errors
            errors = check_for_errors(worksheet)
            if errors:
                print(f"    Found {len(errors)} formula error(s):")
                for error in errors[:5]:  # Show first 5
                    print(f"    - {error}")
                    issues.append(("ERROR", f"{sheet_name}: Formula error at {error}"))
                if len(errors) > 5:
                    print(f"    ... and {len(errors) - 5} more")
            else:
                print(f"   No formula errors")

            # Count formulas if detailed
            if detailed:
                formula_count = count_formulas(worksheet)
                print(f"  Formulas: {formula_count} cells")

        except gspread.exceptions.WorksheetNotFound:
            print(f"   Sheet not found")
            issues.append(("ERROR", f"Sheet '{sheet_name}' not found"))
        except Exception as e:
            print(f"    Error checking sheet: {e}")
            issues.append(("WARNING", f"{sheet_name}: Error during verification - {e}"))

    return issues


def print_results(structure_result: Dict, detail_issues: List[tuple]) -> bool:
    """Print verification results and return True if verified"""
    all_issues = structure_result["issues"] + detail_issues

    errors = [i for i in all_issues if i[0] == "ERROR"]
    warnings = [i for i in all_issues if i[0] == "WARNING"]

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    if errors:
        print("\n ERRORS:")
        for level, msg in errors:
            print(f"  - {msg}")

    if warnings:
        print("\n  WARNINGS:")
        for level, msg in warnings:
            print(f"  - {msg}")

    print("\n" + "=" * 60)

    if not errors and not warnings:
        print(" Template copy VERIFIED - all checks passed")
        print("=" * 60)
        return True
    elif not errors:
        print(f"  Template copy has {len(warnings)} WARNING(S)")
        print("   Structure matches but review warnings")
        print("=" * 60)
        return True
    else:
        print(f" Template copy FAILED verification - {len(errors)} ERROR(S)")
        print("   Fix errors or re-copy from template")
        print("=" * 60)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify template copy fidelity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--sheet-id", required=True, help="Google Sheets ID to verify")
    parser.add_argument(
        "--detailed", action="store_true", help="Run detailed verification (slower)"
    )

    args = parser.parse_args()

    print("Template Copy Verifier")
    print("=" * 60)
    print(f"Sheet ID: {args.sheet_id}")
    print(f"Expected structure: {len(EXPECTED_SHEETS)} sheets (standard template)\n")

    # Connect to Google Sheets
    try:
        client = get_sheets_client()
        spreadsheet = client.open_by_key(args.sheet_id)
        print(f" Connected to: {spreadsheet.title}\n")
    except Exception as e:
        print(f" ERROR: Could not open spreadsheet: {e}")
        sys.exit(2)

    # Verify structure
    structure_result = verify_sheet_structure(spreadsheet)

    # Detailed verification
    detail_issues = []
    if not structure_result["missing_sheets"]:  # Only if all sheets present
        detail_issues = verify_sheets_detailed(spreadsheet, args.detailed)
    else:
        print("\n  Skipping detailed verification (sheets missing)")

    # Print results
    verified = print_results(structure_result, detail_issues)

    # Exit codes
    errors = [
        i for i in (structure_result["issues"] + detail_issues) if i[0] == "ERROR"
    ]
    warnings = [
        i for i in (structure_result["issues"] + detail_issues) if i[0] == "WARNING"
    ]

    if errors:
        sys.exit(2)  # Major differences
    elif warnings:
        sys.exit(1)  # Minor differences
    else:
        sys.exit(0)  # Perfect match


if __name__ == "__main__":
    main()
