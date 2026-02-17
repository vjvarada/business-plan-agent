# Financial Model Master Template

> **MASTER TEMPLATE - Use this for ALL new financial models**
>
> **Template Spreadsheet ID:** `1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY`
> **Template URL:** https://docs.google.com/spreadsheets/d/1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY/edit
> **Master Snapshot:** `.tmp/rapidtools/snapshots/template_master/`
> **Last Updated:** February 2026
> 
> **This template MUST be used as the standard structure for all new financial models.**

---

## Quick Start: Creating a New Financial Model

### Mandatory Precondition

Before creating a model, freeze these inputs in `.tmp/<project>/config/<project>_config.json`:
- Revenue streams (name, price, volume, growth, COGS%)
- Fixed costs and inflation assumptions
- Customer assumptions (CAC, churn, new customers)
- Funding schedule (equity/debt by year)
- Working capital assumptions (debtor/creditor days)

### Option 1: Copy the Template (Recommended)
```bash
# 1. Open Google Sheets template and make a copy
#    File → Make a Copy → Rename for new company

# 2. Download snapshot for local editing reference
python execution/download_model_snapshot.py \
  --sheet-id "YOUR_NEW_SHEET_ID" \
  --output .tmp/<new_project>/snapshots/initial

# 3. Update Assumptions sheet with new business parameters
# 4. Update Sources & References with new market research
# 5. All other sheets auto-calculate via formulas
```

### Option 2: Local-First Creation (Advanced)
```bash
# 1. Copy master snapshot as starting point
cp -r .tmp/rapidtools/snapshots/template_master .tmp/<new_project>/snapshots/base

# 2. Edit CSV files with new business data
# 3. Validate formulas
python execution/validate_model_snapshot.py --snapshot .tmp/<new_project>/snapshots/base

# 4. Upload to Google Sheets
python execution/sync_snapshot_to_sheets.py \
  --snapshot .tmp/<new_project>/snapshots/base \
  --sheet-id "NEW_SHEET_ID" \
  --apply
```

### Option 3: Scripted Template Copy + Validation (Canonical for Agents)

```bash
# 1. Create model from master template (14-sheet fidelity)
python execution/create_financial_model.py \
  --company "<CompanyName>" \
  --config .tmp/<project>/config/<project>_config.json \
  --from-template

# 2. Validate template fidelity + integrity (Gate 1)
python execution/verify_template_copy.py --sheet-id "<SHEET_ID>"
python execution/audit_financial_model.py --mode comprehensive --sheet-id "<SHEET_ID>"
python execution/verify_sheet_integrity.py --sheet-id "<SHEET_ID>"
```

### Option 4: Local Excel Draft Build (Non-Canonical)

Use `execution/create_financial_model_local.py` only for offline prototype drafts; it is not the production 14-sheet baseline.

### Step-Gated Build Order (Required)

Build and verify in this exact dependency order:
1. Sources & References
2. Assumptions
3. Revenue, Headcount Plan, Operating Costs
4. P&L
5. Cash Flow
6. Balance Sheet
7. Summary, Sensitivity, Funding Cap Table, Valuation, Break-even, Charts Data

If any upstream block fails validation, stop and fix before proceeding.

### Required Data Packages (Industry Standard)

Before final model sign-off, maintain these data packages:

1. **Market Sizing Pack**
  - TAM/SAM/SOM calculations
  - Source links and confidence labels
  - Assumption notes for estimated values

2. **Revenue Driver Pack**
  - Price/volume/growth/churn inputs by stream and year
  - Stream formulas and penetration reconciliation to SOM

3. **Cost Driver Pack**
  - COGS logic by stream
  - Headcount and salary schedules
  - Fixed cost and CAC/S&M schedules

4. **Assumption Register**
  - Master list of all key assumptions with source/rationale, confidence, and last update

5. **Validation Pack**
  - Formula integrity results
  - Balance Sheet check status
  - Linkage audit outcomes

