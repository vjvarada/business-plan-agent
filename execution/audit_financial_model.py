#!/usr/bin/env python3
"""
Financial Model Auditor
=======================
Comprehensive audit tool for financial models in Google Sheets.
Validates balance sheets, cash runway, valuations, and investor metrics.

Usage:
    python audit_financial_model.py --sheet-id "1ABC..." --mode balance
    python audit_financial_model.py --sheet-id "1ABC..." --mode runway
    python audit_financial_model.py --sheet-id "1ABC..." --mode valuation --company-type ai
    python audit_financial_model.py --sheet-id "1ABC..." --mode comprehensive

Modes:
    balance     - Verify balance sheet identity (A = L + E)
    runway      - Calculate cash runway and funding sufficiency
    valuation   - Analyze valuations vs industry benchmarks
    metrics     - Check unit economics (CAC, LTV, margins)
    comprehensive - All audits
"""

import argparse
import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    import gspread
except ImportError:
    print("Installing gspread...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread"])
    import gspread


class AuditStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class AuditResult:
    check: str
    status: AuditStatus
    message: str
    details: Optional[dict] = None


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_sheets_client():
    """Get authenticated gspread client using OAuth2 (same as other scripts)"""
    from google.oauth2.credentials import Credentials as OAuthCredentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = OAuthCredentials.from_authorized_user_file('token.json', SCOPES)
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


def parse_value(val) -> float:
    """Parse a cell value to float, handling K/M suffixes and currency"""
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
    
    # Handle parentheses for negative
    if val_str.startswith("(") and val_str.endswith(")"):
        val_str = "-" + val_str[1:-1]
    
    try:
        return float(val_str) * multiplier
    except ValueError:
        return 0.0


def audit_balance_sheet(spreadsheet) -> List[AuditResult]:
    """Audit balance sheet identity: Assets = Liabilities + Equity"""
    results = []
    
    try:
        bs = spreadsheet.worksheet("Balance Sheet")
        data = bs.get_all_values()
    except Exception as e:
        return [AuditResult("Balance Sheet Access", AuditStatus.FAIL, f"Cannot access sheet: {e}")]
    
    # Find header row and year columns
    header_row = None
    for i, row in enumerate(data):
        if "Y0" in row or "Year 0" in row:
            header_row = i
            break
    
    if header_row is None:
        return [AuditResult("Balance Sheet Structure", AuditStatus.FAIL, "Cannot find year headers")]
    
    # Find key rows
    total_assets_row = None
    total_liabilities_row = None
    total_equity_row = None
    check_row = None
    
    for i, row in enumerate(data):
        first_cell = str(row[0]).lower().strip() if row else ""
        if "total assets" in first_cell:
            total_assets_row = i
        elif "total liabilities" in first_cell:
            total_liabilities_row = i
        elif "total equity" in first_cell or "total shareholders" in first_cell:
            total_equity_row = i
        elif "check" in first_cell or "balance" in first_cell and "check" in str(row[0]).lower():
            check_row = i
    
    # Get year columns
    headers = data[header_row]
    year_cols = []
    for j, h in enumerate(headers):
        if h and (h.startswith("Y") or "Year" in h):
            year_cols.append((j, h))
    
    # Check each year
    for col_idx, year_name in year_cols:
        try:
            if total_assets_row and total_liabilities_row and total_equity_row:
                assets = parse_value(data[total_assets_row][col_idx])
                liabilities = parse_value(data[total_liabilities_row][col_idx])
                equity = parse_value(data[total_equity_row][col_idx])
                
                diff = assets - (liabilities + equity)
                
                if abs(diff) < 1:  # Within $1
                    status = AuditStatus.PASS
                    msg = f"A={assets:,.0f}, L+E={liabilities + equity:,.0f}"
                elif abs(diff) < 100:
                    status = AuditStatus.WARN
                    msg = f"Small imbalance: ${diff:,.0f}"
                else:
                    status = AuditStatus.FAIL
                    msg = f"IMBALANCE: Assets={assets:,.0f}, L+E={liabilities + equity:,.0f}, Diff={diff:,.0f}"
                
                results.append(AuditResult(
                    f"Balance Sheet {year_name}",
                    status,
                    msg,
                    {"assets": assets, "liabilities": liabilities, "equity": equity, "diff": diff}
                ))
            
        except Exception as e:
            results.append(AuditResult(f"Balance Sheet {year_name}", AuditStatus.FAIL, str(e)))
    
    return results


