# RapidTools Financial Model - Template Reference

> **Template Spreadsheet ID:** 1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY
> **Template URL:** https://docs.google.com/spreadsheets/d/1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY/edit
> **Last Updated:** January 2026
> 
> **This template should be used as the standard structure for all future financial models.**

---

## How to Use This Template

### Option 1: Copy the Template
1. Open the template URL above
2. File → Make a Copy
3. Rename for your new business
4. Update the Assumptions and Sources sheets with new data

### Option 2: Reference for New Models
When creating a new financial model from scratch:
1. Follow the 14-sheet structure below
2. Use the same row layouts for formula compatibility
3. Apply the same formatting standards (colors, fonts)
4. Maintain cross-sheet linkage patterns

---

## Key Principles

### Formula Linkage Hierarchy
```
Sources & References (Market Research)
    ↓
Assumptions (All Input Parameters)
    ↓
Revenue = Assumptions!Price × Assumptions!Volume
    ↓
Operating Costs = Revenue × COGS% + Fixed Costs + S&M
    ↓
P&L = Revenue - Costs - Depreciation - Interest - Tax
    ↓
Cash Flow = PAT + Depreciation - WC Change + Funding
    ↓
Balance Sheet = Cumulative Cash + Fixed Assets = Liabilities + Equity
```

### No Hardcoded Values
- ALL calculated values must use formulas
- Only Assumptions sheet contains input values
- Sources & References provides linkable market data

---

## Sheet Overview (14 Sheets)

| # | Sheet Name | Purpose |
|---|------------|---------|
| 1 | Sources & References | TAM/SAM/SOM data with sources, linkable values |
| 2 | Assumptions | All input parameters, revenue streams, costs |
| 3 | Headcount Plan | Team growth by department, salary costs |
| 4 | Revenue | Multi-stream revenue calculations |
| 5 | Operating Costs | COGS, Fixed Costs, S&M |
| 6 | P&L | Profit & Loss with margins |
| 7 | Cash Flow | Operating, Investing, Financing |
| 8 | Balance Sheet | Assets, Liabilities, Equity |
| 9 | Summary | KPI dashboard |
| 10 | Sensitivity Analysis | Scenario modeling |
| 11 | Valuation | DCF and multiples |
| 12 | Break-even Analysis | Contribution margin analysis |
| 13 | Funding Cap Table | Equity rounds and dilution |
| 14 | Charts Data | Data for embedded charts |

---

## Detailed Sheet Structures

### Assumptions

| Row | Column A | Column B | Notes |
|-----|----------|----------|-------|
| 1 | Assumptions |  | |
| 3 | GENERAL PARAMETERS |  | |
| 4 | Tax Rate | % | |
| 5 | Capex | $ | |
| 6 | Depreciation Years | yrs | |
| 7 | Debtor Days | days | |
| 8 | Creditor Days | days | |
| 9 | Interest Rate | Year 0 | |
| 10 | Equity Infusion |  | |
| 11 | Debt Drawdown |  | |
| 12 | Cost Inflation Rate |  | |
| 14 | REVENUE STREAMS |  | |
| 15 | Software Subscription: Price | $ | |
| 16 | Software Subscription: Volume | seats | |
| 17 | Software Subscription: Growth | % | |
| 18 | Software Subscription: COGS % |  | |
| 19 | 3D Printer Sales: Price |  | |
| 20 | 3D Printer Sales: Volume | units | |
| 21 | 3D Printer Sales: Growth |  | |
| 22 | 3D Printer Sales: COGS % |  | |
| 23 | Consumables Materials: Price |  | |
| 24 | Consumables Materials: Volume | units | |
| 25 | Consumables Materials: Growth |  | |
| 26 | Consumables Materials: COGS % |  | |
| 27 | AMC Spares: Price |  | |
| 28 | AMC Spares: Volume | contracts | |
| 29 | AMC Spares: Growth |  | |
| 30 | AMC Spares: COGS % |  | |
| 31 | Managed Services: Price |  | |
| 32 | Managed Services: Volume | contracts | |
| 33 | Managed Services: Growth |  | |
| 34 | Managed Services: COGS % |  | |
| 35 | Job Work Services: Price |  | |
| 36 | Job Work Services: Volume |  | |
| 37 | Job Work Services: Growth |  | |
| 38 | Job Work Services: COGS % |  | |
| 40 | FIXED COSTS (Annual) |  | |