### Stage Sign-Off Requirement

For each dependency stage, provide a concise sign-off note with:
- What was collected
- What was derived
- What remains uncertain
- Proceed/revise decision

Do not advance to downstream stages without explicit sign-off.

### Incremental Persistence Requirement

At each stage boundary, persist and validate before moving on:
- Write stage outputs to the business-plan section artifact
- Write stage outputs to the corresponding model sheets
- Re-run stage checks to verify dependency propagation

Do not defer updates and apply them in a single final pass.

---

## Architecture: Data Flow Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SOURCES & REFERENCES                                        │
│     • TAM/SAM/SOM market sizing                                 │
│     • Industry benchmarks                                       │
│     • Linkable values for Assumptions                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. ASSUMPTIONS (Single Source of Truth)                        │
│     • General Parameters (tax, capex, depreciation)             │
│     • Revenue Streams (price × volume × growth)                 │
│     • Fixed Costs (salaries, office, marketing)                 │
│     • Customer Acquisition (CAC, churn, lifetime)               │
│     • Geographic Expansion                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
     ┌────────────────────────┼────────────────────────┐
     ↓                        ↓                        ↓
┌──────────┐          ┌───────────────┐         ┌──────────────┐
│ REVENUE  │          │ HEADCOUNT     │         │ OPERATING    │
│ Price×Vol│          │ PLAN          │         │ COSTS        │
│ by stream│          │ Salaries      │         │ COGS+Fixed   │
└──────────┘          └───────────────┘         └──────────────┘
     │                        │                        │
     └────────────────────────┼────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  P&L: Revenue - COGS - Fixed Costs - D&A - Interest - Tax       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  CASH FLOW: PAT + D&A - Working Capital + Funding               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  BALANCE SHEET: Assets = Liabilities + Equity (Must Balance!)   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
     ┌──────────────────┬─────────────────┬────────────────────┐
     ↓                  ↓                 ↓                    ↓
┌─────────┐      ┌───────────┐     ┌──────────┐        ┌───────────┐
│ SUMMARY │      │ VALUATION │     │ BREAK-   │        │ FUNDING   │
│ KPIs    │      │ DCF/MOIC  │     │ EVEN     │        │ CAP TABLE │
└─────────┘      └───────────┘     └──────────┘        └───────────┘
```

### Critical Rule: NO HARDCODED VALUES
- **Assumptions sheet** = Only place with input values
- **All other sheets** = 100% formulas referencing Assumptions
- **Sources & References** = Market data that feeds Assumptions

---

## 14-Sheet Structure (Exact Specifications)

| # | Sheet Name | Rows | Cols | Purpose |
|---|------------|------|------|---------|
| 1 | Sources & References | 195 | 5 | TAM/SAM/SOM, benchmarks, sources |
| 2 | Assumptions | 83 | 8 | All input parameters |
| 3 | Headcount Plan | 84 | 8 | Team growth, salaries |
| 4 | Revenue | 18 | 8 | Revenue by stream |
| 5 | Operating Costs | 29 | 8 | COGS + Fixed + S&M |
| 6 | P&L | 37 | 8 | Profit & Loss statement |
| 7 | Cash Flow | 15 | 8 | 3-section cash flow |
| 8 | Balance Sheet | 16 | 8 | A = L + E |
| 9 | Summary | 41 | 8 | KPI dashboard |
| 10 | Sensitivity Analysis | 35 | 7 | Scenarios |
| 11 | Funding Cap Table | 27 | 8 | Equity tracking |
| 12 | Valuation | 49 | 5 | DCF + multiples |
| 13 | Break-even Analysis | 32 | 8 | Contribution margin |
| 14 | Charts Data | 54 | 7 | Data for visualizations |

---

## Detailed Sheet Structures

### Sheet 1: Sources & References (195 rows × 5 cols)

**Purpose:** Market research data with linkable values for Assumptions sheet.

**Structure:**
```
SECTION A: KEY METRICS (Rows 3-90)
├── TAM - Total Addressable Market (Rows 5-49)
│   ├── Base Markets (Rows 7-15): Global market sizes with sources
│   ├── Software TAM by Module (Rows 17-29): 10 software modules
│   ├── Hardware & Services TAM (Rows 31-39): 4 revenue streams
│   └── Company Derivation (Rows 41-49): TAM validation
├── SAM - Regional Breakdown (Rows 51-75)
│   ├── India SAM (Rows 53-56)
│   ├── SE Asia SAM (Rows 58-61)
│   ├── MENA SAM (Rows 63-66)
│   ├── Europe SAM (Rows 68-71)
│   └── Total SAM (Rows 73-75)
└── SOM - Serviceable Obtainable (Rows 77-90)
    ├── Penetration rates by year
    └── Customer projections

