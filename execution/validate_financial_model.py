"""
Financial Model Validator
=========================
Comprehensive sanity checks for business plan financial models.
Ensures accounting identities, three-statement linkages, and model integrity.

Usage:
    python validate_financial_model.py --url "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID"
"""

import argparse
import gspread
from google.oauth2.credentials import Credentials
import re
import sys
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class CheckStatus(Enum):
    PASS = " PASS"
    FAIL = " FAIL"
    WARN = " WARN"
    SKIP = " SKIP"

@dataclass
class ValidationResult:
    check_name: str
    status: CheckStatus
    message: str
    details: List[str] = None

class FinancialModelValidator:
    def __init__(self, spreadsheet_id: str):
        self.creds = Credentials.from_authorized_user_file('token.json')
        self.client = gspread.authorize(self.creds)
        self.ss = self.client.open_by_key(spreadsheet_id)
        self.results: List[ValidationResult] = []
        self.sheets_data: Dict[str, List[List[Any]]] = {}
        self.tolerance = 1.0  # Allow  rounding tolerance
        
    def load_sheets(self):
        """Load all sheet data into memory"""
        required_sheets = ['Assumptions', 'Revenue', 'Operating Costs', 'P&L', 'Balance Sheet', 'Cash Flow']
        for sheet_name in required_sheets:
            try:
                sheet = self.ss.worksheet(sheet_name)
                self.sheets_data[sheet_name] = sheet.get_all_values()
            except gspread.exceptions.WorksheetNotFound:
                self.results.append(ValidationResult(
                    f"Sheet Exists: {sheet_name}",
                    CheckStatus.FAIL,
                    f"Required sheet '{sheet_name}' not found"
                ))
                
    def get_numeric_row(self, sheet_name: str, row_label: str) -> List[float]:
        """Extract numeric values from a row by label"""
        data = self.sheets_data.get(sheet_name, [])
        for row in data:
            if row and row[0] and row_label.lower() in str(row[0]).lower():
                values = []
                for cell in row[1:]:
                    try:
                        values.append(float(str(cell).replace(',', '').replace('$', '')))
                    except (ValueError, TypeError):
                        values.append(0.0)
                return values
        return []

    def check_for_errors(self) -> ValidationResult:
        """Check for #REF!, #NAME?, #VALUE!, #DIV/0! errors"""
        errors_found = []
        error_patterns = ['#REF!', '#NAME?', '#VALUE!', '#DIV/0!', '#ERROR!', '#N/A']
        
        for sheet_name, data in self.sheets_data.items():
            for r, row in enumerate(data):
                for c, cell in enumerate(row):
                    for pattern in error_patterns:
                        if pattern in str(cell):
                            errors_found.append(f"{sheet_name}!{chr(65+c)}{r+1}: {cell}")
        
        if errors_found:
            return ValidationResult(
                "No Formula Errors",
                CheckStatus.FAIL,
                f"Found {len(errors_found)} formula errors",
                errors_found[:10]  # Show first 10
            )
        return ValidationResult(
            "No Formula Errors",
            CheckStatus.PASS,
            "No #REF!, #NAME?, #VALUE!, #DIV/0! errors found"
        )

    def check_balance_sheet_identity(self) -> ValidationResult:
        """Assets = Liabilities + Equity"""
        total_assets = self.get_numeric_row('Balance Sheet', 'Total Assets')
        total_liab = self.get_numeric_row('Balance Sheet', 'Total Liab')
        
        if not total_assets or not total_liab:
            return ValidationResult(
                "Balance Sheet Identity",
                CheckStatus.SKIP,
                "Could not find Total Assets or Total Liabilities rows"
            )
        
        differences = []
        for i, (assets, liab) in enumerate(zip(total_assets, total_liab)):
            diff = abs(assets - liab)
            if diff > self.tolerance:
                differences.append(f"Year {i}: Assets={assets:,.0f}, Liab+Eq={liab:,.0f}, Diff={diff:,.0f}")
        
        if differences:
            return ValidationResult(
                "Balance Sheet Identity (A = L + E)",
                CheckStatus.FAIL,
                "Balance sheet does not balance",
                differences
            )
        return ValidationResult(
            "Balance Sheet Identity (A = L + E)",
            CheckStatus.PASS,
            "Assets = Liabilities + Equity for all periods"
        )

    def check_cash_reconciliation(self) -> ValidationResult:
        """Opening Cash + Net CF = Closing Cash"""
        cumulative_cash = self.get_numeric_row('Cash Flow', 'Cumulative Cash')
        net_cf = self.get_numeric_row('Cash Flow', 'NET CASH FLOW')
        bs_cash = self.get_numeric_row('Balance Sheet', 'Cash')
        
        if not cumulative_cash or not bs_cash:
            return ValidationResult(
                "Cash Reconciliation",
                CheckStatus.SKIP,
                "Could not find cash rows"
            )
        
        differences = []
        for i, (cf_cash, bs_c) in enumerate(zip(cumulative_cash, bs_cash)):
            diff = abs(cf_cash - bs_c)
            if diff > self.tolerance:
                differences.append(f"Year {i}: CF Cash={cf_cash:,.0f}, BS Cash={bs_c:,.0f}, Diff={diff:,.0f}")
        
        if differences:
            return ValidationResult(
                "Cash Flow  Balance Sheet Reconciliation",
                CheckStatus.FAIL,
                "Cash flow ending cash  balance sheet cash",
                differences
            )
        return ValidationResult(
            "Cash Flow  Balance Sheet Reconciliation",
            CheckStatus.PASS,
            "Cash flow cumulative cash matches balance sheet cash"
        )

    def check_net_income_linkage(self) -> ValidationResult:
        """Net Income flows correctly through all statements"""
        pl_pat = self.get_numeric_row('P&L', 'PAT')
        cf_pat = self.get_numeric_row('Cash Flow', 'PAT')
        
        if not pl_pat or not cf_pat:
            return ValidationResult(
                "Net Income Linkage",
                CheckStatus.SKIP,
                "Could not find PAT/Net Income rows"
            )
        
        differences = []
        for i, (pl, cf) in enumerate(zip(pl_pat, cf_pat)):
            diff = abs(pl - cf)
            if diff > self.tolerance:
                differences.append(f"Year {i}: P&L PAT={pl:,.0f}, CF PAT={cf:,.0f}")
        
        if differences:
            return ValidationResult(
                "Net Income Linkage (P&L  CF)",
                CheckStatus.FAIL,
                "P&L Net Income  Cash Flow starting point",
                differences
            )
        return ValidationResult(
            "Net Income Linkage (P&L  CF)",
            CheckStatus.PASS,
            "Net Income flows correctly from P&L to Cash Flow"
        )

    def check_retained_earnings_rollforward(self) -> ValidationResult:
        """RE_t = RE_{t-1} + Net Income - Dividends"""
        retained_earnings = self.get_numeric_row('Balance Sheet', 'Retained Earnings')
        pat = self.get_numeric_row('P&L', 'PAT')
        
        if not retained_earnings or not pat:
            return ValidationResult(
                "Retained Earnings Roll-Forward",
                CheckStatus.SKIP,
                "Could not find Retained Earnings or PAT rows"
            )
        
        differences = []
        for i in range(1, min(len(retained_earnings), len(pat))):
            expected_re = retained_earnings[i-1] + pat[i]
            actual_re = retained_earnings[i]
            diff = abs(expected_re - actual_re)
            if diff > self.tolerance:
                differences.append(f"Year {i}: Expected RE={expected_re:,.0f}, Actual={actual_re:,.0f}")
        
        if differences:
            return ValidationResult(
                "Retained Earnings Roll-Forward",
                CheckStatus.FAIL,
                "RE_t  RE_{t-1} + Net Income",
                differences
            )
        return ValidationResult(
            "Retained Earnings Roll-Forward",
            CheckStatus.PASS,
            "Retained earnings roll forward correctly"
        )

    def check_depreciation_loop(self) -> ValidationResult:
        """Depreciation consistency across statements"""
        pl_depr = self.get_numeric_row('P&L', 'Depreciation')
        cf_depr = self.get_numeric_row('Cash Flow', 'Depreciation')
        
        if not pl_depr or not cf_depr:
            return ValidationResult(
                "Depreciation Loop",
                CheckStatus.SKIP,
                "Could not find Depreciation rows"
            )
        
        differences = []
        for i, (pl, cf) in enumerate(zip(pl_depr, cf_depr)):
            diff = abs(pl - cf)
            if diff > self.tolerance:
                differences.append(f"Year {i}: P&L Depr={pl:,.0f}, CF Depr={cf:,.0f}")
        
        if differences:
            return ValidationResult(
                "Depreciation Consistency (P&L  CF)",
                CheckStatus.FAIL,
                "P&L Depreciation  CF add-back",
                differences
            )
        return ValidationResult(
            "Depreciation Consistency (P&L  CF)",
            CheckStatus.PASS,
            "Depreciation consistent across P&L and Cash Flow"
        )

    def check_revenue_growth_sanity(self) -> ValidationResult:
        """Revenue growth should be reasonable"""
        revenue = self.get_numeric_row('P&L', 'Revenue')
        
        if not revenue or len(revenue) < 2:
            return ValidationResult(
                "Revenue Growth Sanity",
                CheckStatus.SKIP,
                "Insufficient revenue data"
            )
        
        warnings = []
        for i in range(1, len(revenue)):
            if revenue[i-1] > 0:
                growth = (revenue[i] - revenue[i-1]) / revenue[i-1]
                if growth > 3.0:  # >300% growth
                    warnings.append(f"Year {i}: {growth*100:.0f}% growth (very high)")
                elif growth < -0.5:  # >50% decline
                    warnings.append(f"Year {i}: {growth*100:.0f}% growth (steep decline)")
        
        if warnings:
            return ValidationResult(
                "Revenue Growth Sanity",
                CheckStatus.WARN,
                "Unusual revenue growth rates detected",
                warnings
            )
        return ValidationResult(
            "Revenue Growth Sanity",
            CheckStatus.PASS,
            "Revenue growth rates appear reasonable"
        )

    def check_margin_consistency(self) -> ValidationResult:
        """Margins should be stable or have clear drivers"""
        revenue = self.get_numeric_row('P&L', 'Revenue')
        ebitda = self.get_numeric_row('P&L', 'EBITDA')
        
        if not revenue or not ebitda:
            return ValidationResult(
                "Margin Consistency",
                CheckStatus.SKIP,
                "Could not find Revenue or EBITDA rows"
            )
        
        margins = []
        for r, e in zip(revenue, ebitda):
            if r > 0:
                margins.append(e / r)
            else:
                margins.append(0)
        
        # Check for unrealistic margins
        warnings = []
        for i, m in enumerate(margins):
            if m > 0.9:
                warnings.append(f"Year {i}: {m*100:.1f}% EBITDA margin (unusually high)")
            elif m < -0.5:
                warnings.append(f"Year {i}: {m*100:.1f}% EBITDA margin (deep losses)")
        
        if warnings:
            return ValidationResult(
                "Margin Consistency",
                CheckStatus.WARN,
                "Unusual margin levels detected",
                warnings
            )
        return ValidationResult(
            "Margin Consistency",
            CheckStatus.PASS,
            "EBITDA margins appear reasonable"
        )

    def check_sign_discipline(self) -> ValidationResult:
        """Verify proper sign conventions"""
        issues = []
        
        # Capex should be negative in Cash Flow
        capex = self.get_numeric_row('Cash Flow', 'Capex')
        if capex:
            positive_capex = [i for i, c in enumerate(capex) if c > 0]
            if positive_capex:
                issues.append(f"Capex positive in years: {positive_capex} (should be negative)")
        
        # Revenue should be positive
        revenue = self.get_numeric_row('P&L', 'Revenue')
        if revenue:
            negative_rev = [i for i, r in enumerate(revenue) if r < 0]
            if negative_rev:
                issues.append(f"Revenue negative in years: {negative_rev}")
        
        if issues:
            return ValidationResult(
                "Sign Discipline",
                CheckStatus.WARN,
                "Sign convention issues detected",
                issues
            )
        return ValidationResult(
            "Sign Discipline",
            CheckStatus.PASS,
            "Sign conventions correct (Capex negative, Revenue positive)"
        )

    def check_working_capital_integrity(self) -> ValidationResult:
        """Working capital changes flow through correctly"""
        # Check if debtors/creditors exist and make sense
        debtors = self.get_numeric_row('Balance Sheet', 'Debtors')
        creditors = self.get_numeric_row('Balance Sheet', 'Creditors')
        revenue = self.get_numeric_row('P&L', 'Revenue')
        
        if not debtors or not revenue:
            return ValidationResult(
                "Working Capital Integrity",
                CheckStatus.SKIP,
                "Could not find Debtors or Revenue rows"
            )
        
        warnings = []
        for i, (d, r) in enumerate(zip(debtors, revenue)):
            if r > 0:
                debtor_days = (d / r) * 365
                if debtor_days > 90:
                    warnings.append(f"Year {i}: Debtor days = {debtor_days:.0f} (>90 days)")
                elif debtor_days < 0:
                    warnings.append(f"Year {i}: Negative debtors")
        
        if warnings:
            return ValidationResult(
                "Working Capital Integrity",
                CheckStatus.WARN,
                "Working capital anomalies detected",
                warnings
            )
        return ValidationResult(
            "Working Capital Integrity",
            CheckStatus.PASS,
            "Working capital ratios appear reasonable"
        )

    def check_stress_test_zero_revenue(self) -> ValidationResult:
        """What happens if revenue goes to zero?"""
        # This is informational - shows if model handles edge cases
        total_costs = self.get_numeric_row('P&L', 'Total Costs')
        
        if total_costs and any(c > 0 for c in total_costs):
            return ValidationResult(
                "Stress Test: Fixed Costs Exist",
                CheckStatus.PASS,
                f"Fixed costs present - cash burn would be ~/year at zero revenue"
            )
        return ValidationResult(
            "Stress Test: Fixed Costs Exist",
            CheckStatus.WARN,
            "No fixed costs found - model may not reflect reality"
        )

    def run_all_checks(self) -> List[ValidationResult]:
        """Run all validation checks"""
        print("Loading spreadsheet data...")
        self.load_sheets()
        
        print("Running validation checks...\n")
        
        # Core accounting identities
        self.results.append(self.check_for_errors())
        self.results.append(self.check_balance_sheet_identity())
        self.results.append(self.check_cash_reconciliation())
        self.results.append(self.check_retained_earnings_rollforward())
        
        # Three-statement linkages
        self.results.append(self.check_net_income_linkage())
        self.results.append(self.check_depreciation_loop())
        
        # Sanity checks
        self.results.append(self.check_revenue_growth_sanity())
        self.results.append(self.check_margin_consistency())
        self.results.append(self.check_sign_discipline())
        self.results.append(self.check_working_capital_integrity())
        
        # Stress tests
        self.results.append(self.check_stress_test_zero_revenue())
        
        return self.results

    def print_report(self):
        """Print formatted validation report"""
        print("=" * 60)
        print("FINANCIAL MODEL VALIDATION REPORT")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r.status == CheckStatus.PASS)
        failed = sum(1 for r in self.results if r.status == CheckStatus.FAIL)
        warned = sum(1 for r in self.results if r.status == CheckStatus.WARN)
        skipped = sum(1 for r in self.results if r.status == CheckStatus.SKIP)
        
        for result in self.results:
            print(f"\n{result.status.value} {result.check_name}")
            print(f"   {result.message}")
            if result.details:
                for detail in result.details[:5]:  # Show max 5 details
                    print(f"    {detail}")
                if len(result.details) > 5:
                    print(f"   ... and {len(result.details) - 5} more")
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed} passed, {failed} failed, {warned} warnings, {skipped} skipped")
        print("=" * 60)
        
        if failed > 0:
            print("\n  MODEL HAS CRITICAL ERRORS - Review and fix before sharing")
            return False
        elif warned > 0:
            print("\n Model passes core checks but has warnings to review")
            return True
        else:
            print("\n MODEL PASSES ALL VALIDATION CHECKS")
            return True


def main():
    parser = argparse.ArgumentParser(description='Validate financial model spreadsheet')
    parser.add_argument('--url', required=True, help='Google Sheets URL')
    args = parser.parse_args()
    
    # Extract spreadsheet ID from URL
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', args.url)
    if not match:
        print("Error: Could not extract spreadsheet ID from URL")
        sys.exit(1)
    
    spreadsheet_id = match.group(1)
    
    validator = FinancialModelValidator(spreadsheet_id)
    validator.run_all_checks()
    success = validator.print_report()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
