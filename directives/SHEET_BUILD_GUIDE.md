# Financial Model — Sheet Build Guide

> **Purpose:** Authoritative reference for building each of the 14 financial model sheets.
> Every sheet's structure, formulas, formatting, and cross-sheet dependencies are
> defined here. The agent and the builder script (`execution/build_financial_model.py`)
> both follow this guide.
>
> **Last Updated:** 2026-02-17

---

## Table of Contents

1. [Config Schema](#config-schema)
2. [Build Order & Dependencies](#build-order--dependencies)
3. [Color Palette & Formatting Standards](#color-palette--formatting-standards)
4. [Sheet 1 — Sources & References](#sheet-1--sources--references)
5. [Sheet 2 — Assumptions](#sheet-2--assumptions)
6. [Sheet 3 — Headcount Plan](#sheet-3--headcount-plan)
7. [Sheet 4 — Revenue](#sheet-4--revenue)
8. [Sheet 5 — Operating Costs](#sheet-5--operating-costs)
9. [Sheet 6 — P&L](#sheet-6--pl)
10. [Sheet 7 — Cash Flow](#sheet-7--cash-flow)
11. [Sheet 8 — Balance Sheet](#sheet-8--balance-sheet)
12. [Sheet 9 — Summary](#sheet-9--summary)
13. [Sheet 10 — Sensitivity Analysis](#sheet-10--sensitivity-analysis)
14. [Sheet 11 — Valuation](#sheet-11--valuation)
15. [Sheet 12 — Break-even Analysis](#sheet-12--break-even-analysis)
16. [Sheet 13 — Funding Cap Table](#sheet-13--funding-cap-table)
17. [Sheet 14 — Charts Data](#sheet-14--charts-data)

---

## Config Schema

The builder reads a single JSON config file. All business-specific data lives in
this config — the builder script contains **zero hardcoded business data**.

```json
{
  "company": "Company Name",
  "company_name": "Company Name",
  "starting_year": 2026,
  "currency": "USD",
  "num_years": 11,
  "tax_rate": 0.25,
  "general": {
    "tax_rate": 0.25,
    "capex_y0": 150000,
    "capex_annual": 50000,
    "depreciation_years": 5,
    "debtor_days": 45,
    "creditor_days": 30,
    "interest_rate": 0.1,
    "cost_inflation": 0.05
  },
  "revenue_streams": [
    {
      "name": "Stream Name",
      "price": 2500,
      "volume": 25,
      "growth": 0.5,
      "cogs_pct": 0.15
    }
  ],
  "fixed_costs": [
    { "name": "Office & Utilities", "annual_cost": 36000 },
    { "name": "Marketing", "annual_cost": 60000 }
  ],
  "headcount": {
    "departments": [
      { "name": "Engineering", "salary": 80000, "y0_count": 5, "growth": 0.4 },
      {
        "name": "Sales & Marketing",
        "salary": 60000,
        "y0_count": 3,
        "growth": 0.5
      },
      { "name": "Operations", "salary": 50000, "y0_count": 2, "growth": 0.35 },
      { "name": "G&A", "salary": 70000, "y0_count": 2, "growth": 0.25 }
    ]
  },
  "funding": {
    "rounds": [
      { "name": "Seed", "amount": 3000000, "year": 0, "pre_money": 10000000 },
      {
        "name": "Series A",
        "amount": 10000000,
        "year": 2,
        "pre_money": 30000000
      },
      {
        "name": "Series B",
        "amount": 25000000,
        "year": 4,
        "pre_money": 75000000
      }
    ]
  },
  "tam": {
    "streams": [
      {
        "name": "Software",
        "value_m": 10000,
        "source": "Research Firm",
        "confidence": "HIGH"
      },
      {
        "name": "Hardware",
        "value_m": 4000,
        "source": "Research Firm",
        "confidence": "HIGH"
      }
    ]
  },
  "sam": {
    "regions": [
      { "name": "India", "value_m": 1800, "years": "Y1-Y2" },
      { "name": "SE Asia", "value_m": 1080, "years": "Y3-Y4" }
    ]
  },
  "som": {
    "year8_revenue_m": 104,
    "terminal_revenue_m": 104
  },
  "valuation": {
    "wacc": 0.15,
    "terminal_growth": 0.03,
    "exit_multiple": 5.0,
    "terminal_year": 8
  }
}
```

### Config Compatibility

The builder also accepts the legacy flat config format:

```json
{
  "headcount": {
    "engineering_salary": 80000,
    "engineering_y0": 5,
    "sales_salary": 60000,
    "sales_y0": 3,
    "ops_salary": 50000,
    "ops_y0": 2,
    "ga_salary": 70000,
    "ga_y0": 2
  },
  "funding": {
    "seed": 3000000,
    "seed_year": 0,
    "series_a": 10000000,
    "series_a_year": 2
  },
  "fixed_costs": [{ "name": "Office", "annual_cost": 36000 }]
}
```

The builder normalizes both formats internally.

---

## Build Order & Dependencies

Sheets **must** be built in this order because downstream sheets reference
upstream sheets by name and row number.

```
Step 1:  Sources & References   (standalone — no dependencies)
Step 2:  Assumptions            (standalone — reads config only)
Step 3:  Headcount Plan         (standalone — reads config only)
Step 4:  Revenue                (depends on  Assumptions)
Step 5:  Operating Costs        (depends on  Assumptions, Revenue, Headcount Plan)
Step 6:  P&L                    (depends on  Revenue, Operating Costs)
Step 7:  Cash Flow              (depends on  P&L, config funding)
Step 8:  Balance Sheet          (depends on  Cash Flow, P&L, config funding)
Step 9:  Summary                (depends on  P&L, Cash Flow, Headcount Plan)
Step 10: Sensitivity Analysis   (depends on  P&L, Cash Flow)
Step 11: Valuation              (depends on  P&L)
Step 12: Break-even Analysis    (depends on  Revenue, Operating Costs)
Step 13: Funding Cap Table      (depends on  config funding)
Step 14: Charts Data            (depends on  P&L, Cash Flow)
```

**Rule:** If an upstream sheet changes structure (row count), all downstream
sheets must be rebuilt.

---

## Color Palette & Formatting Standards

All sheets use a consistent color palette:

| Constant      | Hex       | RGB           | Usage                        |
| ------------- | --------- | ------------- | ---------------------------- |
| TITLE_BLUE    | `#335080` | (51,80,128)   | Sheet title row (row 1)      |
| DARK_BLUE     | `#336699` | (51,102,153)  | Section headers              |
| MEDIUM_BLUE   | `#6699CC` | (102,153,204) | Column headers, sub-headers  |
| SECTION_A_CAT | `#4D80B3` | (77,128,179)  | Category headers (Sources)   |
| LIGHT_BLUE    | `#D8EAF9` | (216,234,249) | Zebra-stripe / category rows |
| LIGHT_GRAY    | `#F2F2F2` | (242,242,242) | Alternate column headers     |
| GREEN         | `#E5F8E5` | (229,248,229) | Total / summary rows         |
| WHITE         | `#FFFFFF` |               | Data rows (odd)              |
| BLACK         | `#000000` |               | Default font color           |
| URL_BLUE      | `#1A4CB3` | (26,76,179)   | Hyperlink text               |
| GRAY          | `#808080` |               | Notes, validation rows       |

### Standard Formatting Rules

| Element             | Font    | Size | Bold | BG Color    | FG Color | Alignment |
| ------------------- | ------- | ---- | ---- | ----------- | -------- | --------- |
| Sheet title (row 1) | Calibri | 14   | Yes  | TITLE_BLUE  | White    | Center    |
| Section header      | Calibri | 11   | Yes  | DARK_BLUE   | White    | Center    |
| Column header       | Calibri | 10   | Yes  | MEDIUM_BLUE | White    | Center    |
| Category label      | Calibri | 10   | Yes  | LIGHT_BLUE  | Black    | Left      |
| Data row (normal)   | Calibri | 10   | No   | White       | Black    | Right     |
| Data row (zebra)    | Calibri | 10   | No   | LIGHT_BLUE  | Black    | Right     |
| Total row           | Calibri | 10   | Yes  | GREEN       | Black    | Right     |
| Row label           | Calibri | 10   | No   | —           | Black    | Left      |

### Number Formats

| Data Type   | Format         | Example    |
| ----------- | -------------- | ---------- |
| Currency    | `[$-409]#,##0` | $1,234,567 |
| Percentage  | `0.0%`         | 25.0%      |
| Integer     | `#,##0`        | 1,234      |
| Decimal     | `#,##0.0`      | 1,234.5    |
| Ratio       | `0.0`          | 3.2        |
| Year header | Plain text     | Year 0     |

### Column Layout Convention

Most sheets follow this column pattern:

| Column | Content      | Width |
| ------ | ------------ | ----- |
| A      | Row label    | 30-48 |
| B      | Unit / Value | 10-15 |
| C      | Year 0       | 12-14 |
| D      | Year 1       | 12-14 |
| ...    | ...          | 12-14 |
| M      | Year 10      | 12-14 |

Year columns start at **column C** (index 3) for most sheets.
Exception: Sources & References uses a different layout (see below).

---

## Sheet 1 — Sources & References

### Purpose

Documents the market sizing (TAM/SAM/SOM) with linkable values that
downstream sheets can reference. Also provides source documentation for
all external data used in the model.

### Dependencies

None — this is a standalone sheet.

### Config Keys Used

- `tam.streams[]` — TAM by revenue stream
- `sam.regions[]` — SAM by geography
- `som.year8_revenue_m` or `som.terminal_revenue_m` — SOM target
- `revenue_streams[]` — stream names (for alignment)

### Column Layout

| Column | Content            | Width |
| ------ | ------------------ | ----- |
| A      | Metric / Label     | 48    |
| B      | Value              | 15    |
| C      | Unit / Calculation | 15    |
| D      | Source             | 15    |
| E      | Confidence         | 15    |

### Row Structure

```
Row 1:  [TITLE] "SOURCES & REFERENCES"  (merged A1:E1, TITLE_BLUE)
Row 2:  (blank)
Row 3:  [SECTION HEADER] "SECTION A: KEY METRICS"  (merged A3:E3, DARK_BLUE)
Row 4:  (blank)
Row 5:  [CATEGORY] "TAM — TOTAL ADDRESSABLE MARKET"  (SECTION_A_CAT)
Row 6:  Column headers: Metric | Value ($M) | Calculation | Source | Confidence
            (MEDIUM_BLUE)

--- For each TAM stream from config.tam.streams[]: ---
Row N:    Stream name  | value_m  | (calculation note) | source | confidence
Row N+1:  ...
--- End loop ---

Row T:  "TOTAL TAM"  | =SUM(B<first>:B<last>)  | "Sum of streams" | — | —
            (GREEN total row, bold)

Row T+2: (blank)
Row T+3: [CATEGORY] "SAM — SERVICEABLE ADDRESSABLE MARKET"  (SECTION_A_CAT)
Row T+4: Column headers: Region | SAM ($M) | Years | Notes | Source

--- For each SAM region from config.sam.regions[]: ---
Row N:    Region name  | value_m  | years | — | —
--- End loop ---

Row S:  "TOTAL SAM"  | =SUM(...)  | — | — | —  (GREEN total row)

Row S+2: (blank)
Row S+3: [CATEGORY] "SOM — SERVICEABLE OBTAINABLE MARKET"  (SECTION_A_CAT)
Row S+4: "Year N Revenue Target"  | som.year8_revenue_m  | "<currency> M" | — | —
Row S+5: "SAM Penetration"  | =B<som>/B<sam_total>  | "%" | — | —

Row S+7: (blank)
Row S+8: [SECTION HEADER] "SECTION B: SOURCE DOCUMENTATION"  (DARK_BLUE)
Row S+9: Column headers: Ref# | Source | Data Point | Value | URL
Row S+10: (placeholder rows — agent fills during research phase)
```

### Key Formulas

| Cell           | Formula                          | Purpose               |
| -------------- | -------------------------------- | --------------------- |
| B(TAM total)   | `=SUM(B<first_tam>:B<last_tam>)` | Total TAM             |
| B(SAM total)   | `=SUM(B<first_sam>:B<last_sam>)` | Total SAM             |
| B(Penetration) | `=B<som_rev>/B<sam_total>`       | SOM/SAM penetration % |

### Formatting Notes

- Section A categories use SECTION_A_CAT background
- Total rows use GREEN background
- Section B source rows use zebra striping
- URL column uses URL_BLUE font color with underline

---

## Sheet 2 — Assumptions

### Purpose

Single source of truth for all input parameters. Other sheets pull values
from this sheet so changes propagate automatically.

### Dependencies

None — reads from config only.

### Config Keys Used

- `general.*` — tax rate, capex, depreciation, debtor/creditor days, inflation
- `revenue_streams[]` — price, volume, growth, cogs_pct per stream
- `fixed_costs[]` — cost categories and amounts
- `funding.rounds[]` — round amounts, timing, pre-money
- `customer_acquisition` — CAC, new customers, churn

### Column Layout

| Column | Content        | Width |
| ------ | -------------- | ----- |
| A      | Parameter name | 35    |
| B      | Value          | 15    |
| C      | Unit           | 10    |
| D-N    | Year 0-10      | 12 ea |

### Row Structure

```
Row 1:  [TITLE] "FINANCIAL MODEL ASSUMPTIONS"  (merged, TITLE_BLUE)
Row 2:  (blank)

--- GENERAL PARAMETERS ---
Row 3:  [SECTION HEADER] "GENERAL PARAMETERS"  (DARK_BLUE)
Row 4:  Tax Rate            | 0.25        | %
Row 5:  CapEx Year 0        | 150000      | USD
Row 6:  CapEx Annual        | 50000       | USD
Row 7:  Depreciation Period | 5           | Years
Row 8:  Debtor Days         | 45          | Days
Row 9:  Creditor Days       | 30          | Days
Row 10: Interest Rate       | 0.10        | %
Row 11: Cost Inflation      | 0.05        | %
Row 12: (blank)

--- REVENUE STREAMS (repeating block per stream) ---
Row 13: [SECTION HEADER] "REVENUE STREAMS"  (DARK_BLUE)
Row 14: Column headers: Stream | Price | Unit | Year 0 | Year 1 | ...

  For each stream (4 rows per stream):
    Row N:   "{Name}: Price"    | price   | USD
    Row N+1: "{Name}: Volume"   | —       | Units  | vol_y0 | =ROUND(prev*(1+growth),0) | ...
    Row N+2: "{Name}: Growth"   | growth  | %
    Row N+3: "{Name}: COGS %"   | cogs_pct| %

--- FIXED COSTS ---
Row F:  [SECTION HEADER] "FIXED COSTS (Annual)"  (DARK_BLUE)
  For each cost:
    Row N:   cost.name  | cost.annual_cost  | USD

--- FUNDING PARAMETERS ---
Row P:  [SECTION HEADER] "FUNDING PARAMETERS"  (DARK_BLUE)
  For each round:
    Row N:   "{Round} Amount"   | amount     | USD
    Row N+1: "{Round} Timing"   | year       | Year
    Row N+2: "{Round} Pre-Money"| pre_money  | USD
```

### Key Row References (tracked by builder)

The builder tracks these row numbers for cross-sheet formulas:

| Reference Key           | Content                     |
| ----------------------- | --------------------------- |
| `assumptions_start`     | First general parameter row |
| `tax_rate`              | Tax Rate row                |
| `cost_inflation`        | Cost Inflation row          |
| `revenue_streams_start` | First stream's Price row    |
| `revenue_streams_end`   | Last stream's COGS % row    |
| `fixed_costs_start`     | First fixed cost row        |
| `fixed_costs_end`       | Last fixed cost row         |
| `funding_start`         | First funding parameter row |

### Revenue Stream Row Arithmetic

Each stream consumes exactly **4 rows** in the Assumptions sheet:

- Row offset 0: Price
- Row offset 1: Volume (with year-by-year growth formulas)
- Row offset 2: Growth rate
- Row offset 3: COGS %

So for stream index `i`, the rows are:

- Price row = `revenue_streams_start + (i * 4)`
- Volume row = `revenue_streams_start + (i * 4) + 1`
- Growth row = `revenue_streams_start + (i * 4) + 2`
- COGS % row = `revenue_streams_start + (i * 4) + 3`

### Volume Growth Formula

For Year 0, volume is the literal `config.volume` value.
For Year 1+, the formula is:

```
=ROUND(<prev_col><volume_row> * (1 + <growth_rate>), 0)
```

Where `<growth_rate>` is the literal value from config (e.g. `0.5`).

---

## Sheet 3 — Headcount Plan

### Purpose

Projects team size and salary costs by department over time.

### Dependencies

None — reads from config only.

### Config Keys Used

- `headcount.departments[]` or legacy `headcount.*_salary` / `headcount.*_y0`

### Column Layout

| Column | Content    | Width |
| ------ | ---------- | ----- |
| A      | Department | 30    |
| B      | Avg Salary | 15    |
| C-M    | Year 0-10  | 12 ea |

### Row Structure

```
Row 1:  [TITLE] "HEADCOUNT PLAN"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers: Department | Avg Salary | Year 0 | Year 1 | ...

--- For each department: ---
Row N:   Department name  | salary  | y0_count | =ROUND(prev*(1+growth),0) | ...

Row T:   "TOTAL HEADCOUNT"  | —  | =SUM(col_start:col_end) per year  (GREEN)
Row T+1: (blank)
Row T+2: "TOTAL SALARY COST" | — | =SUM(count*salary) per year  (GREEN)
```

### Key Formulas

| Row         | Formula per year column                           |
| ----------- | ------------------------------------------------- |
| Dept count  | Y0: literal; Y1+: `=ROUND(<prev>*(1+<growth>),0)` |
| Total HC    | `=SUM(C<first_dept>:C<last_dept>)`                |
| Salary Cost | `=SUM(C<dept1>*B<dept1>, C<dept2>*B<dept2>, ...)` |

### Tracked Row References

| Key                 | Content           |
| ------------------- | ----------------- |
| `headcount_start`   | First department  |
| `headcount_end`     | Last department   |
| `headcount_total`   | Total headcount   |
| `salary_cost_total` | Total salary cost |

---

## Sheet 4 — Revenue

### Purpose

Calculates annual revenue per stream using Price x Volume from Assumptions.

### Dependencies

- **Assumptions** — reads price and volume rows

### Column Layout

| Column | Content        | Width |
| ------ | -------------- | ----- |
| A      | Revenue Stream | 30    |
| B      | Unit           | 10    |
| C-M    | Year 0-10      | 14 ea |

### Row Structure

```
Row 1:  [TITLE] "REVENUE PROJECTIONS"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers: Revenue Stream | Unit | Year 0 | Year 1 | ...

--- For each stream: ---
Row N:   Stream name  | USD  | =Assumptions!$B$<price>*Assumptions!<yr_col>$<volume>

Row T:   "TOTAL REVENUE"  | USD  | =SUM(col_start:col_end)  (GREEN)

Row T+2: [SECTION HEADER] "REVENUE MIX %"
--- For each stream: ---
Row N:   Stream name %  | %  | =IF(total=0, 0, stream/total)
```

### Key Formula

Revenue per stream per year:

```
=Assumptions!$B$<price_row> * Assumptions!<year_col>$<volume_row>
```

- `$B$` locks the price column (always column B in Assumptions)
- `<year_col>` is the year column (D, E, F, ... in Assumptions)
- `$<volume_row>` locks the volume row

### Tracked Row References

| Key             | Content       |
| --------------- | ------------- |
| `revenue_start` | First stream  |
| `revenue_end`   | Last stream   |
| `revenue_total` | Total Revenue |

---

## Sheet 5 — Operating Costs

### Purpose

Aggregates all costs: COGS (variable), salaries (from Headcount), and
other fixed costs (with inflation).

### Dependencies

- **Assumptions** — COGS % per stream
- **Revenue** — revenue per stream (for COGS calculation)
- **Headcount Plan** — salary cost total

### Row Structure

```
Row 1:  [TITLE] "OPERATING COSTS"  (merged, TITLE_BLUE)
Row 2:  (blank)

--- COGS SECTION ---
Row 3:  [SECTION HEADER] "COST OF GOODS SOLD (COGS)"
--- For each stream: ---
Row N:   "COGS: {name}"  | USD  | =Revenue!<col><stream_row> * Assumptions!$B$<cogs_pct>
Row C:   "TOTAL COGS"  | USD  | =SUM(col_start:col_end)  (GREEN)

--- FIXED COSTS SECTION ---
Row C+2: [SECTION HEADER] "FIXED COSTS"
Row F1:  "Salaries & Benefits"  | USD  | ='Headcount Plan'!<col><salary_total>
--- For each non-salary fixed cost: ---
Row N:   cost.name  | USD  | Y0: literal; Y1+: =<prev>*(1+inflation)
Row FT:  "TOTAL FIXED COSTS"  | USD  | =salaries + SUM(other_fixed)  (GREEN)

--- TOTAL ---
Row OT:  "TOTAL OPERATING COSTS"  | USD  | =COGS + FIXED  (GREEN)
```

### Key Formulas

| Row             | Formula                                              |
| --------------- | ---------------------------------------------------- |
| COGS per stream | `=Revenue!<col><stream> * Assumptions!$B$<cogs_pct>` |
| Total COGS      | `=SUM(<first_cogs>:<last_cogs>)`                     |
| Fixed cost Y1+  | `=<prev_col><row> * (1 + <inflation>)`               |
| Total Fixed     | `=<salaries> + SUM(<other_fixed_start>:<other_end>)` |
| Total OpEx      | `=<total_cogs> + <total_fixed>`                      |

### Tracked Row References

| Key                 | Content           |
| ------------------- | ----------------- |
| `cogs_start`        | First COGS row    |
| `cogs_end`          | Last COGS row     |
| `cogs_total`        | Total COGS        |
| `fixed_salaries`    | Salaries row      |
| `other_fixed_start` | First other fixed |
| `other_fixed_end`   | Last other fixed  |
| `fixed_total`       | Total Fixed Costs |
| `opex_total`        | Total Operating   |

---

## Sheet 6 — P&L

### Purpose

Standard Profit & Loss statement: Revenue Gross Profit EBITDA
EBIT PBT Net Income, with margin percentages.

### Dependencies

- **Revenue** — total revenue
- **Operating Costs** — COGS total, fixed costs total

### Row Structure

```
Row 1:  [TITLE] "PROFIT & LOSS STATEMENT"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers: Line Item | Unit | Year 0 | Year 1 | ...

Row 4:  Revenue           | USD | =Revenue!<col><revenue_total>
Row 5:  Cost of Goods Sold| USD | ='Operating Costs'!<col><cogs_total>
Row 6:  GROSS PROFIT      | USD | =Revenue - COGS  (bold)
Row 7:  Gross Margin %    | %   | =IF(Revenue=0, 0, GrossProfit/Revenue)
Row 8:  (blank)
Row 9:  Operating Expenses| USD | ='Operating Costs'!<col><fixed_total>
Row 10: EBITDA            | USD | =GrossProfit - OpEx  (bold, GREEN)
Row 11: EBITDA Margin %   | %   | =IF(Revenue=0, 0, EBITDA/Revenue)
Row 12: (blank)
Row 13: Depreciation      | USD | computed from capex/dep_years
Row 14: EBIT              | USD | =EBITDA - Depreciation  (bold)
Row 15: (blank)
Row 16: Interest Expense  | USD | 0 (no debt assumed)
Row 17: PBT               | USD | =EBIT - Interest  (bold)
Row 18: Tax               | USD | =MAX(0, PBT * tax_rate)
Row 19: NET INCOME        | USD | =PBT - Tax  (bold, GREEN)
Row 20: Net Margin %      | %   | =IF(Revenue=0, 0, NetIncome/Revenue)
```

### Depreciation Calculation

Simplified straight-line depreciation:

```python
Y0: capex_y0 / dep_years
Y1: capex_y0/dep_years + capex_annual/dep_years
Y2: capex_y0/dep_years + (capex_annual * min(2, dep_years))/dep_years
...
YN: capex_y0/dep_years + (capex_annual * min(N, dep_years))/dep_years
```

After `dep_years`, the Y0 asset is fully depreciated and drops off.

### Tracked Row References

| Key                | Content       |
| ------------------ | ------------- |
| `pnl_revenue`      | Revenue row   |
| `pnl_cogs`         | COGS row      |
| `pnl_gross_profit` | Gross Profit  |
| `pnl_opex`         | Operating Exp |
| `pnl_ebitda`       | EBITDA        |
| `pnl_depreciation` | Depreciation  |
| `pnl_ebit`         | EBIT          |
| `pnl_interest`     | Interest      |
| `pnl_pbt`          | PBT           |
| `pnl_tax`          | Tax           |
| `pnl_net_income`   | Net Income    |

---

## Sheet 7 — Cash Flow

### Purpose

Three-section cash flow statement: Operating, Investing, Financing.
Calculates cumulative cash position.

### Dependencies

- **P&L** — net income, depreciation
- **Config** — capex, funding rounds

### Row Structure

```
Row 1:  [TITLE] "CASH FLOW STATEMENT"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers

--- OPERATING ACTIVITIES ---
Row 4:  [SECTION HEADER] "OPERATING ACTIVITIES"  (MEDIUM_BLUE)
Row 5:  Net Income           | USD | ='P&L'!<col><net_income>
Row 6:  + Depreciation       | USD | ='P&L'!<col><depreciation>
Row 7:  Working Capital Change| USD | 0  (simplified)
Row 8:  Operating Cash Flow  | USD | =NetIncome + Dep - WC  (bold, GREEN)

--- INVESTING ACTIVITIES ---
Row 10: [SECTION HEADER] "INVESTING ACTIVITIES"  (MEDIUM_BLUE)
Row 11: Capital Expenditure  | USD | -capex (negative)
Row 12: Investing Cash Flow  | USD | =CapEx  (bold, GREEN)

--- FINANCING ACTIVITIES ---
Row 14: [SECTION HEADER] "FINANCING ACTIVITIES"  (MEDIUM_BLUE)
Row 15: Equity Raised        | USD | funding amount per year
Row 16: Financing Cash Flow  | USD | =Equity  (bold, GREEN)

--- TOTALS ---
Row 18: NET CASH FLOW        | USD | =Operating + Investing + Financing  (GREEN)
Row 20: CUMULATIVE CASH      | USD | Y0: =Net; Y1+: =Prev + Net  (GREEN)
```

### Equity Raised Logic (per year column)

```python
equity = 0
for round in funding.rounds:
    if year == round.year:
        equity += round.amount
cell.value = equity
```

### Tracked Row References

| Key               | Content            |
| ----------------- | ------------------ |
| `cf_net_income`   | Net Income ref     |
| `cf_depreciation` | Depreciation ref   |
| `cf_wc_change`    | Working capital    |
| `cf_operating`    | Operating CF total |
| `cf_capex`        | CapEx row          |
| `cf_investing`    | Investing CF total |
| `cf_equity`       | Equity Raised row  |
| `cf_financing`    | Financing CF total |
| `cf_net`          | Net Cash Flow      |
| `cf_cumulative`   | Cumulative Cash    |

---

## Sheet 8 — Balance Sheet

### Purpose

Assets = Liabilities + Equity validation. Tracks cash, fixed assets,
paid-in capital, and retained earnings.

### Dependencies

- **Cash Flow** — cumulative cash
- **P&L** — net income (for retained earnings)
- **Config** — capex, depreciation, funding

### Row Structure

```
Row 1:  [TITLE] "BALANCE SHEET"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers

--- ASSETS ---
Row 4:  [SECTION HEADER] "ASSETS"  (MEDIUM_BLUE)
Row 5:  Cash & Equivalents    | USD | ='Cash Flow'!<col><cumulative>
Row 6:  Net Fixed Assets      | USD | cumulative_capex - cumulative_dep
Row 7:  TOTAL ASSETS          | USD | =Cash + FixedAssets  (bold, GREEN)

--- LIABILITIES & EQUITY ---
Row 9:  [SECTION HEADER] "LIABILITIES & EQUITY"  (MEDIUM_BLUE)
Row 10: Total Liabilities     | USD | 0  (no debt)
Row 12: Paid-in Capital       | USD | cumulative equity raised
Row 13: Retained Earnings     | USD | Y0: =P&L NetIncome; Y1+: =Prev + P&L NetIncome
Row 14: Total Equity          | USD | =PaidIn + Retained  (bold)
Row 15: TOTAL L&E             | USD | =Liabilities + Equity  (bold, GREEN)

Row 17: BALANCE CHECK         | USD | =TotalAssets - TotalL&E  (GRAY — should be 0)
```

### Retained Earnings Formula

```
Year 0:  ='P&L'!<col><net_income>
Year 1+: =<prev_col><retained_row> + 'P&L'!<col><net_income>
```

### Paid-in Capital Logic

Cumulative equity raised up to and including this year:

```python
cum_equity = sum(round.amount for round in funding.rounds if round.year <= year)
```

### Balance Check

```
=<total_assets> - <total_le>
```

If this is not zero, the model has an error.

---

## Sheet 9 — Summary

### Purpose

KPI dashboard pulling key metrics from P&L, Cash Flow, and Headcount.

### Dependencies

- **P&L** — revenue, gross profit, EBITDA, net income
- **Cash Flow** — cumulative cash, net cash flow
- **Headcount Plan** — total headcount

### Row Structure

```
Row 1:  [TITLE] "KEY PERFORMANCE INDICATORS"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers: Metric | Unit | Year 0 | ...

--- REVENUE METRICS ---
Row 4:  [SECTION HEADER] "REVENUE METRICS"
Row 5:  Total Revenue      | USD | ='P&L'!<col><revenue>
Row 6:  Revenue Growth %   | %   | Y0: 0; Y1+: =(curr-prev)/prev
Row 7:  Gross Margin %     | %   | =GrossProfit/Revenue
Row 8:  EBITDA Margin %    | %   | =EBITDA/Revenue

--- TEAM METRICS ---
Row 10: [SECTION HEADER] "TEAM METRICS"
Row 11: Total Headcount    | FTE | ='Headcount Plan'!<col><hc_total>
Row 12: Revenue/Employee   | USD | =Revenue/Headcount

--- CASH METRICS ---
Row 14: [SECTION HEADER] "CASH METRICS"
Row 15: Cash Balance       | USD | ='Cash Flow'!<col><cumulative>
Row 16: Net Cash Flow      | USD | ='Cash Flow'!<col><net>
```

---

## Sheet 10 — Sensitivity Analysis

### Purpose

Shows Base/Downside/Upside scenarios for key terminal-year metrics.

### Dependencies

- **P&L** — terminal-year revenue, EBITDA
- **Cash Flow** — terminal-year cumulative cash
- **Config** — `valuation.terminal_year` (defaults to 8, capped at `num_years - 1`)

### Row Structure

```
Row 1:  [TITLE] "SENSITIVITY ANALYSIS"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  [SECTION HEADER] "SCENARIO COMPARISON"
Row 4:  Column headers: Metric | Downside (-20%) | Base Case | Upside (+20%)

Row 5:  Year N Revenue   | =0.8*C5  | ='P&L'!<term_col><revenue>  | =1.2*C5
Row 6:  Year N EBITDA     | =0.7*C6  | ='P&L'!<term_col><ebitda>   | =1.3*C6
Row 7:  Year N Cash       | =0.75*C7 | ='Cash Flow'!<term_col><cum>| =1.25*C7
```

Note: Terminal year column is `3 + terminal_year`. For an 11-year model with
`terminal_year=8`, this is column K. For a 5-year model, it caps at Year 4.

---

## Sheet 11 — Valuation

### Purpose

DCF assumptions and implied exit valuation.

### Dependencies

- **P&L** — terminal-year revenue, EBITDA
- **Config** — `valuation.wacc`, `valuation.terminal_growth`, `valuation.exit_multiple`, `valuation.terminal_year`

### Row Structure

```
Row 1:  [TITLE] "VALUATION ANALYSIS"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  [SECTION HEADER] "DCF ASSUMPTIONS"
Row 4:  Discount Rate (WACC)       | config.valuation.wacc     | 0.0%
Row 5:  Terminal Growth Rate       | config.valuation.terminal_growth | 0.0%
Row 6:  Exit Multiple (EV/Revenue) | config.valuation.exit_multiple   | 0.0x
Row 7:  (blank)
Row 8:  [SECTION HEADER] "VALUATION SUMMARY"
Row 9:  Year N Revenue             | ='P&L'!<term_col><revenue>
Row 10: Year N EBITDA              | ='P&L'!<term_col><ebitda>
Row 11: Implied Exit Valuation     | =B9 * B6  (bold)
```

All valuation parameters come from `config.valuation` with sensible defaults.

---

## Sheet 12 — Break-even Analysis

### Purpose

Contribution-margin break-even analysis per revenue stream.

### Dependencies

- **Revenue** — per-stream revenue values
- **Operating Costs** — per-stream COGS values
- **P&L** — total fixed costs (OpEx)

### Row Structure

```
Row 1:  [TITLE] "BREAK-EVEN ANALYSIS"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  [SECTION HEADER] "CONTRIBUTION MARGIN BY STREAM"
Row 4:  Column headers: Revenue Stream | Unit | Year 0 | Year 1 | ...

--- For each revenue stream: ---
Row N:   <Stream>: Revenue             | =Revenue!<col><stream_row>
Row N+1: <Stream>: COGS                | ='Operating Costs'!<col><cogs_row>
Row N+2: <Stream>: Contribution Margin | =Revenue - COGS  (bold)

Row M:   [SECTION HEADER] "BREAK-EVEN CALCULATION"
Row M+1: Total Revenue                 | =SUM(stream revenues)
Row M+2: Total Variable Costs (COGS)   | =SUM(stream COGS)
Row M+3: Total Contribution Margin     | =Revenue - COGS  (bold)
Row M+4: Contribution Margin %         | =CM / Revenue
Row M+5: Total Fixed Costs             | ='P&L'!<col><opex>
Row M+6: Break-Even Revenue             | =Fixed / CM%  (bold, red)
Row M+7: Margin of Safety              | =(Revenue - BE Rev) / Revenue  (bold, green)
```

All values reference the Revenue and Operating Costs sheets — no
hardcoded calculations. This ensures break-even always matches the
actual P&L.

---

## Sheet 13 — Funding Cap Table

### Purpose

Tracks funding rounds with amounts, valuations, and dilution.

### Dependencies

- **Config** — funding.rounds[]

### Row Structure

```
Row 1:  [TITLE] "FUNDING & CAP TABLE"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  [SECTION HEADER] "FUNDING ROUNDS"
Row 4:  Column headers: Round | Amount | Pre-Money | Post-Money | Dilution

--- For each funding round: ---
Row N:   Round name | amount | pre_money | =amount+pre_money | =amount/post_money

Row T:   (blank)
Row T+1: "TOTAL RAISED"  | =SUM(amounts)  (bold, GREEN)
```

### Key Formulas

| Cell         | Formula                  |
| ------------ | ------------------------ |
| Post-Money   | `=B<row> + C<row>`       |
| Dilution     | `=B<row> / D<row>`       |
| Total Raised | `=SUM(B<first>:B<last>)` |

---

## Sheet 14 — Charts Data

### Purpose

Aggregates key time-series data for chart creation. All values are
cross-sheet references.

### Dependencies

- **P&L** — revenue, EBITDA, net income
- **Cash Flow** — cumulative cash

### Row Structure

```
Row 1:  [TITLE] "CHARTS DATA"  (merged, TITLE_BLUE)
Row 2:  (blank)
Row 3:  Column headers: Metric | Year 0 | Year 1 | ...

Row 4:  Revenue       | ='P&L'!<col><revenue>       per year
Row 5:  EBITDA         | ='P&L'!<col><ebitda>        per year
Row 6:  Net Income     | ='P&L'!<col><net_income>    per year
Row 7:  Cash Balance   | ='Cash Flow'!<col><cumul>   per year
```

---

## Builder Script Usage

```bash
# Build all 14 sheets
python execution/build_financial_model.py \
  --config .tmp/<project>/config/<project>_config.json \
  --output .tmp/<project>/financial_model/<project>_model.xlsx

# Build specific sheets (for incremental review)
python execution/build_financial_model.py \
  --config .tmp/<project>/config/<project>_config.json \
  --output .tmp/<project>/financial_model/<project>_model.xlsx \
  --sheets "Sources & References" "Assumptions"

# Build up to a specific sheet (includes all dependencies)
python execution/build_financial_model.py \
  --config .tmp/<project>/config/<project>_config.json \
  --output .tmp/<project>/financial_model/<project>_model.xlsx \
  --up-to "P&L"

# Validate after building
python execution/validate_excel_model.py \
  --file .tmp/<project>/financial_model/<project>_model.xlsx
```

### Incremental Review Workflow

```bash
# Step 1: Build Sources & Assumptions, review in Excel
python execution/build_financial_model.py --config config.json --up-to "Assumptions"

# Step 2: After approval, add Headcount + Revenue
python execution/build_financial_model.py --config config.json --up-to "Revenue"

# Step 3: Add Operating Costs + P&L
python execution/build_financial_model.py --config config.json --up-to "P&L"

# Step 4: Add Cash Flow + Balance Sheet
python execution/build_financial_model.py --config config.json --up-to "Balance Sheet"

# Step 5: Add remaining sheets
python execution/build_financial_model.py --config config.json
```

---

## Validation Checklist

After building, verify:

- [ ] All 14 sheets present in correct order
- [ ] Balance Sheet check row = 0 for all years
- [ ] No `#REF!`, `#VALUE!`, `#DIV/0!` errors
- [ ] Revenue total > 0 for Year 1+
- [ ] Cumulative cash positive after funding rounds
- [ ] Headcount total matches sum of departments
- [ ] Salary cost = sum of (count x salary) per department
- [ ] COGS = sum of (revenue x cogs_pct) per stream
- [ ] Net Income flows correctly to Retained Earnings
- [ ] Cash from Cash Flow matches Balance Sheet cash