SECTION B: FULL SOURCE DOCUMENTATION (Rows 93-195)
├── Market Research Sources
├── Regional Data Sources
├── Competitor Research
└── Industry Benchmarks (Churn, LTV, CAC)
```

---

### Sheet 2: Assumptions (83 rows × 8 cols)

**Purpose:** Single source of truth for all input parameters.

| Row Range | Section | Contents |
|-----------|---------|----------|
| 1-2 | Header | "Assumptions", Year labels (Y0-Y5) |
| 3-12 | GENERAL PARAMETERS | Tax Rate, Capex, Depreciation, Days, Interest, Equity, Debt |
| 14-38 | REVENUE STREAMS | 6 streams × 4 rows each (Price, Volume, Growth, COGS%) |
| 40-50 | FIXED COSTS | 10 cost categories with annual values |
| 52-60 | CUSTOMER ACQUISITION | CAC, New/Churned Customers, Churn Rate, Lifetime |
| 62-71 | GEOGRAPHIC EXPANSION | Revenue % by region (India, SE Asia, MENA, Europe, Americas) |
| 73-78 | INDUSTRY SEGMENTS | % by vertical (Auto, Aerospace, Medical, Electronics) |
| 80-83 | KEY RELATIONSHIPS | Strategic partner status tracking |

**Revenue Stream Template (4 rows per stream):**
```
Row N:   [Stream Name]: Price      $       $1,500    $1,500    ...
Row N+1: [Stream Name]: Volume     units   100       200       ...
Row N+2: [Stream Name]: Growth     %       0%        100%      ...
Row N+3: [Stream Name]: COGS %             15%       15%       ...
```

---

### Sheet 3: Headcount Plan (84 rows × 8 cols)

**Purpose:** Team growth and salary costs with regional premiums.

| Row Range | Section | Contents |
|-----------|---------|----------|
| 1-3 | Header | Title, description |
| 4-12 | PARAMETERS | Annual salary growth (15%), Regional premiums (India 0%, SE Asia 25%, MENA 46%, Europe 88%, Americas 117%) |
| 14-23 | BASE SALARY RATES | 9 role categories with base rates |
| 25-34 | SALARY RATES BY YEAR | Base × (1 + growth)^year |
| 36-44 | TEAM HEADCOUNT | Headcount by role per year |
| 46-52 | REGIONAL MANAGERS | Managers by region per year |
| 54 | TOTAL HEADCOUNT | Sum of all roles |
| 56-72 | SALARY COSTS | Cost per role = Headcount × Salary Rate |
| 74 | TOTAL PEOPLE COST | Sum of all salary costs |
| 76-78 | EFFICIENCY METRICS | Revenue per Employee, People Cost % |
| 80-84 | NOTES | Instructions for editing parameters |

**Key Formula:** `Salary Cost = Headcount × Base Rate × (1 + Growth)^Year × (1 + Regional Premium)`

---

### Sheet 4: Revenue (18 rows × 8 cols)

**Purpose:** Revenue calculations by stream.

| Row | Content | Formula Pattern |
|-----|---------|-----------------|
| 1-2 | Header | "REVENUE", Year labels |
| 3 | Software Subscription | `=Assumptions!C15*Assumptions!C16` |
| 4 | 3D Printer Sales | `=Assumptions!C19*Assumptions!C20` |
| 5 | Consumables Materials | `=Assumptions!C23*Assumptions!C24` |
| 6 | AMC Spares | `=Assumptions!C27*Assumptions!C28` |
| 7 | Managed Services | `=Assumptions!C31*Assumptions!C32` |
| 8 | Job Work Services | `=Assumptions!C35*Assumptions!C36` |
| 10 | **TOTAL REVENUE** | `=SUM(C3:C8)` |
| 12-18 | Revenue Mix % | `=C3/$C$10` per stream |

---

### Sheet 5: Operating Costs (29 rows × 8 cols)

**Purpose:** COGS by stream + Fixed costs + S&M spend.

| Row Range | Section | Formula Pattern |
|-----------|---------|-----------------|
| 3-10 | COST OF GOODS SOLD | `=Revenue × COGS%` per stream |
| 10 | Total COGS | `=SUM(C4:C9)` |
| 12-23 | FIXED COSTS | Links to Assumptions!C41:C50 |
| 23 | Total Fixed Costs | `=SUM(C13:C22)` |
| 25-26 | SALES & MARKETING | CAC Spend from Assumptions |
| 29 | **TOTAL OPERATING COSTS** | `=C10+C23+C26` |

---

### Sheet 6: P&L (37 rows × 8 cols)

**Purpose:** Full Profit & Loss statement.

| Row | Line Item | Formula |
|-----|-----------|---------|
| 4-9 | Revenue by stream | `=Revenue!C3:C8` |
| 10 | **Total Revenue** | `=Revenue!C10` |
| 13 | Total COGS | `='Operating Costs'!C10` |
| 16 | **Gross Profit** | `=C10-C13` |
| 17 | Gross Margin % | `=C16/C10` |
| 20 | Fixed Costs | `='Operating Costs'!C23` |
| 21 | Customer Acquisition | `='Operating Costs'!C26` |
| 22 | Total OpEx | `=C20+C21` |
| 25 | **EBITDA** | `=C16-C22` |
| 26 | EBITDA Margin % | `=C25/C10` |
| 28 | D&A | `=Assumptions!C5/Assumptions!C6` |
| 30 | **EBIT** | `=C25-C28` |
| 32 | Interest | `=Assumptions!C9*'Balance Sheet'!C12` |
| 33 | **PBT** | `=C30-C32` |
| 34 | Tax | `=MAX(0,C33*Assumptions!C4)` |
| 36 | **PAT (Net Income)** | `=C33-C34` |
| 37 | Net Margin % | `=C36/C10` |

---

### Sheet 7: Cash Flow (15 rows × 8 cols)

**Purpose:** 3-section cash flow statement.

| Row | Line Item | Formula |
|-----|-----------|---------|
| 4 | PAT | `='P&L'!C36` |
| 5 | D&A (Add back) | `='P&L'!C28` |
| 6 | Change in Working Capital | `=(C_Debtors-B_Debtors)-(C_Creditors-B_Creditors)` |
| 7 | **Operating Cash Flow** | `=C4+C5-C6` |
| 10 | Capex | `=-Assumptions!C5` |
| 12 | Equity | `=Assumptions!C10` |
| 13 | Debt | `=Assumptions!C11` |
| 14 | **Net Cash Flow** | `=C7+C10+C12+C13` |
| 15 | **Cumulative Cash** | `=B15+C14` |

---

### Sheet 8: Balance Sheet (16 rows × 8 cols)

**Purpose:** Assets = Liabilities + Equity (MUST BALANCE!)

| Row | Line Item | Formula |
|-----|-----------|---------|
| 4 | Fixed Assets (Net) | `=B4+Capex-D&A` |
| 5 | Debtors | `=Revenue*Debtor_Days/365` |
| 6 | Cash | `='Cash Flow'!C15` |
| 7 | **Total Assets** | `=SUM(C4:C6)` |
| 10 | Creditors | `=COGS*Creditor_Days/365` |
| 11 | Equity | `=B11+New_Equity` |
| 12 | Debt | `=B12+New_Debt` |
| 13 | Retained Earnings | `=B13+PAT` |
| 14 | **Total Liab & Equity** | `=SUM(C10:C13)` |
| 16 | **Check (should be 0)** | `=C7-C14` ← CRITICAL VALIDATION |

---

### Sheet 9: Summary (41 rows × 8 cols)

**Purpose:** KPI Dashboard for quick reference.

| Section | Metrics |
|---------|---------|
| REVENUE | Total Revenue, Revenue Growth |
| PROFITABILITY | Gross Profit, Gross Margin, EBITDA, EBITDA Margin, Net Income, Net Margin |
| CASH & FUNDING | Cash Balance, Cash from Operations |
| CUSTOMERS | Total Customers, New Customers, Churned, Growth Rate |
| UNIT ECONOMICS | CAC, Total CAC Spend, ARPU (Annual/Monthly), Churn Rate, Lifetime, LTV, LTV:CAC, Payback |
| REVENUE MIX | Revenue by stream |

---

### Sheet 10: Sensitivity Analysis (35 rows × 7 cols)

**Purpose:** Scenario modeling (Base/Upside/Downside).

| Analysis Type | Variables |
|---------------|-----------|
| Revenue Sensitivity | ±10%, ±20% impact on EBITDA |
| COGS Sensitivity | ±5%, ±10% impact on Gross Margin |
| Growth Sensitivity | ±25%, ±50% growth rate scenarios |
| CAC Sensitivity | Impact on LTV:CAC ratio |

---

### Sheet 11: Funding Cap Table (27 rows × 8 cols)

**Purpose:** Equity rounds, dilution, and investor returns.

| Section | Contents |
|---------|----------|
| FUNDING ROUNDS | Equity/Debt raised per year, Cumulative |
| ROUND DETAILS | Pre-money, Post-money valuation, Round ownership % |
| CAP TABLE | Ownership % (Founders, Seed, Series A, Series B) |
| INVESTOR RETURNS | Exit valuation, Return per investor class, MOIC multiples |

---

### Sheet 12: Valuation (49 rows × 5 cols)

**Purpose:** DCF valuation and comparables.

| Section | Contents |
|---------|----------|
| DCF INPUTS | WACC, Terminal Growth, Risk-free Rate |
| PROJECTED CASH FLOWS | FCF by year |
| TERMINAL VALUE | Gordon Growth calculation |
| DCF VALUATION | NPV of cash flows + terminal |
| MULTIPLES VALUATION | Revenue multiples (3x-10x), EBITDA multiples |
| COMPARABLE ANALYSIS | Public comp valuations |

---

### Sheet 13: Break-even Analysis (32 rows × 8 cols)

**Purpose:** Contribution margin and break-even point.

| Section | Contents |
|---------|----------|
| REVENUE BREAKDOWN | Variable vs Fixed components |
| CONTRIBUTION MARGIN | Revenue - Variable Costs per unit |
| BREAK-EVEN POINT | Fixed Costs / Contribution Margin |
| MARGIN OF SAFETY | Current Revenue - Break-even Revenue |

---

### Sheet 14: Charts Data (54 rows × 7 cols)

**Purpose:** Data formatted for chart visualizations.

| Chart Type | Data Series |
|------------|-------------|
| Revenue Waterfall | Y0 → Y5 progression |
| Revenue Mix | Pie chart data by stream |
| P&L Trend | Revenue, GP, EBITDA, PAT lines |
| Cash Flow Trend | OCF, ICF, FCF bars |
| Customer Growth | Total, New, Churned lines |

---

## Critical Formula Patterns

### Cross-Sheet Linkages

| From Sheet | To Sheet | Cell Reference | Formula |
|------------|----------|----------------|---------|
| Assumptions | Revenue | Price × Volume | `=Assumptions!C15*Assumptions!C16` |
| Assumptions | Operating Costs | COGS % | `=Revenue!C3*Assumptions!C18` |
| Assumptions | Operating Costs | Fixed Costs | `=Assumptions!C41` |
| Assumptions | P&L | Tax Rate | `=Assumptions!C4` |
| Assumptions | Cash Flow | Capex | `=-Assumptions!C5` |
| Assumptions | Cash Flow | Equity | `=Assumptions!C10` |
| Assumptions | Balance Sheet | Debtor Days | `=Assumptions!C7` |
| Revenue | P&L | Total Revenue | `=Revenue!C10` |
| Revenue | Summary | Revenue | `=Revenue!C10` |
| Operating Costs | P&L | COGS | `='Operating Costs'!C10` |
| Operating Costs | P&L | Fixed | `='Operating Costs'!C23` |
| P&L | Cash Flow | PAT | `='P&L'!C36` |
| P&L | Cash Flow | D&A | `='P&L'!C28` |
| P&L | Balance Sheet | Retained | `='P&L'!C36` |
| Cash Flow | Balance Sheet | Cash | `='Cash Flow'!C15` |
| Headcount Plan | Operating Costs | Salaries | `='Headcount Plan'!C74` |

### Revenue Formulas (Column C example)
```
C3 = =Assumptions!$C$15*Assumptions!C16    (Software: Price × Volume)
C4 = =Assumptions!$C$19*Assumptions!C20    (Hardware: Price × Volume)
C5 = =Assumptions!$C$23*Assumptions!C24    (Consumables: Price × Volume)
C6 = =Assumptions!$C$27*Assumptions!C28    (AMC: Price × Volume)
C7 = =Assumptions!$C$31*Assumptions!C32    (Managed Services)
C8 = =Assumptions!$C$35*Assumptions!C36    (Job Work)
C10 = =SUM(C3:C8)                          (Total Revenue)
```

### P&L Formulas (Column C example)
```
C10 = =Revenue!C10                      (Total Revenue)
C13 = ='Operating Costs'!C10            (Total COGS)
C16 = =C10-C13                          (Gross Profit)
C17 = =C16/C10                          (Gross Margin %)
C22 = ='Operating Costs'!C23+'Operating Costs'!C26  (Total OpEx)
C25 = =C16-C22                          (EBITDA)
C28 = =Assumptions!$C$5/Assumptions!$C$6  (D&A)
C30 = =C25-C28                          (EBIT)
C33 = =C30-C32                          (PBT)
C34 = =MAX(0,C33*Assumptions!$C$4)      (Tax)
C36 = =C33-C34                          (PAT)
```

### Balance Sheet Validation Formula
```
C16 = =C7-C14    // Must equal 0 for all years!
```

---

## Formatting Standards

### Color Palette (RGB 0-1 scale)

| Name | RGB Values | Hex | Usage |
|------|------------|-----|-------|
| Title Blue | (0.20, 0.30, 0.50) | #335080 | Main titles (Row 1) |
| Section Blue | (0.20, 0.40, 0.60) | #336699 | Section headers |
| Category Blue | (0.30, 0.50, 0.70) | #4D80B3 | Category headers |
| Light Blue | (0.85, 0.92, 0.98) | #D8EAF9 | Zebra stripe (alternate rows) |
| Light Green | (0.90, 0.97, 0.90) | #E5F8E5 | Total/Summary rows |
| Light Gray | (0.95, 0.95, 0.95) | #F2F2F2 | Column headers |
| URL Blue | (0.10, 0.30, 0.70) | #1A4CB3 | Hyperlinks |

### Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Currency (large) | `$#,##0K` | $1,234K |
| Currency (small) | `$#,##0` | $1,234 |
| Percentage | `0.0%` | 25.5% |
| Integer | `#,##0` | 1,234 |
| Multiplier | `0.0x` | 3.5x |
| Years | `0.0` | 10.0 |

