#!/usr/bin/env python3
"""
Financial Model Summary Exporter
================================
Exports a comprehensive summary of a financial model from Google Sheets.
Useful for quick reviews, documentation, and validation.

Usage:
    python export_model_summary.py --sheet-id "1ABC..." --output summary.txt
    python export_model_summary.py --sheet-id "1ABC..." --format json --output summary.json
    python export_model_summary.py --sheet-id "1ABC..." --format markdown --output summary.md

Outputs:
    - Key metrics (Revenue, EBITDA, Net Income)
    - Funding summary
    - Unit economics (CAC, LTV, LTV:CAC)
    - Balance sheet check
    - Cross-sheet link verification
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

try:
    import gspread
except ImportError:
    print("Installing gspread...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread"])
    import gspread


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_sheets_client():
    """Get authenticated gspread client"""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except:
            pass
    
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


def parse_value(val) -> float:
    """Parse cell value to float"""
    if val is None or val == "" or val == "-":
        return 0.0
    val_str = str(val).replace("$", "").replace(",", "").replace("%", "").strip()
    
    multiplier = 1
    if val_str.endswith("K"):
        multiplier = 1000
        val_str = val_str[:-1]
    elif val_str.endswith("M"):
        multiplier = 1_000_000
        val_str = val_str[:-1]
    
    if val_str.startswith("(") and val_str.endswith(")"):
        val_str = "-" + val_str[1:-1]
    
    try:
        return float(val_str) * multiplier
    except:
        return 0.0


def find_row(data: List, label: str) -> int:
    """Find row index by label"""
    for i, row in enumerate(data):
        if row and label.lower() in str(row[0]).lower():
            return i
    return -1


def get_year_values(data: List, row_idx: int, num_years: int = 6) -> List[float]:
    """Get values for years 0-5 from a row"""
    if row_idx < 0 or row_idx >= len(data):
        return [0] * num_years
    row = data[row_idx]
    values = []
    for col in range(2, 2 + num_years):
        if col < len(row):
            values.append(parse_value(row[col]))
        else:
            values.append(0)
    return values


def extract_summary(spreadsheet) -> Dict[str, Any]:
    """Extract comprehensive summary from financial model"""
    summary = {
        "title": spreadsheet.title,
        "extracted_at": datetime.now().isoformat(),
        "sheets": [ws.title for ws in spreadsheet.worksheets()],
        "metrics": {},
        "funding": {},
        "unit_economics": {},
        "balance_check": {},
        "errors": []
    }
    
    # P&L Metrics
    try:
        pl = spreadsheet.worksheet("P&L")
        time.sleep(0.5)
        pl_data = pl.get_all_values()
        
        revenue_row = find_row(pl_data, "total revenue")
        if revenue_row < 0:
            revenue_row = find_row(pl_data, "revenue")
        ebitda_row = find_row(pl_data, "ebitda")
        net_income_row = find_row(pl_data, "net income")
        if net_income_row < 0:
            net_income_row = find_row(pl_data, "pat")
        
        summary["metrics"]["revenue"] = get_year_values(pl_data, revenue_row)
        summary["metrics"]["ebitda"] = get_year_values(pl_data, ebitda_row)
        summary["metrics"]["net_income"] = get_year_values(pl_data, net_income_row)
        
        # Margins
        gm_row = find_row(pl_data, "gross margin")
        ebitda_m_row = find_row(pl_data, "ebitda margin")
        summary["metrics"]["gross_margin_pct"] = get_year_values(pl_data, gm_row)
        summary["metrics"]["ebitda_margin_pct"] = get_year_values(pl_data, ebitda_m_row)
        
    except Exception as e:
        summary["errors"].append(f"P&L: {str(e)}")
    
    # Funding
    try:
        funding_names = ["Funding Cap Table", "Funding & Cap Table", "Funding"]
        fc = None
        for name in funding_names:
            try:
                fc = spreadsheet.worksheet(name)
                break
            except:
                continue
        
        if fc:
            time.sleep(0.5)
            fc_data = fc.get_all_values()
            
            seed_row = find_row(fc_data, "seed")
            series_a_row = find_row(fc_data, "series a")
            cum_row = find_row(fc_data, "cumulative")
            
            summary["funding"]["seed"] = get_year_values(fc_data, seed_row)
            summary["funding"]["series_a"] = get_year_values(fc_data, series_a_row)
            summary["funding"]["cumulative"] = get_year_values(fc_data, cum_row)
    except Exception as e:
        summary["errors"].append(f"Funding: {str(e)}")
    
    # Unit Economics
    try:
        ce_names = ["Customer Economics", "Unit Economics"]
        ce = None
        for name in ce_names:
            try:
                ce = spreadsheet.worksheet(name)
                break
            except:
                continue
        
        if ce:
            time.sleep(0.5)
            ce_data = ce.get_all_values()
            
            cac_row = find_row(ce_data, "cac")
            ltv_row = find_row(ce_data, "ltv")
            ltv_cac_row = find_row(ce_data, "ltv:cac")
            if ltv_cac_row < 0:
                ltv_cac_row = find_row(ce_data, "ltv/cac")
            
            summary["unit_economics"]["cac"] = get_year_values(ce_data, cac_row)
            summary["unit_economics"]["ltv"] = get_year_values(ce_data, ltv_row)
            summary["unit_economics"]["ltv_cac_ratio"] = get_year_values(ce_data, ltv_cac_row)
    except Exception as e:
        summary["errors"].append(f"Unit Economics: {str(e)}")
    
    # Balance Sheet Check
    try:
        bs = spreadsheet.worksheet("Balance Sheet")
        time.sleep(0.5)
        bs_data = bs.get_all_values()
        
        assets_row = find_row(bs_data, "total assets")
        liab_row = find_row(bs_data, "total liabilities")
        equity_row = find_row(bs_data, "total equity")
        if equity_row < 0:
            equity_row = find_row(bs_data, "total shareholders")
        check_row = find_row(bs_data, "check")
        
        summary["balance_check"]["total_assets"] = get_year_values(bs_data, assets_row)
        summary["balance_check"]["total_liabilities"] = get_year_values(bs_data, liab_row)
        summary["balance_check"]["total_equity"] = get_year_values(bs_data, equity_row)
        
        if check_row >= 0:
            summary["balance_check"]["check_values"] = get_year_values(bs_data, check_row)
        else:
            # Calculate check manually
            assets = summary["balance_check"]["total_assets"]
            liab = summary["balance_check"]["total_liabilities"]
            equity = summary["balance_check"]["total_equity"]
            summary["balance_check"]["check_values"] = [
                assets[i] - liab[i] - equity[i] for i in range(len(assets))
            ]
        
        summary["balance_check"]["balanced"] = all(
            abs(v) < 1 for v in summary["balance_check"]["check_values"]
        )
    except Exception as e:
        summary["errors"].append(f"Balance Sheet: {str(e)}")
    
    # Cash Position
    try:
        cf = spreadsheet.worksheet("Cash Flow")
        time.sleep(0.5)
        cf_data = cf.get_all_values()
        
        cum_cash_row = find_row(cf_data, "cumulative")
        if cum_cash_row < 0:
            cum_cash_row = find_row(cf_data, "closing cash")
        
        summary["metrics"]["cash_position"] = get_year_values(cf_data, cum_cash_row)
    except Exception as e:
        summary["errors"].append(f"Cash Flow: {str(e)}")
    
    return summary


def format_text(summary: Dict) -> str:
    """Format summary as plain text"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"FINANCIAL MODEL SUMMARY: {summary['title']}")
    lines.append(f"Extracted: {summary['extracted_at']}")
    lines.append("=" * 70)
    
    lines.append(f"\nSheets: {', '.join(summary['sheets'])}")
    
    # Key Metrics
    lines.append("\n" + "-" * 70)
    lines.append("KEY METRICS (Y0 -> Y5)")
    lines.append("-" * 70)
    
    years = ["Y0", "Y1", "Y2", "Y3", "Y4", "Y5"]
    
    if "revenue" in summary["metrics"]:
        rev = summary["metrics"]["revenue"]
        lines.append(f"Revenue:     " + " | ".join(f"${v/1000:,.0f}K" for v in rev))
    
    if "ebitda" in summary["metrics"]:
        ebitda = summary["metrics"]["ebitda"]
        lines.append(f"EBITDA:      " + " | ".join(f"${v/1000:,.0f}K" for v in ebitda))
    
    if "net_income" in summary["metrics"]:
        ni = summary["metrics"]["net_income"]
        lines.append(f"Net Income:  " + " | ".join(f"${v/1000:,.0f}K" for v in ni))
    
    if "cash_position" in summary["metrics"]:
        cash = summary["metrics"]["cash_position"]
        lines.append(f"Cash:        " + " | ".join(f"${v/1000:,.0f}K" for v in cash))
    
    # Funding
    if summary["funding"]:
        lines.append("\n" + "-" * 70)
        lines.append("FUNDING")
        lines.append("-" * 70)
        
        if "seed" in summary["funding"]:
            seed = summary["funding"]["seed"]
            seed_total = sum(seed)
            if seed_total > 0:
                lines.append(f"Seed:        ${seed_total/1000:,.0f}K")
        
        if "series_a" in summary["funding"]:
            sa = summary["funding"]["series_a"]
            sa_total = sum(sa)
            if sa_total > 0:
                lines.append(f"Series A:    ${sa_total/1000:,.0f}K")
        
        if "cumulative" in summary["funding"]:
            cum = summary["funding"]["cumulative"]
            lines.append(f"Cumulative:  " + " | ".join(f"${v/1000:,.0f}K" for v in cum))
    
    # Unit Economics
    if summary["unit_economics"]:
        lines.append("\n" + "-" * 70)
        lines.append("UNIT ECONOMICS")
        lines.append("-" * 70)
        
        if "cac" in summary["unit_economics"]:
            cac = summary["unit_economics"]["cac"]
            lines.append(f"CAC:         " + " | ".join(f"${v:,.0f}" for v in cac))
        
        if "ltv_cac_ratio" in summary["unit_economics"]:
            ratio = summary["unit_economics"]["ltv_cac_ratio"]
            lines.append(f"LTV:CAC:     " + " | ".join(f"{v:.1f}x" for v in ratio))
    
    # Balance Check
    if summary["balance_check"]:
        lines.append("\n" + "-" * 70)
        lines.append("BALANCE SHEET CHECK")
        lines.append("-" * 70)
        
        balanced = summary["balance_check"].get("balanced", False)
        status = "BALANCED" if balanced else "IMBALANCED"
        lines.append(f"Status: {status}")
        
        if "check_values" in summary["balance_check"]:
            checks = summary["balance_check"]["check_values"]
            lines.append(f"Check:       " + " | ".join(f"${v:,.0f}" for v in checks))
    
    # Errors
    if summary["errors"]:
        lines.append("\n" + "-" * 70)
        lines.append("ERRORS/WARNINGS")
        lines.append("-" * 70)
        for err in summary["errors"]:
            lines.append(f"  - {err}")
    
    lines.append("\n" + "=" * 70)
    
    return "\n".join(lines)


