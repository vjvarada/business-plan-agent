#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local-first Financial Model Creator - Creates Excel files compatible with Google Sheets"""

import os, sys, json, argparse
from datetime import datetime
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

class Colors:
    TITLE_BLUE, DARK_BLUE, MEDIUM_BLUE = '335080', '336699', '6699CC'
    LIGHT_BLUE, LIGHT_GRAY, GREEN = 'D8EAF9', 'F2F2F2', 'E5F8E5'
    WHITE, BLACK = 'FFFFFF', '000000'

YEAR_HEADERS = ['Year 0', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 
                'Year 6', 'Year 7', 'Year 8', 'Year 9', 'Year 10']

RAPIDTOOLS_CONFIG = {
    'general': {'tax_rate': 0.30, 'capex_y0': 150000, 'capex_annual': 50000,
                'depreciation_years': 5, 'debtor_days': 45, 'creditor_days': 30,
                'interest_rate': 0.10, 'equity_y0': 300000, 'debt_y0': 0, 'cost_inflation': 0.05},
    'revenue_streams': [
        {'name': 'Software Licenses', 'price': 12000, 'volume': 10, 'growth': 0.40, 'cogs_pct': 0.10},
        {'name': 'Hardware Sales', 'price': 180000, 'volume': 4, 'growth': 0.35, 'cogs_pct': 0.60},
        {'name': 'Consumables', 'price': 8000, 'volume': 6, 'growth': 0.30, 'cogs_pct': 0.50},
        {'name': 'Managed Services', 'price': 24000, 'volume': 3, 'growth': 0.45, 'cogs_pct': 0.20},
    ],
    'fixed_costs': {'Salaries': 360000, 'Rent & Utilities': 36000, 'Marketing': 60000,
                    'R&D': 72000, 'Insurance': 12000}
}

def hdr(cell, bg=Colors.DARK_BLUE, fg=Colors.WHITE, sz=12, b=True):
    cell.font = Font(name='Calibri', size=sz, bold=b, color=fg)
    cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

