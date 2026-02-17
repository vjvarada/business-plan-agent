#!/usr/bin/env python3
"""
Financial Model Repair Tool
===========================
Fixes common issues in Google Sheets financial models that occur during creation.
This tool consolidates learnings from repeated model fixes.

Usage:
    python repair_financial_model.py --sheet-id "1ABC..." --action all
    python repair_financial_model.py --sheet-id "1ABC..." --action fix-formulas
    python repair_financial_model.py --sheet-id "1ABC..." --action fix-formatting
    python repair_financial_model.py --sheet-id "1ABC..." --action fix-balance-sheet
    python repair_financial_model.py --sheet-id "1ABC..." --action fix-cash-flow
    python repair_financial_model.py --sheet-id "1ABC..." --action fix-funding
    python repair_financial_model.py --sheet-id "1ABC..." --action trim-years --years 5
    python repair_financial_model.py --sheet-id "1ABC..." --action rebalance-sm --target-pct 35

Actions:
    fix-formulas     - Check and fix formula errors (#REF!, #VALUE!, etc.)
    fix-formatting   - Apply consistent number/currency/percentage formatting
    fix-balance-sheet - Ensure A = L + E identity with proper links
    fix-cash-flow    - Link cash flow to P&L, funding, and balance sheet
    fix-funding      - Fix funding schedule and cap table calculations
    trim-years       - Trim model to specified number of years
    rebalance-sm     - Rebalance S&M spend to target percentage of revenue
    verify-links     - Verify all cross-sheet formula links
    all             - Run all fixes in sequence
"""

import argparse
import os
import sys
import time
from typing import List, Dict, Tuple
from dotenv import load_dotenv

load_dotenv()

try:
    import gspread
    from gspread_formatting import CellFormat, NumberFormat, format_cell_range
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread", "gspread-formatting"])
    import gspread
    from gspread_formatting import CellFormat, NumberFormat, format_cell_range


# Constants
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Number formats
FORMAT_CURRENCY = CellFormat(numberFormat=NumberFormat(type='CURRENCY', pattern='$#,##0'))
FORMAT_CURRENCY_K = CellFormat(numberFormat=NumberFormat(type='NUMBER', pattern='$#,##0,"K"'))
FORMAT_CURRENCY_M = CellFormat(numberFormat=NumberFormat(type='NUMBER', pattern='$#,##0,,"M"'))
FORMAT_PERCENT = CellFormat(numberFormat=NumberFormat(type='PERCENT', pattern='0.0%'))
FORMAT_NUMBER = CellFormat(numberFormat=NumberFormat(type='NUMBER', pattern='#,##0'))
FORMAT_DECIMAL = CellFormat(numberFormat=NumberFormat(type='NUMBER', pattern='#,##0.0'))

# Error values to check
ERROR_VALUES = ['#REF!', '#NAME?', '#VALUE!', '#DIV/0!', '#ERROR!', '#N/A']


def get_sheets_client():
    """Get authenticated gspread client"""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return gspread.authorize(creds)


def rate_limit(seconds=1):
    """Rate limit API calls"""
    time.sleep(seconds)


def find_row_by_label(data: List[List], label: str, partial: bool = True) -> int:
    """Find row index (0-based) by label"""
    for i, row in enumerate(data):
        if row and row[0]:
            cell = str(row[0]).lower()
            if partial and label.lower() in cell:
                return i
            elif not partial and cell == label.lower():
                return i
    return -1


def col_letter(n: int) -> str:
    """Convert column number (1-indexed) to letter"""
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


# ============ FIX FUNCTIONS ============

