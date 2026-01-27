#!/usr/bin/env python3
"""
Google Sheets Utilities
=======================
Consolidated utility functions for reading, writing, and appending to Google Sheets.

Usage:
    python sheets_utils.py read --url <URL> [--worksheet <name>] [--output <file>]
    python sheets_utils.py write --json <file> [--sheet-name <name>]
    python sheets_utils.py append --url <URL> --json <file> [--worksheet <name>]
"""

import argparse
import json
import os
import sys
from datetime import datetime

import gspread
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials():
    """Get OAuth2 credentials for Google Sheets API."""
    creds = None

    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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

    return creds


def extract_sheet_id(url):
    """Extract Google Sheet ID from URL or return as-is if already an ID."""
    if "/d/" in url:
        return url.split("/d/")[1].split("/")[0]
    return url


# =============================================================================
# READ OPERATIONS
# =============================================================================


def read_sheet(sheet_url, worksheet_name=None):
    """
    Read data from a Google Sheet.

    Args:
        sheet_url: Google Sheets URL or ID
        worksheet_name: Name of specific worksheet (default: first sheet)

    Returns:
        List of dictionaries containing row data
    """
    try:
        creds = get_credentials()
        client = gspread.authorize(creds)

        sheet_id = extract_sheet_id(sheet_url)
        spreadsheet = client.open_by_key(sheet_id)

        if worksheet_name:
            worksheet = spreadsheet.worksheet(worksheet_name)
        else:
            worksheet = spreadsheet.sheet1

        records = worksheet.get_all_records()
        print(f"Successfully read {len(records)} rows from Google Sheet")
        return records

    except Exception as e:
        print(f"Error reading Google Sheet: {str(e)}", file=sys.stderr)
        return None


def read_sheet_raw(sheet_url, worksheet_name=None):
    """
    Read raw values from a Google Sheet (no header interpretation).

    Returns:
        List of lists (raw cell values)
    """
    try:
        creds = get_credentials()
        client = gspread.authorize(creds)

        sheet_id = extract_sheet_id(sheet_url)
        spreadsheet = client.open_by_key(sheet_id)

        if worksheet_name:
            worksheet = spreadsheet.worksheet(worksheet_name)
        else:
            worksheet = spreadsheet.sheet1

        values = worksheet.get_all_values()
        print(f"Successfully read {len(values)} rows from Google Sheet")
        return values

    except Exception as e:
        print(f"Error reading Google Sheet: {str(e)}", file=sys.stderr)
        return None


# =============================================================================
# WRITE OPERATIONS
# =============================================================================


def write_sheet(data, sheet_name=None, sheet_id=None):
    """
    Write data to a new or existing Google Sheet.

    Args:
        data: List of dictionaries or list of lists
        sheet_name: Name for new sheet (if sheet_id not provided)
        sheet_id: Existing sheet ID to write to

    Returns:
        Sheet URL on success, None on failure
    """
    try:
        creds = get_credentials()
        client = gspread.authorize(creds)

        # Open existing or create new
        if sheet_id:
            spreadsheet = client.open_by_key(extract_sheet_id(sheet_id))
        elif sheet_name:
            try:
                spreadsheet = client.open(sheet_name)
            except gspread.SpreadsheetNotFound:
                spreadsheet = client.create(sheet_name)
                print(f"Created new sheet: {sheet_name}")
        else:
            spreadsheet = client.create(
                f'Data Export - {datetime.now().strftime("%Y%m%d_%H%M%S")}'
            )

        worksheet = spreadsheet.sheet1
        worksheet.clear()

        # Convert dict list to rows
        if data and isinstance(data[0], dict):
            headers = list(data[0].keys())
            rows = [headers] + [[row.get(h, "") for h in headers] for row in data]
        else:
            rows = data

        worksheet.update(values=rows, value_input_option="RAW")
        print(f"Successfully wrote {len(rows)} rows")

        return spreadsheet.url

    except Exception as e:
        print(f"Error writing to Google Sheet: {str(e)}", file=sys.stderr)
        return None


# =============================================================================
# APPEND OPERATIONS
# =============================================================================


def append_rows(sheet_url, data, worksheet_name=None):
    """
    Append rows to an existing Google Sheet.

    Args:
        sheet_url: Google Sheets URL or ID
        data: List of dictionaries to append
        worksheet_name: Name of specific worksheet (default: first sheet)

    Returns:
        Number of rows appended
    """
    try:
        creds = get_credentials()
        client = gspread.authorize(creds)

        sheet_id = extract_sheet_id(sheet_url)
        spreadsheet = client.open_by_key(sheet_id)

        if worksheet_name:
            worksheet = spreadsheet.worksheet(worksheet_name)
        else:
            worksheet = spreadsheet.sheet1

        existing_headers = worksheet.row_values(1)
        if not existing_headers:
            print("Sheet has no headers. Please add headers first.")
            return 0

        rows_appended = 0
        for record in data:
            row = [record.get(header, "") for header in existing_headers]
            worksheet.append_row(row, value_input_option="RAW")
            rows_appended += 1

        print(f"Successfully appended {rows_appended} row(s)")
        return rows_appended

    except Exception as e:
        print(f"Error appending to sheet: {str(e)}", file=sys.stderr)
        return 0


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(description="Google Sheets Utilities")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Read command
    read_parser = subparsers.add_parser("read", help="Read from a Google Sheet")
    read_parser.add_argument("--url", required=True, help="Google Sheets URL or ID")
    read_parser.add_argument("--worksheet", help="Worksheet name")
    read_parser.add_argument("--output", help="Output JSON file path")
    read_parser.add_argument(
        "--raw", action="store_true", help="Read raw values (no header interpretation)"
    )

    # Write command
    write_parser = subparsers.add_parser("write", help="Write to a Google Sheet")
    write_parser.add_argument("--json", required=True, help="JSON file to write")
    write_parser.add_argument("--sheet-name", help="Name for the sheet")
    write_parser.add_argument("--sheet-id", help="Existing sheet ID to write to")

    # Append command
    append_parser = subparsers.add_parser(
        "append", help="Append rows to a Google Sheet"
    )
    append_parser.add_argument("--url", required=True, help="Google Sheets URL or ID")
    append_parser.add_argument(
        "--json", required=True, help="JSON file with rows to append"
    )
    append_parser.add_argument("--worksheet", help="Worksheet name")

    args = parser.parse_args()

    if args.command == "read":
        if args.raw:
            data = read_sheet_raw(args.url, args.worksheet)
        else:
            data = read_sheet(args.url, args.worksheet)

        if data:
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"Saved to {args.output}")
            else:
                print(json.dumps(data, indent=2))

    elif args.command == "write":
        with open(args.json, "r") as f:
            data = json.load(f)
        url = write_sheet(data, args.sheet_name, args.sheet_id)
        if url:
            print(f"Sheet URL: {url}")

    elif args.command == "append":
        with open(args.json, "r") as f:
            data = json.load(f)
        append_rows(args.url, data, args.worksheet)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
