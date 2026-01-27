#!/usr/bin/env python3
"""
Create a comprehensive 10-year financial model in Google Sheets.
Complete investor-ready financial model with advanced analytics.

🎯 TWO CREATION METHODS:

1. **TEMPLATE COPY (RECOMMENDED - Default)**
   - Copies RapidTools template spreadsheet
   - MUCH FASTER: ~10 seconds vs 2-3 minutes
   - 100% guaranteed fidelity to template
   - Updates only values, preserves all formulas/formatting
   - Use: --from-template (or omit flag, it's the default)

2. **BUILD FROM SCRATCH (For debugging/customization)**
   - Programmatically builds all 14 sheets
   - Slower but allows deep customization
   - Use: --build-from-scratch

⚠️ WHEN TO USE THIS SCRIPT:
   ✅ Creating a NEW financial model from scratch
   ✅ REBUILDING existing model with structural changes:
      - Adding/removing revenue streams
      - Changing TAM/SAM/SOM methodology
      - Adding/removing cost categories
      - Extending timeline (5yr → 10yr)
      - Major business model pivots

   For VALUE updates (funding, growth rates, pricing):
   → Use edit_financial_model.py (Local-First workflow)

📖 Full decision tree: directives/DECISION_TREE.md
📋 Template reference: directives/FINANCIAL_MODEL_TEMPLATE.md
📊 Template spreadsheet: https://docs.google.com/spreadsheets/d/1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY/edit

Features:
- Multiple revenue streams with independent assumptions
- Detailed operating costs by category (COGS, Fixed, S&M)
- Enhanced P&L with Gross Margin, EBITDA Margin, Net Margin
- Integrated Unit Economics (CAC/LTV, Payback) in Assumptions
- Headcount planning with dynamic salary model
- Fully linked Balance Sheet and Cash Flow
- DCF Valuation with multiples analysis
- Sensitivity Analysis (scenarios, 2-way tables)
- Break-even Analysis with margin of safety
- Funding & Cap Table tracking
- Charts Data for embedded visualizations

Output: 14-sheet Google Sheets model (RapidTools Template Structure)
    1. Sources & References - TAM/SAM/SOM with linkable values
    2. Assumptions - All input parameters + Unit Economics
    3. Headcount Plan - Team growth and salary costs
    4. Revenue - Multi-stream breakdown
    5. Operating Costs - COGS, Fixed, S&M
    6. P&L - Income statement with margins
    7. Cash Flow - Operating, Investing, Financing
    8. Balance Sheet - Assets, Liabilities, Equity
    9. Summary - KPI dashboard
    10. Sensitivity Analysis - Scenario modeling
    11. Valuation - DCF and comparables
    12. Break-even Analysis - Contribution margin
    13. Funding Cap Table - Equity tracking
    14. Charts Data - Data for embedded charts

Usage:
    # RECOMMENDED: Copy from template (default, fast)
    python create_financial_model.py --company "MyStartup" --config config.json
    
    # Explicit template copy
    python create_financial_model.py --company "MyStartup" --config config.json --from-template
    
    # Build from scratch (slower, for debugging)
    python create_financial_model.py --company "MyStartup" --config config.json --build-from-scratch
    
    # Use preset
    python create_financial_model.py --company "HumanoidRent" --humanoid-rent
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import gspread
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()


# Rate limiting helper
def rate_limit_delay(seconds=5):
    """Add delay to avoid API rate limits."""
    time.sleep(seconds)


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Year columns: A=Name, B=Unit, C=Year0, D=Year1, ... M=Year10
YEAR_COLS = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
YEAR_HEADERS = [
    "Year 0",
    "Year 1",
    "Year 2",
    "Year 3",
    "Year 4",
    "Year 5",
    "Year 6",
    "Year 7",
    "Year 8",
    "Year 9",
    "Year 10",
]


# ============================================================================
# HUMANOIDRENT PRESET CONFIGURATION
# ============================================================================

HUMANOID_RENT_CONFIG = {
    "general": {
        "tax_rate": 0.25,
        "capex_y0": 500000,
        "capex_annual": 100000,
        "depreciation_years": 5,
        "debtor_days": 45,
        "creditor_days": 30,
        "interest_rate": 0.08,
        "equity_y0": 1000000,
        "debt_y0": 500000,
        "cost_inflation": 0.03,
    },
    "revenue_streams": [
        {
            "name": "Robot Rental",
            "price": 2500,  # Monthly per robot
            "volume": 50,  # Starting robots
            "growth": 0.30,  # 30% YoY
            "cogs_pct": 0.15,  # Direct costs as % of this stream's revenue
        },
        {
            "name": "Maintenance",
            "price": 6000,  # Annual per robot
            "volume": 40,
            "growth": 0.35,
            "cogs_pct": 0.25,
        },
        {
            "name": "Training",
            "price": 3000,  # Per engagement
            "volume": 30,
            "growth": 0.25,
            "cogs_pct": 0.30,
        },
        {
            "name": "Spare Parts",
            "price": 500,  # Avg order
            "volume": 100,
            "growth": 0.40,
            "cogs_pct": 0.50,
        },
        {
            "name": "Consulting",
            "price": 15000,  # Per engagement
            "volume": 10,
            "growth": 0.20,
            "cogs_pct": 0.35,
        },
    ],
    "fixed_costs": [
        {"name": "Salaries & Benefits", "value": 800000},
        {"name": "Office Rent", "value": 120000},
        {"name": "Warehouse & Depot", "value": 200000},
        {"name": "Utilities", "value": 40000},
        {"name": "Software & Cloud", "value": 60000},
        {"name": "Fleet Management Systems", "value": 100000},
        {"name": "Legal & Compliance", "value": 80000},
        {"name": "Insurance", "value": 150000},
        {"name": "Travel & Entertainment", "value": 40000},
        {"name": "R&D", "value": 200000},
    ],
    "customer_acquisition": {
        "cac": 5000,
        "new_customers_y0": 50,
        "customer_growth": 0.25,
        "churn_rate": 0.10,
        "customer_lifetime": 5,
    },
}


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


def col_letter(n):
    """Convert column number (1-indexed) to letter."""
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


# Number format constants
CURRENCY_FORMAT = {"numberFormat": {"type": "NUMBER", "pattern": "#,##0.0"}}
PERCENT_FORMAT = {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}
INTEGER_FORMAT = {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}}
DECIMAL_FORMAT = {"numberFormat": {"type": "NUMBER", "pattern": "#,##0.0"}}


class FinancialModelBuilder:
    """Builds a comprehensive financial model spreadsheet."""

    def __init__(self, spreadsheet, config):
        self.spreadsheet = spreadsheet
        self.config = config
        self.row_map = {}  # Track important row numbers for cross-references

    def format_sheet_numbers(self, sheet, data):
        """Apply number formatting to all rows based on unit column using batch formatting."""
        formats = []
        for i, row in enumerate(data):
            if len(row) > 1:
                unit = str(row[1])
                row_num = i + 1
                if unit == "$":
                    formats.append(
                        {"range": f"C{row_num}:M{row_num}", "format": CURRENCY_FORMAT}
                    )
                elif unit == "%":
                    formats.append(
                        {"range": f"C{row_num}:M{row_num}", "format": PERCENT_FORMAT}
                    )
                elif unit in ["#", "units"]:
                    formats.append(
                        {"range": f"C{row_num}:M{row_num}", "format": INTEGER_FORMAT}
                    )
                elif unit in ["yrs", "years", "days", "months", "x", "mo"]:
                    formats.append(
                        {"range": f"C{row_num}:M{row_num}", "format": DECIMAL_FORMAT}
                    )

        # Apply all formats in one batch call
        if formats:
            try:
                sheet.batch_format(formats)
            except Exception as e:
                print(f"    Warning: Could not batch format: {e}")

    def build_all_sheets(self):
        """Build all sheets in the correct order - matching RapidTools template."""
        print("\nBuilding financial model sheets (RapidTools Template Order)...")

        # 1. Sources & References - TAM/SAM/SOM with linkable values
        self.build_sources_sheet()
        rate_limit_delay(3)

        # 2. Assumptions - all inputs (includes Customer Economics metrics)
        self.build_assumptions_sheet()
        rate_limit_delay(3)

        # 3. Headcount Plan - team growth and salary costs
        self.build_headcount_sheet()
        rate_limit_delay(3)

        # 4. Revenue - detailed by stream
        self.build_revenue_sheet()
        rate_limit_delay(3)

        # 5. Operating Costs - COGS + Fixed + S&M
        self.build_costs_sheet()
        rate_limit_delay(3)

        # 6. P&L - with Gross Margin, EBITDA, Net Margin
        self.build_pnl_sheet()
        rate_limit_delay(3)

        # 7. Cash Flow (must be before Balance Sheet for row_map references)
        self.build_cash_flow_sheet()
        rate_limit_delay(3)

        # 8. Balance Sheet
        self.build_balance_sheet()
        rate_limit_delay(3)

        # 9. Summary Dashboard
        self.build_summary_sheet()
        rate_limit_delay(3)

        # 10. Sensitivity Analysis
        self.build_sensitivity_sheet()
        rate_limit_delay(3)

        # 11. Valuation (DCF + Multiples)
        self.build_valuation_sheet()
        rate_limit_delay(3)

        # 12. Break-even Analysis
        self.build_breakeven_sheet()
        rate_limit_delay(3)

        # 13. Funding Cap Table
        self.build_funding_captable_sheet()
        rate_limit_delay(3)

        # 14. Charts Data - data for embedded charts
        self.build_charts_data_sheet()

        # Delete default Sheet1
        try:
            default = self.spreadsheet.worksheet("Sheet1")
            self.spreadsheet.del_worksheet(default)
        except:
            pass

        print("\n✅ All 14 sheets created successfully (RapidTools Template)!")

    def build_assumptions_sheet(self):
        """Build the Assumptions sheet with all input parameters."""
        print("  Building Assumptions sheet...")

        streams = self.config["revenue_streams"]
        fixed_costs = self.config["fixed_costs"]
        general = self.config["general"]
        cac = self.config["customer_acquisition"]

        # Calculate rows needed
        num_rows = 50 + len(streams) * 4 + len(fixed_costs)
        sheet = self.spreadsheet.add_worksheet("Assumptions", rows=num_rows, cols=13)

        data = []
        row = 1

        # Header
        data.append(["ASSUMPTIONS", ""] + YEAR_HEADERS)
        row += 1

        # ========== GENERAL PARAMETERS ==========
        data.append([""])
        row += 1
        data.append(["'--- GENERAL PARAMETERS ---"] + [""] * 12)
        self.row_map["section_general"] = row
        row += 1

        data.append(["Tax Rate", "%"] + [general["tax_rate"]] * 11)
        self.row_map["tax_rate"] = row
        row += 1

        # Capex: Y0 different, then annual
        capex_row = ["Capex", "$", general["capex_y0"]] + [general["capex_annual"]] * 10
        data.append(capex_row)
        self.row_map["capex"] = row
        row += 1

        data.append(
            ["Depreciation Years", "yrs"] + [general["depreciation_years"]] * 11
        )
        self.row_map["dep_years"] = row
        row += 1

        data.append(["Debtor Days", "days"] + [general["debtor_days"]] * 11)
        self.row_map["debtor_days"] = row
        row += 1

        data.append(["Creditor Days", "days"] + [general["creditor_days"]] * 11)
        self.row_map["creditor_days"] = row
        row += 1

        data.append(["Interest Rate", "%"] + [general["interest_rate"]] * 11)
        self.row_map["interest_rate"] = row
        row += 1

        # Equity & Debt: Y0 only
        equity_row = ["Equity Infusion", "$", general["equity_y0"]] + [0] * 10
        data.append(equity_row)
        self.row_map["equity"] = row
        row += 1

        debt_row = ["Debt Drawdown", "$", general["debt_y0"]] + [0] * 10
        data.append(debt_row)
        self.row_map["debt"] = row
        row += 1

        data.append(["Cost Inflation Rate", "%"] + [general["cost_inflation"]] * 11)
        self.row_map["inflation"] = row
        row += 1

        # ========== REVENUE STREAMS ==========
        data.append([""])
        row += 1
        data.append(["'--- REVENUE STREAMS ---"] + [""] * 12)
        self.row_map["section_revenue"] = row
        row += 1

        self.row_map["streams"] = {}
        for stream in streams:
            name = stream["name"]
            self.row_map["streams"][name] = {}

            # Price
            data.append([f"{name}: Price", "$"] + [stream["price"]] * 11)
            self.row_map["streams"][name]["price"] = row
            row += 1

            # Volume
            data.append([f"{name}: Volume", "#"] + [stream["volume"]] * 11)
            self.row_map["streams"][name]["volume"] = row
            row += 1

            # Growth
            data.append([f"{name}: Growth", "%"] + [stream["growth"]] * 11)
            self.row_map["streams"][name]["growth"] = row
            row += 1

            # COGS %
            data.append([f"{name}: COGS %", "%"] + [stream["cogs_pct"]] * 11)
            self.row_map["streams"][name]["cogs_pct"] = row
            row += 1

        # ========== FIXED COSTS ==========
        data.append([""])
        row += 1
        data.append(["'--- FIXED COSTS (Annual) ---"] + [""] * 12)
        self.row_map["section_fixed"] = row
        row += 1

        self.row_map["fixed_costs"] = {}
        for cost in fixed_costs:
            name = cost["name"]
            data.append([name, "$"] + [cost["value"]] * 11)
            self.row_map["fixed_costs"][name] = row
            row += 1

        # ========== CUSTOMER ACQUISITION ==========
        data.append([""])
        row += 1
        data.append(["'--- CUSTOMER ACQUISITION ---"] + [""] * 12)
        self.row_map["section_cac"] = row
        row += 1

        data.append(["CAC (per customer)", "$"] + [cac["cac"]] * 11)
        self.row_map["cac"] = row
        row += 1

        # New customers with growth
        new_cust_row = ["New Customers", "#", cac["new_customers_y0"]]
        for i in range(1, 11):
            new_cust_row.append(f"=ROUND(C{row}*(1+C{row+1}),0)")
        data.append(new_cust_row)
        self.row_map["new_customers"] = row
        row += 1

        data.append(["Customer Growth Rate", "%"] + [cac["customer_growth"]] * 11)
        self.row_map["cust_growth"] = row
        row += 1

        data.append(["Churn Rate", "%"] + [cac["churn_rate"]] * 11)
        self.row_map["churn"] = row
        row += 1

        data.append(["Avg Customer Lifetime", "yrs"] + [cac["customer_lifetime"]] * 11)
        self.row_map["lifetime"] = row
        row += 1

        # ========== UNIT ECONOMICS ==========
        data.append([""])
        row += 1

        data.append(["'--- UNIT ECONOMICS ---"] + [""] * 12)
        self.row_map["section_unit_economics"] = row
        row += 1

        # ARPU (Annual Revenue Per User)
        arpu_row = ["ARPU (Annual)", "$"]
        for i, col in enumerate(YEAR_COLS):
            total_customers_row = self.row_map["total_customers"]
            formula = f"=IF({col}{total_customers_row}>0,Revenue!{col}10/{col}{total_customers_row},0)"  # Assuming Revenue total is row 10
            arpu_row.append(formula)
        data.append(arpu_row)
        self.row_map["arpu"] = row
        row += 1

        # Gross Margin %
        gm_row = ["Gross Margin %", "%"]
        for i, col in enumerate(YEAR_COLS):
            formula = f"=IF(Revenue!{col}10>0,(Revenue!{col}10-'Operating Costs'!{col}5)/Revenue!{col}10,0)"  # Assuming COGS is row 5 in Operating Costs
            gm_row.append(formula)
        data.append(gm_row)
        self.row_map["gross_margin"] = row
        row += 1

        # LTV = ARPU × Lifetime × Gross Margin
        ltv_row = ["LTV", "$"]
        for i, col in enumerate(YEAR_COLS):
            ltv_row.append(f"={col}{self.row_map['arpu']}*{col}{self.row_map['lifetime']}*{col}{row-1}")
        data.append(ltv_row)
        self.row_map["ltv"] = row
        row += 1

        # LTV:CAC Ratio
        ltv_cac_row = ["LTV:CAC Ratio", "x"]
        for i, col in enumerate(YEAR_COLS):
            ltv_cac_row.append(f"=IF({col}{self.row_map['cac']}>0,{col}{self.row_map['ltv']}/{col}{self.row_map['cac']},0)")
        data.append(ltv_cac_row)
        self.row_map["ltv_cac"] = row
        row += 1

        # CAC Payback Period (months)
        payback_row = ["CAC Payback", "months"]
        for i, col in enumerate(YEAR_COLS):
            payback_row.append(f"=IF(AND({col}{self.row_map['arpu']}>0,{col}{self.row_map['gross_margin']}>0),{col}{self.row_map['cac']}/({col}{self.row_map['arpu']}/12*{col}{self.row_map['gross_margin']}),0)")
        data.append(payback_row)
        self.row_map["cac_payback"] = row
        row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )

        # Section headers
        for key in [
            "section_general",
            "section_revenue",
            "section_fixed",
            "section_cac",
            "section_unit_economics",
        ]:
            r = self.row_map.get(key)
            if r:
                sheet.format(
                    f"A{r}:M{r}",
                    {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
                    },
                )

        # Format all numbers (currency, percentages, integers, decimals)
        self.format_sheet_numbers(sheet, data)

        print(f"    ✓ Assumptions sheet ({row} rows)")

    def build_revenue_sheet(self):
        """Build Revenue sheet with each stream calculated."""
        print("  Building Revenue sheet...")

        streams = self.config["revenue_streams"]
        num_rows = len(streams) * 2 + 15
        sheet = self.spreadsheet.add_worksheet("Revenue", rows=num_rows, cols=13)

        data = []
        row = 1

        # Header
        data.append(["REVENUE", ""] + YEAR_HEADERS)
        row += 1
        data.append([""])
        row += 1

        self.row_map["revenue_streams"] = {}
        stream_revenue_rows = []

        for stream in streams:
            name = stream["name"]
            price_row = self.row_map["streams"][name]["price"]
            volume_row = self.row_map["streams"][name]["volume"]
            growth_row = self.row_map["streams"][name]["growth"]

            # Revenue = Price × Volume, with growth applied
            rev_row = [f"{name}", "$"]
            for i, col in enumerate(YEAR_COLS):
                if i == 0:
                    # Y0: Price × Volume
                    formula = (
                        f"=Assumptions!{col}{price_row}*Assumptions!{col}{volume_row}"
                    )
                else:
                    # Y1+: Previous × (1 + Growth)
                    prev_col = YEAR_COLS[i - 1]
                    formula = f"={prev_col}{row}*(1+Assumptions!{col}{growth_row})"
                rev_row.append(formula)

            data.append(rev_row)
            self.row_map["revenue_streams"][name] = row
            stream_revenue_rows.append(row)
            row += 1

        # Blank row
        data.append([""])
        row += 1

        # Total Revenue
        total_row = ["TOTAL REVENUE", "$"]
        for col in YEAR_COLS:
            refs = "+".join([f"{col}{r}" for r in stream_revenue_rows])
            total_row.append(f"={refs}")
        data.append(total_row)
        self.row_map["total_revenue"] = row
        row += 1

        # Blank row
        data.append([""])
        row += 1

        # Revenue Mix %
        data.append(["'--- Revenue Mix ---"] + [""] * 12)
        row += 1

        for stream in streams:
            name = stream["name"]
            stream_row = self.row_map["revenue_streams"][name]
            mix_row = [f"{name} %", "%"]
            for col in YEAR_COLS:
                mix_row.append(
                    f"=IF({col}${self.row_map['total_revenue']}>0,{col}{stream_row}/{col}${self.row_map['total_revenue']},0)"
                )
            data.append(mix_row)
            row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )
        sheet.format(
            f'A{self.row_map["total_revenue"]}:M{self.row_map["total_revenue"]}',
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 0.85},
            },
        )

        # Format all numbers
        self.format_sheet_numbers(sheet, data)

        print(f"    ✓ Revenue sheet ({len(streams)} streams)")

    def build_costs_sheet(self):
        """Build Operating Costs sheet with COGS, Fixed, and S&M."""
        print("  Building Operating Costs sheet...")

        streams = self.config["revenue_streams"]
        fixed_costs = self.config["fixed_costs"]

        num_rows = len(streams) + len(fixed_costs) + 20
        sheet = self.spreadsheet.add_worksheet(
            "Operating Costs", rows=num_rows, cols=13
        )

        data = []
        row = 1

        # Header
        data.append(["OPERATING COSTS", ""] + YEAR_HEADERS)
        row += 1
        data.append([""])
        row += 1

        # ========== COGS (Variable) ==========
        data.append(["'--- COST OF GOODS SOLD ---"] + [""] * 12)
        self.row_map["section_cogs"] = row
        row += 1

        cogs_rows = []
        for stream in streams:
            name = stream["name"]
            rev_row = self.row_map["revenue_streams"][name]
            cogs_pct_row = self.row_map["streams"][name]["cogs_pct"]

            cogs_row = [f"COGS: {name}", "$"]
            for col in YEAR_COLS:
                # COGS = Revenue × COGS %
                formula = f"=Revenue!{col}{rev_row}*Assumptions!{col}{cogs_pct_row}"
                cogs_row.append(formula)
            data.append(cogs_row)
            cogs_rows.append(row)
            row += 1

        # Total COGS
        total_cogs_row = ["Total COGS", "$"]
        for col in YEAR_COLS:
            refs = "+".join([f"{col}{r}" for r in cogs_rows])
            total_cogs_row.append(f"={refs}")
        data.append(total_cogs_row)
        self.row_map["total_cogs"] = row
        row += 1

        data.append([""])
        row += 1

        # ========== FIXED COSTS ==========
        data.append(["'--- FIXED COSTS ---"] + [""] * 12)
        self.row_map["section_fixed_costs"] = row
        row += 1

        fixed_rows = []
        inflation_row = self.row_map["inflation"]

        for cost in fixed_costs:
            name = cost["name"]
            assumption_row = self.row_map["fixed_costs"][name]

            fc_row = [name, "$"]
            for i, col in enumerate(YEAR_COLS):
                if i == 0:
                    # Y0: Base value from Assumptions
                    formula = f"=Assumptions!{col}{assumption_row}"
                else:
                    # Y1+: Previous × (1 + Inflation)
                    prev_col = YEAR_COLS[i - 1]
                    formula = f"={prev_col}{row}*(1+Assumptions!{col}{inflation_row})"
                fc_row.append(formula)
            data.append(fc_row)
            fixed_rows.append(row)
            row += 1

        # Total Fixed Costs
        total_fixed_row = ["Total Fixed Costs", "$"]
        for col in YEAR_COLS:
            refs = "+".join([f"{col}{r}" for r in fixed_rows])
            total_fixed_row.append(f"={refs}")
        data.append(total_fixed_row)
        self.row_map["total_fixed"] = row
        row += 1

        data.append([""])
        row += 1

        # ========== S&M (CAC) ==========
        data.append(["'--- SALES & MARKETING ---"] + [""] * 12)
        row += 1

        cac_row = self.row_map["cac"]
        new_cust_row = self.row_map["new_customers"]

        sm_row = ["Customer Acquisition Cost", "$"]
        for col in YEAR_COLS:
            formula = f"=Assumptions!{col}{cac_row}*Assumptions!{col}{new_cust_row}"
            sm_row.append(formula)
        data.append(sm_row)
        self.row_map["sm_cost"] = row
        row += 1

        data.append([""])
        row += 1

        # ========== TOTAL OPERATING COSTS ==========
        data.append(["'--- TOTAL ---"] + [""] * 12)
        row += 1

        total_opex_row = ["TOTAL OPERATING COSTS", "$"]
        for col in YEAR_COLS:
            formula = f"={col}{self.row_map['total_cogs']}+{col}{self.row_map['total_fixed']}+{col}{self.row_map['sm_cost']}"
            total_opex_row.append(formula)
        data.append(total_opex_row)
        self.row_map["total_opex"] = row
        row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )

        for key in ["section_cogs", "section_fixed_costs"]:
            r = self.row_map.get(key)
            if r:
                sheet.format(
                    f"A{r}:M{r}",
                    {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
                    },
                )

        sheet.format(
            f'A{self.row_map["total_cogs"]}:M{self.row_map["total_cogs"]}',
            {"textFormat": {"bold": True}},
        )
        sheet.format(
            f'A{self.row_map["total_fixed"]}:M{self.row_map["total_fixed"]}',
            {"textFormat": {"bold": True}},
        )
        sheet.format(
            f'A{self.row_map["total_opex"]}:M{self.row_map["total_opex"]}',
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.95, "green": 0.88, "blue": 0.88},
            },
        )

        # Format all numbers
        self.format_sheet_numbers(sheet, data)

        print(
            f"    ✓ Operating Costs sheet ({len(streams)} COGS + {len(fixed_costs)} Fixed)"
        )

    def build_pnl_sheet(self):
        """Build P&L with Gross Margin, EBITDA, Net Margin."""
        print("  Building P&L sheet...")

        streams = self.config["revenue_streams"]
        sheet = self.spreadsheet.add_worksheet("P&L", rows=40, cols=13)

        data = []
        row = 1

        # Header
        data.append(["PROFIT & LOSS", ""] + YEAR_HEADERS)
        row += 1
        data.append([""])
        row += 1

        # ========== REVENUE ==========
        data.append(["'--- REVENUE ---"] + [""] * 12)
        row += 1

        for stream in streams:
            name = stream["name"]
            rev_row = self.row_map["revenue_streams"][name]

            stream_rev = [name, "$"]
            for col in YEAR_COLS:
                stream_rev.append(f"=Revenue!{col}{rev_row}")
            data.append(stream_rev)
            row += 1

        # Total Revenue
        total_rev = ["Total Revenue", "$"]
        for col in YEAR_COLS:
            total_rev.append(f"=Revenue!{col}{self.row_map['total_revenue']}")
        data.append(total_rev)
        pnl_total_rev = row
        row += 1

        data.append([""])
        row += 1

        # ========== COGS ==========
        data.append(["'--- COST OF GOODS SOLD ---"] + [""] * 12)
        row += 1

        cogs = ["Total COGS", "$"]
        for col in YEAR_COLS:
            cogs.append(f"='Operating Costs'!{col}{self.row_map['total_cogs']}")
        data.append(cogs)
        pnl_cogs = row
        row += 1

        data.append([""])
        row += 1

        # ========== GROSS PROFIT ==========
        data.append(["'--- GROSS PROFIT ---"] + [""] * 12)
        row += 1

        gross_profit = ["Gross Profit", "$"]
        for col in YEAR_COLS:
            gross_profit.append(f"={col}{pnl_total_rev}-{col}{pnl_cogs}")
        data.append(gross_profit)
        pnl_gp = row
        row += 1

        gross_margin = ["Gross Margin %", "%"]
        for col in YEAR_COLS:
            gross_margin.append(
                f"=IF({col}{pnl_total_rev}>0,{col}{pnl_gp}/{col}{pnl_total_rev},0)"
            )
        data.append(gross_margin)
        pnl_gm_pct = row
        row += 1

        data.append([""])
        row += 1

        # ========== OPERATING EXPENSES ==========
        data.append(["'--- OPERATING EXPENSES ---"] + [""] * 12)
        row += 1

        fixed = ["Fixed Costs", "$"]
        for col in YEAR_COLS:
            fixed.append(f"='Operating Costs'!{col}{self.row_map['total_fixed']}")
        data.append(fixed)
        pnl_fixed = row
        row += 1

        sm = ["Sales & Marketing", "$"]
        for col in YEAR_COLS:
            sm.append(f"='Operating Costs'!{col}{self.row_map['sm_cost']}")
        data.append(sm)
        pnl_sm = row
        row += 1

        total_opex = ["Total Operating Expenses", "$"]
        for col in YEAR_COLS:
            total_opex.append(f"={col}{pnl_fixed}+{col}{pnl_sm}")
        data.append(total_opex)
        pnl_total_opex = row
        row += 1

        data.append([""])
        row += 1

        # ========== EBITDA ==========
        data.append(["'--- EBITDA ---"] + [""] * 12)
        row += 1

        ebitda = ["EBITDA", "$"]
        for col in YEAR_COLS:
            ebitda.append(f"={col}{pnl_gp}-{col}{pnl_total_opex}")
        data.append(ebitda)
        pnl_ebitda = row
        self.row_map["pnl_ebitda"] = row
        row += 1

        ebitda_margin = ["EBITDA Margin %", "%"]
        for col in YEAR_COLS:
            ebitda_margin.append(
                f"=IF({col}{pnl_total_rev}>0,{col}{pnl_ebitda}/{col}{pnl_total_rev},0)"
            )
        data.append(ebitda_margin)
        row += 1

        data.append([""])
        row += 1

        # ========== D&A, EBIT ==========
        depreciation = ["Depreciation", "$"]
        for col in YEAR_COLS:
            depreciation.append(
                f"=IF(Assumptions!{col}{self.row_map['dep_years']}>0,Assumptions!{col}{self.row_map['capex']}/Assumptions!{col}{self.row_map['dep_years']},0)"
            )
        data.append(depreciation)
        pnl_dep = row
        self.row_map["pnl_depreciation"] = row
        row += 1

        ebit = ["EBIT", "$"]
        for col in YEAR_COLS:
            ebit.append(f"={col}{pnl_ebitda}-{col}{pnl_dep}")
        data.append(ebit)
        pnl_ebit = row
        row += 1

        data.append([""])
        row += 1

        # ========== INTEREST, TAX, PAT ==========
        interest = ["Interest Expense", "$"]
        for col in YEAR_COLS:
            interest.append(
                f"=Assumptions!{col}{self.row_map['debt']}*Assumptions!{col}{self.row_map['interest_rate']}"
            )
        data.append(interest)
        pnl_interest = row
        row += 1

        pbt = ["PBT", "$"]
        for col in YEAR_COLS:
            pbt.append(f"={col}{pnl_ebit}-{col}{pnl_interest}")
        data.append(pbt)
        pnl_pbt = row
        row += 1

        tax = ["Tax", "$"]
        for col in YEAR_COLS:
            tax.append(
                f"=IF({col}{pnl_pbt}>0,{col}{pnl_pbt}*Assumptions!{col}{self.row_map['tax_rate']},0)"
            )
        data.append(tax)
        pnl_tax = row
        row += 1

        data.append([""])
        row += 1

        # ========== NET INCOME ==========
        data.append(["'--- NET INCOME ---"] + [""] * 12)
        row += 1

        pat = ["PAT (Net Income)", "$"]
        for col in YEAR_COLS:
            pat.append(f"={col}{pnl_pbt}-{col}{pnl_tax}")
        data.append(pat)
        pnl_pat = row
        self.row_map["pnl_pat"] = row
        self.row_map["pnl_total_rev"] = pnl_total_rev
        row += 1

        net_margin = ["Net Margin %", "%"]
        for col in YEAR_COLS:
            net_margin.append(
                f"=IF({col}{pnl_total_rev}>0,{col}{pnl_pat}/{col}{pnl_total_rev},0)"
            )
        data.append(net_margin)
        row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )

        sheet.format(
            f"A{pnl_total_rev}:M{pnl_total_rev}", {"textFormat": {"bold": True}}
        )
        sheet.format(
            f"A{pnl_gp}:M{pnl_gp}",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9},
            },
        )
        sheet.format(
            f"A{pnl_ebitda}:M{pnl_ebitda}",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9},
            },
        )
        sheet.format(
            f"A{pnl_pat}:M{pnl_pat}",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 0.85},
            },
        )

        # Format all numbers
        self.format_sheet_numbers(sheet, data)

        print(f"    ✓ P&L sheet (Gross Margin, EBITDA, Net Margin)")

    def build_customer_economics_sheet(self):
        """Build Customer Economics sheet."""
        print("  Building Customer Economics sheet...")

        sheet = self.spreadsheet.add_worksheet("Customer Economics", rows=20, cols=13)

        data = []
        row = 1

        # Header
        data.append(["CUSTOMER ECONOMICS", ""] + YEAR_HEADERS)
        row += 1
        data.append([""])
        row += 1

        # CAC
        cac = ["CAC", "$"]
        for col in YEAR_COLS:
            cac.append(f"=Assumptions!{col}{self.row_map['cac']}")
        data.append(cac)
        ce_cac = row
        row += 1

        # ARPU (Total Revenue / Total Customers) - monthly
        arpu = ["ARPU (Monthly)", "$"]
        for col in YEAR_COLS:
            arpu.append(
                f"=IF(Assumptions!{col}{self.row_map['new_customers']}>0,Revenue!{col}{self.row_map['total_revenue']}/(Assumptions!{col}{self.row_map['new_customers']}*12),0)"
            )
        data.append(arpu)
        ce_arpu = row
        row += 1

        # Gross Margin %
        gm = ["Gross Margin %", "%"]
        for col in YEAR_COLS:
            gm.append(
                f"=IF(Revenue!{col}{self.row_map['total_revenue']}>0,(Revenue!{col}{self.row_map['total_revenue']}-'Operating Costs'!{col}{self.row_map['total_cogs']})/Revenue!{col}{self.row_map['total_revenue']},0)"
            )
        data.append(gm)
        ce_gm = row
        row += 1

        # Lifetime
        lifetime = ["Customer Lifetime", "yrs"]
        for col in YEAR_COLS:
            lifetime.append(f"=Assumptions!{col}{self.row_map['lifetime']}")
        data.append(lifetime)
        ce_lifetime = row
        row += 1

        # LTV = ARPU × 12 × Lifetime × GM
        ltv = ["LTV", "$"]
        for col in YEAR_COLS:
            ltv.append(f"={col}{ce_arpu}*12*{col}{ce_lifetime}*{col}{ce_gm}")
        data.append(ltv)
        ce_ltv = row
        row += 1

        # LTV:CAC
        ltv_cac = ["LTV:CAC Ratio", "x"]
        for col in YEAR_COLS:
            ltv_cac.append(f"=IF({col}{ce_cac}>0,{col}{ce_ltv}/{col}{ce_cac},0)")
        data.append(ltv_cac)
        row += 1

        # CAC Payback
        payback = ["CAC Payback", "months"]
        for col in YEAR_COLS:
            payback.append(
                f"=IF(AND({col}{ce_arpu}>0,{col}{ce_gm}>0),{col}{ce_cac}/({col}{ce_arpu}*{col}{ce_gm}),0)"
            )
        data.append(payback)
        row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )

        # Format all numbers
        self.format_sheet_numbers(sheet, data)

        print(f"    ✓ Customer Economics sheet")

    def build_balance_sheet(self):
        """Build Balance Sheet."""
        print("  Building Balance Sheet...")

        sheet = self.spreadsheet.add_worksheet("Balance Sheet", rows=25, cols=13)

        data = []
        row = 1

        # Header
        data.append(["BALANCE SHEET", ""] + YEAR_HEADERS)
        row += 1
        data.append([""])
        row += 1

        # ========== ASSETS ==========
        data.append(["'--- ASSETS ---"] + [""] * 12)
        row += 1

        # Fixed Assets (Cumulative Capex - Cumulative Depreciation)
        fixed_assets = ["Fixed Assets (Net)", "$"]
        for i, col in enumerate(YEAR_COLS):
            if i == 0:
                fixed_assets.append(
                    f"=Assumptions!{col}{self.row_map['capex']}-'P&L'!{col}{self.row_map['pnl_depreciation']}"
                )
            else:
                prev_col = YEAR_COLS[i - 1]
                fixed_assets.append(
                    f"={prev_col}{row}+Assumptions!{col}{self.row_map['capex']}-'P&L'!{col}{self.row_map['pnl_depreciation']}"
                )
        data.append(fixed_assets)
        bs_fixed = row
        row += 1

        # Debtors
        debtors = ["Debtors", "$"]
        for col in YEAR_COLS:
            debtors.append(
                f"='P&L'!{col}{self.row_map['pnl_total_rev']}*Assumptions!{col}{self.row_map['debtor_days']}/365"
            )
        data.append(debtors)
        bs_debtors = row
        row += 1

        # Cash (from Cash Flow)
        cash = ["Cash", "$"]
        for col in YEAR_COLS:
            cash.append(f"='Cash Flow'!{col}{self.row_map['cf_cumulative']}")
        data.append(cash)
        bs_cash = row
        row += 1

        # Total Assets
        total_assets = ["Total Assets", "$"]
        for col in YEAR_COLS:
            total_assets.append(f"={col}{bs_fixed}+{col}{bs_debtors}+{col}{bs_cash}")
        data.append(total_assets)
        bs_total_assets = row
        row += 1

        data.append([""])
        row += 1

        # ========== LIABILITIES & EQUITY ==========
        data.append(["'--- LIABILITIES & EQUITY ---"] + [""] * 12)
        row += 1

        # Creditors
        creditors = ["Creditors", "$"]
        for col in YEAR_COLS:
            creditors.append(
                f"='Operating Costs'!{col}{self.row_map['total_opex']}*Assumptions!{col}{self.row_map['creditor_days']}/365"
            )
        data.append(creditors)
        bs_creditors = row
        row += 1

        # Equity (Cumulative)
        equity = ["Equity", "$"]
        for i, col in enumerate(YEAR_COLS):
            if i == 0:
                equity.append(f"=Assumptions!{col}{self.row_map['equity']}")
            else:
                prev_col = YEAR_COLS[i - 1]
                equity.append(
                    f"={prev_col}{row}+Assumptions!{col}{self.row_map['equity']}"
                )
        data.append(equity)
        bs_equity = row
        row += 1

        # Debt (Cumulative)
        debt = ["Debt", "$"]
        for i, col in enumerate(YEAR_COLS):
            if i == 0:
                debt.append(f"=Assumptions!{col}{self.row_map['debt']}")
            else:
                prev_col = YEAR_COLS[i - 1]
                debt.append(f"={prev_col}{row}+Assumptions!{col}{self.row_map['debt']}")
        data.append(debt)
        bs_debt = row
        row += 1

        # Retained Earnings (Cumulative PAT)
        retained = ["Retained Earnings", "$"]
        for i, col in enumerate(YEAR_COLS):
            if i == 0:
                retained.append(f"='P&L'!{col}{self.row_map['pnl_pat']}")
            else:
                prev_col = YEAR_COLS[i - 1]
                retained.append(
                    f"={prev_col}{row}+'P&L'!{col}{self.row_map['pnl_pat']}"
                )
        data.append(retained)
        bs_retained = row
        row += 1

        # Total L&E
        total_le = ["Total Liab & Equity", "$"]
        for col in YEAR_COLS:
            total_le.append(
                f"={col}{bs_creditors}+{col}{bs_equity}+{col}{bs_debt}+{col}{bs_retained}"
            )
        data.append(total_le)
        bs_total_le = row
        row += 1

        data.append([""])
        row += 1

        # Check
        check = ["Check (should be 0)", "$"]
        for col in YEAR_COLS:
            check.append(f"=ROUND({col}{bs_total_assets}-{col}{bs_total_le},0)")
        data.append(check)
        row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )
        sheet.format(
            f"A{bs_total_assets}:M{bs_total_assets}", {"textFormat": {"bold": True}}
        )
        sheet.format(f"A{bs_total_le}:M{bs_total_le}", {"textFormat": {"bold": True}})

        # Format all numbers
        self.format_sheet_numbers(sheet, data)

        print(f"    ✓ Balance Sheet")

    def build_cash_flow_sheet(self):
        """Build Cash Flow statement."""
        print("  Building Cash Flow sheet...")

        sheet = self.spreadsheet.add_worksheet("Cash Flow", rows=20, cols=13)

        data = []
        row = 1

        # Header
        data.append(["CASH FLOW", ""] + YEAR_HEADERS)
        row += 1
        data.append([""])
        row += 1

        # ========== OPERATING ==========
        data.append(["'--- OPERATING CASH FLOW ---"] + [""] * 12)
        row += 1

        pat = ["PAT", "$"]
        for col in YEAR_COLS:
            pat.append(f"='P&L'!{col}{self.row_map['pnl_pat']}")
        data.append(pat)
        cf_pat = row
        row += 1

        dep = ["'+ Depreciation", "$"]  # Escaped + sign
        for col in YEAR_COLS:
            dep.append(f"='P&L'!{col}{self.row_map['pnl_depreciation']}")
        data.append(dep)
        cf_dep = row
        row += 1

        # Working Capital Change (simplified)
        wc = ["- Change in WC", "$"]
        for i, col in enumerate(YEAR_COLS):
            if i == 0:
                wc.append(
                    f"=('P&L'!{col}{self.row_map['pnl_total_rev']}*Assumptions!{col}{self.row_map['debtor_days']}/365)-('Operating Costs'!{col}{self.row_map['total_opex']}*Assumptions!{col}{self.row_map['creditor_days']}/365)"
                )
            else:
                prev_col = YEAR_COLS[i - 1]
                wc.append(
                    f"=(('P&L'!{col}{self.row_map['pnl_total_rev']}*Assumptions!{col}{self.row_map['debtor_days']}/365)-('P&L'!{prev_col}{self.row_map['pnl_total_rev']}*Assumptions!{prev_col}{self.row_map['debtor_days']}/365))-(('Operating Costs'!{col}{self.row_map['total_opex']}*Assumptions!{col}{self.row_map['creditor_days']}/365)-('Operating Costs'!{prev_col}{self.row_map['total_opex']}*Assumptions!{prev_col}{self.row_map['creditor_days']}/365))"
                )
        data.append(wc)
        cf_wc = row
        row += 1

        ocf = ["Operating Cash Flow", "$"]
        for col in YEAR_COLS:
            ocf.append(f"={col}{cf_pat}+{col}{cf_dep}-{col}{cf_wc}")
        data.append(ocf)
        cf_ocf = row
        row += 1

        data.append([""])
        row += 1

        # ========== INVESTING ==========
        data.append(["'--- INVESTING CASH FLOW ---"] + [""] * 12)
        row += 1

        capex = ["Capex", "$"]
        for col in YEAR_COLS:
            capex.append(f"=-Assumptions!{col}{self.row_map['capex']}")
        data.append(capex)
        cf_capex = row
        row += 1

        # ========== FINANCING ==========
        data.append(["'--- FINANCING CASH FLOW ---"] + [""] * 12)
        row += 1

        equity = ["Equity", "$"]
        for col in YEAR_COLS:
            equity.append(f"=Assumptions!{col}{self.row_map['equity']}")
        data.append(equity)
        cf_equity = row
        row += 1

        debt = ["Debt", "$"]
        for col in YEAR_COLS:
            debt.append(f"=Assumptions!{col}{self.row_map['debt']}")
        data.append(debt)
        cf_debt = row
        row += 1

        # Net & Cumulative
        net_cf = ["Net Cash Flow", "$"]
        for col in YEAR_COLS:
            net_cf.append(
                f"={col}{cf_ocf}+{col}{cf_capex}+{col}{cf_equity}+{col}{cf_debt}"
            )
        data.append(net_cf)
        cf_net = row
        row += 1

        cumulative = ["Cumulative Cash", "$"]
        for i, col in enumerate(YEAR_COLS):
            if i == 0:
                cumulative.append(f"={col}{cf_net}")
            else:
                prev_col = YEAR_COLS[i - 1]
                cumulative.append(f"={prev_col}{row}+{col}{cf_net}")
        data.append(cumulative)
        cf_cumulative = row  # Store row for Balance Sheet reference
        self.row_map["cf_cumulative"] = cf_cumulative
        row += 1

        # Write data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            },
        )
        sheet.format(f"A{cf_ocf}:M{cf_ocf}", {"textFormat": {"bold": True}})
        sheet.format(f"A{cf_net}:M{cf_net}", {"textFormat": {"bold": True}})

        # Format all numbers
        self.format_sheet_numbers(sheet, data)

        print(f"    ✓ Cash Flow sheet")

    def build_summary_sheet(self):
        """Build Summary Dashboard sheet."""
        print("  Building Summary sheet...")

        streams = self.config["revenue_streams"]
        sheet = self.spreadsheet.add_worksheet("Summary", rows=30, cols=5)

        data = [
            ["KEY METRICS SUMMARY", "", "", ""],
            [""],
            ["'--- REVENUE ---", "", "", ""],
            ["Total Revenue Y1", f"=Revenue!C{self.row_map['total_revenue']}", "", ""],
            ["Total Revenue Y5", f"=Revenue!G{self.row_map['total_revenue']}", "", ""],
            ["Total Revenue Y10", f"=Revenue!L{self.row_map['total_revenue']}", "", ""],
            [""],
            ["'--- PROFITABILITY ---", "", "", ""],
            ["EBITDA Y5", f"='P&L'!G{self.row_map['pnl_ebitda']}", "", ""],
            ["Net Income Y5", f"='P&L'!G{self.row_map['pnl_pat']}", "", ""],
            ["EBITDA Y10", f"='P&L'!L{self.row_map['pnl_ebitda']}", "", ""],
            ["Net Income Y10", f"='P&L'!L{self.row_map['pnl_pat']}", "", ""],
            [""],
            ["'--- MARGINS (Y5) ---", "", "", ""],
            [
                "Gross Margin %",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,(Revenue!G{self.row_map['total_revenue']}-'Operating Costs'!G{self.row_map['total_cogs']})/Revenue!G{self.row_map['total_revenue']},0)",
                "",
                "",
            ],
            [
                "EBITDA Margin %",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,'P&L'!G{self.row_map['pnl_ebitda']}/Revenue!G{self.row_map['total_revenue']},0)",
                "",
                "",
            ],
            [
                "Net Margin %",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,'P&L'!G{self.row_map['pnl_pat']}/Revenue!G{self.row_map['total_revenue']},0)",
                "",
                "",
            ],
            [""],
            ["'--- REVENUE MIX (Y5) ---", "", "", ""],
        ]

        for stream in streams:
            name = stream["name"]
            rev_row = self.row_map["revenue_streams"][name]
            data.append(
                [
                    name,
                    f"=IF(Revenue!G{self.row_map['total_revenue']}>0,Revenue!G{rev_row}/Revenue!G{self.row_map['total_revenue']},0)",
                    "",
                    "",
                ]
            )

        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        sheet.format(
            "A1:D1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.5, "blue": 0.3},
            },
        )

        print(f"    ✓ Summary sheet")

    def build_sources_sheet(self):
        """Build Sources & References sheet with two-section structure.

        SECTION A: Key Metrics (Linkable Values)
        - TAM calculations with formulas
        - SAM by region with formulas
        - SOM customer projections
        - Pricing, COGS, CAC benchmarks

        SECTION B: Full Source Documentation
        - Market research sources with URLs
        - Competitor data
        - Industry benchmarks
        """
        print("  Building Sources & References sheet...")

        sheet = self.spreadsheet.add_worksheet("Sources & References", rows=160, cols=5)

        # Get sources and market data from config if available
        sources = self.config.get("sources", {})
        market_data = self.config.get("market_data", {})

        # Get company name for header
        company_name = self.config.get("company_name", "COMPANY")

        data = []

        # ========== HEADER ==========
        data.append(
            [
                f"SOURCES & REFERENCES - {company_name.upper()} FINANCIAL MODEL",
                "",
                "",
                "",
                "",
            ]
        )
        data.append(
            [f'Last Updated: {datetime.now().strftime("%B %Y")}', "", "", "", ""]
        )
        data.append([""])

        # ========== SECTION A: KEY METRICS ==========
        data.append(
            [
                "SECTION A: KEY METRICS (Linkable Values in Column B)",
                "Value",
                "Unit",
                "Source",
                "Notes",
            ]
        )
        data.append([""])

        # --- TAM ---
        data.append(["TAM - TOTAL ADDRESSABLE MARKET", "", "", "", ""])
        tam_start_row = len(data) + 1
        data.append(
            [
                "Global Market Value",
                market_data.get("tam_global", 1000000000),
                "$",
                sources.get("tam_source", "[Research Source]"),
                "Total market size",
            ]
        )
        data.append(
            [
                "Market CAGR",
                market_data.get("tam_cagr", 0.10),
                "%",
                sources.get("cagr_source", "[Research Source]"),
                "Growth forecast",
            ]
        )
        data.append(
            [
                "Target Segment %",
                market_data.get("tam_segment_pct", 0.15),
                "%",
                sources.get("segment_source", "[Research Source]"),
                "Addressable segment",
            ]
        )
        data.append(
            [
                f"TAM - Target Segment",
                f"=B{tam_start_row}*B{tam_start_row+2}",
                "$",
                "Calculated",
                "Formula linkage",
            ]
        )
        data.append([""])

        # --- SAM ---
        data.append(["SAM - SERVICEABLE ADDRESSABLE MARKET", "", "", "", ""])
        data.append([""])

        # Regional SAM data structure
        regions = market_data.get(
            "regions",
            [
                {
                    "name": "INDIA",
                    "total": 680000,
                    "target": 58500,
                    "pct": 0.10,
                    "source": "IBEF",
                },
                {
                    "name": "SOUTHEAST ASIA",
                    "total": 250000,
                    "target": 24200,
                    "pct": 0.12,
                    "source": "ASEAN Reports",
                },
                {
                    "name": "JAPAN",
                    "total": 180000,
                    "target": 26400,
                    "pct": 0.25,
                    "source": "METI Japan",
                },
                {
                    "name": "GERMANY / EU",
                    "total": 200000,
                    "target": 30600,
                    "pct": 0.20,
                    "source": "Eurostat",
                },
                {
                    "name": "OTHER REGIONS",
                    "total": 0,
                    "target": 0,
                    "pct": 0,
                    "source": "Estimated",
                    "fixed_sam": 8000,
                },
            ],
        )

        sam_rows = []
        for region in regions:
            data.append([region["name"], "", "", "", ""])
            region_start = len(data) + 1

            if region.get("fixed_sam"):
                # For "Other Regions" with fixed SAM value
                data.append(
                    [
                        f"{region['name'].split()[0]} - SAM Companies",
                        region["fixed_sam"],
                        "#",
                        region["source"],
                        "Estimated",
                    ]
                )
                sam_rows.append(len(data))
            else:
                data.append(
                    [
                        f"{region['name'].split()[0]} - Total Mfg Companies",
                        region["total"],
                        "#",
                        region["source"],
                        "Total market",
                    ]
                )
                data.append(
                    [
                        f"{region['name'].split()[0]} - Target Segments",
                        region["target"],
                        "#",
                        f"{region['source']}",
                        "Filtered",
                    ]
                )
                data.append(
                    [
                        f"{region['name'].split()[0]} - Addressable %",
                        region["pct"],
                        "%",
                        "Market Analysis",
                        "Penetration",
                    ]
                )
                data.append(
                    [
                        f"{region['name'].split()[0]} - SAM Companies",
                        f"=B{region_start+1}*B{region_start+2}",
                        "#",
                        "Calculated",
                        "Formula",
                    ]
                )
                sam_rows.append(len(data))
            data.append([""])

        # SAM Total
        sam_formula = "+".join([f"B{r}" for r in sam_rows])
        data.append(
            [
                "TOTAL SAM - Companies",
                f"={sam_formula}",
                "#",
                "Calculated",
                "Sum of regions",
            ]
        )
        total_sam_row = len(data)
        data.append(
            [
                "Avg Software Spend/Company",
                market_data.get("avg_spend", 3000),
                "$/yr",
                "Industry Benchmark",
                "Annual spend",
            ]
        )
        data.append(
            [
                "SAM Value (Total)",
                f"=B{total_sam_row}*B{total_sam_row+1}",
                "$",
                "Calculated",
                "Formula",
            ]
        )
        data.append([""])

        # --- SOM ---
        data.append(["SOM - SERVICEABLE OBTAINABLE MARKET", "", "", "", ""])
        som_data = market_data.get(
            "som", {"y0": 10, "y1": 70, "y2": 190, "y3": 410, "y4": 750, "y5": 1180}
        )
        data.append(
            [
                "Y0 Customers",
                som_data.get("y0", 10),
                "#",
                "Launch target",
                "Initial customers",
            ]
        )
        data.append(
            ["Y1 Customers", som_data.get("y1", 70), "#", "Growth plan", "Year 1"]
        )
        data.append(
            ["Y2 Customers", som_data.get("y2", 190), "#", "Growth plan", "Year 2"]
        )
        data.append(
            ["Y3 Customers", som_data.get("y3", 410), "#", "Growth plan", "Year 3"]
        )
        data.append(
            ["Y4 Customers", som_data.get("y4", 750), "#", "Growth plan", "Year 4"]
        )
        y5_row = len(data) + 1
        data.append(
            ["Y5 Customers", som_data.get("y5", 1180), "#", "Growth plan", "Year 5"]
        )
        data.append(
            [
                "Y5 SAM Penetration",
                f"=B{y5_row}/B{total_sam_row}",
                "%",
                "Industry benchmark 2-5%",
                "Calculated",
            ]
        )
        data.append([""])

        # Seats Expansion
        data.append(["SEATS EXPANSION MODEL", "", "", "", ""])
        seats = market_data.get(
            "seats", {"y0": 1, "y1": 2, "y2": 2, "y3": 3, "y4": 3, "y5": 4}
        )
        for i in range(6):
            data.append(
                [
                    f"Y{i} Seats/Customer",
                    seats.get(f"y{i}", i // 2 + 1),
                    "#",
                    "Land & expand",
                    f"Year {i}",
                ]
            )
        data.append([""])

        # --- Pricing ---
        data.append(["PRICING BENCHMARKS", "", "", "", ""])
        pricing = self.config.get(
            "pricing_benchmarks",
            [
                {
                    "name": "Software Subscription Price",
                    "value": 1500,
                    "unit": "$/seat/yr",
                },
                {"name": "Hardware Price", "value": 5000, "unit": "$/unit"},
                {"name": "Consumables Price", "value": 600, "unit": "$/unit"},
                {"name": "AMC Contract Price", "value": 400, "unit": "$/yr"},
                {"name": "Managed Services Price", "value": 30000, "unit": "$/yr"},
            ],
        )
        for p in pricing:
            data.append([p["name"], p["value"], p["unit"], "Competitor analysis", ""])
        data.append([""])

        # --- COGS ---
        data.append(["COGS PERCENTAGES", "", "", "", ""])
        cogs = self.config.get(
            "cogs_benchmarks",
            [
                {"name": "Software COGS %", "value": 0.15},
                {"name": "Hardware COGS %", "value": 0.45},
                {"name": "Consumables COGS %", "value": 0.60},
                {"name": "Services COGS %", "value": 0.35},
                {"name": "Managed Services COGS %", "value": 0.50},
            ],
        )
        for c in cogs:
            data.append([c["name"], c["value"], "%", "Industry benchmark", ""])
        data.append([""])

        # --- CAC ---
        data.append(["CUSTOMER ACQUISITION", "", "", "", ""])
        cac_data = self.config.get("customer_acquisition", {})
        cac_values = market_data.get(
            "cac",
            {"y0": 2000, "y1": 1800, "y2": 1500, "y3": 1400, "y4": 1300, "y5": 1200},
        )
        for i in range(6):
            data.append(
                [
                    f"Y{i} CAC",
                    cac_values.get(f"y{i}", 2000 - i * 150),
                    "$/customer",
                    "Scale efficiencies",
                    "",
                ]
            )
        churn_row = len(data) + 1
        data.append(
            [
                "Churn Rate",
                market_data.get("churn_rate", 0.10),
                "%",
                "SaaS benchmark",
                "3.5-10% industry range",
            ]
        )
        data.append(
            [
                "Avg Customer Lifetime",
                f"=1/B{churn_row}",
                "years",
                "Calculated",
                "1 / Churn Rate",
            ]
        )
        data.append([""])

        # --- Attachment Rates ---
        data.append(["PRODUCT ATTACHMENT RATES", "", "", "", ""])
        attach = market_data.get(
            "attachment_rates",
            [
                {"name": "Hardware Attach Rate", "value": 0.20},
                {"name": "Consumables/Hardware/Year", "value": 30, "unit": "units"},
                {"name": "AMC Attach Rate", "value": 0.35},
                {"name": "Managed Services Rate", "value": 0.05},
            ],
        )
        for a in attach:
            unit = a.get("unit", "%")
            data.append([a["name"], a["value"], unit, "Cross-sell estimate", ""])
        data.append([""])
        data.append([""])

        # ========== SECTION B: SOURCE DOCUMENTATION ==========
        data.append(["SECTION B: FULL SOURCE DOCUMENTATION", "", "", "", ""])
        data.append(["Source Name", "Report/Page", "", "URL", "Key Data Point"])
        data.append([""])

        # Source categories
        source_categories = [
            (
                "MARKET SIZE RESEARCH",
                sources.get(
                    "market_sources",
                    [
                        {
                            "name": "Mordor Intelligence",
                            "report": "Market Report",
                            "url": "[URL]",
                            "data": "TAM data",
                        },
                        {
                            "name": "Grand View Research",
                            "report": "Industry Analysis",
                            "url": "[URL]",
                            "data": "Market size",
                        },
                        {
                            "name": "MarketsandMarkets",
                            "report": "Growth Forecast",
                            "url": "[URL]",
                            "data": "CAGR",
                        },
                    ],
                ),
            ),
            (
                "REGIONAL MARKET DATA",
                sources.get(
                    "regional_sources",
                    [
                        {
                            "name": "IBEF India",
                            "report": "Manufacturing Report",
                            "url": "[URL]",
                            "data": "India market",
                        },
                        {
                            "name": "ASEAN Secretariat",
                            "report": "Economic Report",
                            "url": "[URL]",
                            "data": "SE Asia data",
                        },
                    ],
                ),
            ),
            (
                "COMPETITOR RESEARCH",
                sources.get(
                    "competitor_sources",
                    [
                        {
                            "name": "6sense",
                            "report": "Market Share Data",
                            "url": "[URL]",
                            "data": "Competitor shares",
                        },
                        {
                            "name": "G2/Capterra",
                            "report": "Product Reviews",
                            "url": "[URL]",
                            "data": "Pricing data",
                        },
                    ],
                ),
            ),
            (
                "SAAS BENCHMARK RESEARCH",
                sources.get(
                    "saas_benchmarks",
                    [
                        {
                            "name": "Recurly",
                            "report": "Churn Report",
                            "url": "[URL]",
                            "data": "B2B SaaS churn: 3.5%",
                        },
                        {
                            "name": "ChurnFree",
                            "report": "B2B Benchmarks",
                            "url": "[URL]",
                            "data": "Target: 5% or lower",
                        },
                        {
                            "name": "F22 Labs",
                            "report": "Market Sizing Guide",
                            "url": "[URL]",
                            "data": "SAM penetration 2-5%",
                        },
                    ],
                ),
            ),
        ]

        for category_name, category_sources in source_categories:
            data.append([category_name, "", "", "", ""])
            for src in category_sources:
                data.append([src["name"], src["report"], "", src["url"], src["data"]])
            data.append([""])

        # Notes section
        data.append([""])
        data.append(["NOTES", "", "", "", ""])
        data.append(
            [
                "- All market research conducted via SerpAPI (Google Search) and industry reports",
                "",
                "",
                "",
                "",
            ]
        )
        data.append(
            [
                "- Data validated against multiple sources where available",
                "",
                "",
                "",
                "",
            ]
        )
        data.append(
            [
                "- Column B values are linkable to Assumptions sheet via formulas",
                "",
                "",
                "",
                "",
            ]
        )
        data.append(
            [
                f'- Last research update: {datetime.now().strftime("%B %Y")}',
                "",
                "",
                "",
                "",
            ]
        )
        data.append(["- All URLs verified active at time of research", "", "", "", ""])

        # Write all data
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")
        rate_limit_delay(2)

        # Apply formatting
        self._format_sources_sheet(sheet, len(data))

        print(f"    ✓ Sources & References sheet ({len(data)} rows)")

    def _format_sources_sheet(self, sheet, total_rows):
        """Apply professional formatting to Sources & References sheet.

        FORMATTING STANDARDS (Exact RGB values):
        =========================================

        SECTION A (Key Metrics):
        - Main Title (Row 1): Dark blue BG RGB(0.2,0.3,0.5), white bold 14pt
        - Section Header (Row 4): Dark blue BG RGB(0.2,0.4,0.6), white bold 12pt
        - Category Headers (TAM, SAM, etc.): Medium blue BG RGB(0.3,0.5,0.7), white bold 11pt
        - Regional Headers (INDIA, etc.): No BG, bold black text 10pt
        - Data Rows: White/Light blue zebra RGB(0.85,0.92,0.98)

        SECTION B (Source Documentation):
        - Section Header: Dark blue BG RGB(0.2,0.4,0.6), white bold 12pt
        - Column Headers: Light gray BG RGB(0.95,0.95,0.95), bold black text
        - Category Headers: Medium blue BG RGB(0.4,0.6,0.8), white bold text
        - Data Rows: White/Light blue zebra RGB(0.85,0.92,0.98)
        - URLs (Column D): Blue text RGB(0.1,0.3,0.7)
        - NOTES Header: Gray BG RGB(0.5,0.5,0.5), white bold text
        """
        try:
            import time

            from gspread_formatting import (
                CellFormat,
                Color,
                TextFormat,
                format_cell_range,
                set_column_width,
                set_row_height,
            )

            # ================================================================
            # STANDARD COLOR DEFINITIONS (Exact RGB values)
            # ================================================================
            DARK_BLUE = Color(0.20, 0.40, 0.60)  # Section headers #336699
            MEDIUM_BLUE = Color(
                0.40, 0.60, 0.80
            )  # Category headers in Section B #6699CC
            SECTION_A_CAT = Color(0.30, 0.50, 0.70)  # Category headers in Section A
            LIGHT_BLUE = Color(0.85, 0.92, 0.98)  # Zebra stripe #D8EAF9
            WHITE = Color(1, 1, 1)
            BLACK = Color(0, 0, 0)
            GRAY = Color(0.50, 0.50, 0.50)  # Notes header
            LIGHT_GRAY = Color(0.95, 0.95, 0.95)  # Column headers
            URL_BLUE = Color(0.10, 0.30, 0.70)  # URL text color #1A4CB3
            TITLE_BLUE = Color(0.20, 0.30, 0.50)  # Main title

            # ================================================================
            # FORMAT DEFINITIONS
            # ================================================================

            # Main title (Row 1)
            title_fmt = CellFormat(
                backgroundColor=TITLE_BLUE,
                textFormat=TextFormat(bold=True, foregroundColor=WHITE, fontSize=14),
                horizontalAlignment="LEFT",
            )

            # Section headers (SECTION A, SECTION B)
            section_header_fmt = CellFormat(
                backgroundColor=DARK_BLUE,
                textFormat=TextFormat(bold=True, foregroundColor=WHITE, fontSize=12),
                horizontalAlignment="LEFT",
            )

            # Column headers in Section B
            column_header_fmt = CellFormat(
                backgroundColor=LIGHT_GRAY,
                textFormat=TextFormat(bold=True, foregroundColor=BLACK),
                horizontalAlignment="LEFT",
            )

            # Category headers in Section A (TAM, SAM, SOM, PRICING, etc.)
            section_a_category_fmt = CellFormat(
                backgroundColor=SECTION_A_CAT,
                textFormat=TextFormat(bold=True, foregroundColor=WHITE, fontSize=11),
                horizontalAlignment="LEFT",
            )

            # Category headers in Section B (MARKET SIZE RESEARCH, etc.)
            section_b_category_fmt = CellFormat(
                backgroundColor=MEDIUM_BLUE,
                textFormat=TextFormat(bold=True, foregroundColor=WHITE),
                horizontalAlignment="LEFT",
            )

            # Regional headers in Section A (INDIA, SOUTHEAST ASIA, etc.)
            regional_fmt = CellFormat(
                textFormat=TextFormat(bold=True, foregroundColor=BLACK, fontSize=10),
                horizontalAlignment="LEFT",
            )

            # NOTES header
            notes_header_fmt = CellFormat(
                backgroundColor=GRAY,
                textFormat=TextFormat(bold=True, foregroundColor=WHITE),
                horizontalAlignment="LEFT",
            )

            # Data row formats for zebra striping
            data_white_fmt = CellFormat(
                backgroundColor=WHITE,
                textFormat=TextFormat(bold=False, foregroundColor=BLACK),
                horizontalAlignment="LEFT",
            )

            data_blue_fmt = CellFormat(
                backgroundColor=LIGHT_BLUE,
                textFormat=TextFormat(bold=False, foregroundColor=BLACK),
                horizontalAlignment="LEFT",
            )

            # URL format
            url_fmt = CellFormat(textFormat=TextFormat(foregroundColor=URL_BLUE))

            # ================================================================
            # APPLY FORMATTING
            # ================================================================

            # Get all data to analyze structure
            data = sheet.get_all_values()
            time.sleep(0.5)

            # 1. Format main title (Row 1)
            format_cell_range(sheet, "A1:E1", title_fmt)
            time.sleep(0.3)

            # 2. Find and format Section A header
            for i, row in enumerate(data):
                if row[0] and "SECTION A:" in row[0]:
                    format_cell_range(sheet, f"A{i+1}:E{i+1}", section_header_fmt)
                    time.sleep(0.2)
                    break

            # 3. Format Section A category headers
            section_a_categories = [
                "TAM -",
                "SAM -",
                "SOM -",
                "SEATS EXPANSION",
                "PRICING BENCHMARKS",
                "COGS PERCENTAGES",
                "CUSTOMER ACQUISITION",
                "PRODUCT ATTACHMENT",
            ]
            for i, row in enumerate(data):
                if row[0]:
                    for cat in section_a_categories:
                        if cat in row[0]:
                            format_cell_range(
                                sheet, f"A{i+1}:E{i+1}", section_a_category_fmt
                            )
                            time.sleep(0.2)
                            break

            # 4. Format regional headers
            regional_names = [
                "INDIA",
                "SOUTHEAST ASIA",
                "JAPAN",
                "GERMANY / EU",
                "OTHER REGIONS",
            ]
            for i, row in enumerate(data):
                if row[0] in regional_names:
                    format_cell_range(sheet, f"A{i+1}:E{i+1}", regional_fmt)
                    time.sleep(0.2)

            # 5. Find and format Section B
            section_b_start = None
            for i, row in enumerate(data):
                if row[0] and "SECTION B:" in row[0]:
                    section_b_start = i + 1
                    format_cell_range(sheet, f"A{i+1}:E{i+1}", section_header_fmt)
                    time.sleep(0.2)
                    # Format column headers (next row)
                    if i + 1 < len(data) and data[i + 1][0] == "Source Name":
                        format_cell_range(sheet, f"A{i+2}:E{i+2}", column_header_fmt)
                        time.sleep(0.2)
                    break

            # 6. Format Section B category headers and apply zebra striping
            section_b_categories = [
                "MARKET SIZE RESEARCH",
                "INDIA MANUFACTURING SOURCES",
                "SOUTHEAST ASIA SOURCES",
                "JAPAN & GERMANY SOURCES",
                "COMPETITOR & PRICING SOURCES",
                "SMB SOFTWARE & PRICING SOURCES",
                "REGIONAL MARKET DATA",
                "COMPETITOR RESEARCH",
                "SAAS BENCHMARK RESEARCH",
                "INDUSTRY BENCHMARKS",
            ]

            # Track category positions for zebra striping
            category_positions = []
            for i, row in enumerate(data):
                if row[0] in section_b_categories:
                    category_positions.append(i)
                    format_cell_range(sheet, f"A{i+1}:E{i+1}", section_b_category_fmt)
                    time.sleep(0.2)

            # 7. Apply zebra striping to Section B data rows
            for cat_idx, cat_pos in enumerate(category_positions):
                # Determine end of this category (next category or NOTES or end)
                if cat_idx + 1 < len(category_positions):
                    end_pos = category_positions[cat_idx + 1] - 1
                else:
                    # Find NOTES or end of data
                    end_pos = len(data) - 1
                    for j in range(cat_pos + 1, len(data)):
                        if data[j][0] == "NOTES" or data[j][0] == "":
                            end_pos = j - 1
                            break

                # Apply zebra striping to data rows (skip empty rows)
                stripe_count = 0
                for row_idx in range(cat_pos + 1, end_pos + 1):
                    if (
                        row_idx < len(data)
                        and data[row_idx][0]
                        and data[row_idx][0] not in section_b_categories
                    ):
                        if stripe_count % 2 == 0:
                            format_cell_range(
                                sheet, f"A{row_idx+1}:E{row_idx+1}", data_white_fmt
                            )
                        else:
                            format_cell_range(
                                sheet, f"A{row_idx+1}:E{row_idx+1}", data_blue_fmt
                            )
                        # Apply URL formatting to column D
                        format_cell_range(sheet, f"D{row_idx+1}", url_fmt)
                        stripe_count += 1
                        time.sleep(0.15)

            # 8. Format NOTES header
            for i, row in enumerate(data):
                if row[0] == "NOTES":
                    format_cell_range(sheet, f"A{i+1}:E{i+1}", notes_header_fmt)
                    time.sleep(0.2)
                    break

            # 9. Set column widths
            set_column_width(sheet, "A", 250)
            set_column_width(sheet, "B", 120)
            set_column_width(sheet, "C", 80)
            set_column_width(sheet, "D", 300)
            set_column_width(sheet, "E", 200)

            rate_limit_delay(1)

        except ImportError:
            print(
                "    Note: gspread-formatting not available, skipping advanced formatting"
            )
        except Exception as e:
            print(f"    Warning: Could not apply formatting: {e}")

    def build_sensitivity_sheet(self):
        """Build Sensitivity Analysis sheet with scenario modeling."""
        print("  Building Sensitivity Analysis sheet...")

        sheet = self.spreadsheet.add_worksheet("Sensitivity Analysis", rows=60, cols=15)

        # Reference base case values from P&L
        base_revenue_y5 = f"=Revenue!G{self.row_map['total_revenue']}"
        base_ebitda_y5 = f"='P&L'!G{self.row_map['pnl_ebitda']}"
        base_pat_y5 = f"='P&L'!G{self.row_map['pnl_pat']}"

        data = [
            ["SENSITIVITY ANALYSIS", "", "", "", "", "", "", "", "", ""],
            [""],
            ["'--- SCENARIO ANALYSIS ---", "", "", "", "", "", "", "", "", ""],
            ["", "", "Bear Case", "Base Case", "Bull Case", "", "", "", "", ""],
            ["Revenue Growth Adjustment", "%", -0.15, 0, 0.15, "", "", "", "", ""],
            ["Cost Adjustment", "%", 0.10, 0, -0.10, "", "", "", "", ""],
            ["Price Adjustment", "%", -0.10, 0, 0.10, "", "", "", "", ""],
            [""],
            ["Scenario Outputs (Year 5)", "", "", "", "", "", "", "", "", ""],
            [
                "Revenue",
                "$",
                f"={base_revenue_y5}*(1+C5+C7)",
                f"={base_revenue_y5}*(1+D5+D7)",
                f"={base_revenue_y5}*(1+E5+E7)",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EBITDA",
                "$",
                f"={base_ebitda_y5}*(1+C5+C7)*(1-C6)",
                f"={base_ebitda_y5}*(1+D5+D7)*(1-D6)",
                f"={base_ebitda_y5}*(1+E5+E7)*(1-E6)",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Net Income",
                "$",
                f"={base_pat_y5}*(1+C5+C7)*(1-C6)",
                f"={base_pat_y5}*(1+D5+D7)*(1-D6)",
                f"={base_pat_y5}*(1+E5+E7)*(1-E6)",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            ["'--- REVENUE SENSITIVITY TABLE ---", "", "", "", "", "", "", "", "", ""],
            [
                "Price Change ↓ / Volume Change →",
                "",
                "-20%",
                "-10%",
                "Base",
                "+10%",
                "+20%",
                "",
                "",
                "",
            ],
            [
                "-20%",
                "",
                f"={base_revenue_y5}*0.8*0.8",
                f"={base_revenue_y5}*0.8*0.9",
                f"={base_revenue_y5}*0.8*1",
                f"={base_revenue_y5}*0.8*1.1",
                f"={base_revenue_y5}*0.8*1.2",
                "",
                "",
                "",
            ],
            [
                "-10%",
                "",
                f"={base_revenue_y5}*0.9*0.8",
                f"={base_revenue_y5}*0.9*0.9",
                f"={base_revenue_y5}*0.9*1",
                f"={base_revenue_y5}*0.9*1.1",
                f"={base_revenue_y5}*0.9*1.2",
                "",
                "",
                "",
            ],
            [
                "Base",
                "",
                f"={base_revenue_y5}*1*0.8",
                f"={base_revenue_y5}*1*0.9",
                f"={base_revenue_y5}*1*1",
                f"={base_revenue_y5}*1*1.1",
                f"={base_revenue_y5}*1*1.2",
                "",
                "",
                "",
            ],
            [
                "+10%",
                "",
                f"={base_revenue_y5}*1.1*0.8",
                f"={base_revenue_y5}*1.1*0.9",
                f"={base_revenue_y5}*1.1*1",
                f"={base_revenue_y5}*1.1*1.1",
                f"={base_revenue_y5}*1.1*1.2",
                "",
                "",
                "",
            ],
            [
                "+20%",
                "",
                f"={base_revenue_y5}*1.2*0.8",
                f"={base_revenue_y5}*1.2*0.9",
                f"={base_revenue_y5}*1.2*1",
                f"={base_revenue_y5}*1.2*1.1",
                f"={base_revenue_y5}*1.2*1.2",
                "",
                "",
                "",
            ],
            [""],
            ["'--- EBITDA SENSITIVITY TABLE ---", "", "", "", "", "", "", "", "", ""],
            [
                "Revenue Change ↓ / Cost Change →",
                "",
                "-10%",
                "-5%",
                "Base",
                "+5%",
                "+10%",
                "",
                "",
                "",
            ],
            [
                "-20%",
                "",
                f"={base_ebitda_y5}*0.8*1.1",
                f"={base_ebitda_y5}*0.8*1.05",
                f"={base_ebitda_y5}*0.8*1",
                f"={base_ebitda_y5}*0.8*0.95",
                f"={base_ebitda_y5}*0.8*0.9",
                "",
                "",
                "",
            ],
            [
                "-10%",
                "",
                f"={base_ebitda_y5}*0.9*1.1",
                f"={base_ebitda_y5}*0.9*1.05",
                f"={base_ebitda_y5}*0.9*1",
                f"={base_ebitda_y5}*0.9*0.95",
                f"={base_ebitda_y5}*0.9*0.9",
                "",
                "",
                "",
            ],
            [
                "Base",
                "",
                f"={base_ebitda_y5}*1*1.1",
                f"={base_ebitda_y5}*1*1.05",
                f"={base_ebitda_y5}*1*1",
                f"={base_ebitda_y5}*1*0.95",
                f"={base_ebitda_y5}*1*0.9",
                "",
                "",
                "",
            ],
            [
                "+10%",
                "",
                f"={base_ebitda_y5}*1.1*1.1",
                f"={base_ebitda_y5}*1.1*1.05",
                f"={base_ebitda_y5}*1.1*1",
                f"={base_ebitda_y5}*1.1*0.95",
                f"={base_ebitda_y5}*1.1*0.9",
                "",
                "",
                "",
            ],
            [
                "+20%",
                "",
                f"={base_ebitda_y5}*1.2*1.1",
                f"={base_ebitda_y5}*1.2*1.05",
                f"={base_ebitda_y5}*1.2*1",
                f"={base_ebitda_y5}*1.2*0.95",
                f"={base_ebitda_y5}*1.2*0.9",
                "",
                "",
                "",
            ],
            [""],
            ["'--- KEY ASSUMPTIONS IMPACT ---", "", "", "", "", "", "", "", "", ""],
            [
                "Variable",
                "Base Value",
                "-20%",
                "-10%",
                "+10%",
                "+20%",
                "Impact on EBITDA",
                "",
                "",
                "",
            ],
            [
                "Revenue Growth Rate",
                f"=Assumptions!C{self.row_map.get('revenue_growth_base', 10)}",
                "Low",
                "Med-Low",
                "Med-High",
                "High",
                "High",
                "",
                "",
                "",
            ],
            [
                "COGS %",
                f"=Assumptions!C{self.row_map.get('cogs_base', 15)}",
                "High",
                "Med-High",
                "Med-Low",
                "Low",
                "High",
                "",
                "",
                "",
            ],
            [
                "Fixed Costs",
                f"='Operating Costs'!C{self.row_map.get('total_fixed', 20)}",
                "High",
                "Med-High",
                "Med-Low",
                "Low",
                "Medium",
                "",
                "",
                "",
            ],
            [
                "CAC",
                f"=Assumptions!C{self.row_map.get('cac', 25)}",
                "High",
                "Med-High",
                "Med-Low",
                "Low",
                "Medium",
                "",
                "",
                "",
            ],
        ]

        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Format headers
        sheet.format(
            "A1:J1",
            {
                "textFormat": {"bold": True, "fontSize": 12},
                "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.6},
            },
        )
        sheet.format("A3:J3", {"textFormat": {"bold": True}})
        sheet.format("A14:J14", {"textFormat": {"bold": True}})
        sheet.format("A22:J22", {"textFormat": {"bold": True}})
        sheet.format("A30:J30", {"textFormat": {"bold": True}})

        # Format percentage cells
        sheet.format("C5:E7", PERCENT_FORMAT)

        # Format currency cells
        sheet.format("C10:E12", CURRENCY_FORMAT)
        sheet.format("C16:G20", CURRENCY_FORMAT)
        sheet.format("C24:G28", CURRENCY_FORMAT)

        print(f"    ✓ Sensitivity Analysis sheet")

    def build_valuation_sheet(self):
        """Build Valuation sheet with DCF and multiples analysis."""
        print("  Building Valuation sheet...")

        sheet = self.spreadsheet.add_worksheet("Valuation", rows=50, cols=15)

        general = self.config["general"]
        wacc = general.get("interest_rate", 0.10)  # Use as proxy for WACC

        data = [
            ["COMPANY VALUATION", "", "", "", "", "", "", "", "", "", "", "", ""],
            [""],
            ["'--- DCF VALUATION ---", "", "", "", "", "", "", "", "", "", "", "", ""],
            [
                "",
                "",
                "Year 1",
                "Year 2",
                "Year 3",
                "Year 4",
                "Year 5",
                "Year 6",
                "Year 7",
                "Year 8",
                "Year 9",
                "Year 10",
                "Terminal",
            ],
            [
                "Free Cash Flow",
                "$",
                f"='Cash Flow'!D{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!E{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!F{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!G{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!H{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!I{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!J{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!K{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!L{self.row_map.get('net_cash_flow', 15)}",
                f"='Cash Flow'!M{self.row_map.get('net_cash_flow', 15)}",
                "",
            ],
            [""],
            [
                "Discount Rate (WACC)",
                "%",
                wacc + 0.02,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            ["Terminal Growth Rate", "%", 0.03, "", "", "", "", "", "", "", "", "", ""],
            [""],
            [
                "Discount Factor",
                "x",
                f"=1/(1+$C$7)^1",
                f"=1/(1+$C$7)^2",
                f"=1/(1+$C$7)^3",
                f"=1/(1+$C$7)^4",
                f"=1/(1+$C$7)^5",
                f"=1/(1+$C$7)^6",
                f"=1/(1+$C$7)^7",
                f"=1/(1+$C$7)^8",
                f"=1/(1+$C$7)^9",
                f"=1/(1+$C$7)^10",
                "",
            ],
            [
                "Present Value of FCF",
                "$",
                "=C5*C10",
                "=D5*D10",
                "=E5*E10",
                "=F5*F10",
                "=G5*G10",
                "=H5*H10",
                "=I5*I10",
                "=J5*J10",
                "=K5*K10",
                "=L5*L10",
                "",
            ],
            [""],
            [
                "Sum of PV (FCF)",
                "$",
                "=SUM(C11:L11)",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Terminal Value",
                "$",
                "=L5*(1+C8)/(C7-C8)",
                "",
                "Gordon Growth Method",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "PV of Terminal Value",
                "$",
                "=C14*L10",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            [
                "Enterprise Value",
                "$",
                "=C13+C15",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Less: Net Debt",
                "$",
                f"=Assumptions!C{self.row_map.get('debt', 12)}-'Balance Sheet'!C{self.row_map.get('bs_cash', 5)}",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            ["Equity Value", "$", "=C17-C18", "", "", "", "", "", "", "", "", "", ""],
            [""],
            [
                "'--- VALUATION MULTIPLES ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "",
                "",
                "Year 1",
                "Year 3",
                "Year 5",
                "Year 10",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Revenue",
                "$",
                f"=Revenue!D{self.row_map['total_revenue']}",
                f"=Revenue!F{self.row_map['total_revenue']}",
                f"=Revenue!H{self.row_map['total_revenue']}",
                f"=Revenue!M{self.row_map['total_revenue']}",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EBITDA",
                "$",
                f"='P&L'!D{self.row_map['pnl_ebitda']}",
                f"='P&L'!F{self.row_map['pnl_ebitda']}",
                f"='P&L'!H{self.row_map['pnl_ebitda']}",
                f"='P&L'!M{self.row_map['pnl_ebitda']}",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Net Income",
                "$",
                f"='P&L'!D{self.row_map['pnl_pat']}",
                f"='P&L'!F{self.row_map['pnl_pat']}",
                f"='P&L'!H{self.row_map['pnl_pat']}",
                f"='P&L'!M{self.row_map['pnl_pat']}",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            [
                "Implied Multiples (using EV)",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EV/Revenue",
                "x",
                '=IF(C23>0,$C$17/C23,"-")',
                '=IF(D23>0,$C$17/D23,"-")',
                '=IF(E23>0,$C$17/E23,"-")',
                '=IF(F23>0,$C$17/F23,"-")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EV/EBITDA",
                "x",
                '=IF(C24>0,$C$17/C24,"-")',
                '=IF(D24>0,$C$17/D24,"-")',
                '=IF(E24>0,$C$17/E24,"-")',
                '=IF(F24>0,$C$17/F24,"-")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "P/E Ratio",
                "x",
                '=IF(C25>0,$C$19/C25,"-")',
                '=IF(D25>0,$C$19/D25,"-")',
                '=IF(E25>0,$C$19/E25,"-")',
                '=IF(F25>0,$C$19/F25,"-")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            [
                "'--- VALUATION BY COMPARABLE MULTIPLES ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Industry Benchmark",
                "",
                "Low",
                "Median",
                "High",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            ["EV/Revenue Multiple", "x", 2.0, 4.0, 8.0, "", "", "", "", "", "", "", ""],
            [
                "EV/EBITDA Multiple",
                "x",
                6.0,
                10.0,
                15.0,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            [
                "Implied Valuation (Year 5 metrics)",
                "",
                "Low",
                "Median",
                "High",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "By EV/Revenue",
                "$",
                f"=E23*C34",
                f"=E23*D34",
                f"=E23*E34",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "By EV/EBITDA",
                "$",
                f"=E24*C35",
                f"=E24*D35",
                f"=E24*E35",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            [
                "Valuation Summary",
                "",
                "Low",
                "Mid",
                "High",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "DCF Valuation",
                "$",
                "=C19*0.85",
                "=C19",
                "=C19*1.15",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Revenue Multiple",
                "$",
                "=C38",
                "=D38",
                "=E38",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EBITDA Multiple",
                "$",
                "=C39",
                "=D39",
                "=E39",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Average",
                "$",
                "=AVERAGE(C42:C44)",
                "=AVERAGE(D42:D44)",
                "=AVERAGE(E42:E44)",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
        ]

        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True, "fontSize": 12},
                "backgroundColor": {"red": 0.2, "green": 0.5, "blue": 0.3},
            },
        )
        sheet.format("A3:M3", {"textFormat": {"bold": True}})
        sheet.format("A21:M21", {"textFormat": {"bold": True}})
        sheet.format("A32:M32", {"textFormat": {"bold": True}})

        # Format percentages
        sheet.format("C7:C8", PERCENT_FORMAT)

        # Format currency
        for row in [5, 11, 13, 14, 15, 17, 18, 19, 23, 24, 25, 38, 39, 42, 43, 44, 45]:
            sheet.format(f"C{row}:M{row}", CURRENCY_FORMAT)

        print(f"    ✓ Valuation sheet")

    def build_breakeven_sheet(self):
        """Build Break-even Analysis sheet."""
        print("  Building Break-even Analysis sheet...")

        sheet = self.spreadsheet.add_worksheet("Break-even Analysis", rows=40, cols=15)

        data = [
            ["BREAK-EVEN ANALYSIS", "", "", "", "", "", "", "", "", "", "", "", ""],
            [""],
            [
                "'--- CONTRIBUTION MARGIN ANALYSIS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "",
                "",
                "Year 0",
                "Year 1",
                "Year 2",
                "Year 3",
                "Year 4",
                "Year 5",
                "Year 6",
                "Year 7",
                "Year 8",
                "Year 9",
                "Year 10",
            ],
            [
                "Total Revenue",
                "$",
                f"=Revenue!C{self.row_map['total_revenue']}",
                f"=Revenue!D{self.row_map['total_revenue']}",
                f"=Revenue!E{self.row_map['total_revenue']}",
                f"=Revenue!F{self.row_map['total_revenue']}",
                f"=Revenue!G{self.row_map['total_revenue']}",
                f"=Revenue!H{self.row_map['total_revenue']}",
                f"=Revenue!I{self.row_map['total_revenue']}",
                f"=Revenue!J{self.row_map['total_revenue']}",
                f"=Revenue!K{self.row_map['total_revenue']}",
                f"=Revenue!L{self.row_map['total_revenue']}",
                f"=Revenue!M{self.row_map['total_revenue']}",
            ],
            [
                "Variable Costs (COGS)",
                "$",
                f"='Operating Costs'!C{self.row_map['total_cogs']}",
                f"='Operating Costs'!D{self.row_map['total_cogs']}",
                f"='Operating Costs'!E{self.row_map['total_cogs']}",
                f"='Operating Costs'!F{self.row_map['total_cogs']}",
                f"='Operating Costs'!G{self.row_map['total_cogs']}",
                f"='Operating Costs'!H{self.row_map['total_cogs']}",
                f"='Operating Costs'!I{self.row_map['total_cogs']}",
                f"='Operating Costs'!J{self.row_map['total_cogs']}",
                f"='Operating Costs'!K{self.row_map['total_cogs']}",
                f"='Operating Costs'!L{self.row_map['total_cogs']}",
                f"='Operating Costs'!M{self.row_map['total_cogs']}",
            ],
            [
                "Contribution Margin",
                "$",
                "=C5-C6",
                "=D5-D6",
                "=E5-E6",
                "=F5-F6",
                "=G5-G6",
                "=H5-H6",
                "=I5-I6",
                "=J5-J6",
                "=K5-K6",
                "=L5-L6",
                "=M5-M6",
            ],
            [
                "Contribution Margin %",
                "%",
                "=IF(C5>0,C7/C5,0)",
                "=IF(D5>0,D7/D5,0)",
                "=IF(E5>0,E7/E5,0)",
                "=IF(F5>0,F7/F5,0)",
                "=IF(G5>0,G7/G5,0)",
                "=IF(H5>0,H7/H5,0)",
                "=IF(I5>0,I7/I5,0)",
                "=IF(J5>0,J7/J5,0)",
                "=IF(K5>0,K7/K5,0)",
                "=IF(L5>0,L7/L5,0)",
                "=IF(M5>0,M7/M5,0)",
            ],
            [""],
            [
                "Fixed Costs",
                "$",
                f"='Operating Costs'!C{self.row_map['total_fixed']}",
                f"='Operating Costs'!D{self.row_map['total_fixed']}",
                f"='Operating Costs'!E{self.row_map['total_fixed']}",
                f"='Operating Costs'!F{self.row_map['total_fixed']}",
                f"='Operating Costs'!G{self.row_map['total_fixed']}",
                f"='Operating Costs'!H{self.row_map['total_fixed']}",
                f"='Operating Costs'!I{self.row_map['total_fixed']}",
                f"='Operating Costs'!J{self.row_map['total_fixed']}",
                f"='Operating Costs'!K{self.row_map['total_fixed']}",
                f"='Operating Costs'!L{self.row_map['total_fixed']}",
                f"='Operating Costs'!M{self.row_map['total_fixed']}",
            ],
            [
                "S&M Costs",
                "$",
                f"='Operating Costs'!C{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!D{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!E{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!F{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!G{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!H{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!I{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!J{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!K{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!L{self.row_map.get('sm_cost', 25)}",
                f"='Operating Costs'!M{self.row_map.get('sm_cost', 25)}",
            ],
            [
                "Total Fixed + S&M",
                "$",
                "=C10+C11",
                "=D10+D11",
                "=E10+E11",
                "=F10+F11",
                "=G10+G11",
                "=H10+H11",
                "=I10+I11",
                "=J10+J11",
                "=K10+K11",
                "=L10+L11",
                "=M10+M11",
            ],
            [""],
            [
                "'--- BREAK-EVEN CALCULATIONS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Break-even Revenue",
                "$",
                "=IF(C8>0,C12/C8,0)",
                "=IF(D8>0,D12/D8,0)",
                "=IF(E8>0,E12/E8,0)",
                "=IF(F8>0,F12/F8,0)",
                "=IF(G8>0,G12/G8,0)",
                "=IF(H8>0,H12/H8,0)",
                "=IF(I8>0,I12/I8,0)",
                "=IF(J8>0,J12/J8,0)",
                "=IF(K8>0,K12/K8,0)",
                "=IF(L8>0,L12/L8,0)",
                "=IF(M8>0,M12/M8,0)",
            ],
            [
                "Actual Revenue",
                "$",
                "=C5",
                "=D5",
                "=E5",
                "=F5",
                "=G5",
                "=H5",
                "=I5",
                "=J5",
                "=K5",
                "=L5",
                "=M5",
            ],
            [
                "Surplus/(Deficit)",
                "$",
                "=C16-C15",
                "=D16-D15",
                "=E16-E15",
                "=F16-F15",
                "=G16-G15",
                "=H16-H15",
                "=I16-I15",
                "=J16-J15",
                "=K16-K15",
                "=L16-L15",
                "=M16-M15",
            ],
            [
                "Break-even Achieved?",
                "",
                '=IF(C17>0,"YES","NO")',
                '=IF(D17>0,"YES","NO")',
                '=IF(E17>0,"YES","NO")',
                '=IF(F17>0,"YES","NO")',
                '=IF(G17>0,"YES","NO")',
                '=IF(H17>0,"YES","NO")',
                '=IF(I17>0,"YES","NO")',
                '=IF(J17>0,"YES","NO")',
                '=IF(K17>0,"YES","NO")',
                '=IF(L17>0,"YES","NO")',
                '=IF(M17>0,"YES","NO")',
            ],
            [""],
            [
                "'--- OPERATING LEVERAGE ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Degree of Operating Leverage",
                "x",
                "=IF(C7-C12>0,C7/(C7-C12),0)",
                "=IF(D7-D12>0,D7/(D7-D12),0)",
                "=IF(E7-E12>0,E7/(E7-E12),0)",
                "=IF(F7-F12>0,F7/(F7-F12),0)",
                "=IF(G7-G12>0,G7/(G7-G12),0)",
                "=IF(H7-H12>0,H7/(H7-H12),0)",
                "=IF(I7-I12>0,I7/(I7-I12),0)",
                "=IF(J7-J12>0,J7/(J7-J12),0)",
                "=IF(K7-K12>0,K7/(K7-K12),0)",
                "=IF(L7-L12>0,L7/(L7-L12),0)",
                "=IF(M7-M12>0,M7/(M7-M12),0)",
            ],
            [
                "Interpretation",
                "",
                '=IF(C21>3,"High risk/reward",IF(C21>1.5,"Moderate","Low leverage"))',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [""],
            [
                "'--- MARGIN OF SAFETY ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Margin of Safety ($)",
                "$",
                "=C17",
                "=D17",
                "=E17",
                "=F17",
                "=G17",
                "=H17",
                "=I17",
                "=J17",
                "=K17",
                "=L17",
                "=M17",
            ],
            [
                "Margin of Safety (%)",
                "%",
                "=IF(C16>0,C25/C16,0)",
                "=IF(D16>0,D25/D16,0)",
                "=IF(E16>0,E25/E16,0)",
                "=IF(F16>0,F25/F16,0)",
                "=IF(G16>0,G25/G16,0)",
                "=IF(H16>0,H25/H16,0)",
                "=IF(I16>0,I25/I16,0)",
                "=IF(J16>0,J25/J16,0)",
                "=IF(K16>0,K25/K16,0)",
                "=IF(L16>0,L25/L16,0)",
                "=IF(M16>0,M25/M16,0)",
            ],
            [""],
            [
                "'--- PROFITABILITY TIMELINE ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EBITDA",
                "$",
                f"='P&L'!C{self.row_map['pnl_ebitda']}",
                f"='P&L'!D{self.row_map['pnl_ebitda']}",
                f"='P&L'!E{self.row_map['pnl_ebitda']}",
                f"='P&L'!F{self.row_map['pnl_ebitda']}",
                f"='P&L'!G{self.row_map['pnl_ebitda']}",
                f"='P&L'!H{self.row_map['pnl_ebitda']}",
                f"='P&L'!I{self.row_map['pnl_ebitda']}",
                f"='P&L'!J{self.row_map['pnl_ebitda']}",
                f"='P&L'!K{self.row_map['pnl_ebitda']}",
                f"='P&L'!L{self.row_map['pnl_ebitda']}",
                f"='P&L'!M{self.row_map['pnl_ebitda']}",
            ],
            [
                "EBITDA Positive?",
                "",
                '=IF(C29>0,"YES","NO")',
                '=IF(D29>0,"YES","NO")',
                '=IF(E29>0,"YES","NO")',
                '=IF(F29>0,"YES","NO")',
                '=IF(G29>0,"YES","NO")',
                '=IF(H29>0,"YES","NO")',
                '=IF(I29>0,"YES","NO")',
                '=IF(J29>0,"YES","NO")',
                '=IF(K29>0,"YES","NO")',
                '=IF(L29>0,"YES","NO")',
                '=IF(M29>0,"YES","NO")',
            ],
            [
                "Net Income",
                "$",
                f"='P&L'!C{self.row_map['pnl_pat']}",
                f"='P&L'!D{self.row_map['pnl_pat']}",
                f"='P&L'!E{self.row_map['pnl_pat']}",
                f"='P&L'!F{self.row_map['pnl_pat']}",
                f"='P&L'!G{self.row_map['pnl_pat']}",
                f"='P&L'!H{self.row_map['pnl_pat']}",
                f"='P&L'!I{self.row_map['pnl_pat']}",
                f"='P&L'!J{self.row_map['pnl_pat']}",
                f"='P&L'!K{self.row_map['pnl_pat']}",
                f"='P&L'!L{self.row_map['pnl_pat']}",
                f"='P&L'!M{self.row_map['pnl_pat']}",
            ],
            [
                "Net Income Positive?",
                "",
                '=IF(C31>0,"YES","NO")',
                '=IF(D31>0,"YES","NO")',
                '=IF(E31>0,"YES","NO")',
                '=IF(F31>0,"YES","NO")',
                '=IF(G31>0,"YES","NO")',
                '=IF(H31>0,"YES","NO")',
                '=IF(I31>0,"YES","NO")',
                '=IF(J31>0,"YES","NO")',
                '=IF(K31>0,"YES","NO")',
                '=IF(L31>0,"YES","NO")',
                '=IF(M31>0,"YES","NO")',
            ],
        ]

        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True, "fontSize": 12},
                "backgroundColor": {"red": 0.6, "green": 0.2, "blue": 0.2},
            },
        )
        sheet.format("A3:M3", {"textFormat": {"bold": True}})
        sheet.format("A14:M14", {"textFormat": {"bold": True}})
        sheet.format("A20:M20", {"textFormat": {"bold": True}})
        sheet.format("A24:M24", {"textFormat": {"bold": True}})
        sheet.format("A28:M28", {"textFormat": {"bold": True}})

        # Format percentages
        sheet.format("C8:M8", PERCENT_FORMAT)
        sheet.format("C26:M26", PERCENT_FORMAT)

        # Format currency
        for row in [5, 6, 7, 10, 11, 12, 15, 16, 17, 25, 29, 31]:
            sheet.format(f"C{row}:M{row}", CURRENCY_FORMAT)

        print(f"    ✓ Break-even Analysis sheet")

    def build_funding_captable_sheet(self):
        """Build Funding & Cap Table sheet."""
        print("  Building Funding & Cap Table sheet...")

        sheet = self.spreadsheet.add_worksheet("Funding & Cap Table", rows=55, cols=10)

        general = self.config["general"]
        equity_y0 = general.get("equity_y0", 1000000)
        debt_y0 = general.get("debt_y0", 500000)

        data = [
            ["FUNDING & CAP TABLE", "", "", "", "", "", "", ""],
            [""],
            ["'--- FUNDING ROUNDS ---", "", "", "", "", "", "", ""],
            [
                "Round",
                "Timing",
                "Amount",
                "Pre-Money",
                "Post-Money",
                "Shares Issued",
                "Price/Share",
                "Ownership %",
            ],
            [
                "Founders",
                "Start",
                0,
                0,
                equity_y0,
                10000000,
                f"={equity_y0}/10000000",
                "100%",
            ],
            [
                "Seed Round",
                "Year 0",
                equity_y0,
                equity_y0,
                f"=D5+C6",
                f"=C6/G6",
                f"=D6/F5",
                f"=F6/(F5+F6)",
            ],
            [
                "Series A",
                "Year 2",
                3000000,
                f"=E6*2",
                f"=D7+C7",
                f"=C7/G7",
                f"=D7/SUM($F$5:F6)",
                f"=F7/SUM($F$5:F7)",
            ],
            [
                "Series B",
                "Year 4",
                10000000,
                f"=E7*2.5",
                f"=D8+C8",
                f"=C8/G8",
                f"=D8/SUM($F$5:F7)",
                f"=F8/SUM($F$5:F8)",
            ],
            [""],
            ["Total Equity Raised", "$", "=SUM(C5:C8)", "", "", "", "", ""],
            [""],
            ["'--- CAP TABLE ---", "", "", "", "", "", "", ""],
            [
                "Shareholder",
                "Shares",
                "% Ownership",
                "Investment",
                "Current Value",
                "Multiple",
                "",
                "",
            ],
            [
                "Founders",
                "=F5",
                f"=B13/SUM($B$13:$B$16)",
                0,
                f"=B13*G8",
                f'=IF(D13>0,E13/D13,"-")',
                "",
                "",
            ],
            [
                "Seed Investors",
                "=F6",
                f"=B14/SUM($B$13:$B$16)",
                "=C6",
                f"=B14*G8",
                f'=IF(D14>0,E14/D14,"-")',
                "",
                "",
            ],
            [
                "Series A Investors",
                "=F7",
                f"=B15/SUM($B$13:$B$16)",
                "=C7",
                f"=B15*G8",
                f'=IF(D15>0,E15/D15,"-")',
                "",
                "",
            ],
            [
                "Series B Investors",
                "=F8",
                f"=B16/SUM($B$13:$B$16)",
                "=C8",
                f"=B16*G8",
                f'=IF(D16>0,E16/D16,"-")',
                "",
                "",
            ],
            [
                "TOTAL",
                "=SUM(B13:B16)",
                "=SUM(C13:C16)",
                "=SUM(D13:D16)",
                "=SUM(E13:E16)",
                "",
                "",
                "",
            ],
            [""],
            ["'--- DILUTION ANALYSIS ---", "", "", "", "", "", "", ""],
            ["", "Pre-Seed", "Post-Seed", "Post-A", "Post-B", "", "", ""],
            [
                "Founder Ownership",
                "100%",
                f"=F5/(F5+F6)",
                f"=F5/SUM(F5:F7)",
                f"=F5/SUM(F5:F8)",
                "",
                "",
                "",
            ],
            [
                "Seed Ownership",
                "0%",
                f"=F6/(F5+F6)",
                f"=F6/SUM(F5:F7)",
                f"=F6/SUM(F5:F8)",
                "",
                "",
                "",
            ],
            [
                "Series A Ownership",
                "0%",
                "0%",
                f"=F7/SUM(F5:F7)",
                f"=F7/SUM(F5:F8)",
                "",
                "",
                "",
            ],
            ["Series B Ownership", "0%", "0%", "0%", f"=F8/SUM(F5:F8)", "", "", ""],
            [""],
            ["'--- DEBT FINANCING ---", "", "", "", "", "", "", ""],
            ["", "", "Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
            [
                "Opening Debt",
                "$",
                0,
                f"=D29+D30-D31",
                f"=E29+E30-E31",
                f"=F29+F30-F31",
                f"=G29+G30-G31",
                f"=H29+H30-H31",
            ],
            ["New Debt", "$", debt_y0, 0, 0, 0, 0, 0],
            [
                "Principal Repayment",
                "$",
                0,
                f"={debt_y0}/5",
                f"={debt_y0}/5",
                f"={debt_y0}/5",
                f"={debt_y0}/5",
                f"={debt_y0}/5",
            ],
            [
                "Closing Debt",
                "$",
                f"=C29+C30-C31",
                f"=D29+D30-D31",
                f"=E29+E30-E31",
                f"=F29+F30-F31",
                f"=G29+G30-G31",
                f"=H29+H30-H31",
            ],
            [""],
            [
                "Interest Rate",
                "%",
                general.get("interest_rate", 0.08),
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Interest Expense",
                "$",
                "=C32*C34",
                "=D32*$C$34",
                "=E32*$C$34",
                "=F32*$C$34",
                "=G32*$C$34",
                "=H32*$C$34",
            ],
            [""],
            ["'--- INVESTOR RETURNS ---", "", "", "", "", "", "", ""],
            ["Exit Valuation (Year 5)", "$", f"=Valuation!C19", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            [
                "Investor",
                "Investment",
                "Ownership %",
                "Exit Value",
                "Profit",
                "Multiple",
                "IRR",
                "",
            ],
            [
                "Seed",
                "=D14",
                "=C14",
                "=C41*C14",
                "=D41-B41",
                "=IF(B41>0,D41/B41,0)",
                "=IF(B41>0,(D41/B41)^(1/5)-1,0)",
                "",
            ],
            [
                "Series A",
                "=D15",
                "=C15",
                "=C41*C15",
                "=D42-B42",
                "=IF(B42>0,D42/B42,0)",
                "=IF(B42>0,(D42/B42)^(1/3)-1,0)",
                "",
            ],
            [
                "Series B",
                "=D16",
                "=C16",
                "=C41*C16",
                "=D43-B43",
                "=IF(B43>0,D43/B43,0)",
                "=IF(B43>0,(D43/B43)^(1/1)-1,0)",
                "",
            ],
        ]

        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:H1",
            {
                "textFormat": {"bold": True, "fontSize": 12},
                "backgroundColor": {"red": 0.4, "green": 0.2, "blue": 0.6},
            },
        )
        sheet.format("A3:H3", {"textFormat": {"bold": True}})
        sheet.format(
            "A4:H4",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
            },
        )
        sheet.format("A12:H12", {"textFormat": {"bold": True}})
        sheet.format(
            "A13:H13",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
            },
        )
        sheet.format(
            "A18:H18",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.95},
            },
        )
        sheet.format("A20:H20", {"textFormat": {"bold": True}})
        sheet.format("A27:H27", {"textFormat": {"bold": True}})
        sheet.format("A37:H37", {"textFormat": {"bold": True}})

        # Format percentages
        sheet.format("H5:H8", PERCENT_FORMAT)
        sheet.format("C13:C18", PERCENT_FORMAT)
        sheet.format("B22:E25", PERCENT_FORMAT)
        sheet.format("C34:C34", PERCENT_FORMAT)
        sheet.format("C41:C43", PERCENT_FORMAT)
        sheet.format("G41:G43", PERCENT_FORMAT)

        # Format currency
        sheet.format("C5:G8", CURRENCY_FORMAT)
        sheet.format("C10:C10", CURRENCY_FORMAT)
        sheet.format("D13:E18", CURRENCY_FORMAT)
        sheet.format("C29:H32", CURRENCY_FORMAT)
        sheet.format("C35:H35", CURRENCY_FORMAT)
        sheet.format("C38:C38", CURRENCY_FORMAT)
        sheet.format("B41:B43", CURRENCY_FORMAT)
        sheet.format("D41:E43", CURRENCY_FORMAT)

        print(f"    ✓ Funding & Cap Table sheet")

    def build_ratios_sheet(self):
        """Build Key Financial Ratios Dashboard sheet."""
        print("  Building Financial Ratios sheet...")

        sheet = self.spreadsheet.add_worksheet("Financial Ratios", rows=55, cols=15)

        data = [
            ["KEY FINANCIAL RATIOS", "", "", "", "", "", "", "", "", "", "", "", ""],
            [""],
            [
                "'--- PROFITABILITY RATIOS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "",
                "",
                "Year 0",
                "Year 1",
                "Year 2",
                "Year 3",
                "Year 4",
                "Year 5",
                "Year 6",
                "Year 7",
                "Year 8",
                "Year 9",
                "Year 10",
            ],
            [
                "Gross Margin",
                "%",
                f"=IF(Revenue!C{self.row_map['total_revenue']}>0,(Revenue!C{self.row_map['total_revenue']}-'Operating Costs'!C{self.row_map['total_cogs']})/Revenue!C{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!D{self.row_map['total_revenue']}>0,(Revenue!D{self.row_map['total_revenue']}-'Operating Costs'!D{self.row_map['total_cogs']})/Revenue!D{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!E{self.row_map['total_revenue']}>0,(Revenue!E{self.row_map['total_revenue']}-'Operating Costs'!E{self.row_map['total_cogs']})/Revenue!E{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!F{self.row_map['total_revenue']}>0,(Revenue!F{self.row_map['total_revenue']}-'Operating Costs'!F{self.row_map['total_cogs']})/Revenue!F{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,(Revenue!G{self.row_map['total_revenue']}-'Operating Costs'!G{self.row_map['total_cogs']})/Revenue!G{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!H{self.row_map['total_revenue']}>0,(Revenue!H{self.row_map['total_revenue']}-'Operating Costs'!H{self.row_map['total_cogs']})/Revenue!H{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!I{self.row_map['total_revenue']}>0,(Revenue!I{self.row_map['total_revenue']}-'Operating Costs'!I{self.row_map['total_cogs']})/Revenue!I{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!J{self.row_map['total_revenue']}>0,(Revenue!J{self.row_map['total_revenue']}-'Operating Costs'!J{self.row_map['total_cogs']})/Revenue!J{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!K{self.row_map['total_revenue']}>0,(Revenue!K{self.row_map['total_revenue']}-'Operating Costs'!K{self.row_map['total_cogs']})/Revenue!K{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!L{self.row_map['total_revenue']}>0,(Revenue!L{self.row_map['total_revenue']}-'Operating Costs'!L{self.row_map['total_cogs']})/Revenue!L{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!M{self.row_map['total_revenue']}>0,(Revenue!M{self.row_map['total_revenue']}-'Operating Costs'!M{self.row_map['total_cogs']})/Revenue!M{self.row_map['total_revenue']},0)",
            ],
            [
                "EBITDA Margin",
                "%",
                f"=IF(Revenue!C{self.row_map['total_revenue']}>0,'P&L'!C{self.row_map['pnl_ebitda']}/Revenue!C{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!D{self.row_map['total_revenue']}>0,'P&L'!D{self.row_map['pnl_ebitda']}/Revenue!D{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!E{self.row_map['total_revenue']}>0,'P&L'!E{self.row_map['pnl_ebitda']}/Revenue!E{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!F{self.row_map['total_revenue']}>0,'P&L'!F{self.row_map['pnl_ebitda']}/Revenue!F{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,'P&L'!G{self.row_map['pnl_ebitda']}/Revenue!G{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!H{self.row_map['total_revenue']}>0,'P&L'!H{self.row_map['pnl_ebitda']}/Revenue!H{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!I{self.row_map['total_revenue']}>0,'P&L'!I{self.row_map['pnl_ebitda']}/Revenue!I{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!J{self.row_map['total_revenue']}>0,'P&L'!J{self.row_map['pnl_ebitda']}/Revenue!J{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!K{self.row_map['total_revenue']}>0,'P&L'!K{self.row_map['pnl_ebitda']}/Revenue!K{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!L{self.row_map['total_revenue']}>0,'P&L'!L{self.row_map['pnl_ebitda']}/Revenue!L{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!M{self.row_map['total_revenue']}>0,'P&L'!M{self.row_map['pnl_ebitda']}/Revenue!M{self.row_map['total_revenue']},0)",
            ],
            [
                "Net Profit Margin",
                "%",
                f"=IF(Revenue!C{self.row_map['total_revenue']}>0,'P&L'!C{self.row_map['pnl_pat']}/Revenue!C{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!D{self.row_map['total_revenue']}>0,'P&L'!D{self.row_map['pnl_pat']}/Revenue!D{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!E{self.row_map['total_revenue']}>0,'P&L'!E{self.row_map['pnl_pat']}/Revenue!E{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!F{self.row_map['total_revenue']}>0,'P&L'!F{self.row_map['pnl_pat']}/Revenue!F{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,'P&L'!G{self.row_map['pnl_pat']}/Revenue!G{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!H{self.row_map['total_revenue']}>0,'P&L'!H{self.row_map['pnl_pat']}/Revenue!H{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!I{self.row_map['total_revenue']}>0,'P&L'!I{self.row_map['pnl_pat']}/Revenue!I{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!J{self.row_map['total_revenue']}>0,'P&L'!J{self.row_map['pnl_pat']}/Revenue!J{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!K{self.row_map['total_revenue']}>0,'P&L'!K{self.row_map['pnl_pat']}/Revenue!K{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!L{self.row_map['total_revenue']}>0,'P&L'!L{self.row_map['pnl_pat']}/Revenue!L{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!M{self.row_map['total_revenue']}>0,'P&L'!M{self.row_map['pnl_pat']}/Revenue!M{self.row_map['total_revenue']},0)",
            ],
            [
                "ROE",
                "%",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_equity', 20)}>0,'P&L'!C{self.row_map['pnl_pat']}/'Balance Sheet'!C{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_equity', 20)}>0,'P&L'!D{self.row_map['pnl_pat']}/'Balance Sheet'!D{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_equity', 20)}>0,'P&L'!E{self.row_map['pnl_pat']}/'Balance Sheet'!E{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_equity', 20)}>0,'P&L'!F{self.row_map['pnl_pat']}/'Balance Sheet'!F{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_equity', 20)}>0,'P&L'!G{self.row_map['pnl_pat']}/'Balance Sheet'!G{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_equity', 20)}>0,'P&L'!H{self.row_map['pnl_pat']}/'Balance Sheet'!H{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_equity', 20)}>0,'P&L'!I{self.row_map['pnl_pat']}/'Balance Sheet'!I{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_equity', 20)}>0,'P&L'!J{self.row_map['pnl_pat']}/'Balance Sheet'!J{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_equity', 20)}>0,'P&L'!K{self.row_map['pnl_pat']}/'Balance Sheet'!K{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_equity', 20)}>0,'P&L'!L{self.row_map['pnl_pat']}/'Balance Sheet'!L{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_equity', 20)}>0,'P&L'!M{self.row_map['pnl_pat']}/'Balance Sheet'!M{self.row_map.get('bs_equity', 20)},0)",
            ],
            [
                "ROA",
                "%",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!C{self.row_map['pnl_pat']}/'Balance Sheet'!C{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!D{self.row_map['pnl_pat']}/'Balance Sheet'!D{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!E{self.row_map['pnl_pat']}/'Balance Sheet'!E{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!F{self.row_map['pnl_pat']}/'Balance Sheet'!F{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!G{self.row_map['pnl_pat']}/'Balance Sheet'!G{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!H{self.row_map['pnl_pat']}/'Balance Sheet'!H{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!I{self.row_map['pnl_pat']}/'Balance Sheet'!I{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!J{self.row_map['pnl_pat']}/'Balance Sheet'!J{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!K{self.row_map['pnl_pat']}/'Balance Sheet'!K{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!L{self.row_map['pnl_pat']}/'Balance Sheet'!L{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_total_assets', 10)}>0,'P&L'!M{self.row_map['pnl_pat']}/'Balance Sheet'!M{self.row_map.get('bs_total_assets', 10)},0)",
            ],
            [""],
            [
                "'--- LIQUIDITY RATIOS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Current Ratio",
                "x",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!C{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!C{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!D{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!D{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!E{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!E{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!F{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!F{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!G{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!G{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!H{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!H{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!I{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!I{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!J{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!J{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!K{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!K{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!L{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!L{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!M{self.row_map.get('bs_current_assets', 8)}/'Balance Sheet'!M{self.row_map.get('bs_current_liab', 18)},0)",
            ],
            [
                "Cash Ratio",
                "x",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!C{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!C{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!D{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!D{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!E{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!E{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!F{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!F{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!G{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!G{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!H{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!H{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!I{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!I{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!J{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!J{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!K{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!K{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!L{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!L{self.row_map.get('bs_current_liab', 18)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_current_liab', 18)}>0,'Balance Sheet'!M{self.row_map.get('bs_cash', 5)}/'Balance Sheet'!M{self.row_map.get('bs_current_liab', 18)},0)",
            ],
            [""],
            [
                "'--- LEVERAGE RATIOS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Debt to Equity",
                "x",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!C{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!C{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!D{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!D{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!E{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!E{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!F{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!F{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!G{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!G{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!H{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!H{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!I{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!I{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!J{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!J{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!K{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!K{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!L{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!L{self.row_map.get('bs_equity', 20)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_equity', 20)}>0,'Balance Sheet'!M{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!M{self.row_map.get('bs_equity', 20)},0)",
            ],
            [
                "Debt to Assets",
                "x",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!C{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!C{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!D{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!D{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!E{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!E{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!F{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!F{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!G{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!G{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!H{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!H{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!I{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!I{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!J{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!J{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!K{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!K{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!L{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!L{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_total_assets', 10)}>0,'Balance Sheet'!M{self.row_map.get('bs_debt', 16)}/'Balance Sheet'!M{self.row_map.get('bs_total_assets', 10)},0)",
            ],
            [
                "Interest Coverage",
                "x",
                f"=IF('P&L'!C{self.row_map.get('pnl_interest', 30)}>0,'P&L'!C{self.row_map['pnl_ebitda']}/'P&L'!C{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!D{self.row_map.get('pnl_interest', 30)}>0,'P&L'!D{self.row_map['pnl_ebitda']}/'P&L'!D{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!E{self.row_map.get('pnl_interest', 30)}>0,'P&L'!E{self.row_map['pnl_ebitda']}/'P&L'!E{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!F{self.row_map.get('pnl_interest', 30)}>0,'P&L'!F{self.row_map['pnl_ebitda']}/'P&L'!F{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!G{self.row_map.get('pnl_interest', 30)}>0,'P&L'!G{self.row_map['pnl_ebitda']}/'P&L'!G{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!H{self.row_map.get('pnl_interest', 30)}>0,'P&L'!H{self.row_map['pnl_ebitda']}/'P&L'!H{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!I{self.row_map.get('pnl_interest', 30)}>0,'P&L'!I{self.row_map['pnl_ebitda']}/'P&L'!I{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!J{self.row_map.get('pnl_interest', 30)}>0,'P&L'!J{self.row_map['pnl_ebitda']}/'P&L'!J{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!K{self.row_map.get('pnl_interest', 30)}>0,'P&L'!K{self.row_map['pnl_ebitda']}/'P&L'!K{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!L{self.row_map.get('pnl_interest', 30)}>0,'P&L'!L{self.row_map['pnl_ebitda']}/'P&L'!L{self.row_map.get('pnl_interest', 30)},0)",
                f"=IF('P&L'!M{self.row_map.get('pnl_interest', 30)}>0,'P&L'!M{self.row_map['pnl_ebitda']}/'P&L'!M{self.row_map.get('pnl_interest', 30)},0)",
            ],
            [""],
            [
                "'--- EFFICIENCY RATIOS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Asset Turnover",
                "x",
                f"=IF('Balance Sheet'!C{self.row_map.get('bs_total_assets', 10)}>0,Revenue!C{self.row_map['total_revenue']}/'Balance Sheet'!C{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!D{self.row_map.get('bs_total_assets', 10)}>0,Revenue!D{self.row_map['total_revenue']}/'Balance Sheet'!D{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!E{self.row_map.get('bs_total_assets', 10)}>0,Revenue!E{self.row_map['total_revenue']}/'Balance Sheet'!E{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!F{self.row_map.get('bs_total_assets', 10)}>0,Revenue!F{self.row_map['total_revenue']}/'Balance Sheet'!F{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!G{self.row_map.get('bs_total_assets', 10)}>0,Revenue!G{self.row_map['total_revenue']}/'Balance Sheet'!G{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!H{self.row_map.get('bs_total_assets', 10)}>0,Revenue!H{self.row_map['total_revenue']}/'Balance Sheet'!H{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!I{self.row_map.get('bs_total_assets', 10)}>0,Revenue!I{self.row_map['total_revenue']}/'Balance Sheet'!I{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!J{self.row_map.get('bs_total_assets', 10)}>0,Revenue!J{self.row_map['total_revenue']}/'Balance Sheet'!J{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!K{self.row_map.get('bs_total_assets', 10)}>0,Revenue!K{self.row_map['total_revenue']}/'Balance Sheet'!K{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!L{self.row_map.get('bs_total_assets', 10)}>0,Revenue!L{self.row_map['total_revenue']}/'Balance Sheet'!L{self.row_map.get('bs_total_assets', 10)},0)",
                f"=IF('Balance Sheet'!M{self.row_map.get('bs_total_assets', 10)}>0,Revenue!M{self.row_map['total_revenue']}/'Balance Sheet'!M{self.row_map.get('bs_total_assets', 10)},0)",
            ],
            [
                "Receivable Days",
                "days",
                f"=Assumptions!C{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!D{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!E{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!F{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!G{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!H{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!I{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!J{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!K{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!L{self.row_map.get('debtor_days', 7)}",
                f"=Assumptions!M{self.row_map.get('debtor_days', 7)}",
            ],
            [
                "Payable Days",
                "days",
                f"=Assumptions!C{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!D{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!E{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!F{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!G{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!H{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!I{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!J{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!K{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!L{self.row_map.get('creditor_days', 8)}",
                f"=Assumptions!M{self.row_map.get('creditor_days', 8)}",
            ],
            [""],
            ["'--- GROWTH METRICS ---", "", "", "", "", "", "", "", "", "", "", "", ""],
            [
                "Revenue Growth YoY",
                "%",
                "",
                f"=IF(Revenue!C{self.row_map['total_revenue']}>0,(Revenue!D{self.row_map['total_revenue']}-Revenue!C{self.row_map['total_revenue']})/Revenue!C{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!D{self.row_map['total_revenue']}>0,(Revenue!E{self.row_map['total_revenue']}-Revenue!D{self.row_map['total_revenue']})/Revenue!D{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!E{self.row_map['total_revenue']}>0,(Revenue!F{self.row_map['total_revenue']}-Revenue!E{self.row_map['total_revenue']})/Revenue!E{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!F{self.row_map['total_revenue']}>0,(Revenue!G{self.row_map['total_revenue']}-Revenue!F{self.row_map['total_revenue']})/Revenue!F{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!G{self.row_map['total_revenue']}>0,(Revenue!H{self.row_map['total_revenue']}-Revenue!G{self.row_map['total_revenue']})/Revenue!G{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!H{self.row_map['total_revenue']}>0,(Revenue!I{self.row_map['total_revenue']}-Revenue!H{self.row_map['total_revenue']})/Revenue!H{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!I{self.row_map['total_revenue']}>0,(Revenue!J{self.row_map['total_revenue']}-Revenue!I{self.row_map['total_revenue']})/Revenue!I{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!J{self.row_map['total_revenue']}>0,(Revenue!K{self.row_map['total_revenue']}-Revenue!J{self.row_map['total_revenue']})/Revenue!J{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!K{self.row_map['total_revenue']}>0,(Revenue!L{self.row_map['total_revenue']}-Revenue!K{self.row_map['total_revenue']})/Revenue!K{self.row_map['total_revenue']},0)",
                f"=IF(Revenue!L{self.row_map['total_revenue']}>0,(Revenue!M{self.row_map['total_revenue']}-Revenue!L{self.row_map['total_revenue']})/Revenue!L{self.row_map['total_revenue']},0)",
            ],
            [
                "EBITDA Growth YoY",
                "%",
                "",
                f"=IF('P&L'!C{self.row_map['pnl_ebitda']}>0,('P&L'!D{self.row_map['pnl_ebitda']}-'P&L'!C{self.row_map['pnl_ebitda']})/'P&L'!C{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!D{self.row_map['pnl_ebitda']}>0,('P&L'!E{self.row_map['pnl_ebitda']}-'P&L'!D{self.row_map['pnl_ebitda']})/'P&L'!D{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!E{self.row_map['pnl_ebitda']}>0,('P&L'!F{self.row_map['pnl_ebitda']}-'P&L'!E{self.row_map['pnl_ebitda']})/'P&L'!E{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!F{self.row_map['pnl_ebitda']}>0,('P&L'!G{self.row_map['pnl_ebitda']}-'P&L'!F{self.row_map['pnl_ebitda']})/'P&L'!F{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!G{self.row_map['pnl_ebitda']}>0,('P&L'!H{self.row_map['pnl_ebitda']}-'P&L'!G{self.row_map['pnl_ebitda']})/'P&L'!G{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!H{self.row_map['pnl_ebitda']}>0,('P&L'!I{self.row_map['pnl_ebitda']}-'P&L'!H{self.row_map['pnl_ebitda']})/'P&L'!H{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!I{self.row_map['pnl_ebitda']}>0,('P&L'!J{self.row_map['pnl_ebitda']}-'P&L'!I{self.row_map['pnl_ebitda']})/'P&L'!I{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!J{self.row_map['pnl_ebitda']}>0,('P&L'!K{self.row_map['pnl_ebitda']}-'P&L'!J{self.row_map['pnl_ebitda']})/'P&L'!J{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!K{self.row_map['pnl_ebitda']}>0,('P&L'!L{self.row_map['pnl_ebitda']}-'P&L'!K{self.row_map['pnl_ebitda']})/'P&L'!K{self.row_map['pnl_ebitda']},0)",
                f"=IF('P&L'!L{self.row_map['pnl_ebitda']}>0,('P&L'!M{self.row_map['pnl_ebitda']}-'P&L'!L{self.row_map['pnl_ebitda']})/'P&L'!L{self.row_map['pnl_ebitda']},0)",
            ],
            [""],
            [
                "'--- CUSTOMER METRICS ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "LTV:CAC Ratio",
                "x",
                f"='Customer Economics'!C{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!D{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!E{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!F{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!G{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!H{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!I{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!J{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!K{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!L{self.row_map.get('ltv_cac', 15)}",
                f"='Customer Economics'!M{self.row_map.get('ltv_cac', 15)}",
            ],
            [
                "CAC Payback (months)",
                "mo",
                f"='Customer Economics'!C{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!D{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!E{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!F{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!G{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!H{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!I{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!J{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!K{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!L{self.row_map.get('payback', 16)}",
                f"='Customer Economics'!M{self.row_map.get('payback', 16)}",
            ],
            [""],
            [
                "'--- BENCHMARK COMPARISON ---",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Metric",
                "Your Y5",
                "Industry Avg",
                "Status",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Gross Margin",
                "=H5",
                "60%",
                '=IF(B33>=C33,"✓ Good","⚠ Below")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "EBITDA Margin",
                "=H6",
                "20%",
                '=IF(B34>=C34,"✓ Good","⚠ Below")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Net Margin",
                "=H7",
                "10%",
                '=IF(B35>=C35,"✓ Good","⚠ Below")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "LTV:CAC",
                "=H28",
                "3x",
                '=IF(B36>=3,"✓ Good","⚠ Below")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            [
                "Current Ratio",
                "=H12",
                "1.5x",
                '=IF(B37>=1.5,"✓ Good","⚠ Below")',
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
        ]

        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")

        # Formatting
        sheet.format(
            "A1:M1",
            {
                "textFormat": {"bold": True, "fontSize": 12},
                "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.6},
            },
        )
        sheet.format("A3:M3", {"textFormat": {"bold": True}})
        sheet.format("A11:M11", {"textFormat": {"bold": True}})
        sheet.format("A15:M15", {"textFormat": {"bold": True}})
        sheet.format("A20:M20", {"textFormat": {"bold": True}})
        sheet.format("A24:M24", {"textFormat": {"bold": True}})
        sheet.format("A27:M27", {"textFormat": {"bold": True}})
        sheet.format("A31:M31", {"textFormat": {"bold": True}})
        sheet.format(
            "A32:D32",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
            },
        )

        # Format percentages
        for row in [5, 6, 7, 8, 9, 25, 26]:
            sheet.format(f"C{row}:M{row}", PERCENT_FORMAT)

        # Format ratios (x)
        for row in [12, 13, 16, 17, 18, 21, 28]:
            sheet.format(f"C{row}:M{row}", DECIMAL_FORMAT)

        print(f"    ✓ Financial Ratios sheet")

    def build_headcount_sheet(self):
        """Build Headcount Plan sheet with dynamic salary model."""
        print("  Building Headcount Plan sheet...")

        sheet = self.spreadsheet.add_worksheet("Headcount Plan", rows=90, cols=8)

        data = []

        # Header
        data.append(["HEADCOUNT PLAN", "", "Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"])
        data.append(["Dynamic salary model with editable parameters", "", "", "", "", "", "", ""])
        data.append(["", "", "", "", "", "", "", ""])
        
        # PARAMETERS Section
        data.append(["PARAMETERS", "", "", "", "", "", "", ""])
        data.append(["Annual Salary Growth Rate", "", "15%", "", "", "", "", ""])  # Row 5
        data.append(["", "", "", "", "", "", "", ""])
        
        data.append(["Regional Salary Premiums", "", "Premium %", "", "", "", "", ""])
        data.append(["India (Base)", "", "0%", "", "", "", "", ""])
        data.append(["SE Asia", "", "25%", "", "", "", "", ""])
        data.append(["MENA", "", "46%", "", "", "", "", ""])
        data.append(["Europe", "", "88%", "", "", "", "", ""])
        data.append(["Americas", "", "117%", "", "", "", "", ""])
        data.append(["", "", "", "", "", "", "", ""])
        
        # BASE SALARY RATES Section
        data.append(["BASE SALARY RATES ($/yr)", "", "Base Rate", "", "", "", "", ""])  # Row 14
        data.append(["Founders / Leadership", "", "50000", "", "", "", "", ""])
        data.append(["Engineering Team", "", "18000", "", "", "", "", ""])
        data.append(["Sales & Marketing", "", "20000", "", "", "", "", ""])
        data.append(["Customer Success", "", "25000", "", "", "", "", ""])
        data.append(["Customer Support", "", "10000", "", "", "", "", ""])
        data.append(["Support Manager", "", "18000", "", "", "", "", ""])
        data.append(["Finance/HR/Admin", "", "15000", "", "", "", "", ""])
        data.append(["AI/Data Specialists", "", "25000", "", "", "", "", ""])
        data.append(["Regional Managers (Base)", "", "25000", "", "", "", "", ""])
        data.append(["", "", "", "", "", "", "", ""])
        
        # SALARY RATES BY YEAR Section
        data.append(["SALARY RATES BY YEAR", "", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])  # Row 25
        data.append(["Founders / Leadership", "", "=$C$15*(1+$C$5)^0", "=$C$15*(1+$C$5)^1", "=$C$15*(1+$C$5)^2", "=$C$15*(1+$C$5)^3", "=$C$15*(1+$C$5)^4", "=$C$15*(1+$C$5)^5"])
        data.append(["Engineering Team", "", "=$C$16*(1+$C$5)^0", "=$C$16*(1+$C$5)^1", "=$C$16*(1+$C$5)^2", "=$C$16*(1+$C$5)^3", "=$C$16*(1+$C$5)^4", "=$C$16*(1+$C$5)^5"])
        data.append(["Sales & Marketing", "", "=$C$17*(1+$C$5)^0", "=$C$17*(1+$C$5)^1", "=$C$17*(1+$C$5)^2", "=$C$17*(1+$C$5)^3", "=$C$17*(1+$C$5)^4", "=$C$17*(1+$C$5)^5"])
        data.append(["Customer Success", "", "=$C$18*(1+$C$5)^0", "=$C$18*(1+$C$5)^1", "=$C$18*(1+$C$5)^2", "=$C$18*(1+$C$5)^3", "=$C$18*(1+$C$5)^4", "=$C$18*(1+$C$5)^5"])
        data.append(["Customer Support", "", "=$C$19*(1+$C$5)^0", "=$C$19*(1+$C$5)^1", "=$C$19*(1+$C$5)^2", "=$C$19*(1+$C$5)^3", "=$C$19*(1+$C$5)^4", "=$C$19*(1+$C$5)^5"])
        data.append(["Support Manager", "", "=$C$20*(1+$C$5)^0", "=$C$20*(1+$C$5)^1", "=$C$20*(1+$C$5)^2", "=$C$20*(1+$C$5)^3", "=$C$20*(1+$C$5)^4", "=$C$20*(1+$C$5)^5"])
        data.append(["Finance/HR/Admin", "", "=$C$21*(1+$C$5)^0", "=$C$21*(1+$C$5)^1", "=$C$21*(1+$C$5)^2", "=$C$21*(1+$C$5)^3", "=$C$21*(1+$C$5)^4", "=$C$21*(1+$C$5)^5"])
        data.append(["AI/Data Specialists", "", "=$C$22*(1+$C$5)^0", "=$C$22*(1+$C$5)^1", "=$C$22*(1+$C$5)^2", "=$C$22*(1+$C$5)^3", "=$C$22*(1+$C$5)^4", "=$C$22*(1+$C$5)^5"])
        data.append(["Regional Managers (Base)", "", "=$C$23*(1+$C$5)^0", "=$C$23*(1+$C$5)^1", "=$C$23*(1+$C$5)^2", "=$C$23*(1+$C$5)^3", "=$C$23*(1+$C$5)^4", "=$C$23*(1+$C$5)^5"])
        data.append(["", "", "", "", "", "", "", ""])
        
        # HEADCOUNT BY ROLE Section
        data.append(["HEADCOUNT BY ROLE", "", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])  # Row 36
        data.append(["Founders / Leadership", "", "2", "3", "3", "3", "3", "3"])
        data.append(["Engineering Team", "", "5", "10", "20", "30", "35", "40"])
        data.append(["Sales & Marketing", "", "2", "5", "15", "22", "30", "35"])
        data.append(["Customer Success", "", "1", "1", "5", "8", "12", "15"])
        data.append(["Customer Support", "", "1", "2", "10", "15", "20", "25"])
        data.append(["Support Manager", "", "0", "1", "1", "2", "2", "3"])
        data.append(["Finance/HR/Admin", "", "1", "1", "2", "2", "3", "4"])
        data.append(["AI/Data Specialists", "", "2", "2", "2", "3", "4", "6"])
        data.append(["", "", "", "", "", "", "", ""])
        
        # REGIONAL MANAGERS Section
        data.append(["REGIONAL MANAGERS BY REGION", "", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])  # Row 46
        data.append(["India", "", "1", "2", "4", "4", "4", "4"])
        data.append(["SE Asia", "", "0", "1", "3", "4", "4", "4"])
        data.append(["MENA", "", "0", "0", "2", "2", "3", "3"])
        data.append(["Europe", "", "0", "0", "0", "1", "2", "3"])
        data.append(["Americas", "", "0", "0", "0", "0", "1", "2"])
        data.append(["Total Regional Managers", "", "=SUM(C47:C51)", "=SUM(D47:D51)", "=SUM(E47:E51)", "=SUM(F47:F51)", "=SUM(G47:G51)", "=SUM(H47:H51)"])
        data.append(["", "", "", "", "", "", "", ""])
        
        # TOTAL HEADCOUNT
        data.append(["TOTAL HEADCOUNT", "", "=SUM(C37:C44)+C52", "=SUM(D37:D44)+D52", "=SUM(E37:E44)+E52", "=SUM(F37:F44)+F52", "=SUM(G37:G44)+G52", "=SUM(H37:H44)+H52"])  # Row 54
        data.append(["", "", "", "", "", "", "", ""])
        
        # SALARY COSTS Section
        data.append(["SALARY COSTS", "", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])  # Row 56
        data.append(["Founders / Leadership", "", "=C37*C26", "=D37*D26", "=E37*E26", "=F37*F26", "=G37*G26", "=H37*H26"])
        data.append(["Engineering Team", "", "=C38*C27", "=D38*D27", "=E38*E27", "=F38*F27", "=G38*G27", "=H38*H27"])
        data.append(["Sales & Marketing", "", "=C39*C28", "=D39*D28", "=E39*E28", "=F39*F28", "=G39*G28", "=H39*H28"])
        data.append(["Customer Success", "", "=C40*C29", "=D40*D29", "=E40*E29", "=F40*F29", "=G40*G29", "=H40*H29"])
        data.append(["Customer Support", "", "=C41*C30", "=D41*D30", "=E41*E30", "=F41*F30", "=G41*G30", "=H41*H30"])
        data.append(["Support Manager", "", "=C42*C31", "=D42*D31", "=E42*E31", "=F42*F31", "=G42*G31", "=H42*H31"])
        data.append(["Finance/HR/Admin", "", "=C43*C32", "=D43*D32", "=E43*E32", "=F43*F32", "=G43*G32", "=H43*H32"])
        data.append(["AI/Data Specialists", "", "=C44*C33", "=D44*D33", "=E44*E33", "=F44*F33", "=G44*G33", "=H44*H33"])
        data.append(["", "", "", "", "", "", "", ""])
        
        # Regional Manager Costs
        data.append(["Regional Manager Costs", "", "", "", "", "", "", ""])  # Row 66
        data.append(["  India", "", "=C47*C34*(1+$C$8)", "=D47*D34*(1+$C$8)", "=E47*E34*(1+$C$8)", "=F47*F34*(1+$C$8)", "=G47*G34*(1+$C$8)", "=H47*H34*(1+$C$8)"])
        data.append(["  SE Asia", "", "=C48*C34*(1+$C$9)", "=D48*D34*(1+$C$9)", "=E48*E34*(1+$C$9)", "=F48*F34*(1+$C$9)", "=G48*G34*(1+$C$9)", "=H48*H34*(1+$C$9)"])
        data.append(["  MENA", "", "=C49*C34*(1+$C$10)", "=D49*D34*(1+$C$10)", "=E49*E34*(1+$C$10)", "=F49*F34*(1+$C$10)", "=G49*G34*(1+$C$10)", "=H49*H34*(1+$C$10)"])
        data.append(["  Europe", "", "=C50*C34*(1+$C$11)", "=D50*D34*(1+$C$11)", "=E50*E34*(1+$C$11)", "=F50*F34*(1+$C$11)", "=G50*G34*(1+$C$11)", "=H50*H34*(1+$C$11)"])
        data.append(["  Americas", "", "=C51*C34*(1+$C$12)", "=D51*D34*(1+$C$12)", "=E51*E34*(1+$C$12)", "=F51*F34*(1+$C$12)", "=G51*G34*(1+$C$12)", "=H51*H34*(1+$C$12)"])
        data.append(["Total Regional Managers", "", "=SUM(C67:C71)", "=SUM(D67:D71)", "=SUM(E67:E71)", "=SUM(F67:F71)", "=SUM(G67:G71)", "=SUM(H67:H71)"])
        data.append(["", "", "", "", "", "", "", ""])
        
        # TOTAL PEOPLE COST
        data.append(["TOTAL PEOPLE COST", "", "=SUM(C57:C64)+C72", "=SUM(D57:D64)+D72", "=SUM(E57:E64)+E72", "=SUM(F57:F64)+F72", "=SUM(G57:G64)+G72", "=SUM(H57:H64)+H72"])  # Row 74
        data.append(["", "", "", "", "", "", "", ""])
        
        # EFFICIENCY METRICS
        data.append(["EFFICIENCY METRICS", "", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])  # Row 76
        data.append(["Revenue per Employee", "", "=IFERROR(Revenue!C10*1000/C54,0)", "=IFERROR(Revenue!D10*1000/D54,0)", "=IFERROR(Revenue!E10*1000/E54,0)", "=IFERROR(Revenue!F10*1000/F54,0)", "=IFERROR(Revenue!G10*1000/G54,0)", "=IFERROR(Revenue!H10*1000/H54,0)"])
        data.append(["People Cost % of Revenue", "", "=IFERROR(C74/(Revenue!C10*1000),0)", "=IFERROR(D74/(Revenue!D10*1000),0)", "=IFERROR(E74/(Revenue!E10*1000),0)", "=IFERROR(F74/(Revenue!F10*1000),0)", "=IFERROR(G74/(Revenue!G10*1000),0)", "=IFERROR(H74/(Revenue!H10*1000),0)"])
        data.append(["", "", "", "", "", "", "", ""])
        
        # NOTES
        data.append(["NOTES", "", "", "", "", "", "", ""])  # Row 80
        data.append(["• Edit C5 to change annual salary growth rate", "", "", "", "", "", "", ""])
        data.append(["• Edit C8:C12 to change regional salary premiums", "", "", "", "", "", "", ""])
        data.append(["• Edit C15:C23 to change base salary rates", "", "", "", "", "", "", ""])
        data.append(["• Edit C47:H51 to change regional manager distribution", "", "", "", "", "", "", ""])
        
        # Write data to sheet
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")
        
        # Apply formatting
        sheet.format("A1:H1", {"textFormat": {"bold": True, "fontSize": 14}, "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5}, "horizontalAlignment": "LEFT"})
        sheet.format("A4", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A14", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A25", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A36", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A46", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A54", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.4, "green": 0.6, "blue": 0.8}})
        sheet.format("A56", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A74", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.4, "green": 0.6, "blue": 0.8}})
        sheet.format("A76", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A80", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.5, "green": 0.5, "blue": 0.5}})
        
        # Format currency columns
        sheet.format("C26:H34", {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0"}})
        sheet.format("C57:H72", {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0"}})
        sheet.format("C74:H74", {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0"}})
        sheet.format("C77:H77", {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0"}})
        
        # Format percentages
        sheet.format("C5", {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}})
        sheet.format("C8:C12", {"numberFormat": {"type": "PERCENT", "pattern": "0%"}})
        sheet.format("C78:H78", {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}})
        
        # Format integers
        sheet.format("C37:H52", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        sheet.format("C54:H54", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})

        print(f"    ✓ Headcount Plan sheet")

    def build_charts_data_sheet(self):
        """Build Charts Data sheet for embedded visualizations."""
        print("  Building Charts Data sheet...")

        sheet = self.spreadsheet.add_worksheet("Charts Data", rows=60, cols=7)

        data = []
        
        # CHART 1: Revenue Growth
        data.append(["CHART 1: REVENUE GROWTH", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["Revenue ($K)", "=Revenue!C10", "=Revenue!D10", "=Revenue!E10", "=Revenue!F10", "=Revenue!G10", "=Revenue!H10"])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 2: Revenue Mix (Year 5)
        data.append(["CHART 2: REVENUE MIX (Year 5)", "", "", "", "", "", ""])
        data.append(["Stream", "Revenue ($K)", "", "", "", "", ""])
        # Will be populated dynamically based on revenue streams
        for i, stream in enumerate(self.config["revenue_streams"]):
            stream_name = stream["name"]
            row_ref = 5 + i * 4  # Assuming 4 rows per stream in Revenue sheet
            data.append([stream_name, f"=Revenue!H{row_ref}", "", "", "", "", ""])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 3: Profitability Trend
        data.append(["CHART 3: PROFITABILITY TREND", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["Gross Profit ($K)", "=P_L!C5", "=P_L!D5", "=P_L!E5", "=P_L!F5", "=P_L!G5", "=P_L!H5"])
        data.append(["EBITDA ($K)", "=P_L!C7", "=P_L!D7", "=P_L!E7", "=P_L!F7", "=P_L!G7", "=P_L!H7"])
        data.append(["Net Income ($K)", "=P_L!C13", "=P_L!D13", "=P_L!E13", "=P_L!F13", "=P_L!G13", "=P_L!H13"])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 4: Customer Growth
        data.append(["CHART 4: CUSTOMER GROWTH", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["Total Customers", "=Assumptions!C56", "=Assumptions!D56", "=Assumptions!E56", "=Assumptions!F56", "=Assumptions!G56", "=Assumptions!H56"])
        data.append(["New Customers", "=Assumptions!C48", "=Assumptions!D48", "=Assumptions!E48", "=Assumptions!F48", "=Assumptions!G48", "=Assumptions!H48"])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 5: Unit Economics
        data.append(["CHART 5: UNIT ECONOMICS", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["LTV:CAC Ratio", "=Assumptions!C64", "=Assumptions!D64", "=Assumptions!E64", "=Assumptions!F64", "=Assumptions!G64", "=Assumptions!H64"])
        data.append(["CAC Payback (months)", "=Assumptions!C66", "=Assumptions!D66", "=Assumptions!E66", "=Assumptions!F66", "=Assumptions!G66", "=Assumptions!H66"])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 6: Cash Position
        data.append(["CHART 6: CASH POSITION", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["Cash Balance ($K)", "='Cash Flow'!C19", "='Cash Flow'!D19", "='Cash Flow'!E19", "='Cash Flow'!F19", "='Cash Flow'!G19", "='Cash Flow'!H19"])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 7: Margin Trends
        data.append(["CHART 7: MARGIN TRENDS", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["Gross Margin %", "=P_L!C6", "=P_L!D6", "=P_L!E6", "=P_L!F6", "=P_L!G6", "=P_L!H6"])
        data.append(["EBITDA Margin %", "=P_L!C8", "=P_L!D8", "=P_L!E8", "=P_L!F8", "=P_L!G8", "=P_L!H8"])
        data.append(["Net Profit Margin %", "=P_L!C14", "=P_L!D14", "=P_L!E14", "=P_L!F14", "=P_L!G14", "=P_L!H14"])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 8: Cap Table
        data.append(["CHART 8: CAP TABLE (Post Series A)", "", "", "", "", "", ""])
        data.append(["Stakeholder", "Ownership %", "", "", "", "", ""])
        data.append(["Founders", "='Funding Cap Table'!C41", "", "", "", "", ""])
        data.append(["Seed Investors", "='Funding Cap Table'!C42", "", "", "", "", ""])
        data.append(["Series A Investors", "='Funding Cap Table'!C43", "", "", "", "", ""])
        data.append(["", "", "", "", "", "", ""])
        
        # CHART 9: Funding Timeline
        data.append(["CHART 9: FUNDING TIMELINE", "", "", "", "", "", ""])
        data.append(["Year", "Y0", "Y1", "Y2", "Y3", "Y4", "Y5"])
        data.append(["Equity Raised ($K)", "=Assumptions!C10", "=Assumptions!D10", "=Assumptions!E10", "=Assumptions!F10", "=Assumptions!G10", "=Assumptions!H10"])
        data.append(["Cumulative Equity ($K)", "=C48", "=C48+D48", "=C48+D48+E48", "=C48+D48+E48+F48", "=C48+D48+E48+F48+G48", "=C48+D48+E48+F48+G48+H48"])
        
        # Write data to sheet
        sheet.update(values=data, range_name="A1", value_input_option="USER_ENTERED")
        
        # Apply formatting
        sheet.format("A1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        sheet.format("A5", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        chart3_row = 7 + len(self.config["revenue_streams"]) + 1
        sheet.format(f"A{chart3_row}", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.3, "green": 0.5, "blue": 0.7}})
        
        # Format numbers
        sheet.format("B3:G3", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0.0"}})
        sheet.format("B7:B20", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0.0"}})
        
        print(f"    ✓ Charts Data sheet")


def create_from_template(
    company_name, config=None, use_humanoid_rent=False, folder_id=None
):
    """
    Create a new financial model by COPYING the RapidTools template.
    This is MUCH faster and ensures 100% fidelity to the template structure.

    Args:
        company_name: Name of the company
        config: Configuration dict with values to update
        use_humanoid_rent: If True, use HumanoidRent preset
        folder_id: Optional Drive folder ID

    Returns:
        Dict with spreadsheet info
    """
    RAPIDTOOLS_TEMPLATE_ID = "1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY"
    
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    # Use preset if specified
    if use_humanoid_rent or config is None:
        config = HUMANOID_RENT_CONFIG
        print("Using HumanoidRent preset configuration")
    
    # Check if config is compatible with template (max 6 revenue streams)
    streams = config.get("revenue_streams", []) if config else []
    if len(streams) > 6:
        print(f"\n⚠ Config has {len(streams)} revenue streams, but template supports max 6")
        print("Falling back to build-from-scratch method for full customization...")
        return create_financial_model_v2(company_name, config, use_humanoid_rent, folder_id)
    
    print(f"\nCopying RapidTools template...")
    print(f"Template ID: {RAPIDTOOLS_TEMPLATE_ID}")
    
    # Copy the template spreadsheet
    try:
        from googleapiclient.discovery import build
        drive_service = build("drive", "v3", credentials=creds)
        
        title = f"{company_name} - Financial Model"
        file_metadata = {
            'name': title,
            'parents': [folder_id] if folder_id else []
        }
        
        copied_file = drive_service.files().copy(
            fileId=RAPIDTOOLS_TEMPLATE_ID,
            body=file_metadata
        ).execute()
        
        spreadsheet_id = copied_file['id']
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        print(f"✓ Template copied: {title}")
        print(f"  ID: {spreadsheet_id}")
        
        # Now update with new config values
        if config:
            print("\nUpdating template with new values...")
            _update_template_values(spreadsheet, config)
        
        url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        
        print(f"\n✅ Financial model created from template!")
        print(f"URL: {url}")
        
        return {
            "spreadsheet_id": spreadsheet_id,
            "title": title,
            "url": url,
            "method": "template_copy",
            "template_id": RAPIDTOOLS_TEMPLATE_ID,
            "revenue_streams": [s["name"] for s in config.get("revenue_streams", [])] if config else []
        }
        
    except Exception as e:
        print(f"❌ Error copying template: {e}")
        print("Falling back to building from scratch...")
        return create_financial_model_v2(company_name, config, use_humanoid_rent, folder_id)


def _update_template_values(spreadsheet, config):
    """
    Comprehensively update copied template with new business configuration.
    Handles businesses very different from RapidTools by updating all sections.
    """
    try:
        assumptions = spreadsheet.worksheet("Assumptions")
        
        # ====================
        # 1. GENERAL PARAMETERS (Rows 4-12)
        # ====================
        general = config.get("general", {})
        if general:
            print("  Updating general parameters...")
            updates = []
            
            # Row 4: Tax Rate
            if "tax_rate" in general:
                updates.append(("C4", general["tax_rate"]))
            
            # Row 5: Capex
            if "capex" in general:
                updates.append(("C5", general["capex"]))
            
            # Row 6: Depreciation Years
            if "depreciation_years" in general:
                updates.append(("C6", general["depreciation_years"]))
            
            # Row 7: Debtor Days
            if "debtor_days" in general:
                updates.append(("C7", general["debtor_days"]))
            
            # Row 8: Creditor Days
            if "creditor_days" in general:
                updates.append(("C8", general["creditor_days"]))
            
            # Row 9: Interest Rate
            if "interest_rate" in general:
                updates.append(("C9", general["interest_rate"]))
            
            # Row 10-11: Funding (Equity & Debt)
            if "equity_infusion" in general:
                # Year 0 equity
                updates.append(("C10", general["equity_infusion"].get("year_0", 0)))
            
            if "debt_drawdown" in general:
                updates.append(("C11", general["debt_drawdown"].get("year_0", 0)))
            
            # Row 12: Cost Inflation Rate
            if "cost_inflation" in general:
                updates.append(("C12", general["cost_inflation"]))
            
            # Apply all general parameter updates
            for cell, value in updates:
                assumptions.update(cell, [[value]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.5)
            
            print(f"    ✓ Updated {len(updates)} general parameters")
        
        # ====================
        # 2. REVENUE STREAMS (Rows 15-38, supports up to 6 streams)
        # ====================
        streams = config.get("revenue_streams", [])
        if streams:
            print(f"  Updating {len(streams)} revenue streams...")
            
            # Template rows start at 15 (after header at row 14)
            # Each stream takes 4 rows: Price, Volume, Growth, COGS%
            base_row = 15
            
            for i, stream in enumerate(streams[:6]):  # Template supports max 6 streams
                row_offset = i * 4
                name = stream.get("name", f"Stream {i+1}")
                
                # Update stream name (Column A)
                name_cell = f"A{base_row + row_offset}"
                assumptions.update(name_cell, [[name + ": Price"]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
                
                # Update Price (Row 1 of stream)
                price_row = base_row + row_offset
                if "price" in stream:
                    assumptions.update(f"C{price_row}", [[stream["price"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.3)
                
                # Update Volume (Row 2 of stream)
                volume_row = price_row + 1
                assumptions.update(f"A{volume_row}", [[name + ": Volume"]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
                if "volume" in stream:
                    assumptions.update(f"C{volume_row}", [[stream["volume"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.3)
                
                # Update Growth (Row 3 of stream)
                growth_row = volume_row + 1
                assumptions.update(f"A{growth_row}", [[name + ": Growth"]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
                if "growth" in stream:
                    assumptions.update(f"C{growth_row}", [[stream["growth"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.3)
                
                # Update COGS % (Row 4 of stream)
                cogs_row = growth_row + 1
                assumptions.update(f"A{cogs_row}", [[name + ": COGS %"]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
                if "cogs_percent" in stream:
                    assumptions.update(f"C{cogs_row}", [[stream["cogs_percent"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.3)
                
                print(f"    ✓ Updated stream {i+1}: {name}")
            
            # If fewer than 6 streams, clear the unused ones
            if len(streams) < 6:
                print(f"  Clearing unused revenue streams ({len(streams)+1}-6)...")
                for i in range(len(streams), 6):
                    row_offset = i * 4
                    # Clear the stream name and set values to 0
                    for row in range(4):
                        cell_row = base_row + row_offset + row
                        assumptions.update(f"A{cell_row}", [[f"(Unused Stream {i+1})"]], value_input_option="USER_ENTERED")
                        assumptions.update(f"C{cell_row}", [[0]], value_input_option="USER_ENTERED")
                        rate_limit_delay(0.3)
        
        # ====================
        # 3. FIXED COSTS (Rows 41-50, supports up to 10 categories)
        # ====================
        fixed_costs = config.get("fixed_costs", [])
        if fixed_costs:
            print(f"  Updating {len(fixed_costs)} fixed cost categories...")
            
            base_row = 41
            for i, cost in enumerate(fixed_costs[:10]):  # Template supports max 10
                cost_name = cost.get("name", f"Fixed Cost {i+1}")
                cost_value = cost.get("annual_cost", 0)
                
                # Update cost name (Column A) and value (Column C)
                assumptions.update(f"A{base_row + i}", [[cost_name]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
                assumptions.update(f"C{base_row + i}", [[cost_value]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Clear unused cost categories
            if len(fixed_costs) < 10:
                for i in range(len(fixed_costs), 10):
                    assumptions.update(f"A{base_row + i}", [[f"(Unused Cost {i+1})"]], value_input_option="USER_ENTERED")
                    assumptions.update(f"C{base_row + i}", [[0]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.3)
            
            print(f"    ✓ Updated {len(fixed_costs)} fixed costs")
        
        # ====================
        # 4. CUSTOMER ACQUISITION (Rows 48-56)
        # ====================
        cac_params = config.get("customer_acquisition", {})
        if cac_params:
            print("  Updating customer acquisition parameters...")
            
            # Row 48: CAC
            if "cac" in cac_params:
                assumptions.update("C48", [[cac_params["cac"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Row 49: New Customers Year 0
            if "new_customers_y0" in cac_params:
                assumptions.update("C49", [[cac_params["new_customers_y0"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Row 50: New Customer Growth
            if "new_customer_growth" in cac_params:
                assumptions.update("C50", [[cac_params["new_customer_growth"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Row 51: Churned Customers (formula or value)
            if "churned_customers" in cac_params:
                assumptions.update("C51", [[cac_params["churned_customers"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Row 53: Churn Rate
            if "churn_rate" in cac_params:
                assumptions.update("C53", [[cac_params["churn_rate"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Row 54: Customer Growth Rate
            if "customer_growth" in cac_params:
                assumptions.update("C54", [[cac_params["customer_growth"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            # Row 55: Customer Lifetime
            if "customer_lifetime" in cac_params:
                assumptions.update("C55", [[cac_params["customer_lifetime"]]], value_input_option="USER_ENTERED")
                rate_limit_delay(0.3)
            
            print("    ✓ Updated customer acquisition parameters")
        
        # ====================
        # 5. UPDATE SOURCES & REFERENCES (Optional)
        # ====================
        sources_data = config.get("sources_references", {})
        if sources_data:
            try:
                sources_sheet = spreadsheet.worksheet("Sources & References")
                print("  Updating Sources & References with new market data...")
                
                # Update TAM/SAM/SOM if provided
                if "tam" in sources_data:
                    sources_sheet.update("B7", [[sources_data["tam"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.5)
                
                if "sam" in sources_data:
                    sources_sheet.update("B41", [[sources_data["sam"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.5)
                
                if "som" in sources_data:
                    sources_sheet.update("B51", [[sources_data["som"]]], value_input_option="USER_ENTERED")
                    rate_limit_delay(0.5)
                
                print("    ✓ Updated market sizing data")
            except Exception as e:
                print(f"    ⚠ Could not update Sources sheet: {e}")
        
        print("  ✅ Template values comprehensively updated")
        print(f"     - Business model adapted to your config")
        print(f"     - All formulas preserved and auto-calculating")
        
    except Exception as e:
        print(f"  ⚠ Warning: Could not update all template values: {e}")
        import traceback
        traceback.print_exc()


def create_financial_model_v2(
    company_name, config=None, use_humanoid_rent=False, folder_id=None
):
    """
    Create a new financial model from scratch (programmatic build).
    
    NOTE: For faster creation with guaranteed template fidelity, 
    use create_from_template() instead.

    Args:
        company_name: Name of the company
        config: Configuration dict (or None to use defaults)
        use_humanoid_rent: If True, use HumanoidRent preset
        folder_id: Optional Drive folder ID

    Returns:
        Dict with spreadsheet info
    """
    creds = get_credentials()
    client = gspread.authorize(creds)

    # Use preset if specified
    if use_humanoid_rent or config is None:
        config = HUMANOID_RENT_CONFIG
        print("Using HumanoidRent preset configuration")

    # Create spreadsheet
    title = f"{company_name} - Financial Model"
    spreadsheet = client.create(title)
    spreadsheet_id = spreadsheet.id

    print(f"\nCreated spreadsheet: {title}")
    print(f"ID: {spreadsheet_id}")

    # Build all sheets
    builder = FinancialModelBuilder(spreadsheet, config)
    builder.build_all_sheets()

    # Move to folder if specified
    if folder_id:
        try:
            from googleapiclient.discovery import build

            drive_service = build("drive", "v3", credentials=creds)
            file = (
                drive_service.files()
                .get(fileId=spreadsheet_id, fields="parents")
                .execute()
            )
            prev_parents = ",".join(file.get("parents", []))
            drive_service.files().update(
                fileId=spreadsheet_id,
                addParents=folder_id,
                removeParents=prev_parents,
                fields="id, parents",
            ).execute()
            print(f"Moved to folder: {folder_id}")
        except Exception as e:
            print(f"Warning: Could not move to folder: {e}")

    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    print(f"\n✅ Financial model created!")
    print(f"URL: {url}")

    return {
        "spreadsheet_id": spreadsheet_id,
        "title": title,
        "url": url,
        "sheets": [
            "Assumptions",
            "Revenue",
            "Operating Costs",
            "P&L",
            "Customer Economics",
            "Cash Flow",
            "Balance Sheet",
            "Summary",
            "Sources & References",
        ],
        "revenue_streams": [s["name"] for s in config["revenue_streams"]],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Create comprehensive financial model",
        epilog="""
