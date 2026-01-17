#!/usr/bin/env python3
"""
Create a comprehensive 5-year financial projection spreadsheet in Google Sheets.
Part of the Business Planning Agent toolkit.

Creates multiple sheets:
1. Assumptions - All input parameters
2. Revenue - Revenue projections by year
3. Expenses - Cost breakdown
4. Profit & Loss - P&L statement
5. Cash Flow - Cash flow projections
6. Key Metrics - Business metrics and KPIs
"""

import os
import sys
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def get_credentials():
    """Get OAuth2 credentials for Google Sheets API."""
    creds = None
    
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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

    return creds


def create_financial_spreadsheet(
    company_name: str,
    assumptions: dict,
    years: int = 5,
    folder_id: str = None
) -> dict:
    """
    Create a comprehensive financial projection spreadsheet.
    
    Args:
        company_name: Name of the company
        assumptions: Dictionary with financial assumptions
        years: Number of years to project (default 5)
        folder_id: Optional Google Drive folder ID
        
    Returns:
        Dictionary with spreadsheet ID and URL
    """
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    # Create the spreadsheet
    title = f"{company_name} - 5 Year Financial Projections"
    spreadsheet = client.create(title)
    spreadsheet_id = spreadsheet.id
    
    print(f"Created spreadsheet: {title}")
    print(f"Spreadsheet ID: {spreadsheet_id}")
    
    # Extract assumptions with defaults
    initial_investment = assumptions.get('initial_investment', 50000)
    year1_customers = assumptions.get('year1_customers', 100)
    customer_growth_rate = assumptions.get('customer_growth_rate', 0.5)  # 50%
    avg_revenue_per_customer = assumptions.get('avg_revenue_per_customer', 1200)  # Annual
    cogs_percent = assumptions.get('cogs_percent', 0.20)  # 20% of revenue
    
    # Fixed costs
    fixed_costs = assumptions.get('fixed_costs', {
        'Salaries': 120000,
        'Rent/Office': 24000,
        'Software/Tools': 6000,
        'Marketing': 36000,
        'Insurance': 3000,
        'Legal/Accounting': 6000,
        'Other': 5000
    })
    
    # Variable costs as % of revenue
    variable_costs = assumptions.get('variable_costs', {
        'Payment Processing': 0.03,
        'Customer Support': 0.05,
        'Hosting/Infrastructure': 0.02
    })
    
    # Calculate projections
    projections = calculate_projections(
        initial_investment=initial_investment,
        year1_customers=year1_customers,
        customer_growth_rate=customer_growth_rate,
        avg_revenue_per_customer=avg_revenue_per_customer,
        cogs_percent=cogs_percent,
        fixed_costs=fixed_costs,
        variable_costs=variable_costs,
        years=years
    )
    
    # Create sheets
    create_assumptions_sheet(spreadsheet, assumptions, fixed_costs, variable_costs)
    create_revenue_sheet(spreadsheet, projections, years)
    create_expenses_sheet(spreadsheet, projections, fixed_costs, variable_costs, years)
    create_pnl_sheet(spreadsheet, projections, years)
    create_cashflow_sheet(spreadsheet, projections, initial_investment, years)
    create_metrics_sheet(spreadsheet, projections, assumptions, years)
    
    # Delete the default Sheet1
    try:
        default_sheet = spreadsheet.worksheet('Sheet1')
        spreadsheet.del_worksheet(default_sheet)
    except:
        pass
    
    # Move to folder if specified
    if folder_id:
        try:
            from googleapiclient.discovery import build
            drive_service = build('drive', 'v3', credentials=creds)
            file = drive_service.files().get(fileId=spreadsheet_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents', []))
            drive_service.files().update(
                fileId=spreadsheet_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            print(f"Moved to folder: {folder_id}")
        except Exception as e:
            print(f"Warning: Could not move to folder: {e}")
    
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    
    return {
        'spreadsheet_id': spreadsheet_id,
        'title': title,
        'url': spreadsheet_url,
        'projections': projections
    }


def calculate_projections(
    initial_investment: float,
    year1_customers: int,
    customer_growth_rate: float,
    avg_revenue_per_customer: float,
    cogs_percent: float,
    fixed_costs: dict,
    variable_costs: dict,
    years: int
) -> dict:
    """Calculate all financial projections."""
    
    projections = {
        'years': [],
        'customers': [],
        'revenue': [],
        'cogs': [],
        'gross_profit': [],
        'fixed_costs_total': [],
        'variable_costs_total': [],
        'operating_expenses': [],
        'net_income': [],
        'cumulative_cash': [],
        'gross_margin': [],
        'net_margin': []
    }
    
    total_fixed = sum(fixed_costs.values())
    total_variable_rate = sum(variable_costs.values())
    cumulative_cash = initial_investment
    
    for year in range(1, years + 1):
        # Customer growth
        if year == 1:
            customers = year1_customers
        else:
            customers = int(projections['customers'][-1] * (1 + customer_growth_rate))
        
        # Revenue
        revenue = customers * avg_revenue_per_customer
        
        # COGS
        cogs = revenue * cogs_percent
        
        # Gross Profit
        gross_profit = revenue - cogs
        
        # Operating Expenses
        variable_total = revenue * total_variable_rate
        operating_expenses = total_fixed + variable_total
        
        # Net Income
        net_income = gross_profit - operating_expenses
        
        # Cash Flow
        cumulative_cash = cumulative_cash + net_income
        
        # Margins
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
        net_margin = (net_income / revenue * 100) if revenue > 0 else 0
        
        # Store projections
        projections['years'].append(year)
        projections['customers'].append(customers)
        projections['revenue'].append(revenue)
        projections['cogs'].append(cogs)
        projections['gross_profit'].append(gross_profit)
        projections['fixed_costs_total'].append(total_fixed)
        projections['variable_costs_total'].append(variable_total)
        projections['operating_expenses'].append(operating_expenses)
        projections['net_income'].append(net_income)
        projections['cumulative_cash'].append(cumulative_cash)
        projections['gross_margin'].append(gross_margin)
        projections['net_margin'].append(net_margin)
    
    return projections


def create_assumptions_sheet(spreadsheet, assumptions, fixed_costs, variable_costs):
    """Create the Assumptions sheet."""
    sheet = spreadsheet.add_worksheet(title='Assumptions', rows=50, cols=5)
    
    data = [
        ['FINANCIAL ASSUMPTIONS', '', '', '', ''],
        ['', '', '', '', ''],
        ['Revenue Assumptions', '', '', '', ''],
        ['Initial Investment', assumptions.get('initial_investment', 50000), '', '', ''],
        ['Year 1 Customers', assumptions.get('year1_customers', 100), '', '', ''],
        ['Annual Customer Growth Rate', f"{assumptions.get('customer_growth_rate', 0.5) * 100}%", '', '', ''],
        ['Avg Revenue per Customer (Annual)', assumptions.get('avg_revenue_per_customer', 1200), '', '', ''],
        ['Cost of Goods Sold (%)', f"{assumptions.get('cogs_percent', 0.20) * 100}%", '', '', ''],
        ['', '', '', '', ''],
        ['Fixed Costs (Annual)', '', '', '', ''],
    ]
    
    for cost_name, cost_value in fixed_costs.items():
        data.append([cost_name, cost_value, '', '', ''])
    
    data.append(['', '', '', '', ''])
    data.append(['Variable Costs (% of Revenue)', '', '', '', ''])
    
    for cost_name, cost_rate in variable_costs.items():
        data.append([cost_name, f"{cost_rate * 100}%", '', '', ''])
    
    sheet.update('A1', data)
    
    # Format header
    sheet.format('A1', {'textFormat': {'bold': True, 'fontSize': 14}})
    sheet.format('A3', {'textFormat': {'bold': True}})
    sheet.format('A10', {'textFormat': {'bold': True}})


def create_revenue_sheet(spreadsheet, projections, years):
    """Create the Revenue Projections sheet."""
    sheet = spreadsheet.add_worksheet(title='Revenue', rows=20, cols=years + 2)
    
    # Headers
    headers = ['Metric'] + [f'Year {y}' for y in range(1, years + 1)]
    
    data = [
        headers,
        ['Customers'] + projections['customers'],
        ['Revenue'] + [f"" for x in projections['revenue']],
        ['Avg Revenue/Customer'] + [f"" for i in range(years)],
        ['YoY Growth'] + ['N/A'] + [f"{((projections['revenue'][i]/projections['revenue'][i-1])-1)*100:.1f}%" for i in range(1, years)]
    ]
    
    sheet.update('A1', data)
    sheet.format('A1:F1', {'textFormat': {'bold': True}})


def create_expenses_sheet(spreadsheet, projections, fixed_costs, variable_costs, years):
    """Create the Expenses Breakdown sheet."""
    sheet = spreadsheet.add_worksheet(title='Expenses', rows=30, cols=years + 2)
    
    headers = ['Expense Category'] + [f'Year {y}' for y in range(1, years + 1)]
    
    data = [headers, ['FIXED COSTS', '', '', '', '', '']]
    
    for cost_name, cost_value in fixed_costs.items():
        data.append([cost_name] + [f""] * years)
    
    data.append(['Total Fixed Costs'] + [f"" for x in projections['fixed_costs_total']])
    data.append(['', '', '', '', '', ''])
    data.append(['VARIABLE COSTS', '', '', '', '', ''])
    
    for cost_name, cost_rate in variable_costs.items():
        row = [cost_name] + [f"" for i in range(years)]
        data.append(row)
    
    data.append(['Total Variable Costs'] + [f"" for x in projections['variable_costs_total']])
    data.append(['', '', '', '', '', ''])
    data.append(['TOTAL OPERATING EXPENSES'] + [f"" for x in projections['operating_expenses']])
    
    sheet.update('A1', data)
    sheet.format('A1:F1', {'textFormat': {'bold': True}})
    sheet.format('A2', {'textFormat': {'bold': True}})


def create_pnl_sheet(spreadsheet, projections, years):
    """Create the Profit & Loss sheet."""
    sheet = spreadsheet.add_worksheet(title='Profit & Loss', rows=20, cols=years + 2)
    
    headers = ['Line Item'] + [f'Year {y}' for y in range(1, years + 1)]
    
    data = [
        headers,
        ['Revenue'] + [f"" for x in projections['revenue']],
        ['Cost of Goods Sold'] + [f"" for x in projections['cogs']],
        ['Gross Profit'] + [f"" for x in projections['gross_profit']],
        ['Gross Margin'] + [f"{x:.1f}%" for x in projections['gross_margin']],
        ['', '', '', '', '', ''],
        ['Operating Expenses'] + [f"" for x in projections['operating_expenses']],
        ['', '', '', '', '', ''],
        ['Net Income'] + [f"" for x in projections['net_income']],
        ['Net Margin'] + [f"{x:.1f}%" for x in projections['net_margin']]
    ]
    
    sheet.update('A1', data)
    sheet.format('A1:F1', {'textFormat': {'bold': True}})
    sheet.format('A4', {'textFormat': {'bold': True}})
    sheet.format('A9', {'textFormat': {'bold': True}})


def create_cashflow_sheet(spreadsheet, projections, initial_investment, years):
    """Create the Cash Flow sheet."""
    sheet = spreadsheet.add_worksheet(title='Cash Flow', rows=15, cols=years + 2)
    
    headers = ['Item'] + [f'Year {y}' for y in range(1, years + 1)]
    
    # Calculate cash flow items
    beginning_cash = [initial_investment] + projections['cumulative_cash'][:-1]
    
    data = [
        headers,
        ['Beginning Cash'] + [f"" for x in beginning_cash],
        ['Net Income'] + [f"" for x in projections['net_income']],
        ['Ending Cash'] + [f"" for x in projections['cumulative_cash']],
        ['', '', '', '', '', ''],
        ['Cumulative P/L'] + [f"" for i in range(years)]
    ]
    
    sheet.update('A1', data)
    sheet.format('A1:F1', {'textFormat': {'bold': True}})
    sheet.format('A4', {'textFormat': {'bold': True}})


def create_metrics_sheet(spreadsheet, projections, assumptions, years):
    """Create the Key Metrics sheet."""
    sheet = spreadsheet.add_worksheet(title='Key Metrics', rows=20, cols=years + 2)
    
    # Calculate metrics
    cac = assumptions.get('customer_acquisition_cost', 200)
    avg_rev = assumptions.get('avg_revenue_per_customer', 1200)
    churn = assumptions.get('annual_churn_rate', 0.10)
    ltv = avg_rev / churn if churn > 0 else avg_rev * 5
    
    headers = ['Metric'] + [f'Year {y}' for y in range(1, years + 1)]
    
    data = [
        headers,
        ['Customer Acquisition Cost (CAC)', f""] + [''] * (years - 1),
        ['Customer Lifetime Value (LTV)', f""] + [''] * (years - 1),
        ['LTV:CAC Ratio', f"{ltv/cac:.1f}x"] + [''] * (years - 1),
        ['', '', '', '', '', ''],
        ['Customers'] + projections['customers'],
        ['Revenue'] + [f"" for x in projections['revenue']],
        ['Gross Margin'] + [f"{x:.1f}%" for x in projections['gross_margin']],
        ['Net Margin'] + [f"{x:.1f}%" for x in projections['net_margin']],
        ['', '', '', '', '', ''],
        ['Break-even Analysis', '', '', '', '', '']
    ]
    
    # Find break-even year
    breakeven_year = None
    for i, cash in enumerate(projections['cumulative_cash']):
        if cash > 0 and i > 0:
            breakeven_year = i + 1
            break
    
    if breakeven_year:
        data.append([f'Projected Break-even', f'Year {breakeven_year}'] + [''] * (years - 1))
    else:
        data.append(['Projected Break-even', 'Not within projection period'] + [''] * (years - 1))
    
    sheet.update('A1', data)
    sheet.format('A1:F1', {'textFormat': {'bold': True}})
    sheet.format('A11', {'textFormat': {'bold': True}})


def main():
    parser = argparse.ArgumentParser(description='Create 5-year financial projections spreadsheet')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--assumptions-file', help='Path to JSON file with assumptions')
    parser.add_argument('--initial-investment', type=float, default=50000, help='Initial investment amount')
    parser.add_argument('--year1-customers', type=int, default=100, help='Year 1 customer count')
    parser.add_argument('--growth-rate', type=float, default=0.5, help='Annual customer growth rate (0.5 = 50%%)')
    parser.add_argument('--avg-revenue', type=float, default=1200, help='Average annual revenue per customer')
    parser.add_argument('--cogs', type=float, default=0.20, help='Cost of goods sold as %% of revenue')
    parser.add_argument('--years', type=int, default=5, help='Number of years to project')
    parser.add_argument('--folder-id', help='Google Drive folder ID')
    parser.add_argument('--output', help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Build assumptions dictionary
    if args.assumptions_file and os.path.exists(args.assumptions_file):
        with open(args.assumptions_file, 'r') as f:
            assumptions = json.load(f)
    else:
        assumptions = {
            'initial_investment': args.initial_investment,
            'year1_customers': args.year1_customers,
            'customer_growth_rate': args.growth_rate,
            'avg_revenue_per_customer': args.avg_revenue,
            'cogs_percent': args.cogs
        }
    
    try:
        result = create_financial_spreadsheet(
            company_name=args.company,
            assumptions=assumptions,
            years=args.years,
            folder_id=args.folder_id
        )
        
        print(f"\n Spreadsheet created successfully!")
        print(f"URL: {result['url']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to: {args.output}")
        
        return result
        
    except Exception as e:
        print(f"Error creating spreadsheet: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
