# Business Planning Agent Directive

> Standard Operating Procedure for creating comprehensive 10-year business plans with full financial modeling, including P&L, Cash Flow, Balance Sheet, and investment return analysis.

## ⚠️ CRITICAL: Financial Model Editing Decision Tree

**BEFORE editing any Google Sheets financial model, consult: `directives/DECISION_TREE.md`**

**Quick Decision Rule:**

- **Does it add/remove revenue streams?** → Config-Based Rebuild
- **Does it add/remove rows anywhere?** → Config-Based Rebuild
- **Does it change business model structure?** → Config-Based Rebuild
- **Is it just updating values/formulas?** → Local-First Workflow

**Never:**

- ❌ Use Local-First to add/remove revenue streams (breaks 100+ formulas)
- ❌ Use Local-First to restructure TAM/SAM (shifts all references)
- ❌ Edit Google Sheets directly via API for multi-cell changes

---

## Business Plan Document Structure (Section-Based)

**Create business plans as a series of standalone markdown sections.** This approach allows for:
- Independent research and iteration per section
- Cross-section alignment verification before finalizing
- Modular compilation into final documents or pitch decks

### Section Sequence (11 Sections)

| # | Section | Purpose | Key Outputs |
|---|---------|---------|-------------|
| 01 | Market Drivers | Why Now? | Government policies, industry shifts, timing justification |
| 02 | TAM/SAM/SOM | Market Sizing | Bottoms-up market size with research citations |
| 03 | Technology Architecture | Technical Differentiation | Architecture diagrams, tech moats |
| 04 | Competitive Analysis | Competitive Landscape | Positioning matrix, 5-7 competitive moats |
| 05 | Customer Validation | Traction Proof | Pilot logos, testimonials, metrics |
| 06 | Go-To-Market Strategy | Acquisition Strategy | Dual GTM (Enterprise + PLG), channel mix |
| 07 | Revenue Model | Unit Economics | 4-5 revenue streams, ARPU, LTV, payback |
| 08 | Team & Costs | Organization | Headcount plan, fixed costs, efficiency metrics |
| 09 | Fundraising Strategy | Capital Strategy | Round sizing, cap table, exit scenarios |
| 10 | Financial Projections | 8-Year Model | P&L, Cash Flow, Balance Sheet, key metrics |
| 11 | Risk Analysis | Risk Mitigation | Market/execution/competitive risks + responses |

### Section Standards

**Every section MUST include:**
1. **Header** with Last Updated date and Status (Draft/Review/Final)
2. **Executive Summary** (2-3 paragraphs)
3. **Detailed Content** with markdown tables
4. **Key Insights** bullet points
5. **Investment Implications** section
6. **References & Sources** with anchor links: `<a name="ref-X"></a>`

**Inline Citation Format:**
```markdown
The global market reached $12.2B in 2024 [[1]](#ref-1), growing at 6.2% CAGR [[2]](#ref-2).
```

### Project File Structure

```
.tmp/<project_name>/
├── business_plan/
│   └── sections/
│       ├── README.md              # Section index
│       ├── 01_Market_Drivers.md
│       ├── 02_TAM_SAM_SOM_Calculation.md
│       └── ... (01-11)
├── pitch_deck/
│   └── slides/
└── config/
    └── <project>_config.json
```

> **📋 FULL DOCUMENTATION:** See `AGENTS.md` → "Business Plan Document Workflow" for complete standards, templates, and PowerShell file-writing rules.

---

## Goal

Work **collaboratively** with the user to create a professional business plan by:

1. Gathering business concept and unit economics through conversation
2. Conducting market research using real online data (TAM → SAM → SOM)
3. Building comprehensive 10-year financial projections with full statements
4. Delivering: Google Docs business plan + Google Sheets financial model

## Interactive Workflow Philosophy

**This agent is conversational, not transactional.** Don't ask for all inputs upfront. Instead:

1. Start with the business idea and unit economics
2. Ask clarifying questions one step at a time
3. Research as you go and share findings
4. Validate assumptions with the user before finalizing
5. Build the model iteratively with user feedback

---

## EXCEL/SHEETS STRUCTURE (14 Sheets)

**Script:** `execution/create_financial_model.py` + `execution/update_financial_model.py`

> **📋 TEMPLATE REFERENCE:** See `directives/FINANCIAL_MODEL_TEMPLATE.md` for the complete RapidTools template with detailed row structures, formula patterns, and formatting standards.
>
> **Template Spreadsheet:** https://docs.google.com/spreadsheets/d/1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY/edit

| Sheet # | Sheet Name           | Purpose                                                                     |
| ------- | -------------------- | --------------------------------------------------------------------------- |
| 1       | Sources & References | TAM/SAM/SOM data with linkable values + full source documentation           |
| 2       | Assumptions          | All inputs: General, Revenue Streams (multi), Fixed Costs, CAC parameters   |
| 3       | Headcount Plan       | Team growth by department, salary costs, revenue per employee               |
| 4       | Revenue              | Revenue by stream + Total + Revenue Mix %                                   |
| 5       | Operating Costs      | COGS per stream + Fixed Costs by category + S&M (CAC × New Customers)       |
| 6       | P&L                  | Full P&L with **Gross Margin %, EBITDA Margin %, Net Margin %**             |
| 7       | Cash Flow            | Operating CF + Investing CF + Financing CF = Cumulative Cash                |
| 8       | Balance Sheet        | Assets = Liabilities + Equity (with balance check)                          |
| 9       | Summary              | Dashboard with key metrics for quick reference                              |
| 10      | Sensitivity Analysis | Scenario analysis (Bear/Base/Bull), 2-way tables for price/volume/cost      |
| 11      | Valuation            | DCF analysis with terminal value, EV/Revenue and EV/EBITDA multiples        |
| 12      | Break-even Analysis  | Contribution margin, break-even revenue, margin of safety                   |
| 13      | Funding & Cap Table  | Funding rounds, pre/post-money valuation, equity dilution, investor returns |
| 14      | Charts Data          | Pre-formatted data for embedded charts (Revenue Mix, Growth, etc.)          |

> **Note:** Customer Economics metrics (CAC, LTV, LTV:CAC) are now consolidated into the Assumptions sheet. Financial Ratios are embedded in the Summary sheet.

---

## ⚠️ CRITICAL: FORMULA LINKAGE PRINCIPLES

**ALL sheets MUST derive their values from the Assumptions sheet. NO hard-coded values anywhere except in Assumptions.**

### Why This Matters

1. **Single Source of Truth**: Change an assumption once, entire model updates automatically
2. **Auditability**: Investors and analysts can trace every number back to its source
3. **Scenario Analysis**: Sensitivity analysis only works if formulas are properly linked
4. **Error Prevention**: Hard-coded values become stale and create model inconsistencies

### Formula Hierarchy

```
Assumptions (Source of Truth)
    ↓
Revenue = Assumptions!Price × Assumptions!Volume
    ↓
Operating Costs = Revenue × Assumptions!COGS% + Assumptions!FixedCosts
    ↓
P&L = Revenue - Operating Costs
    ↓
Cash Flow = P&L (PAT) + Depreciation - WC Change + Funding
    ↓
Balance Sheet = Cumulative Cash Flow + Retained Earnings
    ↓
Valuation, Ratios, Summary = Derived from above sheets
```

### What Goes in Assumptions

- **Prices**: All unit prices for each revenue stream
- **Volumes**: Starting volumes and growth rates
- **COGS %**: Cost of goods sold as percentage by stream
- **Fixed Costs**: All fixed cost categories (salaries, rent, etc.)
- **CAC**: Customer acquisition cost per customer
- **Customer Metrics**: New customers, growth rate, churn rate, lifetime
- **Funding**: Equity infusion and debt amounts by year
- **Tax Rate, Interest Rate, Depreciation Years**
- **Working Capital Days**: Debtor days, creditor days
- **Geographic Expansion**: Markets entered by year
- **Industry Segments**: Target segments with penetration rates

### What Should NEVER Be Hard-Coded

- Revenue amounts (should be =Price × Volume)
- COGS amounts (should be =Revenue × COGS%)
- Customer counts (should reference Assumptions!NewCustomers)
- Funding amounts (should reference Assumptions!Equity/Debt rows)
- Any metric that derives from another sheet

### Example Formulas

```
Revenue!C3:      =Assumptions!C15 * Assumptions!C16   (Price × Volume)
OpCosts!C4:      =Revenue!C3 * Assumptions!C18        (Revenue × COGS%)
P&L!C12:         ='Operating Costs'!C9                (Total COGS)
CashFlow!C4:     ='P&L'!C35                           (Net Income)
BalSheet!C6:     ='Cash Flow'!C15                     (Cumulative Cash)
Valuation!C8:    ='Cash Flow'!C7 + 'Cash Flow'!C10    (FCF)
```

---

### Sheet 1: Assumptions (Multi-Section Structure)

**Section 1: General Parameters**
| Row | Parameter | Unit | Description |
| --- | -------------------- | ---- | ------------------------------ |
| 3 | Tax Rate | % | Corporate tax rate (e.g., 25%) |
| 4 | Capex | $ | Annual capital expenditure |
| 5 | Depreciation Years | yrs | Asset useful life |
| 6 | Debtor Days | days | Days to collect receivables |
| 7 | Creditor Days | days | Days to pay suppliers |
| 8 | Interest Rate | % | Annual interest on debt |
| 9 | Equity Infusion | $ | Equity capital injected |
| 10 | Debt Drawdown | $ | Debt capital raised |

**Section 2: Revenue Streams (Repeat for each stream)**
| Row | Parameter | Unit | Description |
| --- | -------------------------- | ----- | ---------------------------------- |
| - | [Stream Name]: Price/Unit | $ | Price per unit for this stream |
| - | [Stream Name]: Volume | units | Starting volume |
| - | [Stream Name]: Growth Rate | % | Year-over-year growth |
| - | [Stream Name]: COGS % | % | Cost of goods sold as % of revenue |

