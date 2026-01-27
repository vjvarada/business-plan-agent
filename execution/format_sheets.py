#!/usr/bin/env python3
"""
Reusable formatting utilities for Google Sheets financial models.

This module provides consistent formatting across all sheets in a financial model.
It defines standard colors, formats, and helper functions that ensure visual
consistency throughout the workbook.

Usage:
    from format_sheets import SheetFormatter
    
    formatter = SheetFormatter(spreadsheet)
    formatter.format_assumptions_sheet()
    formatter.format_all_sheets()

Or standalone:
    python format_sheets.py --sheet-id "1-Ss62..." --sheet "Assumptions"
    python format_sheets.py --sheet-id "1-Ss62..." --all
"""

import os
import sys
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# STANDARD COLOR DEFINITIONS (Exact RGB Values)
# ============================================================================

class Colors:
    """Standard color palette for financial model sheets.
    
    All colors defined as RGB tuples (red, green, blue) with values 0.0-1.0
    """
    
    # Primary colors for headers
    TITLE_BLUE = (0.20, 0.30, 0.50)           # Main title - #335080
    DARK_BLUE = (0.20, 0.40, 0.60)            # Section headers - #336699
    MEDIUM_BLUE = (0.40, 0.60, 0.80)          # Category headers (Section B) - #6699CC
    SECTION_A_CAT = (0.30, 0.50, 0.70)        # Category headers (Section A) - #4D80B3
    
    # Data row colors
    LIGHT_BLUE = (0.85, 0.92, 0.98)           # Zebra stripe - #D8EAF9
    WHITE = (1.0, 1.0, 1.0)                   # White - #FFFFFF
    LIGHT_GRAY = (0.95, 0.95, 0.95)           # Column headers - #F2F2F2
    
    # Text colors
    BLACK = (0.0, 0.0, 0.0)                   # Standard text - #000000
    URL_BLUE = (0.10, 0.30, 0.70)             # URL text - #1A4CB3
    
    # Special colors
    GRAY = (0.50, 0.50, 0.50)                 # Notes header - #808080
    GREEN = (0.90, 0.97, 0.90)                # Positive/totals - #E5F8E5
    RED_LIGHT = (0.98, 0.90, 0.90)            # Negative/warnings - #FAE5E5
    YELLOW_LIGHT = (1.0, 0.98, 0.90)          # Highlights - #FFFAE5