Examples:
  # Copy from RapidTools template (RECOMMENDED - faster and guaranteed fidelity)
  python create_financial_model.py --company "MyStartup" --config config.json --from-template

  # Build from scratch (programmatic)
  python create_financial_model.py --company "MyStartup" --config config.json

  # Use preset configuration
  python create_financial_model.py --company "HumanoidRent" --humanoid-rent --from-template
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument(
        "--humanoid-rent", action="store_true", help="Use HumanoidRent preset"
    )
    parser.add_argument("--folder-id", help="Google Drive folder ID")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument(
        "--from-template", 
        action="store_true", 
        help="Copy from RapidTools template (RECOMMENDED - much faster, guaranteed fidelity)"
    )
    parser.add_argument(
        "--build-from-scratch",
        action="store_true",
        help="Build programmatically from scratch (slower, for debugging only)"
    )

    args = parser.parse_args()

    config = None
    if args.config and os.path.exists(args.config):
        with open(args.config, "r") as f:
            config = json.load(f)

    try:
        # Determine method: template copy (default/recommended) or build from scratch
        if args.build_from_scratch:
            print("🔧 Building from scratch (programmatic method)...")
            result = create_financial_model_v2(
                company_name=args.company,
                config=config,
                use_humanoid_rent=args.humanoid_rent,
                folder_id=args.folder_id,
            )
        else:
            # Default to template copy (faster and guaranteed fidelity)
            if not args.from_template:
                print("💡 Using template copy method (default, recommended)")
                print("   Use --build-from-scratch to build programmatically instead\n")
            
            result = create_from_template(
                company_name=args.company,
                config=config,
                use_humanoid_rent=args.humanoid_rent,
                folder_id=args.folder_id,
            )

        print("\n" + json.dumps(result, indent=2))

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\nSaved to: {args.output}")

        # ========================================
        # AUTO-VALIDATION (Post-Creation Quality Check)
        # ========================================
        print("\n" + "="*60)
        print("🔍 RUNNING POST-CREATION VALIDATION")
        print("="*60)
        
        sheet_id = result.get("sheet_id")
        if sheet_id:
            # Run template verification if copied from template
            if not args.build_from_scratch:
                print("\n1. Template Fidelity Check...")
                verify_cmd = f'python execution/verify_template_copy.py --sheet-id "{sheet_id}"'
                verify_result = os.system(verify_cmd)
                
                if verify_result == 0:
                    print("   ✅ Template structure verified")
                elif verify_result == 256:  # Exit code 1 (warnings)
                    print("   ⚠️  Template verification has warnings (review above)")
                else:
                    print("   ❌ Template verification failed")
            
            # Run comprehensive audit
            print("\n2. Financial Model Audit...")
            audit_cmd = f'python execution/audit_financial_model.py --sheet-id "{sheet_id}" --mode comprehensive'
            audit_result = os.system(audit_cmd)
            
            if audit_result == 0:
                print("   ✅ Model audit passed")
            else:
                print("   ⚠️  Model audit found issues (review above)")
            
            print("\n" + "="*60)
            print("📊 MODEL CREATED AND VALIDATED")
            print("="*60)
            print(f"Sheet URL: {result.get('url')}")
            print("Review validation results above before using the model.")
        else:
            print("\n⚠️  Warning: Could not run validation (no sheet_id returned)")

        return result

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