def fix_formulas(spreadsheet) -> Dict:
    """Find and report formula errors"""
    print("\n" + "=" * 60)
    print("CHECKING FOR FORMULA ERRORS")
    print("=" * 60)
    
    errors_found = {}
    total_errors = 0
    
    for ws in spreadsheet.worksheets():
        rate_limit(0.5)
        data = ws.get_all_values()
        sheet_errors = []
        
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                if cell in ERROR_VALUES:
                    sheet_errors.append({
                        'row': i + 1,
                        'col': col_letter(j + 1),
                        'error': cell
                    })
        
        if sheet_errors:
            errors_found[ws.title] = sheet_errors
            total_errors += len(sheet_errors)
            print(f"\n{ws.title}: {len(sheet_errors)} errors")
            for err in sheet_errors[:5]:
                print(f"  {err['col']}{err['row']}: {err['error']}")
            if len(sheet_errors) > 5:
                print(f"  ... and {len(sheet_errors) - 5} more")
    
    if total_errors == 0:
        print("\nNo formula errors found!")
    else:
        print(f"\nTotal errors found: {total_errors}")
    
    return errors_found


def fix_formatting(spreadsheet) -> bool:
    """Apply consistent formatting across all sheets"""
    print("\n" + "=" * 60)
    print("FIXING NUMBER FORMATTING")
    print("=" * 60)
    
    # Sheet-specific formatting rules
    formatting_rules = {
        'Revenue': [('C3:M20', FORMAT_CURRENCY_K)],
        'Operating Costs': [('C3:M30', FORMAT_CURRENCY_K)],
        'P&L': [
            ('C3:M5', FORMAT_CURRENCY_K),   # Revenue, COGS, Gross Profit
            ('C6:M6', FORMAT_PERCENT),       # Gross Margin %
            ('C7:M11', FORMAT_CURRENCY_K),  # OpEx, EBITDA
            ('C12:M12', FORMAT_PERCENT),    # EBITDA Margin %
            ('C13:M17', FORMAT_CURRENCY_K), # D&A to Net Income
            ('C18:M18', FORMAT_PERCENT),    # Net Margin %
        ],
        'Cash Flow': [('C3:M20', FORMAT_CURRENCY_K)],
        'Balance Sheet': [('C3:M25', FORMAT_CURRENCY_K)],
        'Customer Economics': [
            ('C3:M4', FORMAT_CURRENCY),     # CAC, LTV
            ('C5:M5', FORMAT_DECIMAL),      # LTV:CAC ratio
            ('C6:M6', FORMAT_NUMBER),       # Payback months
        ],
    }
    
    for sheet_name, rules in formatting_rules.items():
        try:
            ws = spreadsheet.worksheet(sheet_name)
            print(f"\nFormatting {sheet_name}...")
            
            for range_str, fmt in rules:
                rate_limit(0.5)
                format_cell_range(ws, range_str, fmt)
                print(f"  Applied format to {range_str}")
            
        except gspread.WorksheetNotFound:
            print(f"  Skipped {sheet_name} (not found)")
        except Exception as e:
            print(f"  Error on {sheet_name}: {e}")
    
    return True


