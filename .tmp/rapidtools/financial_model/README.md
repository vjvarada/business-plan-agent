# RapidTools Financial Model - Markdown Specifications

> **Last Updated:** 2026-01-28  
> **Status:** Complete (14/14 sheets documented)  
> **Purpose:** Markdown-first approach to financial model creation

---

## Overview

This folder contains **Markdown specifications for each sheet** in the RapidTools financial model. The Markdown-first approach ensures:

1. **Clear documentation** - Every formula, linkage, and assumption is documented
2. **Version control** - Changes can be tracked via Git
3. **Review before implementation** - Validate logic before creating Excel/Sheets
4. **Audit trail** - Full documentation of data sources and calculations

---

## 14-Sheet Model Structure

| #   | Sheet                                              | Status   | Purpose                                       | Key Data Sources                     |
| --- | -------------------------------------------------- | -------- | --------------------------------------------- | ------------------------------------ |
| 1   | [Sources & References](01_Sources_References.md)   | Complete | TAM/SAM/SOM, benchmarks, source documentation | Market research, SaaS benchmarks     |
| 2   | [Assumptions](02_Assumptions.md)                   | Complete | All model inputs, parameters, volumes         | Sources & References + Business Plan |
| 3   | [Headcount Plan](03_Headcount_Plan.md)             | Complete | Team structure, salaries, efficiency          | Regional salary data                 |
| 4   | [Revenue](04_Revenue.md)                           | Complete | 6 revenue streams calculation                 | Assumptions (Price x Volume)         |
| 5   | [Operating Costs](05_Operating_Costs.md)           | Complete | COGS, Fixed Costs, S&M                        | Revenue x COGS%, Assumptions         |
| 6   | [P&L](06_PL.md)                                    | Complete | Full income statement                         | Revenue, Operating Costs             |
| 7   | [Cash Flow](07_Cash_Flow.md)                       | Complete | 3-section cash flow statement                 | P&L, Balance Sheet changes           |
| 8   | [Balance Sheet](08_Balance_Sheet.md)               | Complete | Assets = Liabilities + Equity                 | P&L, Cash Flow                       |
| 9   | [Summary](09_Summary.md)                           | Complete | KPI dashboard                                 | All sheets                           |
| 10  | [Sensitivity Analysis](10_Sensitivity_Analysis.md) | Complete | Scenario modeling                             | Assumptions variations               |
| 11  | [Valuation](11_Valuation.md)                       | Complete | DCF and multiples                             | P&L, Cash Flow                       |
| 12  | [Break-even Analysis](12_Break_Even.md)            | Complete | Contribution margin                           | Revenue, Costs                       |
| 13  | [Funding Cap Table](13_Funding_Cap_Table.md)       | Complete | Equity tracking                               | Fundraising data                     |
| 14  | [Charts Data](14_Charts_Data.md)                   | Complete | Data for visualizations                       | All sheets                           |

---

## Data Flow Architecture

```
                        SOURCES & REFERENCES
  (TAM/SAM/SOM, Pricing, COGS%, CAC, Churn, Benchmarks)
                              |
                              v
                          ASSUMPTIONS
  (Volumes, Fixed Costs, Parameters) <- Links to Sources & References
        |                 |                    |
        v                 v                    v
   HEADCOUNT         REVENUE          OPERATING COSTS
   PLAN            (6 streams)        (COGS + Fixed)
        |                 |                    |
        |                 v                    |
        |             P&L                      |
        +----------> (Full Income  <-----------+
                      Statement)
                          |
          +---------------+---------------+
          v               v               v
     CASH FLOW      BALANCE        SUMMARY
                    SHEET          (KPIs)
          |               |
          v               v
     VALUATION / ANALYSIS
  (DCF, Sensitivity, Break-even, etc.)
```

---

## Key Linkage Rules

### Sources & References -> Assumptions

| Data                   | Sources Cell | Assumptions Cell             |
| ---------------------- | ------------ | ---------------------------- |
| Software Price         | B66          | C15:H15                      |
| 3D Printer Price       | B67          | C19:H19                      |
| Consumables Price      | B68          | C23:H23                      |
| AMC Price              | B69          | C27:H27                      |
| Managed Services Price | B70          | C31:H31                      |
| Job Work Price         | B71          | C35:H35                      |
| COGS Percentages       | B74:B79      | C18, C22, C26, C30, C34, C38 |
| CAC by Year            | B82:B87      | C53:H53                      |
| Churn Rate             | B89          | C58:H58                      |
| Customer Counts        | B50:B55      | C60:H60                      |

### Assumptions -> Revenue

| Assumptions                | Revenue | Calculation              |
| -------------------------- | ------- | ------------------------ |
| C15 (Price) x C16 (Volume) | C3      | Software Revenue         |
| C19 x C20                  | C4      | 3D Printer Revenue       |
| C23 x C24                  | C5      | Consumables Revenue      |
| C27 x C28                  | C6      | AMC Revenue              |
| C31 x C32                  | C7      | Managed Services Revenue |
| C35 x C36                  | C8      | Job Work Revenue         |