def create_financial_model_local(company_name, config=None, use_rapidtools=False):
    if use_rapidtools: config = RAPIDTOOLS_CONFIG
    if config is None:
        config = {
            'general': {'tax_rate': 0.25, 'capex_y0': 500000, 'capex_annual': 100000,
                        'depreciation_years': 5, 'debtor_days': 45, 'creditor_days': 30,
                        'interest_rate': 0.08, 'equity_y0': 1000000, 'debt_y0': 0, 'cost_inflation': 0.03},
            'revenue_streams': [
                {'name': 'Product A', 'price': 1000, 'volume': 100, 'growth': 0.25, 'cogs_pct': 0.30},
                {'name': 'Product B', 'price': 2000, 'volume': 50, 'growth': 0.30, 'cogs_pct': 0.35},
            ],
            'fixed_costs': {'Salaries': 500000, 'Rent': 50000, 'Marketing': 100000}
        }
    
    wb = Workbook()
    if 'Sheet' in wb.sheetnames: del wb['Sheet']
    
    print(f'Creating financial model for {company_name}...')
    
    # ASSUMPTIONS SHEET
    print('  Creating Assumptions sheet...')
    ws = wb.create_sheet('Assumptions', 0)
    ws.column_dimensions['A'].width, ws.column_dimensions['B'].width = 35, 15
    ws['A1'] = 'FINANCIAL MODEL ASSUMPTIONS'
    hdr(ws['A1'], bg=Colors.TITLE_BLUE, sz=14)
    ws.merge_cells('A1:M1')
    
    r = 3
    ws[f'A{r}'] = 'GENERAL PARAMETERS'
    hdr(ws[f'A{r}'])
    ws.merge_cells(f'A{r}:C{r}')
    r += 1
    
    for name, val, unit in [
        ('Tax Rate', config['general'].get('tax_rate', 0.25), '%'),
        ('CapEx Year 0', config['general'].get('capex_y0', 500000), 'USD'),
        ('CapEx Annual', config['general'].get('capex_annual', 100000), 'USD'),
        ('Depreciation Period', config['general'].get('depreciation_years', 5), 'Years'),
    ]:
        ws[f'A{r}'], ws[f'B{r}'], ws[f'C{r}'] = name, val, unit
        if unit == '%': ws[f'B{r}'].number_format = '0.00%'
        elif unit == 'USD': ws[f'B{r}'].number_format = '#,##0'
        r += 1
    
    r += 1
    ws[f'A{r}'] = 'REVENUE STREAMS'
    hdr(ws[f'A{r}'])
    ws.merge_cells(f'A{r}:M{r}')
    r += 1
    
    for c, h in enumerate(['Stream Name', 'Price (Y0)', 'Unit'] + YEAR_HEADERS, 1):
        hdr(ws.cell(r, c, h), bg=Colors.MEDIUM_BLUE, sz=10)
    r += 1
    
    for stream in config.get('revenue_streams', []):
        ws.cell(r, 1, stream['name'])
        ws.cell(r, 2, stream['price']).number_format = '#,##0'
        ws.cell(r, 3, 'USD')
        for yr in range(11):
            col = yr + 4
            if yr == 0:
                ws.cell(r, col, stream['volume']).number_format = '0'
            else:
                prev = get_column_letter(col - 1)
                ws.cell(r, col).value = f'={prev}{r}*(1+{stream["growth"]})'
                ws.cell(r, col).number_format = '0'
        r += 1
    
    # REVENUE SHEET
    print('  Creating Revenue sheet...')
    ws = wb.create_sheet('Revenue')
    ws.column_dimensions['A'].width = 30
    ws['A1'] = 'REVENUE PROJECTIONS'
    hdr(ws['A1'], bg=Colors.TITLE_BLUE, sz=14)
    ws.merge_cells('A1:M1')
    
    r = 3
    for c, h in enumerate(['Revenue Stream', 'Unit'] + YEAR_HEADERS, 1):
        hdr(ws.cell(r, c, h))
    r += 1
    
    start_r = r
    for idx, stream in enumerate(config.get('revenue_streams', []), 1):
        ws.cell(r, 1, stream['name'])
        ws.cell(r, 2, 'USD')
        for yr in range(11):
            col = yr + 3
            yr_col = get_column_letter(yr + 4)
            ass_row = 17 + idx - 1
            ws.cell(r, col).value = f'=Assumptions!$B${ass_row}*Assumptions!{yr_col}${ass_row}'
            ws.cell(r, col).number_format = '#,##0'
        r += 1
    
    r += 1
    ws.cell(r, 1, 'TOTAL REVENUE').font = Font(bold=True, size=11)
    for yr in range(11):
        col = yr + 3
        c_ltr = get_column_letter(col)
        ws.cell(r, col).value = f'=SUM({c_ltr}{start_r}:{c_ltr}{r-2})'
        ws.cell(r, col).number_format = '#,##0'
        ws.cell(r, col).font = Font(bold=True)
        ws.cell(r, col).fill = PatternFill(start_color=Colors.GREEN, end_color=Colors.GREEN, fill_type='solid')
    
    # P&L SHEET
    print('  Creating P&L sheet...')
    ws = wb.create_sheet('P&L')
    ws.column_dimensions['A'].width = 30
    ws['A1'] = 'PROFIT & LOSS STATEMENT'
    hdr(ws['A1'], bg=Colors.TITLE_BLUE, sz=14)
    ws.merge_cells('A1:M1')
    
    r = 3
    for c, h in enumerate(['Line Item', 'Unit'] + YEAR_HEADERS, 1):
        hdr(ws.cell(r, c, h))
    r += 1
    
    ws.cell(r, 1, 'Revenue')
    ws.cell(r, 2, 'USD')
    for yr in range(11):
        col = yr + 3
        c_ltr = get_column_letter(col)
        ws.cell(r, col).value = f'=Revenue!{c_ltr}8'
        ws.cell(r, col).number_format = '#,##0'
    rev_r = r
    r += 1
    
    ws.cell(r, 1, 'Cost of Goods Sold (COGS)')
    ws.cell(r, 2, 'USD')
    avg_cogs = sum(s['cogs_pct'] for s in config.get('revenue_streams', [])) / max(len(config.get('revenue_streams', [])), 1)
    for yr in range(11):
        col = yr + 3
        c_ltr = get_column_letter(col)
        ws.cell(r, col).value = f'={c_ltr}{rev_r}*{avg_cogs}'
        ws.cell(r, col).number_format = '#,##0'
    cogs_r = r
    r += 1
    
    ws.cell(r, 1, 'Gross Profit').font = Font(bold=True)
    ws.cell(r, 2, 'USD')
    for yr in range(11):
        col = yr + 3
        c_ltr = get_column_letter(col)
        ws.cell(r, col).value = f'={c_ltr}{rev_r}-{c_ltr}{cogs_r}'
        ws.cell(r, col).number_format = '#,##0'
        ws.cell(r, col).font = Font(bold=True)
    gp_r = r
    r += 2
    
    ws.cell(r, 1, 'Operating Expenses').font = Font(bold=True)
    opex_r = r
    r += 1
    
    for cost_name in config.get('fixed_costs', {}).keys():
        ws.cell(r, 1, f'  {cost_name}')
        ws.cell(r, 2, 'USD')
        for yr in range(11):
            col = yr + 3
            ws.cell(r, col, config['fixed_costs'][cost_name])
            ws.cell(r, col).number_format = '#,##0'
        r += 1
    
    r += 1
    ws.cell(r, 1, 'EBITDA').font = Font(bold=True, size=11)
    ws.cell(r, 2, 'USD')
    for yr in range(11):
        col = yr + 3
        c_ltr = get_column_letter(col)
        ws.cell(r, col).value = f'={c_ltr}{gp_r}-SUM({c_ltr}{opex_r+1}:{c_ltr}{r-2})'
        ws.cell(r, col).number_format = '#,##0'
        ws.cell(r, col).font = Font(bold=True)
        ws.cell(r, col).fill = PatternFill(start_color=Colors.GREEN, end_color=Colors.GREEN, fill_type='solid')
    
    # SOURCES SHEET
    print('  Creating Sources & References sheet...')
    ws = wb.create_sheet('Sources & References')
    ws.column_dimensions['A'].width = 30
    ws['A1'] = 'SOURCES & REFERENCES'
    hdr(ws['A1'], bg=Colors.TITLE_BLUE, sz=14)
    ws['A3'] = 'Populate with market research data using serp_market_research.py'
    
    # Save
    os.makedirs('.tmp', exist_ok=True)
    filename = f'{company_name.replace(" ", "_")}_financial_model.xlsx'
    filepath = os.path.join('.tmp', filename)
    wb.save(filepath)
    
    print(f'\n Financial model created!')
    print(f'   File: {filepath}')
    print(f'   Sheets: {', '.join(wb.sheetnames)}')
    print(f'\nNext steps:')
    print(f'  1. Open in Excel to review')
    print(f'  2. Upload to Google Drive when ready')
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Create local Excel financial model')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--config', help='Path to JSON config file')
    parser.add_argument('--rapidtools', action='store_true', help='Use RapidTools preset')
    args = parser.parse_args()
    
    config = None
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    try:
        filepath = create_financial_model_local(
            company_name=args.company,
            config=config,
            use_rapidtools=args.rapidtools
        )
        return filepath
    except Exception as e:
        print(f'\n Error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()