def fix_balance_sheet(spreadsheet) -> bool:
    """Fix balance sheet links and ensure A = L + E"""
    print("\n" + "=" * 60)
    print("FIXING BALANCE SHEET")
    print("=" * 60)
    
    try:
        bs = spreadsheet.worksheet('Balance Sheet')
        rate_limit(1)
        data = bs.get_all_values()
        
        # Find key rows
        cash_row = find_row_by_label(data, 'cash')
        equity_row = find_row_by_label(data, 'equity')
        retained_row = find_row_by_label(data, 'retained')
        total_assets_row = find_row_by_label(data, 'total assets')
        total_liab_row = find_row_by_label(data, 'total liabilities')
        check_row = find_row_by_label(data, 'check')
        
        print(f"Found rows - Cash: {cash_row+1}, Equity: {equity_row+1}, Retained: {retained_row+1}")
        
        # Fix Cash row - link to Cash Flow cumulative
        if cash_row >= 0:
            # Find cumulative cash row in Cash Flow
            cf = spreadsheet.worksheet('Cash Flow')
            rate_limit(0.5)
            cf_data = cf.get_all_values()
            cum_cash_row = find_row_by_label(cf_data, 'cumulative')
            if cum_cash_row < 0:
                cum_cash_row = find_row_by_label(cf_data, 'closing')
            
            if cum_cash_row >= 0:
                cells = []
                for col in range(3, 14):
                    col_l = col_letter(col)
                    cells.append(gspread.Cell(cash_row + 1, col, f"='Cash Flow'!{col_l}{cum_cash_row + 1}"))
                bs.update_cells(cells, value_input_option='USER_ENTERED')
                print(f"  Linked Cash row {cash_row+1} to Cash Flow row {cum_cash_row+1}")
        
        rate_limit(1)
        
        # Fix Retained Earnings - cumulative PAT
        if retained_row >= 0:
            pl = spreadsheet.worksheet('P&L')
            rate_limit(0.5)
            pl_data = pl.get_all_values()
            pat_row = find_row_by_label(pl_data, 'net income')
            if pat_row < 0:
                pat_row = find_row_by_label(pl_data, 'pat')
            
            if pat_row >= 0:
                cells = [gspread.Cell(retained_row + 1, 3, f"='P&L'!C{pat_row + 1}")]
                for col in range(4, 14):
                    prev_col = col_letter(col - 1)
                    curr_col = col_letter(col)
                    cells.append(gspread.Cell(
                        retained_row + 1, col, 
                        f"={prev_col}{retained_row + 1}+'P&L'!{curr_col}{pat_row + 1}"
                    ))
                bs.update_cells(cells, value_input_option='USER_ENTERED')
                print(f"  Fixed Retained Earnings with cumulative PAT formula")
        
        rate_limit(1)
        
        # Verify balance check
        if check_row >= 0 and total_assets_row >= 0 and total_liab_row >= 0:
            # Check should be = Total Assets - Total Liab - Total Equity
            cells = []
            for col in range(3, 14):
                col_l = col_letter(col)
                # Find total equity row (if separate from equity)
                total_eq_row = find_row_by_label(data, 'total equity')
                if total_eq_row < 0:
                    total_eq_row = find_row_by_label(data, 'total shareholders')
                if total_eq_row < 0:
                    total_eq_row = equity_row  # fallback
                
                cells.append(gspread.Cell(
                    check_row + 1, col,
                    f"={col_l}{total_assets_row + 1}-{col_l}{total_liab_row + 1}-{col_l}{total_eq_row + 1}"
                ))
            bs.update_cells(cells, value_input_option='USER_ENTERED')
            print(f"  Updated balance check formula")
        
        return True
        
    except Exception as e:
        print(f"Error fixing balance sheet: {e}")
        return False


