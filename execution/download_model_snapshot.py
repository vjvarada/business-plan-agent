#!/usr/bin/env python3
"""
Download Financial Model Snapshot
==================================
Downloads entire Google Sheets financial model to local CSV files with formulas preserved.

Usage:
    python download_model_snapshot.py --sheet-id <SHEET_ID> [--output <DIR>]

Example:
    python download_model_snapshot.py --sheet-id "1-Ss62..." --output .tmp/snapshot
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Sheets API scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


def get_credentials():
    """Get OAuth2 credentials for Google Sheets API."""
    creds = None
    creds_file = "credentials.json"
    token_file = "token.json"

    # Load existing credentials
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                from google.auth.transport.requests import Request

                creds.refresh(Request())
            except Exception as e:
                print(f"Token refresh failed: {e}")
                print("Running new OAuth flow...")
                creds = None

        if not creds:
            if not os.path.exists(creds_file):
                print(f"Error: {creds_file} not found")
                print("Download credentials from Google Cloud Console")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds


def sanitize_sheet_name(name):
    """Convert sheet name to valid filename."""
    # Replace invalid filename characters
    invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|", "&"]
    for char in invalid_chars:
        name = name.replace(char, "_")
    return name.strip()


def download_snapshot(sheet_id, output_dir):
    """Download all sheets from spreadsheet to CSV files."""
    print(f"\n{'='*80}")
    print("DOWNLOADING FINANCIAL MODEL SNAPSHOT")
    print(f"{'='*80}\n")

    # Create output directory
    output_path = Path(output_dir)
    sheets_dir = output_path / "sheets"
    sheets_dir.mkdir(parents=True, exist_ok=True)

    # Authorize and open spreadsheet
    creds = get_credentials()
    if not creds:
        print("Error: No credentials found. Run setup first.")
        return False

    gc = gspread.authorize(creds)

    try:
        spreadsheet = gc.open_by_key(sheet_id)
        print(f"Spreadsheet: {spreadsheet.title}")
        print(f"Output: {output_path.absolute()}\n")
    except Exception as e:
        print(f"Error opening spreadsheet: {e}")
        return False

    # Get all worksheets
    worksheets = spreadsheet.worksheets()
    print(f"Found {len(worksheets)} sheets to download\n")

    # Metadata structure
    metadata = {
        "spreadsheet_id": sheet_id,
        "spreadsheet_title": spreadsheet.title,
        "snapshot_date": datetime.now().isoformat(),
        "sheets": [],
    }

    # Download each sheet
    for idx, worksheet in enumerate(worksheets):
        sheet_name = worksheet.title
        safe_name = sanitize_sheet_name(sheet_name)

        print(f"[{idx+1}/{len(worksheets)}] {sheet_name}...")

        try:
            # Get values and formulas
            all_values = worksheet.get_all_values()

            # Determine actual column usage
            if all_values:
                rows = len(all_values)
                max_cols = max(len(row) for row in all_values) if all_values else 0

                # Convert column count to column letter (A, B, ..., Z, AA, AB, ...)
                def col_to_letter(col_num):
                    """Convert column number (0-indexed) to letter (A, B, ..., Z, AA, AB, ...)"""
                    result = ""
                    col_num += 1  # Make 1-indexed
                    while col_num > 0:
                        col_num -= 1
                        result = chr(65 + (col_num % 26)) + result
                        col_num //= 26
                    return result

                # Get formulas for entire used range
                if max_cols > 0:
                    last_col = col_to_letter(max_cols - 1)
                    range_notation = f"A1:{last_col}{rows}"
                    all_formulas = worksheet.get(
                        range_notation, value_render_option="FORMULA"
                    )
                else:
                    all_formulas = []
            else:
                rows = 0
                max_cols = 0
                all_formulas = []

            # Generate column headers (A, B, C, ..., up to actual usage)
            col_headers = ["Row"] + [col_to_letter(i) for i in range(max_cols)]

            # Save values CSV
            values_file = sheets_dir / f"{safe_name}.csv"
            with open(values_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(col_headers)
                for i, row in enumerate(all_values):
                    # Pad row to max_cols if needed
                    padded_row = row + [""] * (max_cols - len(row))
                    writer.writerow([i + 1] + padded_row[:max_cols])

            # Save formulas CSV
            formulas_file = sheets_dir / f"{safe_name}_formulas.csv"
            with open(formulas_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(col_headers)
                if all_formulas:
                    for i, row in enumerate(all_formulas):
                        # Pad formula row to max_cols if needed
                        padded_row = row + [""] * (max_cols - len(row))
                        writer.writerow([i + 1] + padded_row[:max_cols])

            # Track sheet metadata
            sheet_meta = {
                "name": sheet_name,
                "safe_name": safe_name,
                "index": idx,
                "rows": rows,
                "cols": max_cols,
                "values_file": str(values_file.relative_to(output_path)),
                "formulas_file": str(formulas_file.relative_to(output_path)),
            }
            metadata["sheets"].append(sheet_meta)

            print(f"     {rows} rows × {max_cols} cols")

            print(f"     {len(all_values)} rows × {sheet_meta['cols']} cols")

        except Exception as e:
            print(f"     Error: {e}")
            continue

    # Save metadata
    metadata_file = output_path / "snapshot.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'='*80}")
    print(" SNAPSHOT COMPLETE")
    print(f"{'='*80}")
    print(f"\nFiles saved to: {output_path.absolute()}")
    print(f"  - {len(metadata['sheets'])} sheet pairs (values + formulas)")
    print(f"  - 1 metadata file (snapshot.json)")
    print(f"\nTotal files: {len(metadata['sheets']) * 2 + 1}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Download Google Sheets financial model to local snapshot"
    )
    parser.add_argument(
        "--sheet-id", required=True, help="Google Sheets spreadsheet ID"
    )
    parser.add_argument("--output", default=".tmp/snapshot", help="Output directory")

    args = parser.parse_args()

    success = download_snapshot(args.sheet_id, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