### Revenue x COGS% -> Operating Costs

| Revenue | x   | COGS% | =   | COGS                       |
| ------- | --- | ----- | --- | -------------------------- |
| C3      | x   | 20%   | =   | Software COGS              |
| C4      | x   | 76%   | =   | 3D Printer COGS            |
| C5      | x   | 67%   | =   | Consumables COGS           |
| C6      | x   | 60%   | =   | AMC COGS (incl. OEM share) |
| C7      | x   | 72%   | =   | Managed Services COGS      |
| C8      | x   | 75%   | =   | Job Work COGS              |

---

## Revenue Targets (Business Plan Alignment)

| Year | Business Plan | Model Target | Variance Allowed |
| ---- | ------------- | ------------ | ---------------- |
| Y0   | $500K         | $496K        | +/-2%            |
| Y1   | $2.5M         | $2.48M       | +/-2%            |
| Y2   | $7.0M         | $7.00M       | +/-2%            |
| Y3   | $15.0M        | $15.05M      | +/-2%            |
| Y4   | $30.0M        | $30.11M      | +/-2%            |
| Y5   | $50.0M        | $50.18M      | +/-2%            |

---

## Workflow: Markdown -> Excel

### Step 1: Create/Update Markdown Specs

Edit the relevant `.md` file with:

- Updated values
- New formulas
- Changed linkages

### Step 2: Review Changes

```bash
git diff .tmp/rapidtools/financial_model/
```

### Step 3: Generate Excel

```bash
python execution/build_complete_financial_model.py \
  --spec .tmp/rapidtools/financial_model/ \
  --output .tmp/RapidTools_Financial_Model.xlsx
```

### Step 4: Validate

```bash
python execution/validate_excel_model.py \
  --file .tmp/RapidTools_Financial_Model.xlsx \
  --verbose
```

### Step 5: Upload to Google Sheets (Optional)

```bash
python execution/sync_to_cloud.py \
  --file .tmp/RapidTools_Financial_Model.xlsx
```

---

## Formatting Standards (All Sheets)

### Color Palette

| Element       | RGB                | Hex     | Usage           |
| ------------- | ------------------ | ------- | --------------- |
| Title Blue    | (0.20, 0.30, 0.50) | #335080 | Sheet titles    |
| Header Blue   | (0.20, 0.40, 0.60) | #336699 | Section headers |
| Category Blue | (0.30, 0.50, 0.70) | #4D80B3 | Sub-headers     |
| Light Blue    | (0.85, 0.92, 0.98) | #D8EAF9 | Zebra stripes   |
| Light Gray    | (0.95, 0.95, 0.95) | #F2F2F2 | Column headers  |
| Total Row     | (0.90, 0.95, 1.00) | #E6F2FF | Summary rows    |
| Input Yellow  | (1.00, 1.00, 0.90) | #FFFFE6 | Editable cells  |

### Number Formats

| Data Type     | Format      | Example |
| ------------- | ----------- | ------- |
| Currency ($K) | $#,##0"K"   | $1,234K |
| Currency ($M) | $#,##0.0"M" | $1.2M   |
| Percentage    | 0.0%        | 15.5%   |
| Count         | #,##0       | 1,234   |
| Ratio         | 0.0x        | 3.5x    |

---

## Files in This Directory

| File                       | Description                        | Status |
| -------------------------- | ---------------------------------- | ------ |
| README.md                  | This file - overview and structure | Done   |
| 01_Sources_References.md   | TAM/SAM/SOM, benchmarks, sources   | Done   |
| 02_Assumptions.md          | All model inputs                   | Done   |
| 03_Headcount_Plan.md       | Team and salary model              | Done   |
| 04_Revenue.md              | Revenue by stream                  | Done   |
| 05_Operating_Costs.md      | COGS + Fixed Costs                 | Done   |
| 06_PL.md                   | Profit & Loss statement            | Done   |
| 07_Cash_Flow.md            | Cash flow statement                | Done   |
| 08_Balance_Sheet.md        | Balance sheet                      | Done   |
| 09_Summary.md              | KPI dashboard                      | Done   |
| 10_Sensitivity_Analysis.md | Scenarios                          | Done   |
| 11_Valuation.md            | DCF model                          | Done   |
| 12_Break_Even.md           | Contribution margin                | Done   |
| 13_Funding_Cap_Table.md    | Equity tracking                    | Done   |
| 14_Charts_Data.md          | Chart data                         | Done   |

---

## Related Resources

- **Business Plan Sections:** .tmp/rapidtools/business_plan/sections/
- **Google Sheet Template:** https://docs.google.com/spreadsheets/d/1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY/
- **Applied Additive Excel:** .tmp/Applied_Additive_v9.xlsx
- **Execution Scripts:** execution/