### Font Standards

| Element | Font | Size | Style |
|---------|------|------|-------|
| Sheet Title | Arial | 14pt | Bold |
| Section Header | Arial | 12pt | Bold |
| Category Header | Arial | 11pt | Bold |
| Data Row | Arial | 10pt | Normal |
| Total Row | Arial | 10pt | Bold |

---

## Validation Checklist

Before finalizing any financial model, verify:

### 1. Balance Sheet Equation
```bash
# Row 16 on Balance Sheet sheet must be $0K for ALL years
Check (Y0) = $0K ✓
Check (Y1) = $0K ✓
Check (Y2) = $0K ✓
...
```

### 2. Formula Consistency
- [ ] All Revenue cells use `=Assumptions!Price*Assumptions!Volume`
- [ ] All COGS cells use `=Revenue*COGS%`
- [ ] No hardcoded numbers in calculation sheets
- [ ] Year-over-year formulas copy correctly (relative references)

### 3. Cross-Sheet Links
- [ ] P&L!Revenue = Revenue!Total
- [ ] P&L!COGS = Operating Costs!Total COGS
- [ ] Cash Flow!PAT = P&L!PAT
- [ ] Balance Sheet!Cash = Cash Flow!Cumulative Cash

### 4. Unit Economics
- [ ] LTV:CAC > 3.0x (healthy)
- [ ] CAC Payback < 12 months
- [ ] Churn Rate realistic (5-15% for B2B SaaS)