> **Multi-Revenue Stream Support:** Each business can have 3-6 revenue streams (e.g., Product Sales, Services, Maintenance, Spare Parts, Consulting) with independent pricing, volume, growth, and COGS assumptions.

**Section 3: Fixed Costs by Category**
| Category | Example Value | Description |
| ------------------------------ | ------------- | ------------------------------- |
| Salaries & Benefits | $800,000 | Employee compensation |
| Office Rent | $120,000 | Headquarters rent |
| Warehouse & Depot | $200,000 | Storage facilities |
| Utilities | $40,000 | Electricity, water, internet |
| Software & Cloud | $60,000 | SaaS, hosting, tools |
| IT Infrastructure | $100,000 | Hardware, networking |
| Legal & Compliance | $80,000 | Professional services |
| Insurance | $150,000 | Business insurance |
| Travel & Entertainment | $40,000 | Business travel |
| R&D / Product Development | $200,000 | Innovation spend |

> Fixed costs grow at 3% annually (inflation adjustment)

**Section 4: Customer Acquisition**
| Row | Parameter | Unit | Description |
| --- | ---------------------- | ---- | ----------------------------------------- |
| - | CAC (per customer) | $ | Cost to acquire one customer |
| - | New Customers Y0 | # | Starting new customers |
| - | Customer Growth Rate | % | YoY growth in new customer acquisition |
| - | Churn Rate | % | Annual customer loss rate |
| - | Avg Customer Lifetime | yrs | How long customers stay |

> **CAC Logic:** S&M Cost = CAC × New Customers. New Customers grow by Customer Growth Rate each year.

### Sheet 2: Revenue (Multi-Stream)

**Structure per Stream:**

```
[Stream Name]: Price/Unit    | $     | 2500   | 2500   | ...
[Stream Name]: Volume        | units | 50     | 50     | ...
[Stream Name]: Growth Rate   | %     | 30%    | 30%    | ...
[Stream Name]: Revenue       | $     | =Price×Volume | =Prev×(1+Growth) | ...
```

**Revenue Formulas:**

- Year 0: `=Assumptions!Price × Assumptions!Volume`
- Year 1+: `=PreviousYear × (1 + Assumptions!GrowthRate)`

**Consolidated Section:**

- Total Revenue: Sum of all stream revenues
- Revenue Mix %: Each stream as % of total (formatted as percentage)

### Sheet 3: Operating Costs (Detailed Breakdown)

**Section 1: COGS (Cost of Goods Sold) - Per Revenue Stream**

```
COGS: [Stream 1]  | $ | =Revenue[Stream1] × COGS%[Stream1]
COGS: [Stream 2]  | $ | =Revenue[Stream2] × COGS%[Stream2]
...
Total COGS        | $ | =SUM(all COGS rows)
```

**Section 2: Fixed Costs by Category**

```
Salaries & Benefits       | $ | =Assumptions value × 1.03^year (3% inflation)
Office Rent               | $ | ...
Warehouse & Depot         | $ | ...
Utilities                 | $ | ...
Software & Cloud          | $ | ...
IT Infrastructure         | $ | ...
Legal & Compliance        | $ | ...
Insurance                 | $ | ...
Travel & Entertainment    | $ | ...
R&D                       | $ | ...
Total Fixed Costs         | $ | =SUM(all fixed cost rows)
```

**Section 3: Sales & Marketing**

```
S&M Cost (CAC)    | $ | =Assumptions!CAC × Assumptions!NewCustomers
```

**Total Operating Costs:** `=Total COGS + Total Fixed + S&M`

### Sheet 4: P&L (Enhanced with Margins)

**Full Structure with Margin Calculations:**
| Line Item | Unit | Formula |
| ---------------------- | ---- | -------------------------------------- |
| **REVENUE** | | |
| [Stream 1] | $ | =Revenue![Stream1] |
| [Stream 2] | $ | =Revenue![Stream2] |
| ... | | |
| **Total Revenue** | $ | =SUM(all streams) |
| **COST OF GOODS SOLD** | | |
| COGS | $ | =Operating Costs!Total COGS |
| **GROSS PROFIT** | | |
| Gross Profit | $ | =Total Revenue - COGS |
| **Gross Margin %** | % | =Gross Profit / Total Revenue |
| **OPERATING EXPENSES** | | |
| Fixed Costs | $ | =Operating Costs!Total Fixed |
| S&M (CAC) | $ | =Operating Costs!S&M |
| Total OpEx | $ | =Fixed + S&M |
| **EBITDA** | | |
| EBITDA | $ | =Gross Profit - Total OpEx |
| **EBITDA Margin %** | % | =EBITDA / Total Revenue |
| **D&A** | | |
| Depreciation | $ | =Capex / Depreciation Years |
| EBIT | $ | =EBITDA - Depreciation |
| **INTEREST & TAX** | | |
| Interest | $ | =Debt × Interest Rate |
| PBT | $ | =EBIT - Interest |
| Tax | $ | =MAX(0, PBT × Tax Rate) |
| **NET INCOME** | | |
| PAT (Net Income) | $ | =PBT - Tax |
| **Net Margin %** | % | =PAT / Total Revenue |

### Sheet 5: Headcount Plan

**Dynamic salary model with regional adjustments:**

| Section | Rows | Content |
| ----------------------------- | ----- | ---------------------------------------------------------------------- |
| Parameters | 4-12 | Annual salary growth rate (15%), Regional salary premiums by geography |
| Base Salary Rates | 14-23 | Base salaries for 9 role types (Founders, Engineering, Sales, etc.) |
| Salary Rates by Year | 25-34 | Calculated salaries with annual growth: `=BaseRate*(1+GrowthRate)^Year` |
| Headcount by Role | 36-44 | Employee count projections by role (Y0-Y5) |
| Regional Managers | 46-52 | Regional manager distribution (India, SE Asia, MENA, Europe, Americas) |
| Total Headcount | 54 | =SUM(All Roles) + Regional Managers |
| Salary Costs | 56-64 | `=Headcount × Salary Rate` per role |
| Regional Manager Costs | 66-72 | Salaries adjusted for regional premiums |
| Total People Cost | 74 | =SUM(All Salary Costs) |
| Efficiency Metrics | 76-78 | Revenue per Employee, People Cost % of Revenue |

**Key Formulas:**

- Regional Manager Salary: `=Count * BaseRate * (1 + RegionalPremium)`
- Revenue per Employee: `=Revenue!TotalRevenue / TotalHeadcount`
- People Cost % of Revenue: `=TotalPeopleCost / TotalRevenue`

> **Note:** This sheet is fully dynamic. Edit parameters (rows 5, 8-12, 15-23) to recalculate entire model.

### Sheet 6: Cash Flow

**Operating Cash Flow:**

- PAT + Depreciation - Change in Working Capital

**Investing Cash Flow:**

- (Capex) - negative

**Financing Cash Flow:**

- Equity Infusion + Debt Drawdown

**Net Cash Flow:** Sum of all three
**Cumulative Cash:** Running total (used in Balance Sheet)

### Sheet 7: Balance Sheet

**Assets:**

- Fixed Assets: Cumulative Capex - Cumulative Depreciation
- Working Capital: (Revenue × Debtor Days / 365) - (Costs × Creditor Days / 365)
- Cash: From Cash Flow statement

**Liabilities & Equity:**

- Equity: Cumulative equity infusions
- Debt: Cumulative debt drawdowns
- Retained Earnings: Cumulative PAT

**Validation:** `Total Assets = Total Liabilities + Equity`

### Sheet 8: Summary (Dashboard)

**Key Metrics at a Glance:**

- Year 10 Revenue
- Year 10 PAT
- Year 10 EBITDA Margin %
- 10-Year IRR
- Payback Period

**Milestone Tracking:**

- Break-even Year
- First Profitable Year
- Peak Investment Required

### Sheet 9: Sources & References

**Purpose:** Document all external data sources AND provide linkable calculated values for the Assumptions sheet. This is a critical sheet that provides both traceability and formula linkages.

---

#### TWO-SECTION STRUCTURE

**SECTION A: Key Metrics (Rows 4-90+)**
Contains all calculated values that can be referenced by formulas in the Assumptions sheet.

**Column Structure:**
| Column A | Column B | Column C | Column D | Column E |
|----------|----------|----------|----------|----------|
| Metric Name | **Value (Linkable)** | Unit | Source | Notes/Calculation |

**SECTION B: Full Source Documentation (Rows 93+)**
Contains detailed source information with URLs.

**Column Structure:**
| Column A | Column B | Column C | Column D | Column E |
|----------|----------|----------|----------|----------|
| Source Name | Report/Page | URL | Key Data Point | Notes |

---

#### SECTION A: KEY METRICS BREAKDOWN

**1. TAM - Total Addressable Market (Rows 6-11)**

```
TAM Header Row
Global Market Value          | 3,450,000,000 | $   | [Research Source] | Market report 2025
Market CAGR                  | 9.62%         | %   | [Research Source] | 2025-2030 forecast
Target Segment %             | 15.00%        | %   | [Research Source] | Segment analysis
TAM - Target Segment         | =B7*B9        | $   | Calculated        | Formula linkage
```

**2. SAM - Serviceable Addressable Market (Rows 12-44)**
Organized by geographic region with the following structure per region:

```
REGION HEADER (e.g., INDIA)
[Region] - Total Companies   | 680,000       | #   | [Govt/Industry]   | Total market
[Region] - Target Segments   | 58,500        | #   | [Research]        | Filtered segments
[Region] - Addressable %     | 10.00%        | %   | [Research]        | Penetration estimate
[Region] - SAM Companies     | =B16*B17      | #   | Calculated        | Formula linkage
```

**Supported Regions:** India, Southeast Asia, Japan, Germany/EU, Other Regions

**SAM Summary:**

```
TOTAL SAM - Companies        | =SUM(regional SAMs) | #     | Calculated
Avg Spend/Company            | 3,000              | $/yr  | Industry benchmark
SAM Value (Total)            | =B41*B42           | $     | Calculated
```