def fix_cash_flow(spreadsheet) -> bool:
    """Fix cash flow links to P&L, funding, and balance sheet"""
    print("\n" + "=" * 60)
    print("FIXING CASH FLOW")
    print("=" * 60)
    
    try:
        cf = spreadsheet.worksheet('Cash Flow')
        rate_limit(1)
        data = cf.get_all_values()
        
        # Find key rows
        pat_row = find_row_by_label(data, 'net income')
        if pat_row < 0:
            pat_row = find_row_by_label(data, 'pat')
        depreciation_row = find_row_by_label(data, 'depreciation')
        equity_row = find_row_by_label(data, 'equity')
        capex_row = find_row_by_label(data, 'capex')
        
        # Link PAT to P&L
        if pat_row >= 0:
            pl = spreadsheet.worksheet('P&L')
            rate_limit(0.5)
            pl_data = pl.get_all_values()
            pl_pat_row = find_row_by_label(pl_data, 'net income')
            if pl_pat_row < 0:
                pl_pat_row = find_row_by_label(pl_data, 'pat')
            
            if pl_pat_row >= 0:
                cells = []
                for col in range(3, 14):
                    col_l = col_letter(col)
                    cells.append(gspread.Cell(pat_row + 1, col, f"='P&L'!{col_l}{pl_pat_row + 1}"))
                cf.update_cells(cells, value_input_option='USER_ENTERED')
                print(f"  Linked PAT row {pat_row+1} to P&L row {pl_pat_row+1}")
        
        rate_limit(1)
        
        # Link Equity to Funding
        if equity_row >= 0:
            try:
                fc = spreadsheet.worksheet('Funding Cap Table')
                rate_limit(0.5)
                fc_data = fc.get_all_values()
                
                # Find funding rows (supports both detailed rounds and template summary rows)
                equity_raised_row = find_row_by_label(fc_data, 'equity raised')
                seed_row = find_row_by_label(fc_data, 'seed')
                series_a_row = find_row_by_label(fc_data, 'series a')
                series_b_row = find_row_by_label(fc_data, 'series b')
                
                if equity_raised_row >= 0:
                    cells = []
                    for col in range(3, 14):
                        col_l = col_letter(col)
                        cells.append(gspread.Cell(equity_row + 1, col, f"='Funding Cap Table'!{col_l}{equity_raised_row + 1}"))
                    cf.update_cells(cells, value_input_option='USER_ENTERED')
                    print(f"  Linked Equity row {equity_row+1} to Funding Cap Table Equity Raised row {equity_raised_row+1}")
                elif seed_row >= 0:
                    cells = []
                    for col in range(3, 14):
                        col_l = col_letter(col)
                        formula_parts = [f"='Funding Cap Table'!{col_l}{seed_row + 1}"]
                        if series_a_row >= 0:
                            formula_parts.append(f"'Funding Cap Table'!{col_l}{series_a_row + 1}")
                        if series_b_row >= 0:
                            formula_parts.append(f"'Funding Cap Table'!{col_l}{series_b_row + 1}")
                        cells.append(gspread.Cell(equity_row + 1, col, "+".join(formula_parts)))
                    cf.update_cells(cells, value_input_option='USER_ENTERED')
                    print(f"  Linked Equity row {equity_row+1} to Funding Cap Table")
                else:
                    print("  Could not find funding source rows (Equity Raised / Seed / Series), skipping equity link")
            except gspread.WorksheetNotFound:
                print("  Funding Cap Table not found, skipping equity link")
        
        return True
        
    except Exception as e:
        print(f"Error fixing cash flow: {e}")
        return False


def fix_funding(spreadsheet) -> bool:
    """Fix funding schedule and cap table"""
    print("\n" + "=" * 60)
    print("FIXING FUNDING & CAP TABLE")
    print("=" * 60)
    
    try:
        fc = spreadsheet.worksheet('Funding Cap Table')
        rate_limit(1)
        data = fc.get_all_values()
        
        # Find cumulative row
        cum_row = find_row_by_label(data, 'cumulative')
        seed_row = find_row_by_label(data, 'seed')
        series_a_row = find_row_by_label(data, 'series a')
        series_b_row = find_row_by_label(data, 'series b')
        
        if cum_row >= 0 and seed_row >= 0:
            cells = []
            for col in range(3, 14):
                col_l = col_letter(col)
                prev_col = col_letter(col - 1) if col > 3 else None
                
                formula_parts = [f"{col_l}{seed_row + 1}"]
                if series_a_row >= 0:
                    formula_parts.append(f"{col_l}{series_a_row + 1}")
                if series_b_row >= 0:
                    formula_parts.append(f"{col_l}{series_b_row + 1}")
                
                if prev_col:
                    cells.append(gspread.Cell(cum_row + 1, col, f"={prev_col}{cum_row + 1}+{'+'.join(formula_parts)}"))
                else:
                    cells.append(gspread.Cell(cum_row + 1, col, f"={'+'.join(formula_parts)}"))
            
            fc.update_cells(cells, value_input_option='USER_ENTERED')
            print(f"  Fixed cumulative funding formula (row {cum_row+1})")
        
        return True
        
    except gspread.WorksheetNotFound:
        print("  Funding Cap Table not found")
        return False
    except Exception as e:
        print(f"Error fixing funding: {e}")
        return False


