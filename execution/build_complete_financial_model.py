#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete 14-Sheet Financial Model Builder

Creates a comprehensive financial model with all 14 sheets:
1. Sources & References - TAM/SAM/SOM with research links
2. Assumptions - All input parameters
3. Headcount Plan - Team growth by department
4. Revenue - Multi-stream revenue calculations
5. Operating Costs - COGS, Fixed, S&M
6. P&L - Profit & Loss with margins
7. Cash Flow - Operating, Investing, Financing
8. Balance Sheet - Assets, Liabilities, Equity
9. Summary - KPI dashboard
10. Sensitivity Analysis - Scenario modeling
11. Valuation - DCF and multiples
12. Break-even Analysis - Contribution margin
13. Funding Cap Table - Equity rounds
14. Charts Data - Data for visualizations

Usage:
    python build_complete_financial_model.py --config .tmp/rapidtools/config/rapidtools_config.json
    python build_complete_financial_model.py --company "RapidTools" --years 8
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
    from openpyxl.utils import get_column_letter
    from openpyxl.formatting.rule import FormulaRule
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl")
    sys.exit(1)


# =============================================================================
# COLOR PALETTE
# =============================================================================
class Colors:
    """Standard color palette matching the template."""
    TITLE_BLUE = '335080'      # Main titles - dark blue
    DARK_BLUE = '336699'       # Section headers
    MEDIUM_BLUE = '6699CC'     # Category headers
    SECTION_A_CAT = '4D80B3'   # Section A categories
    LIGHT_BLUE = 'D8EAF9'      # Zebra stripe / alternating rows
    LIGHT_GRAY = 'F2F2F2'      # Column headers
    GREEN = 'E5F8E5'           # Total/summary rows
    LIGHT_GREEN = 'C6EFCE'     # Positive values
    LIGHT_RED = 'FFC7CE'       # Negative values
    YELLOW = 'FFEB9C'          # Warning/attention
    WHITE = 'FFFFFF'
    BLACK = '000000'
    URL_BLUE = '1A4CB3'        # Hyperlinks
    GRAY = '808080'            # Notes


# =============================================================================
# STYLING HELPERS
# =============================================================================
def create_header_style(bg_color=Colors.DARK_BLUE, font_color=Colors.WHITE, 
                        size=12, bold=True):
    """Create header cell styling."""
    return {
        'font': Font(name='Calibri', size=size, bold=bold, color=font_color),
        'fill': PatternFill(start_color=bg_color, end_color=bg_color, fill_type='solid'),
        'alignment': Alignment(horizontal='center', vertical='center', wrap_text=True),
        'border': Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    }


def apply_style(cell, style_dict):
    """Apply a style dictionary to a cell."""
    for attr, value in style_dict.items():
        setattr(cell, attr, value)


def style_header(cell, bg=Colors.DARK_BLUE, fg=Colors.WHITE, size=12, bold=True):
    """Apply header styling to a cell."""
    cell.font = Font(name='Calibri', size=size, bold=bold, color=fg)
    cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )


def style_title(cell, text, bg=Colors.TITLE_BLUE):
    """Apply title styling."""
    cell.value = text
    cell.font = Font(name='Calibri', size=14, bold=True, color=Colors.WHITE)
    cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')
    cell.alignment = Alignment(horizontal='center', vertical='center')


def style_section_header(cell, text, bg=Colors.DARK_BLUE):
    """Apply section header styling."""
    cell.value = text
    style_header(cell, bg=bg, size=11)


def style_data_row(ws, row, start_col, end_col, is_total=False, zebra=False):
    """Apply styling to a data row."""
    bg = None
    if is_total:
        bg = Colors.GREEN
    elif zebra:
        bg = Colors.LIGHT_BLUE
    
    if bg:
        for col in range(start_col, end_col + 1):
            ws.cell(row, col).fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')


# =============================================================================
# YEAR HELPERS
# =============================================================================
def get_year_headers(num_years: int = 11) -> List[str]:
    """Get year headers from Year 0 to Year N."""
    return [f'Year {i}' for i in range(num_years)]


def get_year_columns(start_col: int = 3, num_years: int = 11) -> Dict[int, str]:
    """Get mapping of year index to column letter."""
    return {yr: get_column_letter(start_col + yr) for yr in range(num_years)}


# =============================================================================
# SHEET BUILDERS
# =============================================================================

