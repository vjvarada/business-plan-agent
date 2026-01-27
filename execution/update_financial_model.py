#!/usr/bin/env python3
"""
Update Financial Model Sheets
=============================
Utility for updating specific sheets in an existing financial model.

Features:
- Update Sources & References with market research data
- Update Assumptions with new growth rates
- Add Headcount Plan sheet
- Add remaining sheets (Break-even, Funding, Ratios)
- Fix percentage formatting across sheets

Usage:
    python update_financial_model.py --sheet-id <ID> --action <action> [options]

Actions:
    update-sources    - Update Sources & References sheet with market data
    update-growth     - Update growth rates for geographic expansion
    add-headcount     - Add Headcount Plan sheet
    add-remaining     - Add Break-even, Funding, Financial Ratios sheets
    fix-formatting    - Fix percentage formatting across all sheets

Examples:
    python update_financial_model.py --sheet-id "1ABC..." --action update-sources --sources-file sources.json
    python update_financial_model.py --sheet-id "1ABC..." --action update-growth --growth-file growth.json
    python update_financial_model.py --sheet-id "1ABC..." --action fix-formatting
"""

import os
import sys
import json
import time
import argparse
from dotenv import load_dotenv
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

YEAR_HEADERS = ['Year 0', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 
                'Year 6', 'Year 7', 'Year 8', 'Year 9', 'Year 10']


def get_credentials():
    """Get OAuth2 credentials."""
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception:
            pass
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def rate_limit_delay(seconds=2):
    """Add delay to avoid Google API rate limits."""
    time.sleep(seconds)


def update_sources(spreadsheet, sources_data):
    """Update the Sources & References sheet."""
    print("Updating Sources & References sheet...")
    
    try:
        sources = spreadsheet.worksheet('Sources & References')
    except gspread.WorksheetNotFound:
        sources = spreadsheet.add_worksheet('Sources & References', rows=60, cols=10)
    
    rate_limit_delay(2)
    sources.clear()
    rate_limit_delay(2)
    
    sources.update(values=sources_data, range_name='A1', value_input_option='USER_ENTERED')
    rate_limit_delay(2)
    
    # Format headers
    pct_format = {'numberFormat': {'type': 'PERCENT', 'pattern': '0.0%'}}
    sources.format('A1:E1', {
        'textFormat': {'bold': True, 'fontSize': 14},
        'backgroundColor': {'red': 0.2, 'green': 0.3, 'blue': 0.5}
    })
    rate_limit_delay(1)
    sources.format('A4:E4', {
        'textFormat': {'bold': True},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
    })
    
    print("  Sources & References updated!")
    return True


def update_growth_rates(spreadsheet, growth_config):
    """Update growth rates in Assumptions sheet."""
    print("Updating growth rates...")
    
    assumptions = spreadsheet.worksheet('Assumptions')
    rate_limit_delay(2)
    
    # Get current data to find rows
    data = assumptions.get_all_values()
    
    # Find and update growth rate rows
    for i, row in enumerate(data):
        if len(row) > 0:
            row_name = row[0].lower()
            for stream_name, rates in growth_config.items():
                if stream_name.lower() in row_name and 'growth' in row_name:
                    # Update growth rates for Years 1-10
                    for year, rate in enumerate(rates):
                        col = chr(ord('C') + year)  # C, D, E, ...
                        assumptions.update_acell(f'{col}{i+1}', rate)
                        rate_limit_delay(0.3)
                    print(f"  Updated: {row[0]}")
    
    print("  Growth rates updated!")
    return True