def trim_years(spreadsheet, num_years: int) -> bool:
    """Trim model to specified number of years"""
    print("\n" + "=" * 60)
    print(f"TRIMMING MODEL TO {num_years} YEARS (Y0-Y{num_years})")
    print("=" * 60)
    
    # Columns: C=Y0, D=Y1, ... C+num_years = last year to keep
    # Clear columns after the last year
    last_col = 2 + num_years  # C (3) + num_years
    clear_start_col = col_letter(last_col + 1)  # First column to clear
    
    for ws in spreadsheet.worksheets():
        rate_limit(0.5)
        try:
            data = ws.get_all_values()
            if not data:
                continue
            
            last_row = len(data)
            
            # Check if sheet has data beyond the trim point
            if len(data[0]) > last_col:
                clear_range = f'{clear_start_col}1:M{last_row}'
                ws.batch_clear([clear_range])
                print(f"  {ws.title}: Cleared columns {clear_start_col}-M")
            else:
                print(f"  {ws.title}: No columns to clear")
                
        except Exception as e:
            print(f"  {ws.title}: Error - {e}")
    
    # Update headers
    headers = [f'Y{i}' for i in range(num_years + 1)]
    print(f"\nUpdating headers to: {headers}")
    
    for ws in spreadsheet.worksheets():
        rate_limit(0.5)
        try:
            row2 = ws.row_values(2)
            if row2 and len(row2) > 2 and any('Y' in str(cell) for cell in row2):
                cells = []
                for i, h in enumerate(headers):
                    cells.append(gspread.Cell(2, i + 3, h))
                ws.update_cells(cells, value_input_option='USER_ENTERED')
                print(f"  {ws.title}: Updated headers")
        except Exception as e:
            pass
    
    return True


def rebalance_sm(spreadsheet, target_pct: float) -> bool:
    """Rebalance S&M spend to target percentage of revenue"""
    print("\n" + "=" * 60)
    print(f"REBALANCING S&M TO {target_pct}% OF REVENUE")
    print("=" * 60)
    
    try:
        # Get revenue data
        rev = spreadsheet.worksheet('Revenue')
        rate_limit(0.5)
        rev_data = rev.get_all_values()
        
        # Find total revenue row
        total_rev_row = find_row_by_label(rev_data, 'total revenue')
        if total_rev_row < 0:
            total_rev_row = find_row_by_label(rev_data, 'total')
        
        if total_rev_row < 0:
            print("  Could not find total revenue row")
            return False
        
        # Get revenue values
        revenues = []
        for col in range(2, 14):
            try:
                val = rev_data[total_rev_row][col]
                # Parse value (remove $, K, M, commas)
                val_str = str(val).replace('$', '').replace(',', '').replace('K', '000').replace('M', '000000')
                revenues.append(float(val_str) if val_str else 0)
            except:
                revenues.append(0)
        
        print(f"  Revenue values: {revenues[:6]}")
        
        # Calculate target S&M
        target_sm = [int(r * target_pct / 100) for r in revenues]
        print(f"  Target S&M ({target_pct}%): {target_sm[:6]}")
        
        # Update Operating Costs S&M row
        oc = spreadsheet.worksheet('Operating Costs')
        rate_limit(0.5)
        oc_data = oc.get_all_values()
        
        sm_row = find_row_by_label(oc_data, 's&m')
        if sm_row < 0:
            sm_row = find_row_by_label(oc_data, 'sales & marketing')
        if sm_row < 0:
            sm_row = find_row_by_label(oc_data, 'marketing')
        
        if sm_row >= 0:
            cells = []
            for i, col in enumerate(range(3, 14)):
                if i < len(target_sm):
                    cells.append(gspread.Cell(sm_row + 1, col, target_sm[i]))
            oc.update_cells(cells, value_input_option='USER_ENTERED')
            format_cell_range(oc, f'C{sm_row+1}:M{sm_row+1}', FORMAT_CURRENCY_K)
            print(f"  Updated S&M in Operating Costs row {sm_row+1}")
        
        return True
        
    except Exception as e:
        print(f"Error rebalancing S&M: {e}")
        return False


