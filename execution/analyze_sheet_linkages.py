#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze Sheet Linkages - Find all formula references between sheets

Usage:
    python execution/analyze_sheet_linkages.py --sheet-id SPREADSHEET_ID --source "Sources & References" --target "Assumptions"
    python execution/analyze_sheet_linkages.py --sheet-id SPREADSHEET_ID --all

This tool helps understand which cells in one sheet are referenced by formulas in another sheet.
Critical for maintaining data integrity when restructuring sheets.

Examples:
    # Find all Sources & References cells linked from Assumptions
    python execution/analyze_sheet_linkages.py --sheet-id "1-Ss62..." --source "Sources & References" --target "Assumptions"
    
    # Find all linkages across all sheets
    python execution/analyze_sheet_linkages.py --sheet-id "1-Ss62..." --all
"""

import argparse
import re
from google.oauth2.credentials import Credentials
import gspread

def find_linkages(spreadsheet_id, source_sheet_name, target_sheet_name):
    """Find all cells in source_sheet referenced by formulas in target_sheet"""
    
    creds = Credentials.from_authorized_user_file("token.json", 
        scopes=["https://www.googleapis.com/auth/spreadsheets"])
    
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    target_sheet = spreadsheet.worksheet(target_sheet_name)
    source_sheet = spreadsheet.worksheet(source_sheet_name)
    
    print("="*80)
    print(f"FINDING LINKAGES: {source_sheet_name}  {target_sheet_name}")
    print("="*80)
    
    # Get all formulas from target sheet
    print(f"\nFetching formulas from {target_sheet_name}...")
    
    ranges = [f'{target_sheet_name}!A1:Z500']
    result = spreadsheet.values_batch_get(ranges, params={'valueRenderOption': 'FORMULA'})
    
    linked_cells = {}
    if result.get('valueRanges'):
        data = result['valueRanges'][0].get('values', [])
        
        for i, row in enumerate(data, 1):
            for j, cell in enumerate(row, 1):
                if cell and isinstance(cell, str) and (f"'{source_sheet_name}'" in cell or f"{source_sheet_name}!" in cell):
                    col_letter = chr(64 + j) if j <= 26 else chr(64 + (j-1)//26) + chr(65 + (j-1)%26)
                    
                    # Extract cell references
                    pattern = rf"'{source_sheet_name}'!([A-Z]+)(\d+)"
                    matches = re.finditer(pattern, cell)
                    
                    for match in matches:
                        src_col = match.group(1)
                        src_row = match.group(2)
                        ref = f"{src_col}{src_row}"
                        
                        if ref not in linked_cells:
                            linked_cells[ref] = []
                        linked_cells[ref].append(f"{target_sheet_name}!{col_letter}{i}")
    
    print(f"\nFound {len(linked_cells)} unique cells in '{source_sheet_name}' that are referenced")
    
    # Get values from source sheet
    src_data = source_sheet.get_all_values()
    
    print("\n" + "="*80)
    print("LINKAGE DETAILS")
    print("="*80)
    
    for src_cell in sorted(linked_cells.keys(), key=lambda x: (x[0], int(re.search(r'\d+', x).group()))):
        # Parse cell reference
        col_match = re.match(r'([A-Z]+)', src_cell)
        row_match = re.search(r'(\d+)', src_cell)
        
        if col_match and row_match:
            col_letters = col_match.group(1)
            row_num = int(row_match.group(1))
            
            # Convert column letters to index
            col_idx = 0
            for char in col_letters:
                col_idx = col_idx * 26 + (ord(char) - ord('A') + 1)
            col_idx -= 1
            
            # Get value and label
            if row_num - 1 < len(src_data):
                row_data = src_data[row_num - 1]
                label = row_data[0] if row_data else ""
                value = row_data[col_idx] if col_idx < len(row_data) else ""
                
                print(f"\n  {source_sheet_name}!{src_cell}: {label[:50]:50} = {value}")
                print(f"    Referenced by {len(linked_cells[src_cell])} cell(s):")
                for ref in linked_cells[src_cell][:3]:
                    print(f"       {ref}")
                if len(linked_cells[src_cell]) > 3:
                    print(f"      ... and {len(linked_cells[src_cell]) - 3} more")
    
    return linked_cells

def find_all_linkages(spreadsheet_id):
    """Find all linkages across all sheets in the spreadsheet"""
    
    creds = Credentials.from_authorized_user_file("token.json", 
        scopes=["https://www.googleapis.com/auth/spreadsheets"])
    
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    worksheets = spreadsheet.worksheets()
    
    print("="*80)
    print("FINDING ALL SHEET LINKAGES")
    print("="*80)
    print(f"\nAnalyzing {len(worksheets)} sheets...")
    
    all_linkages = {}
    
    for target_sheet in worksheets:
        target_name = target_sheet.title
        
        # Get all formulas
        data = target_sheet.get_all_values()
        ranges = [f'{target_name}!A1:Z500']
        result = spreadsheet.values_batch_get(ranges, params={'valueRenderOption': 'FORMULA'})
        
        if result.get('valueRanges'):
            formula_data = result['valueRanges'][0].get('values', [])
            
            for i, row in enumerate(formula_data, 1):
                for j, cell in enumerate(row, 1):
                    if cell and isinstance(cell, str) and '!' in cell:
                        # Extract sheet names referenced
                        matches = re.findall(r"'([^']+)'!", cell)
                        for source_name in matches:
                            if source_name != target_name:
                                key = f"{source_name}  {target_name}"
                                if key not in all_linkages:
                                    all_linkages[key] = 0
                                all_linkages[key] += 1
    
    print("\n" + "="*80)
    print("LINKAGE SUMMARY")
    print("="*80)
    
    for link, count in sorted(all_linkages.items(), key=lambda x: -x[1]):
        print(f"  {link:50} {count:5} references")
    
    return all_linkages

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze sheet linkages in Google Sheets financial model")
    parser.add_argument("--sheet-id", required=True, help="Google Sheets spreadsheet ID")
    parser.add_argument("--source", help="Source sheet name (e.g., 'Sources & References')")
    parser.add_argument("--target", help="Target sheet name (e.g., 'Assumptions')")
    parser.add_argument("--all", action="store_true", help="Find all linkages across all sheets")
    
    args = parser.parse_args()
    
    if args.all:
        find_all_linkages(args.sheet_id)
    elif args.source and args.target:
        find_linkages(args.sheet_id, args.source, args.target)
    else:
        print("Error: Provide either --all or both --source and --target")
        parser.print_help()