---

### Revenue

| Row | Column A | Column B | Notes |
|-----|----------|----------|-------|
| 1 | REVENUE |  | |
| 3 | Software Subscription | $ | |
| 4 | 3D Printer Sales | $ | |
| 5 | Consumables Materials | $ | |
| 6 | AMC Spares | $ | |
| 7 | Managed Services | $ | |
| 8 | Job Work Services |  | |
| 10 | TOTAL REVENUE | $ | |
| 12 | Revenue Mix |  | |
| 13 | Software Subscription % | % | |
| 14 | 3D Printer Sales % | % | |
| 15 | Consumables Materials % | % | |
| 16 | AMC Spares % | % | |
| 17 | Managed Services % | % | |
| 18 | Job Work Services % |  | |

---

### Operating Costs

| Row | Column A | Column B | Notes |
|-----|----------|----------|-------|
| 1 | OPERATING COSTS |  | |
| 3 | COST OF GOODS SOLD |  | |
| 4 | COGS: Software Subscription | $ | |
| 5 | COGS: 3D Printer Sales | $ | |
| 6 | COGS: Consumables Materials | $ | |
| 7 | COGS: AMC Spares | $ | |
| 8 | COGS: Managed Services | $ | |
| 9 | COGS: Job Work Services |  | |
| 10 | Total COGS | $ | |
| 12 | FIXED COSTS |  | |
| 13 | Salaries and Benefits | $ | |
| 14 | Office and Coworking | $ | |
| 15 | Warehouse and Depot | $ | |
| 16 | Utilities | $ | |
| 17 | Software Cloud Internal | $ | |
| 18 | RD Product Development | $ | |
| 19 | Legal and Compliance | $ | |
| 20 | Insurance | $ | |
| 21 | Travel Trade Shows | $ | |
| 22 | Marketing Content | $ | |
| 23 | Total Fixed Costs | $ | |
| 25 | SALES & MARKETING |  | |
| 26 | Customer Acquisition Cost | $ | |
| 28 | TOTAL |  | |
| 29 | TOTAL OPERATING COSTS | $ | |

---

### P&L

| Row | Column A | Column B | Notes |
|-----|----------|----------|-------|
| 1 | PROFIT & LOSS |  | |
| 3 | REVENUE |  | |
| 4 | Software Subscription | $ | |
| 5 | 3D Printer Sales | $ | |
| 6 | Consumables Materials | $ | |
| 7 | AMC Spares | $ | |
| 8 | Managed Services | $ | |
| 9 | Job Work Services | $ | |
| 10 | Total Revenue | $ | |
| 12 | COST OF GOODS SOLD |  | |
| 13 | Total COGS | $ | |
| 15 | GROSS PROFIT |  | |
| 16 | Gross Profit | $ | |
| 17 | Gross Margin % | % | |
| 19 | OPERATING EXPENSES |  | |
| 20 | Fixed Costs | $ | |
| 21 | Sales & Marketing | $ | |
| 22 | Total Operating Expenses | $ | |
| 24 | EBITDA |  | |
| 25 | EBITDA | $ | |
| 26 | EBITDA Margin % | % | |
| 28 | Depreciation & Amortization | $ | |
| 30 | EBIT (Operating Profit) | $ | |
| 32 | Interest Expense | $ | |
| 33 | PBT (Profit Before Tax) | $ | |
| 34 | Tax (25%) | $ | |
| 35 | NET INCOME |  | |
| 36 | PAT (Net Income) | $ | |
| 37 | Net Margin % | % | |

---

### Sources & References