class FinancialModelBuilder:
    """Builds a complete 14-sheet financial model."""
    
    def __init__(self, config: Dict[str, Any], num_years: int = 11):
        self.config = config
        self.num_years = num_years
        self.wb = Workbook()
        
        # Remove default sheet
        if 'Sheet' in self.wb.sheetnames:
            del self.wb['Sheet']
        
        # Track row positions for cross-sheet references
        self.row_refs = {}
    
    def build(self) -> Workbook:
        """Build all 14 sheets."""
        print("Building 14-sheet financial model...")
        print("=" * 60)
        
        # Build sheets in order (order matters for cross-references)
        self._build_sources_references()
        self._build_assumptions()
        self._build_headcount()
        self._build_revenue()
        self._build_operating_costs()
        self._build_pnl()
        self._build_cash_flow()
        self._build_balance_sheet()
        self._build_summary()
        self._build_sensitivity()
        self._build_valuation()
        self._build_breakeven()
        self._build_cap_table()
        self._build_charts_data()
        
        print("=" * 60)
        print(f"✅ Created {len(self.wb.sheetnames)} sheets")
        
        return self.wb
    
    def _build_sources_references(self):
        """Sheet 1: Sources & References - TAM/SAM/SOM data."""
        print("  📚 Building Sources & References...")
        ws = self.wb.create_sheet('Sources & References', 0)
        
        # Column widths
        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 60
        
        # Title
        style_title(ws['A1'], 'SOURCES & REFERENCES')
        ws.merge_cells('A1:D1')
        
        # Section A: Key Metrics
        row = 3
        style_section_header(ws.cell(row, 1), 'SECTION A: KEY METRICS (Linkable Values)')
        ws.merge_cells(f'A{row}:D{row}')
        row += 2
        
        # TAM Section
        style_section_header(ws.cell(row, 1), 'TAM - Total Addressable Market', bg=Colors.SECTION_A_CAT)
        ws.merge_cells(f'A{row}:D{row}')
        row += 1
        
        # TAM headers
        for col, header in enumerate(['Metric', 'Value', 'Unit', 'Source'], 1):
            style_header(ws.cell(row, col), bg=Colors.MEDIUM_BLUE, size=10)
            ws.cell(row, col).value = header
        row += 1
        
        # TAM data from config
        tam_data = self.config.get('tam', {})
        tam_items = [
            ('Software TAM', tam_data.get('software', 10000), 'M USD', 'Future Market Insights'),
            ('Hardware TAM', tam_data.get('hardware', 4000), 'M USD', 'GM Insights'),
            ('Consumables TAM', tam_data.get('consumables', 8000), 'M USD', 'Grand View Research'),
            ('Services TAM', tam_data.get('services', 20000), 'M USD', 'Mordor Intelligence'),
        ]
        
        self.row_refs['tam_start'] = row
        for metric, value, unit, source in tam_items:
            ws.cell(row, 1).value = metric
            ws.cell(row, 2).value = value
            ws.cell(row, 2).number_format = '#,##0'
            ws.cell(row, 3).value = unit
            ws.cell(row, 4).value = source
            row += 1
        
        # Total TAM
        ws.cell(row, 1).value = 'TOTAL TAM'
        ws.cell(row, 1).font = Font(bold=True)
        tam_end = row - 1
        ws.cell(row, 2).value = f'=SUM(B{self.row_refs["tam_start"]}:B{tam_end})'
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 2).font = Font(bold=True)
        ws.cell(row, 3).value = 'M USD'
        style_data_row(ws, row, 1, 4, is_total=True)
        self.row_refs['tam_total'] = row
        row += 2
        
        # SAM Section
        style_section_header(ws.cell(row, 1), 'SAM - Serviceable Addressable Market', bg=Colors.SECTION_A_CAT)
        ws.merge_cells(f'A{row}:D{row}')
        row += 1
        
        sam_data = self.config.get('sam', {})
        ws.cell(row, 1).value = 'India SAM'
        ws.cell(row, 2).value = sam_data.get('india', 1800)
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 3).value = 'M USD'
        self.row_refs['sam_india'] = row
        row += 1
        
        ws.cell(row, 1).value = 'SE Asia SAM'
        ws.cell(row, 2).value = sam_data.get('se_asia', 1080)
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 3).value = 'M USD'
        self.row_refs['sam_se_asia'] = row
        row += 1
        
        ws.cell(row, 1).value = 'TOTAL SAM'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = f'=B{self.row_refs["sam_india"]}+B{self.row_refs["sam_se_asia"]}'
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 2).font = Font(bold=True)
        ws.cell(row, 3).value = 'M USD'
        style_data_row(ws, row, 1, 4, is_total=True)
        self.row_refs['sam_total'] = row
        row += 2
        
        # SOM Section
        style_section_header(ws.cell(row, 1), 'SOM - Serviceable Obtainable Market', bg=Colors.SECTION_A_CAT)
        ws.merge_cells(f'A{row}:D{row}')
        row += 1
        
        som_data = self.config.get('som', {})
        ws.cell(row, 1).value = 'Year 8 Revenue Target'
        ws.cell(row, 2).value = som_data.get('year8_revenue', 104)
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 3).value = 'M USD'
        self.row_refs['som_target'] = row
        row += 1
        
        ws.cell(row, 1).value = 'Market Penetration'
        ws.cell(row, 2).value = f'=B{self.row_refs["som_target"]}/(B{self.row_refs["sam_total"]}*2)'
        ws.cell(row, 2).number_format = '0.00%'
        ws.cell(row, 3).value = '%'
        row += 2
        
        # Section B: Full Source Documentation
        style_section_header(ws.cell(row, 1), 'SECTION B: FULL SOURCE DOCUMENTATION')
        ws.merge_cells(f'A{row}:D{row}')
        row += 1
        
        ws.cell(row, 1).value = 'Add market research sources, URLs, and citations here'
        ws.cell(row, 1).font = Font(italic=True, color=Colors.GRAY)
    
    def _build_assumptions(self):
        """Sheet 2: Assumptions - All input parameters."""
        print("  ⚙️  Building Assumptions...")
        ws = self.wb.create_sheet('Assumptions')
        
        # Column widths
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 10
        for i in range(4, 4 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 12
        
        # Title
        style_title(ws['A1'], 'FINANCIAL MODEL ASSUMPTIONS')
        ws.merge_cells(f'A1:{get_column_letter(3 + self.num_years)}1')
        
        row = 3
        
        # General Parameters
        style_section_header(ws.cell(row, 1), 'GENERAL PARAMETERS')
        ws.merge_cells(f'A{row}:C{row}')
        row += 1
        
        general = self.config.get('general', {})
        params = [
            ('Tax Rate', general.get('tax_rate', 0.25), '%'),
            ('CapEx Year 0', general.get('capex_y0', 150000), 'USD'),
            ('CapEx Annual', general.get('capex_annual', 50000), 'USD'),
            ('Depreciation Period', general.get('depreciation_years', 5), 'Years'),
            ('Debtor Days', general.get('debtor_days', 45), 'Days'),
            ('Creditor Days', general.get('creditor_days', 30), 'Days'),
            ('Interest Rate', general.get('interest_rate', 0.10), '%'),
            ('Cost Inflation', general.get('cost_inflation', 0.05), '%'),
        ]
        
        self.row_refs['assumptions_start'] = row
        for name, value, unit in params:
            ws.cell(row, 1).value = name
            ws.cell(row, 2).value = value
            ws.cell(row, 3).value = unit
            if unit == '%':
                ws.cell(row, 2).number_format = '0.00%'
            elif unit == 'USD':
                ws.cell(row, 2).number_format = '#,##0'
            
            # Store row references for key params
            if name == 'Tax Rate':
                self.row_refs['tax_rate'] = row
            elif name == 'Depreciation Period':
                self.row_refs['depreciation_years'] = row
            elif name == 'Cost Inflation':
                self.row_refs['cost_inflation'] = row
            row += 1
        
        row += 1
        
        # Revenue Streams
        style_section_header(ws.cell(row, 1), 'REVENUE STREAMS')
        ws.merge_cells(f'A{row}:{get_column_letter(3 + self.num_years)}{row}')
        row += 1
        
        # Revenue headers
        headers = ['Stream', 'Price', 'Unit'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col), bg=Colors.MEDIUM_BLUE, size=10)
            ws.cell(row, col).value = header
        row += 1
        
        # Revenue stream data
        self.row_refs['revenue_streams_start'] = row
        streams = self.config.get('revenue_streams', [])
        
        for stream in streams:
            name = stream.get('name', 'Product')
            price = stream.get('price', 1000)
            volume_y0 = stream.get('volume', 10)
            growth = stream.get('growth', 0.25)
            
            # Price row
            ws.cell(row, 1).value = f"{name}: Price"
            ws.cell(row, 2).value = price
            ws.cell(row, 2).number_format = '#,##0'
            ws.cell(row, 3).value = 'USD'
            row += 1
            
            # Volume row with growth formula
            ws.cell(row, 1).value = f"{name}: Volume"
            ws.cell(row, 3).value = 'Units'
            for yr in range(self.num_years):
                col = 4 + yr
                if yr == 0:
                    ws.cell(row, col).value = volume_y0
                else:
                    prev_col = get_column_letter(col - 1)
                    ws.cell(row, col).value = f'=ROUND({prev_col}{row}*(1+{growth}),0)'
                ws.cell(row, col).number_format = '#,##0'
            row += 1
            
            # Growth rate row
            ws.cell(row, 1).value = f"{name}: Growth"
            ws.cell(row, 2).value = growth
            ws.cell(row, 2).number_format = '0.0%'
            ws.cell(row, 3).value = '%'
            row += 1
            
            # COGS % row
            ws.cell(row, 1).value = f"{name}: COGS %"
            ws.cell(row, 2).value = stream.get('cogs_pct', 0.30)
            ws.cell(row, 2).number_format = '0.0%'
            ws.cell(row, 3).value = '%'
            row += 1
        
        self.row_refs['revenue_streams_end'] = row - 1
        row += 1
        
        # Fixed Costs
        style_section_header(ws.cell(row, 1), 'FIXED COSTS (Annual)')
        ws.merge_cells(f'A{row}:C{row}')
        row += 1
        
        self.row_refs['fixed_costs_start'] = row
        fixed_costs = self.config.get('fixed_costs', {})
        if isinstance(fixed_costs, list):
            fixed_costs = {item['name']: item['value'] for item in fixed_costs}
        
        for name, value in fixed_costs.items():
            ws.cell(row, 1).value = name
            ws.cell(row, 2).value = value
            ws.cell(row, 2).number_format = '#,##0'
            ws.cell(row, 3).value = 'USD'
            row += 1
        
        self.row_refs['fixed_costs_end'] = row - 1
        row += 1
        
        # Funding Parameters
        style_section_header(ws.cell(row, 1), 'FUNDING PARAMETERS')
        ws.merge_cells(f'A{row}:C{row}')
        row += 1
        
        funding = self.config.get('funding', {})
        funding_params = [
            ('Seed Round', funding.get('seed', 3000000), 'USD'),
            ('Series A', funding.get('series_a', 10000000), 'USD'),
            ('Series B', funding.get('series_b', 25000000), 'USD'),
            ('Seed Timing (Year)', funding.get('seed_year', 0), 'Year'),
            ('Series A Timing (Year)', funding.get('series_a_year', 2), 'Year'),
            ('Series B Timing (Year)', funding.get('series_b_year', 4), 'Year'),
        ]
        
        self.row_refs['funding_start'] = row
        for name, value, unit in funding_params:
            ws.cell(row, 1).value = name
            ws.cell(row, 2).value = value
            if unit == 'USD':
                ws.cell(row, 2).number_format = '#,##0'
            ws.cell(row, 3).value = unit
            row += 1
        self.row_refs['funding_end'] = row - 1
    
    def _build_headcount(self):
        """Sheet 3: Headcount Plan."""
        print("  👥 Building Headcount Plan...")
        ws = self.wb.create_sheet('Headcount Plan')
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 15
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 12
        
        # Title
        style_title(ws['A1'], 'HEADCOUNT PLAN')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # Headers
        headers = ['Department', 'Avg Salary'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col))
            ws.cell(row, col).value = header
        row += 1
        
        # Headcount data
        headcount = self.config.get('headcount', {})
        departments = [
            ('Engineering', headcount.get('engineering_salary', 80000), headcount.get('engineering_y0', 5), 0.40),
            ('Sales & Marketing', headcount.get('sales_salary', 60000), headcount.get('sales_y0', 3), 0.50),
            ('Operations', headcount.get('ops_salary', 50000), headcount.get('ops_y0', 2), 0.35),
            ('G&A', headcount.get('ga_salary', 70000), headcount.get('ga_y0', 2), 0.25),
        ]
        
        self.row_refs['headcount_start'] = row
        for dept, salary, y0_count, growth in departments:
            ws.cell(row, 1).value = dept
            ws.cell(row, 2).value = salary
            ws.cell(row, 2).number_format = '#,##0'
            
            for yr in range(self.num_years):
                col = 3 + yr
                if yr == 0:
                    ws.cell(row, col).value = y0_count
                else:
                    prev_col = get_column_letter(col - 1)
                    ws.cell(row, col).value = f'=ROUND({prev_col}{row}*(1+{growth}),0)'
                ws.cell(row, col).number_format = '#,##0'
            row += 1
        
        self.row_refs['headcount_end'] = row - 1
        
        # Total headcount
        ws.cell(row, 1).value = 'TOTAL HEADCOUNT'
        ws.cell(row, 1).font = Font(bold=True)
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=SUM({col_letter}{self.row_refs["headcount_start"]}:{col_letter}{self.row_refs["headcount_end"]})'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['headcount_total'] = row
        row += 2
        
        # Total salary cost
        ws.cell(row, 1).value = 'TOTAL SALARY COST'
        ws.cell(row, 1).font = Font(bold=True)
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            # Sum of (headcount × salary) for each department
            formula_parts = []
            for dept_row in range(self.row_refs['headcount_start'], self.row_refs['headcount_end'] + 1):
                formula_parts.append(f'({col_letter}{dept_row}*B{dept_row})')
            ws.cell(row, col).value = f'={"+".join(formula_parts)}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['salary_cost_total'] = row
    
    def _build_revenue(self):
        """Sheet 4: Revenue calculations."""
        print("  📈 Building Revenue...")
        ws = self.wb.create_sheet('Revenue')
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 10
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 14
        
        # Title
        style_title(ws['A1'], 'REVENUE PROJECTIONS')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # Headers
        headers = ['Revenue Stream', 'Unit'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col))
            ws.cell(row, col).value = header
        row += 1
        
        # Revenue calculations per stream
        streams = self.config.get('revenue_streams', [])
        self.row_refs['revenue_start'] = row
        
        # Calculate which rows in Assumptions correspond to each stream
        # Each stream takes 4 rows (Price, Volume, Growth, COGS%)
        assumptions_stream_start = self.row_refs.get('revenue_streams_start', 17)
        
        for idx, stream in enumerate(streams):
            name = stream.get('name', f'Stream {idx+1}')
            ws.cell(row, 1).value = name
            ws.cell(row, 2).value = 'USD'
            
            # Price is at assumptions_stream_start + (idx * 4)
            # Volume is at assumptions_stream_start + (idx * 4) + 1
            price_row = assumptions_stream_start + (idx * 4)
            volume_row = price_row + 1
            
            for yr in range(self.num_years):
                col = 3 + yr
                yr_col = get_column_letter(4 + yr)  # Assumptions years start at column D
                # Revenue = Price × Volume
                ws.cell(row, col).value = f'=Assumptions!$B${price_row}*Assumptions!{yr_col}${volume_row}'
                ws.cell(row, col).number_format = '#,##0'
            row += 1
        
        self.row_refs['revenue_end'] = row - 1
        row += 1
        
        # Total Revenue
        ws.cell(row, 1).value = 'TOTAL REVENUE'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=SUM({col_letter}{self.row_refs["revenue_start"]}:{col_letter}{self.row_refs["revenue_end"]})'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['revenue_total'] = row
        row += 2
        
        # Revenue Mix %
        style_section_header(ws.cell(row, 1), 'REVENUE MIX %', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        for idx, stream in enumerate(streams):
            name = stream.get('name', f'Stream {idx+1}')
            ws.cell(row, 1).value = f'{name} %'
            ws.cell(row, 2).value = '%'
            
            stream_row = self.row_refs['revenue_start'] + idx
            for yr in range(self.num_years):
                col = 3 + yr
                col_letter = get_column_letter(col)
                ws.cell(row, col).value = f'=IF({col_letter}{self.row_refs["revenue_total"]}=0,0,{col_letter}{stream_row}/{col_letter}{self.row_refs["revenue_total"]})'
                ws.cell(row, col).number_format = '0.0%'
            row += 1
    
    def _build_operating_costs(self):
        """Sheet 5: Operating Costs - COGS, Fixed, S&M."""
        print("  💰 Building Operating Costs...")
        ws = self.wb.create_sheet('Operating Costs')
        
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 10
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 14
        
        # Title
        style_title(ws['A1'], 'OPERATING COSTS')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # COGS Section
        style_section_header(ws.cell(row, 1), 'COST OF GOODS SOLD (COGS)')
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        # COGS per stream
        streams = self.config.get('revenue_streams', [])
        self.row_refs['cogs_start'] = row
        assumptions_stream_start = self.row_refs.get('revenue_streams_start', 17)
        
        for idx, stream in enumerate(streams):
            name = stream.get('name', f'Stream {idx+1}')
            ws.cell(row, 1).value = f'COGS: {name}'
            ws.cell(row, 2).value = 'USD'
            
            # COGS % is at assumptions_stream_start + (idx * 4) + 3
            cogs_pct_row = assumptions_stream_start + (idx * 4) + 3
            revenue_row = self.row_refs['revenue_start'] + idx
            
            for yr in range(self.num_years):
                col = 3 + yr
                col_letter = get_column_letter(col)
                # COGS = Revenue × COGS%
                ws.cell(row, col).value = f'=Revenue!{col_letter}{revenue_row}*Assumptions!$B${cogs_pct_row}'
                ws.cell(row, col).number_format = '#,##0'
            row += 1
        
        self.row_refs['cogs_end'] = row - 1
        
        # Total COGS
        ws.cell(row, 1).value = 'TOTAL COGS'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=SUM({col_letter}{self.row_refs["cogs_start"]}:{col_letter}{self.row_refs["cogs_end"]})'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['cogs_total'] = row
        row += 2
        
        # Fixed Costs Section
        style_section_header(ws.cell(row, 1), 'FIXED COSTS')
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        # Salary costs from Headcount sheet
        ws.cell(row, 1).value = 'Salaries & Benefits'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Headcount Plan'!{col_letter}{self.row_refs.get('salary_cost_total', 10)}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['fixed_salaries'] = row
        row += 1
        
        # Other fixed costs from Assumptions
        self.row_refs['other_fixed_start'] = row
        fixed_costs = self.config.get('fixed_costs', {})
        if isinstance(fixed_costs, list):
            fixed_costs = {item['name']: item['value'] for item in fixed_costs}
        
        # Skip salaries if in fixed_costs (already from Headcount)
        cost_inflation = self.config.get('general', {}).get('cost_inflation', 0.05)
        
        for name, value in fixed_costs.items():
            if 'salary' not in name.lower() and 'salaries' not in name.lower():
                ws.cell(row, 1).value = name
                ws.cell(row, 2).value = 'USD'
                for yr in range(self.num_years):
                    col = 3 + yr
                    if yr == 0:
                        ws.cell(row, col).value = value
                    else:
                        prev_col = get_column_letter(col - 1)
                        ws.cell(row, col).value = f'={prev_col}{row}*(1+{cost_inflation})'
                    ws.cell(row, col).number_format = '#,##0'
                row += 1
        
        self.row_refs['other_fixed_end'] = row - 1
        
        # Total Fixed Costs
        ws.cell(row, 1).value = 'TOTAL FIXED COSTS'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["fixed_salaries"]}+SUM({col_letter}{self.row_refs["other_fixed_start"]}:{col_letter}{self.row_refs["other_fixed_end"]})'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['fixed_total'] = row
        row += 2
        
        # Total Operating Costs
        ws.cell(row, 1).value = 'TOTAL OPERATING COSTS'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["cogs_total"]}+{col_letter}{self.row_refs["fixed_total"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['opex_total'] = row
    
    def _build_pnl(self):
        """Sheet 6: Profit & Loss Statement."""
        print("  📊 Building P&L...")
        ws = self.wb.create_sheet('P&L')
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 10
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 14
        
        # Title
        style_title(ws['A1'], 'PROFIT & LOSS STATEMENT')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # Headers
        headers = ['Line Item', 'Unit'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col))
            ws.cell(row, col).value = header
        row += 1
        
        # Revenue
        ws.cell(row, 1).value = 'Revenue'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=Revenue!{col_letter}{self.row_refs["revenue_total"]}'
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['pnl_revenue'] = row
        row += 1
        
        # COGS
        ws.cell(row, 1).value = 'Cost of Goods Sold'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Operating Costs'!{col_letter}{self.row_refs['cogs_total']}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['pnl_cogs'] = row
        row += 1
        
        # Gross Profit
        ws.cell(row, 1).value = 'GROSS PROFIT'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["pnl_revenue"]}-{col_letter}{self.row_refs["pnl_cogs"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        self.row_refs['pnl_gross_profit'] = row
        row += 1
        
        # Gross Margin %
        ws.cell(row, 1).value = 'Gross Margin %'
        ws.cell(row, 2).value = '%'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=IF({col_letter}{self.row_refs["pnl_revenue"]}=0,0,{col_letter}{self.row_refs["pnl_gross_profit"]}/{col_letter}{self.row_refs["pnl_revenue"]})'
            ws.cell(row, col).number_format = '0.0%'
        row += 2
        
        # Operating Expenses
        ws.cell(row, 1).value = 'Operating Expenses'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Operating Costs'!{col_letter}{self.row_refs['fixed_total']}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['pnl_opex'] = row
        row += 1
        
        # EBITDA
        ws.cell(row, 1).value = 'EBITDA'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["pnl_gross_profit"]}-{col_letter}{self.row_refs["pnl_opex"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['pnl_ebitda'] = row
        row += 1
        
        # EBITDA Margin %
        ws.cell(row, 1).value = 'EBITDA Margin %'
        ws.cell(row, 2).value = '%'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=IF({col_letter}{self.row_refs["pnl_revenue"]}=0,0,{col_letter}{self.row_refs["pnl_ebitda"]}/{col_letter}{self.row_refs["pnl_revenue"]})'
            ws.cell(row, col).number_format = '0.0%'
        row += 2
        
        # Depreciation
        general = self.config.get('general', {})
        capex_y0 = general.get('capex_y0', 150000)
        capex_annual = general.get('capex_annual', 50000)
        dep_years = general.get('depreciation_years', 5)
        
        ws.cell(row, 1).value = 'Depreciation'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            # Simplified depreciation: Y0 capex / dep_years + annual capex / dep_years
            dep_value = capex_y0 / dep_years
            if yr > 0:
                dep_value += (capex_annual * min(yr, dep_years)) / dep_years
            ws.cell(row, col).value = round(dep_value)
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['pnl_depreciation'] = row
        row += 1
        
        # EBIT
        ws.cell(row, 1).value = 'EBIT (Operating Profit)'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["pnl_ebitda"]}-{col_letter}{self.row_refs["pnl_depreciation"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        self.row_refs['pnl_ebit'] = row
        row += 2
        
        # Interest (placeholder - 0 if no debt)
        ws.cell(row, 1).value = 'Interest Expense'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            ws.cell(row, col).value = 0
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['pnl_interest'] = row
        row += 1
        
        # PBT
        ws.cell(row, 1).value = 'PBT (Profit Before Tax)'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["pnl_ebit"]}-{col_letter}{self.row_refs["pnl_interest"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        self.row_refs['pnl_pbt'] = row
        row += 1
        
        # Tax
        tax_rate = general.get('tax_rate', 0.25)
        ws.cell(row, 1).value = f'Tax ({int(tax_rate*100)}%)'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=MAX(0,{col_letter}{self.row_refs["pnl_pbt"]}*{tax_rate})'
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['pnl_tax'] = row
        row += 1
        
        # PAT (Net Income)
        ws.cell(row, 1).value = 'NET INCOME (PAT)'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["pnl_pbt"]}-{col_letter}{self.row_refs["pnl_tax"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['pnl_net_income'] = row
        row += 1
        
        # Net Margin %
        ws.cell(row, 1).value = 'Net Margin %'
        ws.cell(row, 2).value = '%'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'=IF({col_letter}{self.row_refs["pnl_revenue"]}=0,0,{col_letter}{self.row_refs["pnl_net_income"]}/{col_letter}{self.row_refs["pnl_revenue"]})'
            ws.cell(row, col).number_format = '0.0%'
    
    def _build_cash_flow(self):
        """Sheet 7: Cash Flow Statement."""
        print("  💵 Building Cash Flow...")
        ws = self.wb.create_sheet('Cash Flow')
        
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 10
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 14
        
        # Title
        style_title(ws['A1'], 'CASH FLOW STATEMENT')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # Headers
        headers = ['Line Item', 'Unit'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col))
            ws.cell(row, col).value = header
        row += 1
        
        # Operating Activities
        style_section_header(ws.cell(row, 1), 'OPERATING ACTIVITIES', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        # Net Income
        ws.cell(row, 1).value = 'Net Income'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='P&L'!{col_letter}{self.row_refs['pnl_net_income']}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['cf_net_income'] = row
        row += 1
        
        # Add back Depreciation
        ws.cell(row, 1).value = '+ Depreciation'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='P&L'!{col_letter}{self.row_refs['pnl_depreciation']}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['cf_depreciation'] = row
        row += 1
        
        # Working Capital Change (simplified)
        ws.cell(row, 1).value = 'Working Capital Change'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            ws.cell(row, col).value = 0  # Simplified - would need AR/AP calculation
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['cf_wc_change'] = row
        row += 1
        
        # Operating Cash Flow
        ws.cell(row, 1).value = 'Operating Cash Flow'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["cf_net_income"]}+{col_letter}{self.row_refs["cf_depreciation"]}-{col_letter}{self.row_refs["cf_wc_change"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['cf_operating'] = row
        row += 2
        
        # Investing Activities
        style_section_header(ws.cell(row, 1), 'INVESTING ACTIVITIES', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        general = self.config.get('general', {})
        capex_y0 = general.get('capex_y0', 150000)
        capex_annual = general.get('capex_annual', 50000)
        
        ws.cell(row, 1).value = 'Capital Expenditure'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            capex = capex_y0 if yr == 0 else capex_annual
            ws.cell(row, col).value = -capex
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['cf_capex'] = row
        row += 1
        
        # Investing Cash Flow
        ws.cell(row, 1).value = 'Investing Cash Flow'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["cf_capex"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['cf_investing'] = row
        row += 2
        
        # Financing Activities
        style_section_header(ws.cell(row, 1), 'FINANCING ACTIVITIES', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        funding = self.config.get('funding', {})
        seed = funding.get('seed', 3000000)
        seed_year = funding.get('seed_year', 0)
        series_a = funding.get('series_a', 10000000)
        series_a_year = funding.get('series_a_year', 2)
        series_b = funding.get('series_b', 25000000)
        series_b_year = funding.get('series_b_year', 4)
        
        ws.cell(row, 1).value = 'Equity Raised'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            equity = 0
            if yr == seed_year:
                equity += seed
            if yr == series_a_year:
                equity += series_a
            if yr == series_b_year:
                equity += series_b
            ws.cell(row, col).value = equity
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['cf_equity'] = row
        row += 1
        
        # Financing Cash Flow
        ws.cell(row, 1).value = 'Financing Cash Flow'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["cf_equity"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['cf_financing'] = row
        row += 2
        
        # Net Cash Flow
        ws.cell(row, 1).value = 'NET CASH FLOW'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["cf_operating"]}+{col_letter}{self.row_refs["cf_investing"]}+{col_letter}{self.row_refs["cf_financing"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['cf_net'] = row
        row += 2
        
        # Cumulative Cash
        ws.cell(row, 1).value = 'CUMULATIVE CASH'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            if yr == 0:
                ws.cell(row, col).value = f'={col_letter}{self.row_refs["cf_net"]}'
            else:
                prev_col = get_column_letter(col - 1)
                ws.cell(row, col).value = f'={prev_col}{row}+{col_letter}{self.row_refs["cf_net"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['cf_cumulative'] = row
    
    def _build_balance_sheet(self):
        """Sheet 8: Balance Sheet."""
        print("  📋 Building Balance Sheet...")
        ws = self.wb.create_sheet('Balance Sheet')
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 10
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 14
        
        # Title
        style_title(ws['A1'], 'BALANCE SHEET')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # Headers
        headers = ['Line Item', 'Unit'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col))
            ws.cell(row, col).value = header
        row += 1
        
        # ASSETS
        style_section_header(ws.cell(row, 1), 'ASSETS', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        # Cash
        ws.cell(row, 1).value = 'Cash & Equivalents'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Cash Flow'!{col_letter}{self.row_refs['cf_cumulative']}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['bs_cash'] = row
        row += 1
        
        # Fixed Assets (simplified - Capex accumulation minus depreciation)
        ws.cell(row, 1).value = 'Net Fixed Assets'
        ws.cell(row, 2).value = 'USD'
        general = self.config.get('general', {})
        capex_y0 = general.get('capex_y0', 150000)
        capex_annual = general.get('capex_annual', 50000)
        dep_years = general.get('depreciation_years', 5)
        
        for yr in range(self.num_years):
            col = 3 + yr
            # Cumulative capex - cumulative depreciation
            cum_capex = capex_y0 + (capex_annual * yr)
            cum_dep = (capex_y0 / dep_years) * min(yr + 1, dep_years)
            if yr > 0:
                cum_dep += sum((capex_annual / dep_years) * min(yr - y, dep_years) for y in range(yr))
            ws.cell(row, col).value = round(max(0, cum_capex - cum_dep))
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['bs_fixed_assets'] = row
        row += 1
        
        # Total Assets
        ws.cell(row, 1).value = 'TOTAL ASSETS'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["bs_cash"]}+{col_letter}{self.row_refs["bs_fixed_assets"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['bs_total_assets'] = row
        row += 2
        
        # LIABILITIES & EQUITY
        style_section_header(ws.cell(row, 1), 'LIABILITIES & EQUITY', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        # Liabilities (simplified - 0 for now)
        ws.cell(row, 1).value = 'Total Liabilities'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            ws.cell(row, col).value = 0
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['bs_liabilities'] = row
        row += 2
        
        # Equity
        ws.cell(row, 1).value = 'Paid-in Capital'
        ws.cell(row, 2).value = 'USD'
        funding = self.config.get('funding', {})
        seed = funding.get('seed', 3000000)
        seed_year = funding.get('seed_year', 0)
        series_a = funding.get('series_a', 10000000)
        series_a_year = funding.get('series_a_year', 2)
        series_b = funding.get('series_b', 25000000)
        series_b_year = funding.get('series_b_year', 4)
        
        for yr in range(self.num_years):
            col = 3 + yr
            cum_equity = 0
            if yr >= seed_year:
                cum_equity += seed
            if yr >= series_a_year:
                cum_equity += series_a
            if yr >= series_b_year:
                cum_equity += series_b
            ws.cell(row, col).value = cum_equity
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['bs_paid_capital'] = row
        row += 1
        
        # Retained Earnings
        ws.cell(row, 1).value = 'Retained Earnings'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            if yr == 0:
                ws.cell(row, col).value = f"='P&L'!{col_letter}{self.row_refs['pnl_net_income']}"
            else:
                prev_col = get_column_letter(col - 1)
                ws.cell(row, col).value = f"={prev_col}{row}+'P&L'!{col_letter}{self.row_refs['pnl_net_income']}"
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['bs_retained_earnings'] = row
        row += 1
        
        # Total Equity
        ws.cell(row, 1).value = 'Total Equity'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["bs_paid_capital"]}+{col_letter}{self.row_refs["bs_retained_earnings"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        self.row_refs['bs_total_equity'] = row
        row += 1
        
        # Total Liabilities & Equity
        ws.cell(row, 1).value = 'TOTAL LIABILITIES & EQUITY'
        ws.cell(row, 1).font = Font(bold=True, size=11)
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["bs_liabilities"]}+{col_letter}{self.row_refs["bs_total_equity"]}'
            ws.cell(row, col).number_format = '#,##0'
            ws.cell(row, col).font = Font(bold=True)
        style_data_row(ws, row, 1, 2 + self.num_years, is_total=True)
        self.row_refs['bs_total_le'] = row
        row += 2
        
        # Balance Check
        ws.cell(row, 1).value = 'BALANCE CHECK (Assets = L+E)'
        ws.cell(row, 1).font = Font(bold=True, color=Colors.GRAY)
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f'={col_letter}{self.row_refs["bs_total_assets"]}-{col_letter}{self.row_refs["bs_total_le"]}'
            ws.cell(row, col).number_format = '#,##0'
        self.row_refs['bs_check'] = row
    
    def _build_summary(self):
        """Sheet 9: KPI Summary Dashboard."""
        print("  📈 Building Summary...")
        ws = self.wb.create_sheet('Summary')
        
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 10
        for i in range(3, 3 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 14
        
        # Title
        style_title(ws['A1'], 'KEY PERFORMANCE INDICATORS')
        ws.merge_cells(f'A1:{get_column_letter(2 + self.num_years)}1')
        
        row = 3
        
        # Headers
        headers = ['Metric', 'Unit'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col))
            ws.cell(row, col).value = header
        row += 1
        
        # Revenue Metrics
        style_section_header(ws.cell(row, 1), 'REVENUE METRICS', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        kpis = [
            ('Total Revenue', 'USD', f"='P&L'!{{col}}{self.row_refs['pnl_revenue']}", '#,##0'),
            ('Revenue Growth %', '%', None, '0.0%'),  # Calculated below
            ('Gross Margin %', '%', f"='P&L'!{{col}}{self.row_refs['pnl_gross_profit']}/'P&L'!{{col}}{self.row_refs['pnl_revenue']}", '0.0%'),
            ('EBITDA Margin %', '%', f"='P&L'!{{col}}{self.row_refs['pnl_ebitda']}/'P&L'!{{col}}{self.row_refs['pnl_revenue']}", '0.0%'),
        ]
        
        for name, unit, formula_template, num_format in kpis:
            ws.cell(row, 1).value = name
            ws.cell(row, 2).value = unit
            
            for yr in range(self.num_years):
                col = 3 + yr
                col_letter = get_column_letter(col)
                
                if name == 'Revenue Growth %':
                    if yr == 0:
                        ws.cell(row, col).value = 0
                    else:
                        prev_col = get_column_letter(col - 1)
                        rev_row = self.row_refs['pnl_revenue']
                        ws.cell(row, col).value = f"=IF('P&L'!{prev_col}{rev_row}=0,0,('P&L'!{col_letter}{rev_row}-'P&L'!{prev_col}{rev_row})/'P&L'!{prev_col}{rev_row})"
                elif formula_template:
                    formula = formula_template.replace('{col}', col_letter)
                    ws.cell(row, col).value = f'=IF(\'P&L\'!{col_letter}{self.row_refs["pnl_revenue"]}=0,0,{formula})'
                
                ws.cell(row, col).number_format = num_format
            row += 1
        
        row += 1
        
        # Team Metrics
        style_section_header(ws.cell(row, 1), 'TEAM METRICS', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        ws.cell(row, 1).value = 'Total Headcount'
        ws.cell(row, 2).value = 'FTE'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Headcount Plan'!{col_letter}{self.row_refs.get('headcount_total', 8)}"
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Revenue per Employee'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            hc_row = self.row_refs.get('headcount_total', 8)
            rev_row = self.row_refs['pnl_revenue']
            ws.cell(row, col).value = f"=IF('Headcount Plan'!{col_letter}{hc_row}=0,0,'P&L'!{col_letter}{rev_row}/'Headcount Plan'!{col_letter}{hc_row})"
            ws.cell(row, col).number_format = '#,##0'
        row += 2
        
        # Cash Metrics
        style_section_header(ws.cell(row, 1), 'CASH METRICS', bg=Colors.MEDIUM_BLUE)
        ws.merge_cells(f'A{row}:{get_column_letter(2 + self.num_years)}{row}')
        row += 1
        
        ws.cell(row, 1).value = 'Cash Balance'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Cash Flow'!{col_letter}{self.row_refs['cf_cumulative']}"
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Net Cash Flow'
        ws.cell(row, 2).value = 'USD'
        for yr in range(self.num_years):
            col = 3 + yr
            col_letter = get_column_letter(col)
            ws.cell(row, col).value = f"='Cash Flow'!{col_letter}{self.row_refs['cf_net']}"
            ws.cell(row, col).number_format = '#,##0'
    
    def _build_sensitivity(self):
        """Sheet 10: Sensitivity Analysis."""
        print("  🔬 Building Sensitivity Analysis...")
        ws = self.wb.create_sheet('Sensitivity Analysis')
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
        
        # Title
        style_title(ws['A1'], 'SENSITIVITY ANALYSIS')
        ws.merge_cells('A1:D1')
        
        row = 3
        
        # Scenario headers
        style_section_header(ws.cell(row, 1), 'SCENARIO COMPARISON')
        ws.merge_cells(f'A{row}:D{row}')
        row += 1
        
        headers = ['Metric', 'Downside (-20%)', 'Base Case', 'Upside (+20%)']
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col), bg=Colors.MEDIUM_BLUE, size=10)
            ws.cell(row, col).value = header
        row += 1
        
        ws.cell(row, 1).value = 'Year 8 Revenue'
        ws.cell(row, 2).value = '=0.8*C' + str(row)
        ws.cell(row, 3).value = "='P&L'!K4"  # Year 8 revenue (column K = 11 = Year 8)
        ws.cell(row, 4).value = '=1.2*C' + str(row)
        for col in range(2, 5):
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Year 8 EBITDA'
        ws.cell(row, 2).value = '=0.7*C' + str(row)  # More sensitive
        ws.cell(row, 3).value = f"='P&L'!K{self.row_refs['pnl_ebitda']}"
        ws.cell(row, 4).value = '=1.3*C' + str(row)
        for col in range(2, 5):
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Year 8 Cash'
        ws.cell(row, 2).value = '=0.75*C' + str(row)
        ws.cell(row, 3).value = f"='Cash Flow'!K{self.row_refs['cf_cumulative']}"
        ws.cell(row, 4).value = '=1.25*C' + str(row)
        for col in range(2, 5):
            ws.cell(row, col).number_format = '#,##0'
    
    def _build_valuation(self):
        """Sheet 11: DCF Valuation."""
        print("  💎 Building Valuation...")
        ws = self.wb.create_sheet('Valuation')
        
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 15
        
        # Title
        style_title(ws['A1'], 'VALUATION ANALYSIS')
        ws.merge_cells('A1:B1')
        
        row = 3
        
        # DCF Inputs
        style_section_header(ws.cell(row, 1), 'DCF ASSUMPTIONS')
        ws.merge_cells(f'A{row}:B{row}')
        row += 1
        
        dcf_inputs = [
            ('Discount Rate (WACC)', 0.15, '0.0%'),
            ('Terminal Growth Rate', 0.03, '0.0%'),
            ('Exit Multiple (EV/Revenue)', 5.0, '0.0x'),
        ]
        
        for name, value, fmt in dcf_inputs:
            ws.cell(row, 1).value = name
            ws.cell(row, 2).value = value
            ws.cell(row, 2).number_format = fmt
            row += 1
        
        row += 1
        
        # Valuation Summary
        style_section_header(ws.cell(row, 1), 'VALUATION SUMMARY')
        ws.merge_cells(f'A{row}:B{row}')
        row += 1
        
        ws.cell(row, 1).value = 'Year 8 Revenue'
        ws.cell(row, 2).value = f"='P&L'!K{self.row_refs['pnl_revenue']}"
        ws.cell(row, 2).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Implied Exit Valuation (5x Rev)'
        ws.cell(row, 2).value = f"=B{row-1}*5"
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 2).font = Font(bold=True)
    
    def _build_breakeven(self):
        """Sheet 12: Break-even Analysis."""
        print("  ⚖️  Building Break-even Analysis...")
        ws = self.wb.create_sheet('Break-even Analysis')
        
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 15
        
        # Title
        style_title(ws['A1'], 'BREAK-EVEN ANALYSIS')
        ws.merge_cells('A1:B1')
        
        row = 3
        
        ws.cell(row, 1).value = 'Analysis to be populated based on contribution margin'
        ws.cell(row, 1).font = Font(italic=True, color=Colors.GRAY)
    
    def _build_cap_table(self):
        """Sheet 13: Funding & Cap Table."""
        print("  📊 Building Cap Table...")
        ws = self.wb.create_sheet('Funding Cap Table')
        
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        
        # Title
        style_title(ws['A1'], 'FUNDING & CAP TABLE')
        ws.merge_cells('A1:E1')
        
        row = 3
        
        # Funding Rounds
        style_section_header(ws.cell(row, 1), 'FUNDING ROUNDS')
        ws.merge_cells(f'A{row}:E{row}')
        row += 1
        
        headers = ['Round', 'Amount', 'Pre-Money', 'Post-Money', 'Dilution']
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col), bg=Colors.MEDIUM_BLUE, size=10)
            ws.cell(row, col).value = header
        row += 1
        
        funding = self.config.get('funding', {})
        rounds = [
            ('Seed', funding.get('seed', 3000000), funding.get('seed_pre', 10000000)),
            ('Series A', funding.get('series_a', 10000000), funding.get('series_a_pre', 30000000)),
            ('Series B', funding.get('series_b', 25000000), funding.get('series_b_pre', 75000000)),
        ]
        
        for round_name, amount, pre_money in rounds:
            ws.cell(row, 1).value = round_name
            ws.cell(row, 2).value = amount
            ws.cell(row, 2).number_format = '#,##0'
            ws.cell(row, 3).value = pre_money
            ws.cell(row, 3).number_format = '#,##0'
            ws.cell(row, 4).value = f'=B{row}+C{row}'
            ws.cell(row, 4).number_format = '#,##0'
            ws.cell(row, 5).value = f'=B{row}/D{row}'
            ws.cell(row, 5).number_format = '0.0%'
            row += 1
        
        # Total Raised
        row += 1
        ws.cell(row, 1).value = 'TOTAL RAISED'
        ws.cell(row, 1).font = Font(bold=True)
        ws.cell(row, 2).value = f'=SUM(B{row-4}:B{row-2})'
        ws.cell(row, 2).number_format = '#,##0'
        ws.cell(row, 2).font = Font(bold=True)
        style_data_row(ws, row, 1, 5, is_total=True)
    
    def _build_charts_data(self):
        """Sheet 14: Charts Data."""
        print("  📉 Building Charts Data...")
        ws = self.wb.create_sheet('Charts Data')
        
        ws.column_dimensions['A'].width = 25
        for i in range(2, 2 + self.num_years):
            ws.column_dimensions[get_column_letter(i)].width = 12
        
        # Title
        style_title(ws['A1'], 'CHARTS DATA')
        ws.merge_cells(f'A1:{get_column_letter(1 + self.num_years)}1')
        
        row = 3
        
        # Revenue data for charts
        headers = ['Metric'] + get_year_headers(self.num_years)
        for col, header in enumerate(headers, 1):
            style_header(ws.cell(row, col), bg=Colors.MEDIUM_BLUE, size=10)
            ws.cell(row, col).value = header
        row += 1
        
        ws.cell(row, 1).value = 'Revenue'
        for yr in range(self.num_years):
            col = 2 + yr
            col_letter = get_column_letter(3 + yr)  # P&L starts at column C
            ws.cell(row, col).value = f"='P&L'!{col_letter}{self.row_refs['pnl_revenue']}"
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'EBITDA'
        for yr in range(self.num_years):
            col = 2 + yr
            col_letter = get_column_letter(3 + yr)
            ws.cell(row, col).value = f"='P&L'!{col_letter}{self.row_refs['pnl_ebitda']}"
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Net Income'
        for yr in range(self.num_years):
            col = 2 + yr
            col_letter = get_column_letter(3 + yr)
            ws.cell(row, col).value = f"='P&L'!{col_letter}{self.row_refs['pnl_net_income']}"
            ws.cell(row, col).number_format = '#,##0'
        row += 1
        
        ws.cell(row, 1).value = 'Cash Balance'
        for yr in range(self.num_years):
            col = 2 + yr
            col_letter = get_column_letter(3 + yr)
            ws.cell(row, col).value = f"='Cash Flow'!{col_letter}{self.row_refs['cf_cumulative']}"
            ws.cell(row, col).number_format = '#,##0'
    
    def save(self, filepath: str):
        """Save the workbook to file."""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        self.wb.save(filepath)
        print(f"\n✅ Saved: {filepath}")
        return filepath


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"WARNING: Config not found: {config_path}")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_default_config() -> Dict[str, Any]:
    """Create default configuration for testing."""
    return {
        'company': 'TestCompany',
        'general': {
            'tax_rate': 0.25,
            'capex_y0': 150000,
            'capex_annual': 50000,
            'depreciation_years': 5,
            'debtor_days': 45,
            'creditor_days': 30,
            'interest_rate': 0.10,
            'cost_inflation': 0.05
        },
        'revenue_streams': [
            {'name': 'Software', 'price': 2500, 'volume': 25, 'growth': 0.50, 'cogs_pct': 0.15},
            {'name': 'Hardware', 'price': 5000, 'volume': 15, 'growth': 0.35, 'cogs_pct': 0.60},
            {'name': 'Services', 'price': 10000, 'volume': 5, 'growth': 0.40, 'cogs_pct': 0.45},
        ],
        'fixed_costs': {
            'Office & Utilities': 36000,
            'Marketing': 60000,
            'R&D': 72000,
            'Legal & Compliance': 24000,
            'Insurance': 12000,
        },
        'headcount': {
            'engineering_salary': 80000, 'engineering_y0': 5,
            'sales_salary': 60000, 'sales_y0': 3,
            'ops_salary': 50000, 'ops_y0': 2,
            'ga_salary': 70000, 'ga_y0': 2,
        },
        'funding': {
            'seed': 3000000, 'seed_year': 0, 'seed_pre': 10000000,
            'series_a': 10000000, 'series_a_year': 2, 'series_a_pre': 30000000,
            'series_b': 25000000, 'series_b_year': 4, 'series_b_pre': 75000000,
        },
        'tam': {'software': 10000, 'hardware': 4000, 'consumables': 8000, 'services': 20000},
        'sam': {'india': 1800, 'se_asia': 1080},
        'som': {'year8_revenue': 104},
    }


def main():
    parser = argparse.ArgumentParser(
        description='Build complete 14-sheet financial model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python build_complete_financial_model.py --config .tmp/rapidtools/config/rapidtools_config.json
  python build_complete_financial_model.py --company "TestCompany" --years 8
  python build_complete_financial_model.py --company "RapidTools" --output .tmp/rapidtools_model.xlsx

The script creates all 14 sheets with proper cross-sheet formulas:
  1. Sources & References    9. Summary
  2. Assumptions            10. Sensitivity Analysis
  3. Headcount Plan         11. Valuation
  4. Revenue                12. Break-even Analysis
  5. Operating Costs        13. Funding Cap Table
  6. P&L                    14. Charts Data
  7. Cash Flow
  8. Balance Sheet
        '''
    )
    parser.add_argument('--config', '-c', help='Path to JSON config file')
    parser.add_argument('--company', help='Company name (for default config)')
    parser.add_argument('--years', type=int, default=11, help='Number of years (default: 11 = Year 0 to Year 10)')
    parser.add_argument('--output', '-o', help='Output Excel file path')
    parser.add_argument('--validate', '-v', action='store_true', help='Validate after creation')
    
    args = parser.parse_args()
    
    # Load or create config
    if args.config:
        config = load_config(args.config)
        company = config.get('company', 'FinancialModel')
    elif args.company:
        config = create_default_config()
        config['company'] = args.company
        company = args.company
    else:
        print("ERROR: Provide --config or --company")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        os.makedirs('.tmp', exist_ok=True)
        output_path = f'.tmp/{company.replace(" ", "_")}_complete_model.xlsx'
    
    # Build the model
    builder = FinancialModelBuilder(config, num_years=args.years)
    builder.build()
    builder.save(output_path)
    
    # Validate if requested
    if args.validate:
        print("\nValidating formulas...")
        try:
            from validate_excel_model import validate_excel_model
            success, report = validate_excel_model(output_path, verbose=True)
            print(report)
            if not success:
                sys.exit(1)
        except ImportError:
            print("WARNING: validate_excel_model not available")
    
    print(f"\nNext steps:")
    print(f"  1. Review in Excel: start {output_path}")
    print(f"  2. Validate formulas:")
    print(f"     python execution/validate_excel_model.py --file {output_path}")
    print(f"  3. Upload to Google Sheets:")
    print(f"     python execution/sync_to_cloud.py --file {output_path}")


if __name__ == '__main__':
    main()