### 5. Growth Realism
- [ ] Year-over-year growth decreases as company scales
- [ ] No >200% growth after Year 2
- [ ] Margins improve as scale increases

---

## Quick Reference Commands

### Download Fresh Snapshot
```bash
python execution/download_model_snapshot.py \
  --sheet-id "1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY" \
  --output .tmp/rapidtools/snapshots/$(date +%Y-%m-%d)
```

### Validate Model
```bash
python execution/validate_model_snapshot.py \
  --snapshot .tmp/rapidtools/snapshots/template_master
```

### Audit Financial Model
```bash
python execution/audit_financial_model.py \
  --sheet-id "YOUR_SHEET_ID" \
  --mode comprehensive
```

### Sync Changes Back
```bash
python execution/sync_snapshot_to_sheets.py \
  --snapshot .tmp/<project>/snapshots/edited \
  --sheet-id "YOUR_SHEET_ID" \
  --dry-run  # Preview first
  --apply    # Then apply
```

---

## Adapting for Different Businesses

### Revenue Streams
The template has 6 revenue streams. To customize:
1. Rename streams in Assumptions rows 15-38
2. Adjust COGS % for each stream
3. Update Revenue and Operating Costs sheet row labels
4. P&L will auto-update via formulas

### Fixed Costs
Add/remove cost categories in Assumptions rows 40-50:
1. Update row labels in Assumptions
2. Mirror changes in Operating Costs sheet
3. Ensure Total Fixed Costs formula includes all rows

### Geographic Expansion
Modify regions in Assumptions rows 62-71:
1. Update region names and percentages
2. Headcount Plan regional premiums (rows 7-12) auto-adjust salaries
3. Update regional manager distribution (rows 46-52)

### Industry Segments
Change verticals in Assumptions rows 73-78:
1. Update segment names
2. Adjust percentages to equal 100%

---

## Template Files Reference

| File | Location | Purpose |
|------|----------|---------|
| Master Snapshot | `.tmp/rapidtools/snapshots/template_master/` | CSV + formulas for all 14 sheets |
| Snapshot JSON | `.tmp/rapidtools/snapshots/template_master/snapshot.json` | Sheet metadata |
| Config Template | `.tmp/rapidtools/config/rapidtools_config.json` | Business parameters |
| Sample Business Plan | `.tmp/rapidtools/business_plan/sections/` | 11 markdown sections |

---

*Last Updated: February 2026*