| Row | Column A | Column B | Notes |
|-----|----------|----------|-------|
| 1 | Sources & References - RapidTools Financial Model |  | |
| 3 | SECTION A: KEY METRICS (Linkable Values) |  | |
| 5 | TAM - Total Addressable Market |  | |
| 6 | Metric | Value | |
| 7 | Dies, Jigs & Tools Market 2024 | $60,180 M | |
| 8 | EOAT Market 2024 | $2,600 M | |
| 9 | Industrial 3D Printing 2024 | $3,560 M | |
| 10 | 3D Printing Services 2024 | $9,830 M | |
| 11 | Sand Casting Market 2024 | $345,500 M | |
| 12 | Vacuum Casting Market 2024 | $2,560 M | |
| 13 | Palletizing Equipment 2024 | $2,900 M | |
| 14 | Workholding Devices 2024 | $4,440 M | |
| 15 | Global Tooling Market 2024 | $273,890 M | |
| 17 | Design Automation Software TAM (10 Modules) |  | |
| 18 | Module | Software TAM ($M) | |
| 19 | 1. Jigs & Fixtures | $181 M | |
| 20 | 2. Assembly Guides | $60 M | |
| 21 | 3. Drilling Guides | $48 M | |
| 22 | 4. Alignment Tools | $30 M | |
| 23 | 5. Shadow Boxes | $18 M | |
| 24 | 6. Custom Palletizing | $44 M | |
| 25 | 7. Sand Casting Tools | $69 M | |
| 26 | 8. Vacuum Casting Tools | $51 M | |
| 27 | 9. Soft Jaws | $9 M | |
| 28 | 10. EOAT | $52 M | |
| 29 | SOFTWARE TAM TOTAL | $562 M | |
| 31 | Hardware & Services TAM |  | |
| 32 | Revenue Stream | TAM ($M) | |
| 33 | 3D Printers (Hardware) | $534 M | |
| 34 | Consumables | $313 M | |
| 35 | Job Work Services | $492 M | |
| 36 | Managed Services | $197 M | |
| 37 | HARDWARE & SERVICES TAM | $1,535 M | |
| 39 | TOTAL RapidTools TAM | $2,097 M | |

---



---

## Critical Formula Patterns

### Revenue Sheet Formulas

| Cell | Formula Pattern | Description |
|------|-----------------|-------------|
| C3 (Software Rev) | =Assumptions!C15*Assumptions!C16 | Price x Volume |
| C4 (Printer Rev) | =Assumptions!C19*Assumptions!C20 | Price x Volume |
| C10 (Total Rev) | =SUM(C3:C9) | Sum all streams |
| C13 (Software pct) | =C3/C10 | Revenue mix |

### P&L Formulas

| Cell | Formula Pattern | Description |
|------|-----------------|-------------|
| C10 (Total Rev) | =Revenue!C10 | Link to Revenue |
| C13 (Total COGS) | =Operating Costs!C12 | Link to Op Costs |
| C16 (Gross Profit) | =C10-C13 | Revenue - COGS |
| C17 (Gross Margin) | =C16/C10 | GP / Revenue |
| C25 (EBITDA) | =C16-C22 | GP - OpEx |
| C36 (PAT) | =C33-C34 | PBT - Tax |

---

## Formatting Standards

### Color Palette (RGB 0-1 scale)

| Name | RGB Values | Hex | Usage |
|------|------------|-----|-------|
| Title Blue | (0.20, 0.30, 0.50) | #335080 | Main titles |
| Section Blue | (0.20, 0.40, 0.60) | #336699 | Section headers |
| Category Blue | (0.30, 0.50, 0.70) | #4D80B3 | Category headers |
| Light Blue | (0.85, 0.92, 0.98) | #D8EAF9 | Zebra stripe |
| Light Green | (0.90, 0.97, 0.90) | #E5F8E5 | Total rows |

### Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Currency (K) | dollar#,##0K | dollar1,234K |
| Percentage | 0.0pct | 25.5pct |
| Integer | #,##0 | 1,234 |

---

## Validation Checklist

Before finalizing any financial model:

- Balance Sheet balances (A = L + E) for all years
- Cash Flow cumulative = Balance Sheet cash
- PAT flows correctly to Retained Earnings
- All Sources and References values have URLs
- No hardcoded values in calculated sheets
- All revenue streams appear in P and L and Charts
- Growth formulas handle Y0 (avoid DIV/0 errors)