class SheetFormatter:
    """Formats Google Sheets with consistent styling.
    
    Provides methods to format individual sheets or the entire workbook
    with standardized colors, fonts, and layouts.
    """
    
    def __init__(self, spreadsheet):
        """Initialize formatter with a gspread spreadsheet object.
        
        Args:
            spreadsheet: gspread.Spreadsheet object
        """
        self.spreadsheet = spreadsheet
        self._import_formatting()
    
    def _import_formatting(self):
        """Import gspread_formatting module."""
        try:
            from gspread_formatting import (
                CellFormat, Color, TextFormat, format_cell_range,
                set_column_width, set_row_height, batch_updater
            )
            self.CellFormat = CellFormat
            self.Color = Color
            self.TextFormat = TextFormat
            self.format_cell_range = format_cell_range
            self.set_column_width = set_column_width
            self.set_row_height = set_row_height
            self.batch_updater = batch_updater
            self._formatting_available = True
        except ImportError:
            print("Warning: gspread-formatting not available. Install with: pip install gspread-formatting")
            self._formatting_available = False
    
    def _color(self, rgb_tuple):
        """Convert RGB tuple to gspread Color object."""
        return self.Color(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
    
    def _delay(self, seconds=0.3):
        """Rate limit delay to avoid API limits."""
        time.sleep(seconds)
    
    # ========================================================================
    # STANDARD FORMAT DEFINITIONS
    # ========================================================================
    
    def get_title_format(self, font_size=14):
        """Main title format - dark blue background, white bold text."""
        return self.CellFormat(
            backgroundColor=self._color(Colors.TITLE_BLUE),
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.WHITE), fontSize=font_size),
            horizontalAlignment='LEFT'
        )
    
    def get_section_header_format(self, font_size=12):
        """Section header format - dark blue background, white bold text."""
        return self.CellFormat(
            backgroundColor=self._color(Colors.DARK_BLUE),
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.WHITE), fontSize=font_size),
            horizontalAlignment='LEFT'
        )
    
    def get_category_header_format(self, section='B', font_size=11):
        """Category header format - medium blue background, white bold text.
        
        Args:
            section: 'A' for Section A style, 'B' for Section B style
            font_size: Font size in points
        """
        bg_color = Colors.SECTION_A_CAT if section == 'A' else Colors.MEDIUM_BLUE
        return self.CellFormat(
            backgroundColor=self._color(bg_color),
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.WHITE), fontSize=font_size),
            horizontalAlignment='LEFT'
        )
    
    def get_column_header_format(self):
        """Column header format - light gray background, bold black text."""
        return self.CellFormat(
            backgroundColor=self._color(Colors.LIGHT_GRAY),
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.BLACK)),
            horizontalAlignment='CENTER'
        )
    
    def get_data_row_format(self, striped=False):
        """Data row format with optional zebra striping.
        
        Args:
            striped: If True, uses light blue background; if False, white
        """
        bg_color = Colors.LIGHT_BLUE if striped else Colors.WHITE
        return self.CellFormat(
            backgroundColor=self._color(bg_color),
            textFormat=self.TextFormat(bold=False, foregroundColor=self._color(Colors.BLACK)),
            horizontalAlignment='LEFT'
        )
    
    def get_total_row_format(self):
        """Total/summary row format - light green background, bold text."""
        return self.CellFormat(
            backgroundColor=self._color(Colors.GREEN),
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.BLACK)),
            horizontalAlignment='LEFT'
        )
    
    def get_url_format(self):
        """URL text format - blue text color."""
        return self.CellFormat(
            textFormat=self.TextFormat(foregroundColor=self._color(Colors.URL_BLUE))
        )
    
    def get_notes_header_format(self):
        """Notes section header - gray background, white bold text."""
        return self.CellFormat(
            backgroundColor=self._color(Colors.GRAY),
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.WHITE)),
            horizontalAlignment='LEFT'
        )
    
    def get_subsection_header_format(self):
        """Subsection header - no background, bold black text."""
        return self.CellFormat(
            textFormat=self.TextFormat(bold=True, foregroundColor=self._color(Colors.BLACK), fontSize=10),
            horizontalAlignment='LEFT'
        )
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def apply_zebra_striping(self, sheet, start_row, end_row, start_col='A', end_col='M'):
        """Apply zebra striping to a range of data rows.
        
        Args:
            sheet: gspread worksheet object
            start_row: First row number (1-indexed)
            end_row: Last row number (1-indexed)
            start_col: Start column letter
            end_col: End column letter
        """
        if not self._formatting_available:
            return
        
        for i, row in enumerate(range(start_row, end_row + 1)):
            striped = (i % 2 == 1)
            fmt = self.get_data_row_format(striped=striped)
            self.format_cell_range(sheet, f'{start_col}{row}:{end_col}{row}', fmt)
            self._delay(0.15)
    
    def format_header_row(self, sheet, row_num, end_col='M'):
        """Format a row as column headers.
        
        Args:
            sheet: gspread worksheet object
            row_num: Row number (1-indexed)
            end_col: End column letter
        """
        if not self._formatting_available:
            return
        
        self.format_cell_range(sheet, f'A{row_num}:{end_col}{row_num}', self.get_column_header_format())
        self._delay()
    
    def format_section_by_markers(self, sheet, section_markers, category_markers=None):
        """Format a sheet based on section and category markers.
        
        Args:
            sheet: gspread worksheet object
            section_markers: List of strings that indicate section headers (e.g., '--- GENERAL ---')
            category_markers: Optional list of category header markers
        """
        if not self._formatting_available:
            return
        
        data = sheet.get_all_values()
        self._delay(0.5)
        
        for i, row in enumerate(data):
            cell_value = row[0] if row else ''
            
            # Check for section headers
            for marker in section_markers:
                if marker in cell_value:
                    self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_section_header_format())
                    self._delay(0.2)
                    break
            
            # Check for category headers
            if category_markers:
                for marker in category_markers:
                    if marker in cell_value:
                        self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_category_header_format(section='A'))
                        self._delay(0.2)
                        break
    
    # ========================================================================
    # SHEET-SPECIFIC FORMATTING
    # ========================================================================
    
    def format_assumptions_sheet(self):
        """Format the Assumptions sheet with consistent styling."""
        if not self._formatting_available:
            print("Formatting not available - skipping")
            return
        
        try:
            sheet = self.spreadsheet.worksheet('Assumptions')
        except Exception as e:
            print(f"Could not find Assumptions sheet: {e}")
            return
        
        print("Formatting Assumptions sheet...")
        data = sheet.get_all_values()
        self._delay(0.5)
        
        # 1. Format title row
        print("  - Title row...")
        self.format_cell_range(sheet, 'A1:M1', self.get_title_format())
        self._delay()
        
        # 2. Format column header row (row 2 with Year labels)
        print("  - Column headers...")
        self.format_cell_range(sheet, 'A2:M2', self.get_column_header_format())
        self._delay()
        
        # 3. Find and format section headers
        section_markers = [
            '--- GENERAL',
            '--- REVENUE',
            '--- FIXED COSTS',
            '--- CUSTOMER',
            '--- GEOGRAPHIC',
            '--- INDUSTRY',
            '--- KEY RELATIONSHIPS',
            '--- REGIONAL',
            '--- SEATS',
            '--- TAM',
            '--- SAM',
            '--- SOM'
        ]
        
        print("  - Section headers...")
        section_rows = []
        for i, row in enumerate(data):
            cell_value = row[0] if row else ''
            for marker in section_markers:
                if marker in cell_value:
                    section_rows.append(i + 1)
                    self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_section_header_format())
                    self._delay(0.2)
                    break
        
        # 4. Apply zebra striping to data rows (between sections)
        print("  - Data row formatting...")
        section_rows.append(len(data) + 1)  # Add end marker
        
        for idx in range(len(section_rows) - 1):
            start = section_rows[idx] + 1
            end = section_rows[idx + 1] - 1
            if end > start:
                self.apply_zebra_striping(sheet, start, end, 'A', 'M')
        
        # 5. Set column widths
        print("  - Column widths...")
        self.set_column_width(sheet, 'A', 280)
        self.set_column_width(sheet, 'B', 80)
        for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
            self.set_column_width(sheet, col, 100)
        self._delay()
        
        print("  ✓ Assumptions sheet formatted")
    
    def format_pnl_sheet(self):
        """Format the P&L sheet with consistent styling."""
        if not self._formatting_available:
            return
        
        try:
            sheet = self.spreadsheet.worksheet('P&L')
        except Exception:
            return
        
        print("Formatting P&L sheet...")
        data = sheet.get_all_values()
        self._delay(0.5)
        
        # Title
        self.format_cell_range(sheet, 'A1:M1', self.get_title_format())
        self._delay()
        
        # Column headers
        self.format_cell_range(sheet, 'A2:M2', self.get_column_header_format())
        self._delay()
        
        # Find key rows
        total_markers = ['Total Revenue', 'Gross Profit', 'EBITDA', 'Net Income', 'PAT']
        section_markers = ['Revenue', 'Cost of Goods', 'Operating Expenses', 'COGS']
        
        for i, row in enumerate(data):
            cell_value = row[0] if row else ''
            
            # Total rows
            for marker in total_markers:
                if marker in cell_value:
                    self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_total_row_format())
                    self._delay(0.15)
                    break
            
            # Section headers
            for marker in section_markers:
                if cell_value.strip() == marker or cell_value.startswith(f'{marker} '):
                    self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_section_header_format())
                    self._delay(0.15)
                    break
        
        print("  ✓ P&L sheet formatted")
    
    def format_revenue_sheet(self):
        """Format the Revenue sheet with consistent styling."""
        if not self._formatting_available:
            return
        
        try:
            sheet = self.spreadsheet.worksheet('Revenue')
        except Exception:
            return
        
        print("Formatting Revenue sheet...")
        data = sheet.get_all_values()
        self._delay(0.5)
        
        # Title and headers
        self.format_cell_range(sheet, 'A1:M1', self.get_title_format())
        self._delay()
        self.format_cell_range(sheet, 'A2:M2', self.get_column_header_format())
        self._delay()
        
        # Find Total Revenue row
        for i, row in enumerate(data):
            if row[0] and 'Total Revenue' in row[0]:
                self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_total_row_format())
                self._delay()
                break
        
        print("  ✓ Revenue sheet formatted")
    
    def format_operating_costs_sheet(self):
        """Format the Operating Costs sheet."""
        if not self._formatting_available:
            return
        
        try:
            sheet = self.spreadsheet.worksheet('Operating Costs')
        except Exception:
            return
        
        print("Formatting Operating Costs sheet...")
        data = sheet.get_all_values()
        self._delay(0.5)
        
        self.format_cell_range(sheet, 'A1:M1', self.get_title_format())
        self._delay()
        self.format_cell_range(sheet, 'A2:M2', self.get_column_header_format())
        self._delay()
        
        section_markers = ['COGS', 'Fixed Costs', 'S&M', 'Sales & Marketing']
        total_markers = ['Total COGS', 'Total Fixed', 'Total S&M', 'Total Operating']
        
        for i, row in enumerate(data):
            cell_value = row[0] if row else ''
            
            for marker in section_markers:
                if cell_value.strip().startswith(marker):
                    self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_section_header_format())
                    self._delay(0.15)
                    break
            
            for marker in total_markers:
                if marker in cell_value:
                    self.format_cell_range(sheet, f'A{i+1}:M{i+1}', self.get_total_row_format())
                    self._delay(0.15)
                    break
        
        print("  ✓ Operating Costs sheet formatted")
    
    def format_all_sheets(self):
        """Format all sheets in the financial model."""
        print("="*60)
        print("FORMATTING ALL SHEETS")
        print("="*60)
        
        self.format_assumptions_sheet()
        self.format_revenue_sheet()
        self.format_operating_costs_sheet()
        self.format_pnl_sheet()
        
        # Add more sheets as needed
        # self.format_cash_flow_sheet()
        # self.format_balance_sheet()
        # etc.
        
        print("="*60)
        print("✓ All sheets formatted")
        print("="*60)


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================