def add_headcount_sheet(spreadsheet, headcount_config):
    """Add Headcount Plan sheet."""
    print("Adding Headcount Plan sheet...")
    
    try:
        hc = spreadsheet.add_worksheet('Headcount Plan', rows=20, cols=15)
    except:
        hc = spreadsheet.worksheet('Headcount Plan')
    
    rate_limit_delay(2)
    
    data = [
        ['HEADCOUNT PLAN', ''] + YEAR_HEADERS,
        [''],
        ['Engineering', '#'] + headcount_config.get('engineering', [2]*11),
        ['Sales & Marketing', '#'] + headcount_config.get('sales', [1]*11),
        ['Operations', '#'] + headcount_config.get('operations', [1]*11),
        ['G&A', '#'] + headcount_config.get('ga', [0]*11),
        [''],
        ['Total Headcount', '#', '=SUM(C3:C6)', '=SUM(D3:D6)', '=SUM(E3:E6)', 
         '=SUM(F3:F6)', '=SUM(G3:G6)', '=SUM(H3:H6)', '=SUM(I3:I6)', 
         '=SUM(J3:J6)', '=SUM(K3:K6)', '=SUM(L3:L6)', '=SUM(M3:M6)'],
        [''],
        ['Avg Salary', '$', 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000, 105000, 110000],
        ['Total Salary Cost', '$', '=C8*C10', '=D8*D10', '=E8*E10', '=F8*F10', 
         '=G8*G10', '=H8*H10', '=I8*I10', '=J8*J10', '=K8*K10', '=L8*L10', '=M8*M10']
    ]
    
    hc.update(values=data, range_name='A1', value_input_option='USER_ENTERED')
    rate_limit_delay(2)
    
    hc.format('A1:M1', {
        'textFormat': {'bold': True},
        'backgroundColor': {'red': 0.2, 'green': 0.3, 'blue': 0.5}
    })
    
    print("  Headcount Plan added!")
    return True