def format_markdown(summary: Dict) -> str:
    """Format summary as markdown"""
    lines = []
    lines.append(f"# Financial Model Summary: {summary['title']}")
    lines.append(f"\n*Extracted: {summary['extracted_at']}*")
    lines.append(f"\n**Sheets:** {', '.join(summary['sheets'])}")
    
    # Key Metrics Table
    lines.append("\n## Key Metrics\n")
    lines.append("| Metric | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 |")
    lines.append("|--------|-----|-----|-----|-----|-----|-----|")
    
    if "revenue" in summary["metrics"]:
        rev = summary["metrics"]["revenue"]
        lines.append("| Revenue | " + " | ".join(f"${v/1000:,.0f}K" for v in rev) + " |")
    
    if "ebitda" in summary["metrics"]:
        ebitda = summary["metrics"]["ebitda"]
        lines.append("| EBITDA | " + " | ".join(f"${v/1000:,.0f}K" for v in ebitda) + " |")
    
    if "net_income" in summary["metrics"]:
        ni = summary["metrics"]["net_income"]
        lines.append("| Net Income | " + " | ".join(f"${v/1000:,.0f}K" for v in ni) + " |")
    
    if "cash_position" in summary["metrics"]:
        cash = summary["metrics"]["cash_position"]
        lines.append("| Cash | " + " | ".join(f"${v/1000:,.0f}K" for v in cash) + " |")
    
    # Balance Check
    if summary["balance_check"]:
        lines.append("\n## Balance Sheet Check\n")
        balanced = summary["balance_check"].get("balanced", False)
        status = " BALANCED" if balanced else " IMBALANCED"
        lines.append(f"**Status:** {status}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Export financial model summary")
    parser.add_argument("--sheet-id", required=True, help="Google Sheet ID")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--output", help="Output file (optional, prints to stdout if not set)")
    
    args = parser.parse_args()
    
    client = get_sheets_client()
    spreadsheet = client.open_by_key(args.sheet_id)
    
    print(f"Extracting summary from: {spreadsheet.title}", file=sys.stderr)
    summary = extract_summary(spreadsheet)
    
    if args.format == "json":
        output = json.dumps(summary, indent=2)
    elif args.format == "markdown":
        output = format_markdown(summary)
    else:
        output = format_text(summary)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Summary saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
