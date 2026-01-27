#!/usr/bin/env python3
"""Verify Sheet Integrity - Check formulas after restructuring"""
import argparse, re
from google.oauth2.credentials import Credentials
import gspread

def verify_formulas(sheet_id, sheet_name):
    creds = Credentials.from_authorized_user_file("token.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)
    sheet = spreadsheet.worksheet(sheet_name)
    
    result = spreadsheet.values_batch_get([f'{sheet_name}!A1:Z500'], params={'valueRenderOption':'FORMULA'})
    formulas = result['valueRanges'][0].get('values',[])
    values = sheet.get_all_values()
    
    errors = []
    for i, row in enumerate(formulas):
        for j, cell in enumerate(row):
            if cell and isinstance(cell, str) and cell.startswith('='):
                val = values[i][j] if i<len(values) and j<len(values[i]) else ''
                if val in ['#ERROR!','#REF!','#VALUE!','#DIV/0!']:
                    errors.append({'cell':f"{chr(65+j)}{i+1}", 'error':val})
    
    print(f"{sheet_name}: {len(errors)} errors")
    for e in errors[:10]:
        print(f"  {e['cell']}: {e['error']}")
    return errors

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--sheet", required=True)
    args = p.parse_args()
    verify_formulas(args.sheet_id, args.sheet)