def audit_cash_runway(spreadsheet) -> List[AuditResult]:
    """Audit cash runway and funding sufficiency"""
    results = []
    
    try:
        cf = spreadsheet.worksheet("Cash Flow")
        cf_data = cf.get_all_values()
        
        bs = spreadsheet.worksheet("Balance Sheet")
        bs_data = bs.get_all_values()
    except Exception as e:
        return [AuditResult("Cash Flow Access", AuditStatus.FAIL, str(e))]
    
    # Find cash balance row in balance sheet
    cash_row = None
    for i, row in enumerate(bs_data):
        if row and "cash" in str(row[0]).lower():
            cash_row = i
            break
    
    if cash_row is None:
        return [AuditResult("Cash Row", AuditStatus.FAIL, "Cannot find cash row")]
    
    # Find header row
    header_row = None
    for i, row in enumerate(bs_data):
        if "Y0" in row or "Year 0" in row:
            header_row = i
            break
    
    headers = bs_data[header_row]
    year_cols = [(j, h) for j, h in enumerate(headers) if h and h.startswith("Y")]
    
    # Get cash balances
    cash_by_year = {}
    for col_idx, year_name in year_cols:
        cash_by_year[year_name] = parse_value(bs_data[cash_row][col_idx])
    
    # Check for negative cash (runway issue)
    for year, cash in cash_by_year.items():
        if cash < 0:
            results.append(AuditResult(
                f"Cash Runway {year}",
                AuditStatus.FAIL,
                f"Negative cash balance: ${cash:,.0f}",
                {"year": year, "cash": cash}
            ))
        elif cash < 50000:  # Less than $50K
            results.append(AuditResult(
                f"Cash Runway {year}",
                AuditStatus.WARN,
                f"Low cash balance: ${cash:,.0f}",
                {"year": year, "cash": cash}
            ))
        else:
            results.append(AuditResult(
                f"Cash Runway {year}",
                AuditStatus.PASS,
                f"Cash: ${cash:,.0f}",
                {"year": year, "cash": cash}
            ))
    
    return results


def audit_valuations(spreadsheet, company_type: str = "saas") -> List[AuditResult]:
    """Audit valuations vs industry benchmarks"""
    results = []
    
    # Benchmark multiples by company type
    benchmarks = {
        "saas": {"seed": (8, 15), "series_a": (6, 12), "series_b": (5, 10)},
        "ai": {"seed": (12, 30), "series_a": (10, 20), "series_b": (8, 15)},
        "traditional": {"seed": (5, 10), "series_a": (4, 8), "series_b": (3, 7)},
    }
    
    try:
        funding = spreadsheet.worksheet("Funding & Cap Table")
        data = funding.get_all_values()
    except Exception as e:
        return [AuditResult("Funding Sheet Access", AuditStatus.FAIL, str(e))]
    
    # Find revenue at funding rounds
    try:
        pl = spreadsheet.worksheet("P&L")
        pl_data = pl.get_all_values()
        
        # Find revenue row and year columns
        revenue_row = None
        for i, row in enumerate(pl_data):
            if row and "revenue" in str(row[0]).lower():
                revenue_row = i
                break
        
        header_row = None
        for i, row in enumerate(pl_data):
            if "Y0" in row:
                header_row = i
                break
        
        if revenue_row and header_row:
            headers = pl_data[header_row]
            year_cols = [(j, h) for j, h in enumerate(headers) if h and h.startswith("Y")]
            
            revenue_by_year = {}
            for col_idx, year_name in year_cols:
                revenue_by_year[year_name] = parse_value(pl_data[revenue_row][col_idx])
    except:
        revenue_by_year = {}
    
    # Analyze funding rows
    round_benchmarks = benchmarks.get(company_type, benchmarks["saas"])
    
    for i, row in enumerate(data):
        if not row:
            continue
        
        first_cell = str(row[0]).lower()
        
        if "seed" in first_cell:
            round_type = "seed"
        elif "series a" in first_cell:
            round_type = "series_a"
        elif "series b" in first_cell:
            round_type = "series_b"
        else:
            continue
        
        # Try to find valuation info
        # Look for post-money or valuation columns
        post_money = None
        for j, cell in enumerate(row):
            val = parse_value(cell)
            if val > 500000:  # Likely a valuation
                post_money = val
                break
        
        if post_money:
            # Find corresponding revenue
            year_key = "Y0" if "seed" in first_cell.lower() else "Y2" if "series a" in first_cell.lower() else "Y3"
            revenue = revenue_by_year.get(year_key, 0)
            
            if revenue > 0:
                multiple = post_money / revenue
                low, high = round_benchmarks.get(round_type, (5, 15))
                
                if low <= multiple <= high:
                    status = AuditStatus.PASS
                    msg = f"{multiple:.1f}x revenue (benchmark: {low}-{high}x for {company_type})"
                elif multiple < low:
                    status = AuditStatus.WARN
                    msg = f"{multiple:.1f}x revenue - below benchmark ({low}-{high}x)"
                else:
                    status = AuditStatus.WARN
                    msg = f"{multiple:.1f}x revenue - above benchmark ({low}-{high}x)"
                
                results.append(AuditResult(
                    f"Valuation {round_type}",
                    status,
                    msg,
                    {"post_money": post_money, "revenue": revenue, "multiple": multiple}
                ))
    
    if not results:
        results.append(AuditResult("Valuation Analysis", AuditStatus.WARN, "Could not analyze funding rounds"))
    
    return results