**3. SOM - Serviceable Obtainable Market (Rows 45-61)**

```
SOM Header Row
Y0 Customers                 | 10            | #   | Launch target     | Initial customers
Y1 Customers                 | 70            | #   | Growth plan       | Year 1 target
Y2 Customers                 | 190           | #   | Growth plan       | Year 2 target
Y3 Customers                 | 410           | #   | Growth plan       | Year 3 target
Y4 Customers                 | 750           | #   | Growth plan       | Year 4 target
Y5 Customers                 | 1,180         | #   | Growth plan       | Year 5 target
Y5 SAM Penetration           | =B51/B41      | %   | Calculated        | Industry benchmark 2-5%

SEATS EXPANSION MODEL
Y0 Seats/Customer            | 1             | #   | Land strategy     | Initial seats
Y1-Y5 Seats/Customer         | 2-4           | #   | Expand strategy   | Seat growth
```

**4. Pricing Benchmarks (Rows 62-68)**

```
PRICING BENCHMARKS
Product 1 Price              | 1,500         | $/unit  | Competitor analysis
Product 2 Price              | 5,000         | $/unit  | Market research
...
```

**5. COGS Percentages (Rows 69-75)**

```
COGS PERCENTAGES
Software COGS %              | 15.00%        | %   | SaaS benchmark
Hardware COGS %              | 45.00%        | %   | Manufacturing benchmark
Services COGS %              | 35.00%        | %   | Industry average
```

**6. Customer Acquisition (Rows 76-85)**

```
CUSTOMER ACQUISITION
Y0 CAC                       | 2,000         | $/customer | Launch phase
Y1-Y5 CAC                    | declining     | $/customer | Scale efficiencies
Churn Rate                   | 10.00%        | %   | SaaS benchmark (3.5-10%)
Avg Customer Lifetime        | =1/B83        | years | Calculated (1/churn)
```

**7. Product Attachment Rates (Rows 86-91)**

```
PRODUCT ATTACHMENT RATES
Product A Attach Rate        | 20.00%        | %   | Cross-sell estimate
Product B Attach Rate        | 35.00%        | %   | Upsell estimate
```

---

#### SECTION B: SOURCE DOCUMENTATION

**Required Source Categories with URLs:**

1. **MARKET SIZE RESEARCH**
   - Industry market reports (Mordor Intelligence, Grand View Research, MarketsandMarkets)
   - TAM/SAM calculations methodology
2. **REGIONAL MARKET DATA**
   - India manufacturing data (IBEF, Make in India)
   - SE Asia data (ASEAN reports)
   - Japan/EU data (Government statistics)
3. **COMPETITOR RESEARCH**
   - Competitor pricing and positioning
   - Market share data (6sense, G2, Capterra)
4. **SAAS BENCHMARK RESEARCH**
   - Churn rate benchmarks (Recurly, ChurnFree)
   - LTV/CAC benchmarks (ProfitWell, ChartMogul)
   - Market penetration benchmarks (F22 Labs, industry guides)

5. **SMB/INDUSTRY DATA**
   - Segment-specific research
   - Pricing surveys

---

#### FORMATTING REQUIREMENTS (Exact RGB Values)

**SECTION A (Key Metrics) Formatting:**

| Element                           | Background Color                    | Text Color | Font      |
| --------------------------------- | ----------------------------------- | ---------- | --------- |
| Main Title (Row 1)                | RGB(0.2,0.3,0.5) #335080            | White      | Bold 14pt |
| Section Header                    | RGB(0.2,0.4,0.6) #336699            | White      | Bold 12pt |
| Category Headers (TAM, SAM, etc.) | RGB(0.3,0.5,0.7) #4D80B3            | White      | Bold 11pt |
| Regional Headers (INDIA, etc.)    | None                                | Black      | Bold 10pt |
| Data Rows                         | White / RGB(0.85,0.92,0.98) #D8EAF9 | Black      | Normal    |

**SECTION B (Source Documentation) Formatting:**

| Element          | Background Color                    | Text Color               | Font      |
| ---------------- | ----------------------------------- | ------------------------ | --------- |
| Section Header   | RGB(0.2,0.4,0.6) #336699            | White                    | Bold 12pt |
| Column Headers   | RGB(0.95,0.95,0.95) #F2F2F2         | Black                    | Bold      |
| Category Headers | RGB(0.4,0.6,0.8) #6699CC            | White                    | Bold      |
| Data Rows        | White / RGB(0.85,0.92,0.98) #D8EAF9 | Black                    | Normal    |
| URLs (Column D)  | -                                   | RGB(0.1,0.3,0.7) #1A4CB3 | Normal    |
| NOTES Header     | RGB(0.5,0.5,0.5) #808080            | White                    | Bold      |

**Data Row Zebra Striping Pattern:**