def add_remaining_sheets(spreadsheet):
    """Add Break-even, Funding & Cap Table, Financial Ratios sheets."""
    print("Adding remaining sheets...")
    pct_format = {'numberFormat': {'type': 'PERCENT', 'pattern': '0.0%'}}
    
    # Sheet 1: Break-even Analysis
    print("  Creating Break-even Analysis...")
    try:
        breakeven = spreadsheet.add_worksheet('Break-even Analysis', rows=30, cols=15)
    except:
        breakeven = spreadsheet.worksheet('Break-even Analysis')
    
    rate_limit_delay(2)
    
    be_data = [
        ['BREAK-EVEN ANALYSIS', ''] + YEAR_HEADERS,
        [''],
        ['--- CONTRIBUTION MARGIN ---'] + [''] * 12,
        ['Total Revenue', '$'] + [f"='P&L'!{chr(ord('C')+i)}4" for i in range(11)],
        ['Variable Costs', '$'] + [f"='Operating Costs'!{chr(ord('C')+i)}9" for i in range(11)],
        ['Fixed Costs', '$'] + [f"='Operating Costs'!{chr(ord('C')+i)}22" for i in range(11)],
        ['Contribution Margin', '$'] + [f'={chr(ord("C")+i)}4-{chr(ord("C")+i)}5' for i in range(11)],
        ['CM Percentage', '%'] + [f'={chr(ord("C")+i)}7/{chr(ord("C")+i)}4' for i in range(11)],
        [''],
        ['--- BREAK-EVEN ---'] + [''] * 12,
        ['Break-even Revenue', '$'] + [f'={chr(ord("C")+i)}6/{chr(ord("C")+i)}8' for i in range(11)],
        ['Margin of Safety', '$'] + [f'={chr(ord("C")+i)}4-{chr(ord("C")+i)}11' for i in range(11)],
        ['MoS Percentage', '%'] + [f'={chr(ord("C")+i)}12/{chr(ord("C")+i)}4' for i in range(11)]
    ]
    
    breakeven.update(values=be_data, range_name='A1', value_input_option='USER_ENTERED')
    rate_limit_delay(2)
    breakeven.format('A1:M1', {'textFormat': {'bold': True}, 'backgroundColor': {'red': 0.2, 'green': 0.3, 'blue': 0.5}})
    rate_limit_delay(1)
    breakeven.format('C8:M8', pct_format)
    rate_limit_delay(0.5)
    breakeven.format('C13:M13', pct_format)
    print("    Break-even Analysis done!")
    
    # Sheet 2: Funding & Cap Table
    print("  Creating Funding & Cap Table...")
    rate_limit_delay(3)
    try:
        funding = spreadsheet.add_worksheet('Funding Cap Table', rows=30, cols=15)
    except:
        funding = spreadsheet.worksheet('Funding Cap Table')
    
    rate_limit_delay(2)
    
    fund_data = [
        ['FUNDING & CAP TABLE', ''] + YEAR_HEADERS,
        [''],
        ['--- FUNDING ROUNDS ---'] + [''] * 12,
        ['Seed Round', '$', 500000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['Series A', '$', 0, 0, 2500000, 0, 0, 0, 0, 0, 0, 0, 0],
        ['Series B', '$', 0, 0, 0, 0, 12000000, 0, 0, 0, 0, 0, 0],
        ['Cumulative', '$', '=C4', '=C7+D4+D5+D6', '=D7+E4+E5+E6', '=E7+F4+F5+F6', 
         '=F7+G4+G5+G6', '=G7+H4+H5+H6', '=H7+I4+I5+I6', '=I7+J4+J5+J6', 
         '=J7+K4+K5+K6', '=K7+L4+L5+L6', '=L7+M4+M5+M6'],
        [''],
        ['--- CAP TABLE ---'] + [''] * 12,
        ['Founders', '%', 0.75, 0.75, 0.5625, 0.5625, 0.4219, 0.4219, 0.4219, 0.4219, 0.4219, 0.4219, 0.4219],
        ['Seed Investors', '%', 0.25, 0.25, 0.1875, 0.1875, 0.1406, 0.1406, 0.1406, 0.1406, 0.1406, 0.1406, 0.1406],
        ['Series A', '%', 0, 0, 0.25, 0.25, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875, 0.1875],
        ['Series B', '%', 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    ]
    
    funding.update(values=fund_data, range_name='A1', value_input_option='USER_ENTERED')
    rate_limit_delay(2)
    funding.format('A1:M1', {'textFormat': {'bold': True}, 'backgroundColor': {'red': 0.2, 'green': 0.3, 'blue': 0.5}})
    rate_limit_delay(1)
    for row in [10, 11, 12, 13]:
        funding.format(f'C{row}:M{row}', pct_format)
        rate_limit_delay(0.3)
    print("    Funding & Cap Table done!")
    
    # Sheet 3: Financial Ratios
    print("  Creating Financial Ratios...")
    rate_limit_delay(3)
    try:
        ratios = spreadsheet.add_worksheet('Financial Ratios', rows=25, cols=15)
    except:
        ratios = spreadsheet.worksheet('Financial Ratios')
    
    rate_limit_delay(2)
    
    ratio_data = [
        ['FINANCIAL RATIOS', ''] + YEAR_HEADERS,
        [''],
        ['--- PROFITABILITY ---'] + [''] * 12,
        ['Gross Margin', '%'] + [f"='P&L'!{chr(ord('C')+i)}9" for i in range(11)],
        ['EBITDA Margin', '%'] + [f"='P&L'!{chr(ord('C')+i)}14" for i in range(11)],
        ['Net Margin', '%'] + [f"='P&L'!{chr(ord('C')+i)}23" for i in range(11)],
        [''],
        ['--- GROWTH ---'] + [''] * 12,
        ['Revenue Growth', '%', 0] + [f"=('P&L'!{chr(ord('D')+i)}4-'P&L'!{chr(ord('C')+i)}4)/'P&L'!{chr(ord('C')+i)}4" for i in range(10)],
        [''],
        ['--- EFFICIENCY ---'] + [''] * 12,
        ['Revenue/Employee', '$'] + [f"='P&L'!{chr(ord('C')+i)}4/'Headcount Plan'!{chr(ord('C')+i)}8" for i in range(11)]
    ]
    
    ratios.update(values=ratio_data, range_name='A1', value_input_option='USER_ENTERED')
    rate_limit_delay(2)
    ratios.format('A1:M1', {'textFormat': {'bold': True}, 'backgroundColor': {'red': 0.2, 'green': 0.3, 'blue': 0.5}})
    rate_limit_delay(1)
    for row in [4, 5, 6, 9]:
        ratios.format(f'C{row}:M{row}', pct_format)
        rate_limit_delay(0.3)
    print("    Financial Ratios done!")
    
    return True


def fix_percentage_formatting(spreadsheet):
    """Fix percentage formatting across all sheets."""
    print("Fixing percentage formatting...")
    pct_format = {'numberFormat': {'type': 'PERCENT', 'pattern': '0.0%'}}
    
    # P&L margins
    print("  Fixing P&L...")
    try:
        pl = spreadsheet.worksheet('P&L')
        rate_limit_delay(2)
        for row in [9, 14, 23]:  # Gross, EBITDA, Net margins
            pl.format(f'C{row}:M{row}', pct_format)
            rate_limit_delay(0.5)
    except Exception as e:
        print(f"    P&L error: {e}")
    
    # Customer Economics
    print("  Fixing Customer Economics...")
    try:
        ce = spreadsheet.worksheet('Customer Economics')
        rate_limit_delay(2)
        for row in [3, 4]:  # Churn, Retention
            ce.format(f'C{row}:M{row}', pct_format)
            rate_limit_delay(0.5)
    except Exception as e:
        print(f"    Customer Economics error: {e}")
    
    # Sensitivity Analysis
    print("  Fixing Sensitivity Analysis...")
    try:
        sens = spreadsheet.worksheet('Sensitivity Analysis')
        rate_limit_delay(2)
        sens.format('C4:M5', pct_format)
        rate_limit_delay(0.5)
        sens.format('C10:M11', pct_format)
    except Exception as e:
        print(f"    Sensitivity error: {e}")
    
    # Valuation
    print("  Fixing Valuation...")
    try:
        val = spreadsheet.worksheet('Valuation')
        rate_limit_delay(2)
        val.format('B4:B6', pct_format)
    except Exception as e:
        print(f"    Valuation error: {e}")
    
    # Assumptions
    print("  Fixing Assumptions...")
    try:
        assumptions = spreadsheet.worksheet('Assumptions')
        rate_limit_delay(2)
        data = assumptions.get_all_values()
        for i, row in enumerate(data):
            if len(row) > 0 and ('growth' in row[0].lower() or 'rate' in row[0].lower() or 
                                'margin' in row[0].lower() or 'cogs' in row[0].lower()):
                assumptions.format(f'C{i+1}:M{i+1}', pct_format)
                rate_limit_delay(0.3)
    except Exception as e:
        print(f"    Assumptions error: {e}")
    
    print("  Percentage formatting fixed!")
    return True


def main():
    parser = argparse.ArgumentParser(description='Update Financial Model Sheets')
    parser.add_argument('--sheet-id', required=True, help='Google Sheet ID')
    parser.add_argument('--action', required=True, 
                       choices=['update-sources', 'update-growth', 'add-headcount', 
                               'add-remaining', 'fix-formatting', 'all'],
                       help='Action to perform')
    parser.add_argument('--sources-file', help='JSON file with sources data')
    parser.add_argument('--growth-file', help='JSON file with growth rates')
    parser.add_argument('--headcount-file', help='JSON file with headcount config')
    
    args = parser.parse_args()
    
    # Connect to spreadsheet
    creds = get_credentials()
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(args.sheet_id)
    print(f"Opened: {spreadsheet.title}")
    
    success = True
    
    if args.action in ['update-sources', 'all']:
        if args.sources_file:
            with open(args.sources_file) as f:
                sources_data = json.load(f)
            success = success and update_sources(spreadsheet, sources_data)
        else:
            print("Warning: --sources-file required for update-sources action")
    
    if args.action in ['update-growth', 'all']:
        if args.growth_file:
            with open(args.growth_file) as f:
                growth_config = json.load(f)
            success = success and update_growth_rates(spreadsheet, growth_config)
        else:
            print("Warning: --growth-file required for update-growth action")
    
    if args.action in ['add-headcount', 'all']:
        headcount_config = {}
        if args.headcount_file:
            with open(args.headcount_file) as f:
                headcount_config = json.load(f)
        success = success and add_headcount_sheet(spreadsheet, headcount_config)
    
    if args.action in ['add-remaining', 'all']:
        success = success and add_remaining_sheets(spreadsheet)
    
    if args.action in ['fix-formatting', 'all']:
        success = success and fix_percentage_formatting(spreadsheet)
    
    if success:
        print(f"\nSuccess! URL: https://docs.google.com/spreadsheets/d/{args.sheet_id}/edit")
    else:
        print("\nSome operations failed. Check logs above.")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