def verify_links(spreadsheet) -> Dict:
    """Verify all cross-sheet formula links"""
    print("\n" + "=" * 60)
    print("VERIFYING CROSS-SHEET LINKS")
    print("=" * 60)
    
    link_status = {}
    
    expected_links = [
        ('P&L', 'Revenue', 'Total Revenue should link to Revenue sheet'),
        ('P&L', 'Operating Costs', 'COGS and OpEx should link to Operating Costs'),
        ('Cash Flow', 'P&L', 'PAT should link to P&L Net Income'),
        ('Balance Sheet', 'Cash Flow', 'Cash should link to Cash Flow cumulative'),
        ('Balance Sheet', 'P&L', 'Retained Earnings should link to P&L cumulative'),
    ]
    
    for source_sheet, target_sheet, description in expected_links:
        try:
            ws = spreadsheet.worksheet(source_sheet)
            rate_limit(0.3)
            formulas = ws.get('C1:M30', value_render_option='FORMULA')
            
            has_link = False
            for row in formulas:
                for cell in row:
                    if f"'{target_sheet}'" in str(cell) or f"={target_sheet}!" in str(cell):
                        has_link = True
                        break
                if has_link:
                    break
            
            status = "OK" if has_link else "MISSING"
            link_status[f"{source_sheet} -> {target_sheet}"] = {
                'status': status,
                'description': description
            }
            print(f"  [{status}] {source_sheet} -> {target_sheet}: {description}")
            
        except gspread.WorksheetNotFound:
            link_status[f"{source_sheet} -> {target_sheet}"] = {
                'status': 'SHEET_NOT_FOUND',
                'description': description
            }
    
    return link_status


def main():
    parser = argparse.ArgumentParser(description="Repair financial model")
    parser.add_argument("--sheet-id", required=True, help="Google Sheet ID")
    parser.add_argument("--action", required=True,
                       choices=["fix-formulas", "fix-formatting", "fix-balance-sheet", 
                               "fix-cash-flow", "fix-funding", "trim-years", 
                               "rebalance-sm", "verify-links", "all"],
                       help="Repair action to perform")
    parser.add_argument("--years", type=int, default=5, help="Number of years (for trim-years action)")
    parser.add_argument("--target-pct", type=float, default=35.0, help="Target SM percent (for rebalance-sm action)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("FINANCIAL MODEL REPAIR TOOL")
    print("=" * 60)
    
    client = get_sheets_client()
    spreadsheet = client.open_by_key(args.sheet_id)
    print(f"Opened: {spreadsheet.title}")
    
    if args.action == "fix-formulas" or args.action == "all":
        fix_formulas(spreadsheet)
    
    if args.action == "fix-formatting" or args.action == "all":
        fix_formatting(spreadsheet)
    
    if args.action == "fix-balance-sheet" or args.action == "all":
        fix_balance_sheet(spreadsheet)
    
    if args.action == "fix-cash-flow" or args.action == "all":
        fix_cash_flow(spreadsheet)
    
    if args.action == "fix-funding" or args.action == "all":
        fix_funding(spreadsheet)
    
    if args.action == "trim-years":
        trim_years(spreadsheet, args.years)
    
    if args.action == "rebalance-sm":
        rebalance_sm(spreadsheet, args.target_pct)
    
    if args.action == "verify-links" or args.action == "all":
        verify_links(spreadsheet)
    
    print("\n" + "=" * 60)
    print("REPAIR COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