def audit_metrics(spreadsheet) -> List[AuditResult]:
    """Audit unit economics metrics"""
    results = []
    
    try:
        ce = spreadsheet.worksheet("Customer Economics")
        data = ce.get_all_values()
    except Exception as e:
        return [AuditResult("Customer Economics Access", AuditStatus.FAIL, str(e))]
    
    # Find key metric rows
    cac_row = None
    ltv_row = None
    ltv_cac_row = None
    
    for i, row in enumerate(data):
        if not row:
            continue
        first_cell = str(row[0]).lower()
        
        if "cac" in first_cell and "ltv" not in first_cell:
            cac_row = i
        elif "ltv" in first_cell and "cac" not in first_cell:
            ltv_row = i
        elif "ltv" in first_cell and "cac" in first_cell:
            ltv_cac_row = i
    
    # Find header row
    header_row = None
    for i, row in enumerate(data):
        if "Y0" in row or "Year 0" in row:
            header_row = i
            break
    
    if header_row:
        headers = data[header_row]
        year_cols = [(j, h) for j, h in enumerate(headers) if h and h.startswith("Y")]
        
        # Check LTV:CAC ratio
        if ltv_cac_row:
            for col_idx, year_name in year_cols:
                ratio = parse_value(data[ltv_cac_row][col_idx])
                
                if ratio >= 5:
                    status = AuditStatus.PASS
                    msg = f"Excellent: {ratio:.1f}x"
                elif ratio >= 3:
                    status = AuditStatus.PASS
                    msg = f"Good: {ratio:.1f}x"
                elif ratio >= 1:
                    status = AuditStatus.WARN
                    msg = f"Marginal: {ratio:.1f}x (target >3x)"
                else:
                    status = AuditStatus.FAIL
                    msg = f"Poor: {ratio:.1f}x (losing money on customers)"
                
                results.append(AuditResult(f"LTV:CAC {year_name}", status, msg))
        
        # Check CAC
        if cac_row:
            for col_idx, year_name in year_cols:
                cac = parse_value(data[cac_row][col_idx])
                
                # B2B SaaS typical CAC: $500-2000 for SMB, $5000-50000 for enterprise
                if 500 <= cac <= 50000:
                    status = AuditStatus.PASS
                    msg = f"CAC: ${cac:,.0f}"
                elif cac < 500:
                    status = AuditStatus.WARN
                    msg = f"CAC seems low: ${cac:,.0f} (verify data)"
                else:
                    status = AuditStatus.WARN
                    msg = f"CAC seems high: ${cac:,.0f}"
                
                results.append(AuditResult(f"CAC {year_name}", status, msg))
    
    return results


def print_audit_report(results: List[AuditResult], mode: str):
    """Print formatted audit report"""
    print("\n" + "=" * 80)
    print(f"FINANCIAL MODEL AUDIT REPORT - {mode.upper()}")
    print("=" * 80)
    
    # Group by status
    passed = [r for r in results if r.status == AuditStatus.PASS]
    warnings = [r for r in results if r.status == AuditStatus.WARN]
    failed = [r for r in results if r.status == AuditStatus.FAIL]
    
    print(f"\nSummary: {len(passed)} PASS | {len(warnings)} WARN | {len(failed)} FAIL")
    print("-" * 80)
    
    for result in results:
        icon = "" if result.status == AuditStatus.PASS else "" if result.status == AuditStatus.WARN else ""
        print(f"{icon} [{result.status.value}] {result.check}: {result.message}")
    
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Audit financial model")
    parser.add_argument("--sheet-id", required=True, help="Google Sheet ID")
    parser.add_argument("--mode", required=True,
                       choices=["balance", "runway", "valuation", "metrics", "comprehensive"],
                       help="Audit mode")
    parser.add_argument("--company-type", default="saas",
                       choices=["saas", "ai", "traditional"],
                       help="Company type for valuation benchmarks")
    
    args = parser.parse_args()
    
    client = get_sheets_client()
    spreadsheet = client.open_by_key(args.sheet_id)
    
    all_results = []
    
    if args.mode in ["balance", "comprehensive"]:
        results = audit_balance_sheet(spreadsheet)
        all_results.extend(results)
        if args.mode == "balance":
            print_audit_report(results, "Balance Sheet")
    
    if args.mode in ["runway", "comprehensive"]:
        results = audit_cash_runway(spreadsheet)
        all_results.extend(results)
        if args.mode == "runway":
            print_audit_report(results, "Cash Runway")
    
    if args.mode in ["valuation", "comprehensive"]:
        results = audit_valuations(spreadsheet, args.company_type)
        all_results.extend(results)
        if args.mode == "valuation":
            print_audit_report(results, "Valuations")
    
    if args.mode in ["metrics", "comprehensive"]:
        results = audit_metrics(spreadsheet)
        all_results.extend(results)
        if args.mode == "metrics":
            print_audit_report(results, "Unit Economics")
    
    if args.mode == "comprehensive":
        print_audit_report(all_results, "Comprehensive")
    
    # Return exit code based on failures
    failures = [r for r in all_results if r.status == AuditStatus.FAIL]
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