- First data row after category header: White (#FFFFFF)
- Second data row: Light blue RGB(0.85,0.92,0.98) / #D8EAF9
- Continue alternating

**Column Widths:**

- Column A (Metric/Source Name): 250px
- Column B (Value/Report): 120px
- Column C (Unit/empty): 80px
- Column D (Source/URL): 300px
- Column E (Notes/Key Data): 200px

**Calculated Values:**

- Bold labels for calculated rows (e.g., "TAM - Target Segment", "SAM Companies")
- Use actual formulas (=B7\*B9) not hardcoded values

**Notes Section (Bottom):**

- Gray background header
- Include: Research methodology, last update date, data validation notes

---

#### FORMULA LINKAGE EXAMPLES

The Assumptions sheet should reference Sources & References values:

```
Assumptions!C15 (Price)     = 'Sources & References'!B63
Assumptions!C25 (CAC)       = 'Sources & References'!B77
Assumptions!C30 (Churn)     = 'Sources & References'!B83
```

> ⚠️ **CRITICAL**: All calculated values in Column B MUST use formulas, not hardcoded values:
>
> - TAM Segment Value: `=B7*B9` (not 517500000)
> - Regional SAM: `=B16*B17` (not 5850)
> - Total SAM: `=B18+B24+B30+B36+B39` (not 29474)
> - SAM Penetration: `=B51/B41` (not 0.04)
> - Customer Lifetime: `=1/B83` (not 10)

> ⚠️ **IMPORTANT**: Always populate this sheet with actual research data from market research tools (SerpAPI). Never leave placeholders like "[To be filled]".

### Sheet 10: Sensitivity Analysis

**Purpose:** Test how key assumptions impact financial outcomes through scenario modeling.

**Section 1: Scenario Analysis**
| Scenario | Revenue Growth Adj | Cost Adj | Price Adj |
|----------|-------------------|----------|-----------|
| Bear Case | -15% | +10% | -10% |
| Base Case | 0% | 0% | 0% |
| Bull Case | +15% | -10% | +10% |

**Output:** Scenario impact on Year 5 Revenue, EBITDA, Net Income

**Section 2: Revenue Sensitivity Table (2-way)**

- Rows: Price change (-20% to +20%)
- Columns: Volume change (-20% to +20%)
- Cell values: Resulting revenue

**Section 3: EBITDA Sensitivity Table (2-way)**

- Rows: Revenue change (-20% to +20%)
- Columns: Cost change (-10% to +10%)
- Cell values: Resulting EBITDA

**Section 4: Key Assumptions Impact**

- Shows which variables have High/Medium/Low impact on EBITDA

### Sheet 11: Valuation

**Purpose:** Calculate company valuation using DCF and comparable multiples.

**Section 1: DCF Valuation**
| Row | Metric | Year 1-10 | Terminal |
|-----|--------|-----------|----------|
| 1 | Free Cash Flow | From Cash Flow sheet | - |
| 2 | Discount Rate (WACC) | User input (e.g., 12%) | - |
| 3 | Terminal Growth Rate | User input (e.g., 3%) | - |
| 4 | Discount Factor | 1/(1+WACC)^n | - |
| 5 | Present Value of FCF | FCF × Discount Factor | - |

**Key Outputs:**

- Sum of PV (FCF) Years 1-10
- Terminal Value = FCF_Year10 × (1+g) / (WACC - g)
- PV of Terminal Value
- **Enterprise Value = Sum PV + PV Terminal**
- Less: Net Debt
- **Equity Value**

**Section 2: Valuation by Multiples**
| Multiple | Industry Range | Applied to |
|----------|---------------|------------|
| EV/Revenue | 2x - 8x | Year 5 Revenue |
| EV/EBITDA | 6x - 15x | Year 5 EBITDA |
| P/E | 10x - 25x | Year 5 Net Income |

**Section 3: Valuation Summary**

- Shows Low/Mid/High valuation range from DCF and multiples
- Average valuation across methods

### Sheet 12: Break-even Analysis

**Purpose:** Calculate when the business becomes profitable.

**Section 1: Contribution Margin Analysis (Years 0-10)**
| Row | Metric | Formula |
|-----|--------|---------|
| 1 | Total Revenue | From Revenue sheet |
| 2 | Variable Costs (COGS) | From Operating Costs sheet |
| 3 | Contribution Margin | Revenue - Variable Costs |
| 4 | Contribution Margin % | CM / Revenue |

**Section 2: Break-even Calculations**
| Row | Metric | Formula |
|-----|--------|---------|
| 1 | Fixed Costs + S&M | From Operating Costs sheet |
| 2 | Break-even Revenue | Fixed Costs / CM% |
| 3 | Actual Revenue | From Revenue sheet |
| 4 | Surplus/(Deficit) | Actual - Break-even |
| 5 | Break-even Achieved? | YES/NO |

**Section 3: Operating Leverage**

- Degree of Operating Leverage = CM / (CM - Fixed Costs)
- Interpretation: High (>3x), Moderate (1.5-3x), Low (<1.5x)

**Section 4: Margin of Safety**

- Margin of Safety ($) = Actual Revenue - Break-even Revenue
- Margin of Safety (%) = MoS / Actual Revenue

**Section 5: Profitability Timeline**

- First year EBITDA positive
- First year Net Income positive

### Sheet 13: Funding & Cap Table

**Purpose:** Track equity rounds, ownership dilution, and investor returns.

**Section 1: Funding Rounds**
| Round | Timing | Amount | Pre-Money | Post-Money | Shares | Price/Share | Ownership % |
|-------|--------|--------|-----------|------------|--------|-------------|-------------|
| Founders | Start | $0 | $0 | $1M | 10M | $0.10 | 100% |
| Seed | Year 0 | $1M | $1M | $2M | 5M | $0.20 | 33% |
| Series A | Year 2 | $3M | $4M | $7M | 2.1M | $1.43 | 23% |
| Series B | Year 4 | $10M | $17.5M | $27.5M | 5.7M | $1.75 | 17% |

**Section 2: Cap Table**
| Shareholder | Shares | % Ownership | Investment | Current Value | Multiple |
|-------------|--------|-------------|------------|---------------|----------|
| Founders | 10M | 58% | $0 | $X | - |
| Seed Investors | 5M | 29% | $1M | $X | Xx |
| Series A | 2.1M | 12% | $3M | $X | Xx |
| Total | 17.1M | 100% | $4M | $X | - |

**Section 3: Dilution Analysis**

- Shows founder ownership % at each stage (Pre-Seed → Post-Seed → Post-A → Post-B)

**Section 4: Debt Financing**

- Opening/Closing debt by year
- Principal repayment schedule
- Interest expense calculation

**Section 5: Investor Returns**

- Exit valuation from Valuation sheet
- Investor profit, multiple, and IRR for each round

### Sheet 14: Charts Data

**Purpose:** Pre-formatted datasets for embedded Google Sheets charts and visualizations.

**Chart 1: Revenue Growth**

- Year, Total Revenue ($K) from Revenue sheet
- Line chart showing revenue trajectory Y0-Y5

**Chart 2: Revenue Mix (Year 5)**

- Revenue stream breakdown in final year
- Pie/Column chart for revenue diversification

**Chart 3: Profitability Trend**

- Gross Profit, EBITDA, Net Income ($K) by year
- Multi-line chart showing profitability evolution

**Chart 4: Customer Growth**

- Total Customers, New Customers by year
- Stacked area/column chart

**Chart 5: Unit Economics**

- LTV:CAC Ratio, CAC Payback (months) by year
- Dual-axis chart (ratio + time)

**Chart 6: Cash Position**

- Cash Balance ($K) from Cash Flow sheet
- Area chart showing runway

**Chart 7: Margin Trends**

- Gross Margin %, EBITDA Margin %, Net Margin % by year
- Multi-line chart (all percentages)

**Chart 8: Cap Table (Post Series A)**

- Stakeholder ownership percentages
- Pie chart for equity distribution

**Chart 9: Funding Timeline**

- Equity Raised ($K), Cumulative Equity by year
- Waterfall/Stacked column chart

> **All data points use formulas** referencing source sheets (Revenue, P&L, Cash Flow, Assumptions). Edit source data to auto-update charts.

---

## NUMBER FORMATTING STANDARDS

All financial model sheets must follow consistent formatting:

**Currency Values (Revenue, Costs, etc.):**

- Format: `#,##0.0` (comma separators, 1 decimal place)
- Example: 1,234,567.8

**Percentages (Margins, Growth Rates, etc.):**

- Format: `0.0%` (percentage with 1 decimal)
- Example: 25.5%

**Integers (Customer counts, Units):**

- Format: `#,##0` (comma separators, no decimals)
- Example: 1,234

**Formatting Applied Per Sheet:**
| Sheet | Currency Rows | Percentage Rows |
|-------|---------------|-----------------|
| Assumptions | Prices, Costs, Unit Economics (ARPU, LTV, CAC) | Growth rates, Margins, Tax rate, LTV:CAC |
| Revenue | All revenue lines | - |
| Operating Costs | All cost lines | COGS % |
| P&L | All financial lines | Gross Margin %, EBITDA Margin %, Net Margin % |
| Headcount Plan | Salary rates, Total people cost | People cost % of revenue |
| Cash Flow | All cash flow lines | - |
| Balance Sheet | All asset/liability lines | - |

---

## 14-STEP WORKFLOW

### STEP 0: Initialize Project Structure (MANDATORY FIRST STEP)

**Before starting any business plan work, create proper .tmp folder structure:**

```bash
# Initialize core folders (if first time)
python execution/setup_project_structure.py --init-only

# Create project-specific structure
python execution/setup_project_structure.py --project <project_name>

# Example:
python execution/setup_project_structure.py --project rapidtools
```

**This creates:**
```
.tmp/
├── consolidated_research/    [Shared] Research database (6 categories)
├── research_archive/         [Shared] Raw research files
├── templates/                [Shared] Reusable templates
├── scripts_archive/          [Shared] Analysis scripts
└── <project_name>/           [Project] Your business plan project
    ├── business_plan/        Business plan documents
    ├── pitch_deck/           Pitch deck content
    ├── config/               Financial model configs
    └── notes/                Work notes and updates
```

**Why This Matters:**
- ✓ Organized structure from the start
- ✓ All project files in one place
- ✓ Research database shared across projects
- ✓ Easy to find and archive files
- ✓ Professional organization

**Check current structure:**
```bash
python execution/setup_project_structure.py --summary
```

---

### STEP 1: Define Business & Unit Economics (Foundation)

**Agent asks:**

- "Tell me about your business idea. What product/service are you offering?"
- "What are your **revenue streams**? (List all ways you'll make money)"
- "For each revenue stream, what's the pricing model and unit?"
- "Are there any capacity constraints?"

**Multi-Revenue Stream Collection:**

For each revenue stream, collect:
| Parameter | Description | Example |
|-----------|-------------|---------|
| Stream Name | Revenue source name | "Equipment Sales" |
| Unit Price (Year 0) | Starting price | ₹50,00,000 |
| Unit | What triggers revenue | "per robot" |
| Volume (Year 0) | Starting quantity | 10 units |
| Volume Growth Rate | Annual growth | 25% |
| COGS % | Direct cost as % of revenue | 60% |

**Example Revenue Streams (Robotics Company):**
| Stream | Unit Price | Unit | Y0 Volume | Growth | COGS% |
|--------|------------|------|-----------|--------|-------|
| Equipment Sales | ₹50,00,000 | per robot | 10 | 25% | 60% |
| Spares & Parts | ₹5,00,000 | per robot | 8 | 30% | 45% |
| Annual Maintenance | ₹6,00,000 | per contract | 5 | 40% | 35% |
| Consumables | ₹2,00,000 | per robot/year | 5 | 35% | 50% |
| Consulting | ₹10,00,000 | per project | 3 | 20% | 25% |

**Data Parameters to Collect:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Product/Service | What the business does | "Industrial humanoid robots for warehouses" |
| Revenue Streams | Multiple sources | Equipment, Spares, Services, Consumables |
| Unit of Sale | Revenue trigger per stream | "Per robot", "Per contract", "Per project" |
| Capacity Constraints | Maximum capacity | "Manufacturing: 50 units/year" |

**Sheet Setup: Assumptions**

```
--- General Business Parameters ---
- Company Name
- Currency
- Tax Rate (%)
- Discount Rate / WACC (%)
- Inflation Rate (%)

--- Revenue Streams (per stream) ---
- Stream Name
- Unit Price (Year 0)
- Unit
- Volume (Year 0)
- Volume Growth Rate (%)
- COGS (%)

--- Customer Economics ---
- New Customers (Year 0)
- Customer Growth Rate (%)
- Customer Acquisition Cost (CAC)
- Churn Rate (%)

--- Fixed Costs by Category ---
- Salaries & Benefits
- Office Rent
- Utilities
- Software & Subscriptions
- Insurance
- Professional Services
- Travel & Entertainment
- Marketing (non-CAC)
- R&D
- Miscellaneous
```

---

### STEP 2: Market Sizing (TAM → SAM → SOM)

**🔬 CATEGORIZED RESEARCH APPROACH**

Research is organized into **6 logical categories** for better organization and reuse:

1. **Market Research** - TAM/SAM/SOM, market size, industry trends
2. **Headcount/Hiring** - Team composition, salaries, roles, hiring benchmarks
3. **Geographic/Location** - Regional data, market entry, expansion strategies
4. **Business Model** - Revenue models, pricing, unit economics
5. **Competitors** - Competitive landscape, positioning
6. **Financial Benchmarks** - CAC, LTV, margins, financial ratios

**Script:** `execution/serp_market_research.py` (conducts research) → `execution/consolidate_market_research.py` (organizes by category)

**Research Workflow:**

```bash
# 1. Conduct category-specific research
python execution/serp_market_research.py --mode search --query "[industry] market size India 2026" --output .tmp/market_research_tam.json
python execution/serp_market_research.py --mode search --query "software engineer salary India 2026" --output .tmp/headcount_research.json
python execution/serp_market_research.py --mode search --query "[industry] India vs Southeast Asia" --output .tmp/geographic_research.json

# 2. Consolidate all research into categorized files
python execution/consolidate_market_research.py --research-dir .tmp --output-dir .tmp/consolidated_research --verbose

# Output: .tmp/consolidated_research/
#   - market_research.json (TAM/SAM/SOM data)
#   - headcount_research.json (salary, hiring data)
#   - geographic_research.json (regional expansion)
#   - business_model_research.json (pricing, revenue models)
#   - competitors_research.json (competitive landscape)
#   - benchmarks_research.json (CAC, LTV, margins)
#   - _metadata.json (consolidation stats)
```

**Benefits of Categorized Research:**

- ✓ Single source of truth per category
- ✓ No duplicates across research files
- ✓ Easy to update specific categories independently
- ✓ Clean separation between market, team, and financial research
- ✓ Reusable across multiple business plans

**Agent actions:**

```bash
# Market sizing research (save to .tmp root for consolidation)
python execution/serp_market_research.py --mode search --query "[industry] market size India 2026" --output .tmp/market_research_tam.json

# Market growth trends
python execution/serp_market_research.py --mode trends --query "[industry] growth rate forecast" --output .tmp/market_research_trends.json

# Competitor analysis
python execution/serp_market_research.py --mode competitors --query "[industry] top companies India" --output .tmp/competitors_research.json

# Consolidate all research into shared database
python execution/consolidate_market_research.py --research-dir .tmp --output-dir .tmp/consolidated_research

# Archive raw research files (optional)
# Move-Item .tmp/*_research*.json .tmp/research_archive/
```

**Data Parameters to Collect:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Total Addressable Customers | Total market | 500,000 restaurants in India |
| Average Revenue Per Customer (ARPU) | Annual value | ₹12,000/year |
| Market Growth Rate | YoY growth | 15% |
| Expected Penetration % | Target share by year | Year 1: 0.1%, Year 5: 2% |

**Sources to Capture (for Sources & References sheet):**
| Data Point | Source Example |
|------------|----------------|
| TAM Value & Source | "Grand View Research: $X billion by 2030" |
| SAM Value & Source | "Statista: $Y billion serviceable" |
| Growth Rate Source | "MarketsandMarkets: X% CAGR" |
| CAC Benchmark Source | "ProfitWell: SaaS CAC averages $X" |
| LTV:CAC Benchmark | "ChartMogul: 3:1 ratio is healthy" |

**Sheet Structure: Market Size**
| Year | Total Market Size | Serviceable % | Target Share % | Addressable Revenue |
|------|-------------------|---------------|----------------|---------------------|
| 1 | =Customers × ARPU | 40% | 0.1% | =TAM × SAM% × SOM% |

**Key Formulas:**

- TAM = Total Customers × ARPU
- SAM = TAM × Serviceable %
- SOM = SAM × Market Share %

> ⚠️ Use market share **ramp-up**, not a flat percentage
> ⚠️ **Always capture source URLs** for TAM/SAM/SOM - add to Sources sheet

---

### STEP 3: Demand & Volume Build-up

**Agent asks:**

- "How many customers do you expect to acquire in Year 1?"
- "What's your expected customer churn/retention rate?"
- "What's your capacity utilization plan (if manufacturing/services)?"
- "What's your ramp-up period?"

**Data Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| New Customers/Year | Acquisition target | Year 1: 500, Year 2: 1,200 |
| Churn Rate | Annual loss rate | 10% |
| Retention Rate | 1 - Churn | 90% |
| Capacity Utilization | % of max capacity | 60% → 85% ramp |

**Sheet Structure: Volume Build-up**
| Year | Opening Customers | Additions | Churn | Closing Customers |
|------|-------------------|-----------|-------|-------------------|
| 1 | 0 | 500 | 50 | 450 |
| 2 | 450 | 1,200 | 165 | 1,485 |

**Formula:**

```
Closing Customers = Opening + Additions – Churn
```

---

### STEP 4: Revenue Model

**Agent asks:**

- "What's your price per unit/subscription?"
- "What's your annual price increase assumption?"
- "Do you have multiple revenue streams?"

**Data Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Price per Unit | Base price | ₹999/month |
| Annual Price Increase | Inflation/value | 5% |
| Revenue Streams | Multiple sources | Subscription, Setup fee, Add-ons |

**Sheet Structure: Revenue**
| Year | Customers | Price | Revenue |
|------|-----------|-------|---------|
| 1 | 450 | ₹11,988 | ₹53,94,600 |

**Formula:**

```
Revenue = Customers × Price (Annual)
```

> If multiple revenue streams → create separate tables + consolidated total

---

### STEP 5: Operating Cost Structure

**Agent asks:**

- "What are your major fixed costs? (salaries, rent, marketing)"
- "What are your variable costs as % of revenue?"
- "What's your expected annual cost escalation?"

**Split costs into Variable vs Fixed:**

**Fixed Costs:**
| Cost Head | Year 1 | Annual Escalation |
|-----------|--------|-------------------|
| Salaries | ₹24,00,000 | 10% |
| Rent/Office | ₹6,00,000 | 5% |
| Marketing | ₹12,00,000 | 8% |
| Admin/IT | ₹3,00,000 | 5% |
| Insurance | ₹1,00,000 | 5% |

**Variable Costs (% of Revenue):**
| Cost Head | % of Revenue |
|-----------|--------------|
| Payment Processing | 2% |
| Customer Support | 5% |
| Hosting/Infrastructure | 3% |
| Sales Commission | 8% |

**Formula Example:**

```
Marketing Cost = Revenue × Marketing %
Total Variable = Revenue × Sum(Variable %)
```

---

### STEP 6: EBITDA Calculation

**In P&L sheet:**

```
EBITDA = Revenue – COGS – Operating Costs
```

---

### STEP 7: Capital Expenditure & Depreciation

**Agent asks:**

- "What's your initial capital expenditure (equipment, setup)?"
- "What's your annual maintenance capex?"
- "What's the useful life of assets?"

**Data Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Initial Capex | Setup costs | ₹50,00,000 |
| Maintenance Capex | Annual upkeep | 5% of gross block |
| Asset Life | Depreciation period | 5-10 years |
| Depreciation Method | Calculation type | Straight Line |

**Sheet Structure: Capex**
| Year | Opening Gross Block | Additions | Closing Gross Block |
|------|---------------------|-----------|---------------------|

**Depreciation Formula:**

```
Depreciation = Gross Block / Useful Life
```

---

### STEP 8: Working Capital

**Agent asks:**

- "What are your debtor days (time to collect payment)?"
- "What are your inventory days (if applicable)?"
- "What are your creditor days (time to pay suppliers)?"

**Data Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Debtor Days | Collection period | 30 days |
| Inventory Days | Stock holding | 15 days |
| Creditor Days | Payment period | 45 days |

**Sheet Structure: Working Capital**
| Component | Formula |
|-----------|---------|
| Debtors | Revenue × Debtor Days / 365 |
| Inventory | COGS × Inventory Days / 365 |
| Creditors | Costs × Creditor Days / 365 |

**Key Formula:**

```
Net Working Capital = Debtors + Inventory – Creditors
Change in WC = Current Year NWC – Previous Year NWC
```

---

### STEP 9: Funding Structure (Debt / Equity)

**Agent asks:**

- "What's your equity contribution (year-wise)?"
- "Are you taking any debt? How much?"
- "What interest rate and tenure?"
- "Is there a moratorium period?"

**Data Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Equity Infusion | Capital by owners | ₹30,00,000 Year 1 |
| Debt Amount | Loan amount | ₹20,00,000 |
| Interest Rate | Annual rate | 12% |
| Repayment Tenure | Loan period | 5 years |
| Moratorium | Grace period | 1 year |

**Sheet Structure: Debt Schedule**
| Year | Opening Debt | Drawdown | Repayment | Closing Debt |
|------|--------------|----------|-----------|--------------|

**Interest Formula:**

```
Interest = Average Debt × Interest Rate
Average Debt = (Opening + Closing) / 2
```

---

### STEP 10: Profit & Loss Statement (10 Years)

**Sheet Structure: P&L**
| Line Item | Yr1 | Yr2 | ... | Yr10 |
|-----------|-----|-----|-----|------|
| Revenue | | | | |
| COGS | | | | |
| **Gross Profit** | | | | |
| Operating Costs | | | | |
| **EBITDA** | | | | |
| Depreciation | | | | |
| **EBIT** | | | | |
| Interest | | | | |
| **Profit Before Tax** | | | | |
| Tax | | | | |
| **Profit After Tax (PAT)** | | | | |

---

### STEP 11: Cash Flow Statement

**Sheet Structure: Cash Flow**

**Operating Cash Flow:**

```
PAT
+ Depreciation
– Change in Working Capital
= Operating Cash Flow
```

**Investing Cash Flow:**

```
– Capex
= Investing Cash Flow
```

**Financing Cash Flow:**

```
+ Equity Infusion
+ Debt Drawdown
– Debt Repayment
– Dividends (if any)
= Financing Cash Flow
```

**Net Position:**

```
Net Cash Flow = Operating + Investing + Financing
Closing Cash = Opening Cash + Net Cash Flow
```

---

### STEP 12: Balance Sheet

**Sheet Structure: Balance Sheet**

**Assets:**

- Fixed Assets (net of depreciation)
- Working Capital (Debtors + Inventory)
- Cash & Bank

**Liabilities:**

- Equity Capital
- Retained Earnings
- Debt (Outstanding)
- Creditors

**Validation Checkpoint:**

```
✅ Assets = Liabilities + Equity
```

> This is the biggest validation checkpoint. If this doesn't balance, there's an error somewhere.

---

### STEP 13: Returns & Decision Metrics

**Key Outputs to Calculate:**
| Metric | Formula | Target |
|--------|---------|--------|
| IRR | Internal Rate of Return on equity | >20% |
| NPV | Net Present Value at WACC | Positive |
| ROE | PAT / Average Equity | >15% |
| DSCR | (PAT + Depreciation + Interest) / (Interest + Principal) | >1.5x |
| EBITDA Margin | EBITDA / Revenue | Industry benchmark |
| Payback Period | Years to recover investment | <5 years |
| Cash Break-even | Year when cumulative cash > 0 | Target year |

---

### STEP 14: Scenarios & Sensitivity (Optional but Recommended)

**Create Three Scenarios:**
| Scenario | Description |
|----------|-------------|
| Base Case | Most likely assumptions |
| Upside | Optimistic (faster growth, lower costs) |
| Downside | Conservative (slower growth, higher costs) |

**Key Variables to Sensitize:**

- Price per unit (±10-20%)
- Volume/customer growth (±20-30%)
- Cost inflation (±2-5%)
- Working capital days (±10-15 days)
- Interest rate (±1-2%)

---

## Tools/Scripts

### Market Research

- `serp_market_research.py` - Search Google, analyze competitors, track trends, get news
  - Modes: `search`, `competitors`, `trends`, `news`, `sources`, `full-report`
  - Requires: `SERPAPI_API_KEY`

### Business Analysis (Copilot Mode)

- `generate_business_plan.py` - Generate SWOT, financials, canvas, compile plans
  - Modes: `swot`, `financials`, `canvas`, `compile`
  - **In Copilot mode**: Use `--copilot` flag to get prompts, then generate content directly
  - Includes References section in compiled business plans

### Financial Model

- `create_financial_model.py` - **Create comprehensive multi-stream financial model in Google Sheets**
  - Supports multiple revenue streams with independent assumptions
  - Detailed cost breakdown (COGS per stream, 10 fixed cost categories, S&M)
  - Enhanced P&L with Gross Margin %, EBITDA Margin %, Net Margin %
  - Customer Economics with CAC tied to new customer acquisition
  - Automatic number formatting (commas, decimals, percentages)
  - Creates 11 interconnected sheets with formulas

**Usage:**

```bash
python execution/create_financial_model.py --company "Company Name" --config config.json
```

**Features:**

- Multi-revenue stream support (configurable per business)
- COGS calculated per revenue stream (not flat %)
- Fixed costs by category with 3-5% annual inflation
- S&M = New Customers × CAC (with customer growth rate)
- Proper formula cross-references between sheets
- All % cells formatted as percentages
- All numbers with comma separators and 1 decimal

**Output Sheets (11 core + 4 additional):**

1. Assumptions (General, Revenue Streams, Fixed Costs, Customer Economics)
2. Revenue (Per-stream calculations + Total)
3. Operating Costs (COGS per stream, Fixed by category, S&M)
4. P&L (Enhanced with margin percentages)
5. Customer Economics (CAC, CLV, LTV:CAC, Payback)
6. Cash Flow (Operating, Investing, Financing)
7. Balance Sheet (Assets, Liabilities, Equity)
8. Summary (Dashboard metrics)
9. Sources & References (Data sources with URLs)
10. Sensitivity Analysis (Scenario modeling)
11. Valuation (DCF and multiples)

### Financial Model Updates

- `update_financial_model.py` - **Update existing financial models**
  - Add missing sheets (Break-even, Funding, Financial Ratios, Headcount)
  - Update growth rates for geographic expansion
  - Populate Sources & References with market research
  - Fix percentage formatting across all sheets

**Usage:**

```bash
# Add remaining sheets (Break-even, Funding, Ratios)
python execution/update_financial_model.py --sheet-id "1ABC..." --action add-remaining

# Fix percentage formatting
python execution/update_financial_model.py --sheet-id "1ABC..." --action fix-formatting

# Update sources with market research data
python execution/update_financial_model.py --sheet-id "1ABC..." --action update-sources --sources-file sources.json

# Add headcount plan
python execution/update_financial_model.py --sheet-id "1ABC..." --action add-headcount --headcount-file headcount.json

# Run all updates
python execution/update_financial_model.py --sheet-id "1ABC..." --action all
```

**Actions:**
| Action | Description |
|--------|-------------|
| `update-sources` | Populate Sources & References with market data |
| `update-growth` | Update growth rates for expansion phases |
| `add-headcount` | Add Headcount Plan sheet |
| `add-remaining` | Add Break-even, Funding, Financial Ratios |
| `fix-formatting` | Fix percentage formatting across sheets |
| `all` | Run all update actions |

> ⚠️ **Rate Limiting**: Google Sheets API has rate limits. The script includes built-in delays (2-3 seconds between operations) to avoid 429 errors.

### Financial Model Audit

- `audit_financial_model.py` - **Comprehensive audit tool for financial model validation**
  - Validates balance sheet identity (Assets = Liabilities + Equity)
  - Checks cash runway and funding sufficiency
  - Benchmarks valuations against industry standards (SaaS, AI, traditional)
  - Audits unit economics (CAC, LTV:CAC ratios)

**Usage:**

```bash
# Validate balance sheet identity
python execution/audit_financial_model.py --sheet-id "1ABC..." --mode balance

# Check cash runway
python execution/audit_financial_model.py --sheet-id "1ABC..." --mode runway

# Validate valuations for AI company
python execution/audit_financial_model.py --sheet-id "1ABC..." --mode valuation --company-type ai

# Check unit economics
python execution/audit_financial_model.py --sheet-id "1ABC..." --mode metrics

# Run all audits
python execution/audit_financial_model.py --sheet-id "1ABC..." --mode comprehensive
```

**Audit Modes:**
| Mode | Description |
|------|-------------|
| `balance` | Verify A = L + E for each year |
| `runway` | Check cash balances, identify negative runway |
| `valuation` | Compare multiples to benchmarks by company type |
| `metrics` | Validate CAC, LTV:CAC ratios |
| `comprehensive` | Run all audits, return summary |

**Company Types for Valuation:**
| Type | Seed Multiple | Series A Multiple |
|------|---------------|-------------------|
| `saas` | 8-15x | 6-12x |
| `ai` | 12-30x | 10-20x |
| `traditional` | 5-10x | 4-8x |

### Industry Benchmark Analysis

- `analyze_benchmarks.py` - **Research industry benchmarks using SerpAPI**
  - S&M spend benchmarks by company stage
  - CAC benchmarks by industry
  - Valuation multiples for AI vs traditional companies
  - Gross/EBITDA margin benchmarks

**Usage:**

```bash
# Get S&M spend benchmarks
python execution/analyze_benchmarks.py --mode sm --industry "3D printing software"

# Get CAC benchmarks
python execution/analyze_benchmarks.py --mode cac --industry "B2B SaaS manufacturing"

# Get valuation benchmarks
python execution/analyze_benchmarks.py --mode valuation --industry "AI automation"

# Get margin benchmarks
python execution/analyze_benchmarks.py --mode margins --industry "design software"

# Get all benchmarks
python execution/analyze_benchmarks.py --mode comprehensive --industry "design automation AI" --output benchmarks.json
```

**Benchmark Modes:**
| Mode | Description |
|------|-------------|
| `sm` | Sales & Marketing % of revenue by stage |
| `cac` | Customer acquisition cost benchmarks |
| `valuation` | Revenue multiples by company type |
| `margins` | Gross margin, EBITDA margin benchmarks |
| `comprehensive` | All of the above |

**Standard Benchmarks (Built-in):**

**S&M % of Revenue:**
| Stage | Range | Notes |
|-------|-------|-------|
| Pre-revenue (Y0) | 40-60% | Heavy GTM investment |
| Early (Y1-Y2) | 35-50% | Building sales, brand |
| Growth (Y3-Y4) | 25-40% | Scaling efficiently |
| Scale (Y5+) | 15-25% | Mature, word-of-mouth |

**Comparable Companies (Manufacturing/3D):**
| Company | S&M % | Gross Margin | Revenue |
|---------|-------|--------------|---------|
| Materialise | 23% | 56.5% | $289M |
| Stratasys | 25% | 45% | $573M |
| 3D Systems | 28% | 37-40% | $450M |

### Financial Model Repair

- `repair_financial_model.py` - **Comprehensive repair tool for fixing common issues**
  - Fixes formula errors (#REF!, #VALUE!, #DIV/0!)
  - Applies consistent number formatting across all sheets
  - Fixes balance sheet links (Cash, Equity, Retained Earnings)
  - Fixes cash flow links (PAT, Equity, Cumulative)
  - Fixes funding cap table calculations
  - Trims model to specified number of years
  - Rebalances S&M spend to target percentage

**Usage:**

```bash
# Run all fixes
python execution/repair_financial_model.py --sheet-id "1ABC..." --action all

# Check for formula errors
python execution/repair_financial_model.py --sheet-id "1ABC..." --action fix-formulas

# Fix number formatting
python execution/repair_financial_model.py --sheet-id "1ABC..." --action fix-formatting

# Fix balance sheet links
python execution/repair_financial_model.py --sheet-id "1ABC..." --action fix-balance-sheet

# Fix cash flow links
python execution/repair_financial_model.py --sheet-id "1ABC..." --action fix-cash-flow

# Fix funding schedule
python execution/repair_financial_model.py --sheet-id "1ABC..." --action fix-funding

# Trim to 5 years
python execution/repair_financial_model.py --sheet-id "1ABC..." --action trim-years --years 5

# Rebalance S&M to 35% of revenue
python execution/repair_financial_model.py --sheet-id "1ABC..." --action rebalance-sm --target-pct 35

# Verify cross-sheet links
python execution/repair_financial_model.py --sheet-id "1ABC..." --action verify-links
```

**Repair Actions:**
| Action | Description |
|--------|-------------|
| `fix-formulas` | Find and report formula errors |
| `fix-formatting` | Apply K/M currency formats, percentages |
| `fix-balance-sheet` | Link Cash, Equity, Retained Earnings properly |
| `fix-cash-flow` | Link PAT to P&L, Equity to Funding |
| `fix-funding` | Fix cumulative funding formulas |
| `trim-years` | Clear columns beyond specified years |
| `rebalance-sm` | Set S&M to target % of revenue |
| `verify-links` | Check all cross-sheet references |
| `all` | Run all fixes in sequence |

**Common Issues This Tool Fixes:**

1. Balance sheet doesn't balance (A ≠ L + E)
2. Cash not linking to Cash Flow cumulative
3. Retained Earnings not accumulating PAT correctly
4. Funding not flowing to Cash Flow Equity
5. Percentage cells showing decimals (0.25 instead of 25%)
6. Currency cells without K/M formatting
7. Model has 10 years but only need 5

### Google Docs

- `create_google_doc.py` - Create new documents
- `update_google_doc.py` - Update existing documents (append, prepend, replace)

### Google Sheets Utilities

- `sheets_utils.py` - Consolidated utility for reading, writing, and appending to Google Sheets
  - **Read**: `python execution/sheets_utils.py read --url <URL> [--worksheet <name>] [--output <file>]`
  - **Write**: `python execution/sheets_utils.py write --json <file> [--sheet-name <name>]`
  - **Append**: `python execution/sheets_utils.py append --url <URL> --json <file> [--worksheet <name>]`

### Pitch Deck Creation

- `create_pitch_deck.py` - Professional pitch deck generator
  - Creates decks programmatically with proper formatting
  - Includes References slide at the end of all deck types
  - Supports embedded charts from financial model

**Usage:**

```bash
# Create startup pitch deck (11 slides including References)
python execution/create_pitch_deck.py --company "MyCompany" --type startup

# Create minimal deck (6 slides including References)
python execution/create_pitch_deck.py --company "MyCompany" --type minimal

# Create Series A deck (15 slides including References)
python execution/create_pitch_deck.py --company "MyCompany" --type series_a

# Custom slide selection
python execution/create_pitch_deck.py --company "MyCompany" --slides "title,problem,solution,market,ask,references"

# With content from JSON file
python execution/create_pitch_deck.py --company "MyCompany" --type startup --content-file pitch_content.json
```

**Pitch Templates:**
| Type | Slides | Use Case |
|------|--------|----------|
| `minimal` | 6 | Quick overview, demo day |
| `seed` | 8 | Seed round pitch |
| `startup` | 10 | Standard startup pitch |
| `investor` | 12 | Investor meeting |
| `series_a` | 14 | Comprehensive Series A |
| `full` | 19 | Full presentation |

**Available Slide Types:**

- `title` - Opening slide with company name
- `introduction` - Company intro
- `company` - Company overview
- `team` - Team members
- `problem` - Problem statement
- `solution` - Solution description
- `swot` - SWOT analysis
- `product` - Product demo
- `traction` - Traction metrics
- `market` - TAM/SAM/SOM
- `target` - Target demographics
- `competitors` - Competitive analysis
- `business_model` - Revenue model
- `timeline` - Roadmap
- `growth` - Growth projections
- `financials` - Financial charts
- `ask` - Investment ask
- `closing` - Contact info

**Loading Financial Data from Spreadsheet:**

```bash
# Create pitch deck with data from financial model
python execution/create_pitch_deck.py --company "MyCompany" --type investor \
  --financial-model "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit" \
  --content-file pitch_content.json
```

The script will automatically:

1. Read the "Pitch Deck Data" sheet from the financial model
2. Extract key metrics (Revenue, EBITDA, Margins for Y1, Y5, Y10)
3. Populate the pitch deck slides with real financial data

**Content JSON Format:**

```json
{
  "tagline": "One-line description",
  "company_description": "Detailed description",
  "problems": ["Problem 1", "Problem 2"],
  "solutions": ["Solution 1", "Solution 2"],
  "tam": "$50B",
  "sam": "$5B",
  "som": "$500M",
  "revenue_y1": "$1M",
  "team": [{ "name": "John Doe", "role": "CEO" }],
  "contact_email": "hello@company.com",
  "contact_website": "www.company.com"
}
```

### Template File

- `10_Year_Financial_Model_Template.xlsx` - Excel template with all formulas
  - Can be parsed with openpyxl to understand structure
  - Structure saved to `.tmp/template_structure.json` for reference

---

## Markdown-as-Intermediate Workflow (MANDATORY)

**This is the standard pattern for editing Google Sheets.** Never edit Google Sheets directly through inline API calls or sequential cell updates. Instead, use a markdown file as the source of truth.

### Why This Pattern is Required

| Direct API Edits             | Markdown-as-Intermediate              |
| ---------------------------- | ------------------------------------- |
| Hard to review changes       | Clear diff in markdown                |
| Formatting inconsistent      | Centralized formatting in sync script |
| Easy to break formulas       | Formula logic in one place            |
| No audit trail               | Markdown file is version-controllable |
| Scattered logic              | Single source of truth                |
| Formula row references break | Row mapping in sync script            |

### The 3-Step Edit Pattern

**Step 1: Create/Update Markdown File** (Source of Truth)

- All sheet data lives in `.tmp/<sheet_name>.md`
- Markdown tables are human-readable and auditable
- Easy to review, diff, and version control
- Include row numbers for linkable values

**Step 2: Create Sync Script** (Deterministic Execution)

- Python script in `.tmp/sync_<sheet>_to_sheets.py`
- Reads markdown, parses tables, writes to Google Sheets
- Handles formatting, formulas, and colors consistently
- Maintains backward compatibility with existing formula references

**Step 3: Execute Sync** (Apply Changes)

- Run the sync script to push changes to Google Sheets
- Verify the changes in the cloud
- Keep markdown file as audit trail

### Markdown File Structure

```markdown
# Sheet Name - Project Name

> Last Updated: [Date]
>
> **IMPORTANT**: This Markdown file is the source of truth. Edit here, then sync to Google Sheets.
> Other sheets reference cells in this sheet - be careful with row numbers!

---

## SECTION A: KEY METRICS (Linkable Values)

### Category Name

| Row | Metric      | Value          | Unit | Source               | Notes          |
| --- | ----------- | -------------- | ---- | -------------------- | -------------- |
| 7   | Market Size | 60,180,000,000 | $    | Business Research Co | 2024 data      |
| 8   | Growth Rate | 5.25%          | %    | Industry Report      | CAGR 2024-2030 |
```

### Standard Intermediate Files

| File                             | Purpose                                       |
| -------------------------------- | --------------------------------------------- |
| `.tmp/sources_references.md`     | Sources & References sheet - TAM/SAM/SOM data |
| `.tmp/assumptions.md`            | Assumptions sheet parameters                  |
| `.tmp/market_analysis.md`        | Compiled market research                      |
| `.tmp/sync_<sheet>_to_sheets.py` | Sync script for each sheet                    |

### Sync Script Template

```python
"""
Sync <sheet_name>.md to Google Sheets
MAINTAINS EXISTING ROW STRUCTURE for backward compatibility
"""

import gspread
from google.oauth2.credentials import Credentials
import json
import time

SPREADSHEET_ID = "your-spreadsheet-id"
SHEET_NAME = "Sheet Name"

# Standard color definitions (RGB 0-1 scale)
COLORS = {
    "title": {"red": 0.20, "green": 0.30, "blue": 0.50},
    "section": {"red": 0.20, "green": 0.40, "blue": 0.60},
    "category": {"red": 0.30, "green": 0.50, "blue": 0.70},
    "column_header": {"red": 0.95, "green": 0.95, "blue": 0.95},
    "zebra": {"red": 0.85, "green": 0.92, "blue": 0.98},
    "total": {"red": 0.90, "green": 0.97, "blue": 0.90},
    "white": {"red": 1.0, "green": 1.0, "blue": 1.0},
}

def connect():
    with open("token.json", "r") as f:
        token_data = json.load(f)
    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"]
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID)

def build_data():
    """Build sheet data maintaining row positions for referenced cells"""
    # Build data array from markdown structure
    data = []
    fmt = {"title": [], "section": [], "category": [], "zebra": []}
    # ... parse markdown and build data
    return data, fmt

def apply_formatting(worksheet, sheet_id, fmt):
    """Apply consistent formatting"""
    requests = []
    # Build formatting requests
    # ... apply colors, fonts, etc.
    return requests

def main():
    ss = connect()
    ws = ss.worksheet(SHEET_NAME)
    data, fmt = build_data()
    ws.update('A1', data, value_input_option='USER_ENTERED')
    time.sleep(2)
    # Apply formatting
    apply_formatting(ws, ws.id, fmt)
    print("Done!")

if __name__ == "__main__":
    main()
```

### When to Use This Pattern

**ALWAYS use Markdown-as-Intermediate when:**

- Making more than 2-3 cell edits to a sheet
- Adding new sections or restructuring a sheet
- Updating data that other sheets reference (Sources & References)
- Formatting multiple rows/columns
- Adding new rows that may shift formula references

**Exception (Inline edits allowed):**

- Single-cell formula fixes
- Quick value corrections
- Testing/debugging (temporary)

### Benefits Demonstrated in RapidTools Project

1. **Audit Trail**: All Sources & References changes documented in `.tmp/sources_references.md`
2. **Reproducibility**: Can rebuild entire sheet by running sync script
3. **Row Stability**: Sync script maintains row numbers for cross-sheet references
4. **Formatting Consistency**: Colors, fonts, column widths defined once in sync script
5. **Formula Safety**: Formula logic centralized, not scattered across inline edits

---

### Financial Model Sheets

The financial model now creates 7 sheets (+ optional scenario sheets):

1. **Assumptions** - All input parameters
2. **Revenue** - Revenue calculations
3. **Operating Costs** - Variable and fixed costs
4. **P&L** - Profit & Loss statement
5. **Balance Sheet** - Assets, Liabilities, Equity
6. **Cash Flow** - Cash flow statement
7. **Pitch Deck Data** - Pre-calculated metrics for pitch decks
   - Revenue Y1, Y5, Y10
   - EBITDA Y1, Y5, Y10
   - Margins Y1, Y5, Y10
   - Total Funding (Equity + Debt)
   - Growth chart data (all 10 years)

---

## Outputs

| Output                 | Location           | Description                   |
| ---------------------- | ------------------ | ----------------------------- |
| Business Plan Document | Google Docs        | Full narrative business plan  |
| Financial Model        | Google Sheets      | 15-sheet comprehensive model  |
| Pitch Deck             | Google Slides      | Dynamic slides from template  |
| Market Research Data   | `.tmp/`            | JSON files with research data |
| Assumptions Log        | `.tmp/config.json` | All user-provided assumptions |

### References Integration Across All Deliverables

**All three deliverables must properly cite data sources:**

1. **Business Plan Document** (Google Docs)
   - Section 9: "References & Sources"
   - Lists all market research sources with URLs
   - Includes TAM/SAM/SOM sources, industry data, competitor info

2. **Financial Model** (Google Sheets)
   - Sheet 9: "Sources & References"
   - Structured table: Category | Data Point | Value | Source | URL
   - Covers market size, growth rates, pricing, customer metrics, competitors
   - **Must be populated with actual research data, not placeholders**

3. **Pitch Deck** (Google Slides)
   - Final slide: "Sources & References"
   - Condensed list of key sources (up to 12)
   - Links to full sources in Financial Model sheet

**Required Source Categories:**
| Category | Data Points to Source |
|----------|----------------------|
| Market Size | TAM, SAM, SOM values with calculation methodology |
| Growth Rates | Industry CAGR, market growth forecasts |
| Pricing | Industry pricing benchmarks, competitor pricing |
| Costs | COGS by type (software 10-20%, hardware 35-45%, services 50-60%) |
| Customer Metrics | CAC benchmarks, LTV:CAC ratios, churn rates |
| Competitors | Key competitors with market position and revenue |
| Internal Data | Parent company metrics, existing customers |

---

## Geographic Expansion Modeling

**For businesses with phased geographic expansion, model growth rates to reflect expansion phases:**

**Example: India → Southeast Asia → Europe → Global**

| Phase   | Years | Markets     | Growth Rate Adjustment        |
| ------- | ----- | ----------- | ----------------------------- |
| Phase 1 | Y0-Y1 | India + SEA | Base growth (40-60%)          |
| Phase 2 | Y2    | + Europe    | Accelerated (70-100%)         |
| Phase 3 | Y3+   | Global      | Peak then decline (80% → 15%) |

**Implementation:**

1. Set different growth rates for each year in Assumptions sheet
2. Growth rates should peak at expansion years, then gradually decline
3. Consider market saturation and competition in later years

**Growth Rate Pattern (Aggressive Expansion):**

```
Year 1: 60% (India + SEA launch)
Year 2: 80-100% (Europe expansion)
Year 3: 80-100% (Global reach)
Year 4: 60-70% (Market penetration)
Year 5+: 25-40% (Maturation)
Year 8+: 15-25% (Steady state)
```

> Use `update_financial_model.py --action update-growth` to update growth rates for expansion scenarios.

---

## Edge Cases and Error Handling

### Balance Sheet Doesn't Balance

- Check retained earnings calculation
- Verify working capital components
- Confirm debt/equity movements match cash flow

### Negative Cash Position

- Flag to user immediately
- Suggest additional funding or cost reduction
- Show which year cash goes negative

### IRR Cannot Be Calculated

- Ensure there's at least one sign change in cash flows
- Check if initial investment is negative (outflow)
- Verify terminal value or exit assumptions

### Unrealistic Assumptions

- Compare to industry benchmarks from research
- Flag assumptions outside normal ranges
- Suggest adjustments with reasoning

---

## VALIDATION & QUALITY ASSURANCE

**Always run validation after creating a financial model.**

### Validation Script

```bash
python execution/validate_financial_model.py --url "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID"
```

### Core Accounting Checks (Non-Negotiable)

| Check                  | Rule                          | If Fails                         |
| ---------------------- | ----------------------------- | -------------------------------- |
| Balance Sheet Identity | Assets = Liabilities + Equity | Model is fundamentally broken    |
| Cash Reconciliation    | CF Cumulative Cash = BS Cash  | Cash flow not connected properly |
| Retained Earnings      | RE*t = RE*{t-1} + PAT         | P&L not flowing to Balance Sheet |
| Net Income Linkage     | P&L PAT = CF Starting Point   | Statements not linked            |
| Depreciation Loop      | P&L Depr = CF Add-back        | Capex/Depr not consistent        |

### Three-Statement Linkage Checks

1. **Net Income Consistency**
   - P&L Net Income → Cash Flow (CFO starting point) → Balance Sheet (Retained Earnings)
   - If any differ → broken links

2. **Depreciation & Capex Loop**
   - Capex increases Fixed Assets
   - Depreciation reduces Fixed Assets
   - Depreciation added back in CFO
   - Fixed Assets should never go negative

3. **Working Capital Integrity**
   - Change in Debtors/Creditors flows through CFO
   - WC days should be reasonable (typically 30-90 days)

### Sanity Checks

| Check          | Warning Threshold                    |
| -------------- | ------------------------------------ |
| Revenue Growth | >300% or <-50% flagged               |
| EBITDA Margin  | >90% or <-50% flagged                |
| Debtor Days    | >90 days flagged                     |
| Negative Cash  | Warn but may be valid in early years |

### Sign Discipline

| Item           | Expected Sign       |
| -------------- | ------------------- |
| Revenue        | Positive            |
| Costs          | Positive            |
| Capex (in CF)  | Negative            |
| Debt Repayment | Negative            |
| Depreciation   | Positive (add-back) |

### Error Detection

Check for these formula errors:

- `#REF!` - Broken reference
- `#NAME?` - Invalid function/name
- `#VALUE!` - Wrong data type
- `#DIV/0!` - Division by zero
- `#N/A` - Lookup failed

### Stress Tests

1. **Zero Revenue Test**: Do fixed costs still show?
2. **Double Revenue Test**: Do variable costs scale correctly?
3. **No Funding Test**: Does cash go negative appropriately?
4. **Sensitivity Test**: Change one input → all dependent outputs should move logically

### When Validation Fails

1. Identify the specific check that failed
2. Trace back to the formula causing the issue
3. Fix the formula (usually a reference or link)
4. Re-run validation
5. Document what was learned in this directive

---

## Example Conversation Flow

**User:** "I want to start a cloud kitchen business in Bangalore"

**Agent:**
"Great! Cloud kitchens are growing rapidly in India. Let me research the market first..."

_[Runs market research]_

"Here's what I found:

- Indian cloud kitchen market: ₹4,000 Cr+ by 2025, growing 25%+ annually
- Key players: Rebel Foods (Faasos), CloudKitch, Kitchens@
- Average order value: ₹250-400
- Typical unit economics: 30-40% food cost, 20-25% delivery commission

Let's start building your model. First, the basics:

1. What type of cuisine/food will you focus on?
2. What's your expected average order value?
3. How many orders per day are you targeting in Year 1?"

_[Continues gathering Step 1-14 data progressively...]_

---

## Required Environment Variables

```env
SERPAPI_API_KEY=your_serpapi_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

## Dependencies

```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
google-search-results
gspread
pandas
python-dotenv
```

---

## Known Issues & Learnings

### Google Sheets Editing - Use Markdown-as-Intermediate (MANDATORY)

**Problem:** Direct inline API calls to Google Sheets cause several issues:

- Formula references break when rows shift
- Formatting inconsistencies across multiple edit sessions
- No audit trail of changes made
- Difficult to review or revert changes
- PowerShell quote escaping issues with complex formulas

**Solution:** Always use the Markdown-as-Intermediate pattern:

1. Create/update a markdown file in `.tmp/<sheet_name>.md`
2. Create a sync script `.tmp/sync_<sheet>_to_sheets.py`
3. Run the sync script to apply changes

**See the "Markdown-as-Intermediate Workflow" section above for full details.**

**Exception:** Single-cell fixes (1-2 cells) can be done inline for speed.

### Google API Rate Limits (429 Errors)

**Problem:** Google Sheets API has strict rate limits. Creating multiple sheets or formatting many cells rapidly triggers 429 errors.

**Solution:**

- Add `time.sleep(2-3)` between sheet operations
- Add `time.sleep(0.3-0.5)` between cell formatting operations
- Use batch updates when possible instead of individual cell updates
- Wait 60-90 seconds between major sheet creation operations

**Implementation:**

```python
def rate_limit_delay(seconds=2):
    """Add delay to avoid Google API rate limits."""
    time.sleep(seconds)
```

### Percentage Formatting Issues

**Problem:** Percentages stored as decimals (0.25) display as "0.25" instead of "25.0%".

**Solution:**

```python
pct_format = {'numberFormat': {'type': 'PERCENT', 'pattern': '0.0%'}}
worksheet.format('C4:M4', pct_format)
```

**Apply to all percentage rows:**

- Assumptions: Growth rates, COGS %, Tax rate
- P&L: Gross Margin %, EBITDA Margin %, Net Margin %
- Customer Economics: Churn Rate, Retention Rate
- Sensitivity Analysis: Change percentages
- Financial Ratios: All margin ratios

### Sources Sheet Not Auto-Populated

**Problem:** The create_financial_model.py script creates a Sources & References sheet with placeholder values.

**Solution:**

- Always run market research BEFORE creating the financial model
- Use `update_financial_model.py --action update-sources` to populate actual data
- Store research results in `.tmp/` and reference when building sources

### Multi-Revenue Stream Complexity

**Problem:** Businesses with 5+ revenue streams make the Assumptions and Revenue sheets complex.

**Best Practices:**

- Group similar streams (e.g., "Hardware" = Printers + Spares)
- Use consistent naming conventions
- Document stream dependencies in Sources sheet

### Growth Rate Modeling for Global Expansion

**Problem:** Flat growth rates don't reflect expansion dynamics.

**Solution:** Use phased growth rates:

- Phase 1 (Launch): 40-60% growth
- Phase 2 (Expansion): 70-100% growth
- Phase 3 (Global): Peak at 80-100%, then decline
- Phase 4 (Maturity): 15-25% steady state

### Pitch Deck API Errors

**Problem:** `create_pitch_deck.py` sometimes fails with "object has no text" errors when financial data is missing.

**Solution:**

- Use simpler deck types (`seed` or `minimal`) when data is incomplete
- Ensure all required content fields are populated in JSON
- The `investor` and `series_a` types require complete financial data

---

## Session Learnings Log

**2026-01-19: RapidTools Business Plan**

- Created 15-sheet financial model with 5 revenue streams
- Added Headcount Plan sheet for team growth modeling
- Implemented geographic expansion growth modeling (India → SEA → Europe → Global)
- Fixed percentage formatting across all sheets
- Populated Sources & References with actual market research
- Created seed pitch deck (investor type had API errors)
- Learned: Always add rate limiting delays for Google API operations