def get_credentials():
    """Get OAuth2 credentials for Google Sheets API."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


def main():
    parser = argparse.ArgumentParser(description='Format Google Sheets financial model')
    parser.add_argument('--sheet-id', required=True, help='Google Sheets ID')
    parser.add_argument('--sheet', help='Specific sheet to format (e.g., Assumptions, P&L)')
    parser.add_argument('--all', action='store_true', help='Format all sheets')
    
    args = parser.parse_args()
    
    import gspread
    
    creds = get_credentials()
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(args.sheet_id)
    
    formatter = SheetFormatter(spreadsheet)
    
    if args.all:
        formatter.format_all_sheets()
    elif args.sheet:
        sheet_name = args.sheet.lower()
        if sheet_name == 'assumptions':
            formatter.format_assumptions_sheet()
        elif sheet_name == 'p&l' or sheet_name == 'pnl':
            formatter.format_pnl_sheet()
        elif sheet_name == 'revenue':
            formatter.format_revenue_sheet()
        elif sheet_name == 'operating costs':
            formatter.format_operating_costs_sheet()
        else:
            print(f"Unknown sheet: {args.sheet}")
            sys.exit(1)
    else:
        print("Please specify --sheet or --all")
        sys.exit(1)


if __name__ == '__main__':
    main()
