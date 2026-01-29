# 02 - Assumptions Sheet

> **Last Updated:** 2026-01-28  
> **Purpose:** Central input sheet for all model parameters - links to Sources & References  
> **Sheet Position:** 2 of 14

---

## Overview

The Assumptions sheet is the **single source of truth for all model inputs**. It contains:

1. General parameters (tax, capex, depreciation, etc.)
2. Revenue stream pricing and volumes (linked to Sources & References)
3. Fixed costs with inflation adjustments
4. Customer acquisition metrics
5. Geographic expansion percentages
6. Industry segment breakdown
7. Key relationship status tracking

**Key Principle:** Prices and COGS % should link to Sources & References. Volumes are explicit inputs.

---

## Sheet Structure

### Row Layout

| Row Range | Section                  | Description                                         |
| --------- | ------------------------ | --------------------------------------------------- |
| 1-2       | Header                   | Sheet title and year labels                         |
| 3-12      | GENERAL PARAMETERS       | Tax, capex, depreciation, working capital           |
| 14-38     | REVENUE STREAMS          | 6 streams with price, volume, growth, COGS          |
| 40-41     | PEOPLE COST              | Salaries & Benefits (from Headcount)                |
| 43-48     | S&M VARIABLE             | Marketing, trade shows, VAR incentives, commissions |
| 50-60     | FIXED COSTS (G&A)        | Facilities, tools, R&D, professional services       |
| 62-63     | STOCK-BASED COMPENSATION | Non-cash equity grants                              |
| 65-75     | CUSTOMER ACQUISITION     | CAC, churn, lifetime, customer counts               |
| 77-86     | GEOGRAPHIC EXPANSION     | Revenue % by region                                 |
| 88-94     | INDUSTRY SEGMENTS        | Revenue % by vertical                               |
| 96-99     | KEY RELATIONSHIPS        | Status tracking (Honda, Toyota, TVS)                |

---

## GENERAL PARAMETERS (Rows 3-12)

| Row | Parameter           | Unit | Y0        | Y1      | Y2      | Y3         | Y4      | Y5         | Formula/Source                                                       |
| --- | ------------------- | ---- | --------- | ------- | ------- | ---------- | ------- | ---------- | -------------------------------------------------------------------- |
| 4   | Tax Rate            | %    | 30%       | 30%     | 30%     | 30%        | 30%     | 30%        | India corporate tax                                                  |
| 5   | Capex               | $    | 75,000    | 100,000 | 200,000 | 300,000    | 500,000 | 750,000    | [BP 09_Fundraising_Strategy.md L313-317](#capex-source)              |
| 6   | Depreciation Years  | yrs  | 5         | 5       | 5       | 5          | 5       | 5          | Straight-line (5-7 year useful life per BP 07_Revenue_Model.md L966) |
| 7   | Debtor Days         | days | 45        | 45      | 45      | 45         | 45      | 45         | [BP 07_Revenue_Model.md L1160](#working-capital-source)              |
| 8   | Creditor Days       | days | 30        | 30      | 30      | 30         | 30      | 30         | [BP 07_Revenue_Model.md L1161](#working-capital-source)              |
| 9   | Interest Rate       | %    | 10%       | 10%     | 10%     | 10%        | 10%     | 10%        | India lending rate                                                   |
| 10  | Equity Infusion     | $    | 3,000,000 | 0       | 0       | 10,000,000 | 0       | 25,000,000 | [BP 09_Fundraising_Strategy.md L56, L186, L228](#funding-source)     |
| 11  | Debt Drawdown       | $    | 0         | 0       | 0       | 0          | 0       | 0          | No debt initially                                                    |
| 12  | Cost Inflation Rate | %    | 5%        | 5%      | 5%      | 5%         | 5%      | 5%         | India CPI benchmark                                                  |

### CapEx Breakdown (from Business Plan) {#capex-source}

**Source:** [09_Fundraising_Strategy.md](../business_plan/sections/09_Fundraising_Strategy.md#L307-L317)

RapidTools is **asset-light**—Fracktal Works provides manufacturing capacity for Tooling Services at cost:

| Category            | Y1        | Y2        | Y3        | Y4        | Y5+          |
| ------------------- | --------- | --------- | --------- | --------- | ------------ |
| IT Equipment        | $50K      | $100K     | $150K     | $200K     | $300K/yr     |
| Office Buildout     | $0        | $50K      | $100K     | $150K     | $200K/yr     |
| Demo Equipment      | $50K      | $50K      | $50K      | $100K     | $150K/yr     |
| Security/Compliance | $0        | $0        | $0        | $50K      | $100K/yr     |
| **Total CapEx**     | **$100K** | **$200K** | **$300K** | **$500K** | **$750K/yr** |

### Working Capital Metrics (from Business Plan) {#working-capital-source}

**Source:** [07_Revenue_Model.md](../business_plan/sections/07_Revenue_Model.md#L1145-L1200)

| Metric                           | Value   | Rationale                                        |
| -------------------------------- | ------- | ------------------------------------------------ |
| Days Sales Outstanding (DSO)     | 45 days | Enterprise Net-45; SMB/Mid-market Net-30 blended |
| Days Payable Outstanding (DPO)   | 30 days | Standard supplier terms (India)                  |
| Days Inventory Outstanding (DIO) | 15 days | Minimal—consumables buffer only                  |
| Cash Conversion Cycle            | 30 days | DSO + DIO − DPO = 45 + 15 − 30                   |

### Funding Rounds (from Business Plan) {#funding-source}

**Source:** [09_Fundraising_Strategy.md](../business_plan/sections/09_Fundraising_Strategy.md)

| Round        | Amount     | Timing           | Pre-Money | Post-Money | Dilution | BP Reference     |
| ------------ | ---------- | ---------------- | --------- | ---------- | -------- | ---------------- |
| **Seed**     | $3.0M      | Y0 (Jan 2026)    | $10M      | $13M       | 23%      | [L56](#ref-seed) |
| **Series A** | $10.0M     | Y3 Q2 (Jun 2028) | $30M      | $40M       | 25%      | [L186](#ref-a)   |
| **Series B** | $25.0M     | Y5 Q2 (Jun 2030) | $75M      | $100M      | 25%      | [L228](#ref-b)   |
| **Total**    | **$38.0M** | —                | —         | —          | —        | —                |

---

## REVENUE STREAMS (Rows 14-38)

### Software Subscription (Rows 15-18)

| Row | Metric    | Unit  | Y0    | Y1               | Y2               | Y3    | Y4    | Y5     | Formula                                           |
| --- | --------- | ----- | ----- | ---------------- | ---------------- | ----- | ----- | ------ | ------------------------------------------------- |
| 15  | Net Price | $     | 2,272 | 2,088            | 1,964            | 1,909 | 1,876 | 1,876  | `='Sources & References'!B75:B80` (by year)       |
| 16  | Volume    | seats | 120   | 665              | 1,989            | 4,384 | 9,082 | 15,932 | Customers × Seats/Customer                        |
| 17  | Growth    | %     | 0%    | `=(D16-C16)/C16` | `=(E16-D16)/D16` | ...   | ...   | ...    | Calculated                                        |
| 18  | COGS %    | %     | 20%   | 20%              | 20%              | 20%   | 20%   | 20%    | [BP 07_Revenue_Model.md L251-260](#cogs-software) |

**Pricing Documentation:**

- **List Price:** $2,400/seat/year (what customer pays at SMB tier)
- **Volume Discounts:** 10% Mid-Market, 20% Enterprise
- **Channel Commission:** 0% Direct, 27% VAR, 25% Distributor, 10% OEM ([BP 06_Go_To_Market L821](#channel-source))
- **Blended Channel Cost:** Evolves from 5.3% (Y0, mostly direct) to 21.8% (Y5, VAR-dominant)
- **Net Recognized Price:** List Price × (1 - Blended Channel Cost)

**COGS Source:** {#cogs-software} Per business plan, Software COGS is 17-23% (target 80% gross margin). Using 20% midpoint.

- Cloud Infrastructure: 8-10%
- Third-Party APIs: 2-3%
- Customer Success: 5-7%
- Payment Processing: 2-3%

**Volume Calculation (Realistic Seats per Customer):**

- Y0: 20 customers × 6.0 seats = 120 seats (enterprise pilots: Honda, TVS)
- Y1: 133 customers × 5.0 seats = 665 seats (building VAR channel)
- Y2: 442 customers × 4.5 seats = 1,989 seats (SMB growing via VARs)
- Y3: 1,096 customers × 4.0 seats = 4,384 seats (VAR-led growth)
- Y4: 2,390 customers × 3.8 seats = 9,082 seats (65% channel, SMB-heavy)
- Y5: 4,552 customers × 3.5 seats = 15,932 seats (mature: 70% SMB, 25% MM, 5% Ent)

**Segment Mix at Maturity (Y5):**

- SMB (70%): 3,186 customers × 2.0 seats = 6,372 seats
- Mid-Market (25%): 1,138 customers × 5.0 seats = 5,690 seats
- Enterprise (5%): 228 customers × 15.0 seats = 3,420 seats
- **Total: 4,552 customers × 3.5 avg = 15,933 seats**

### 3D Printer Sales (Rows 19-22)

| Row | Metric | Unit  | Y0    | Y1    | Y2    | Y3    | Y4    | Y5    | Formula                                                  |
| --- | ------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- | -------------------------------------------------------- |
| 19  | Price  | $     | 7,000 | 7,000 | 7,000 | 7,000 | 7,000 | 7,000 | `='Sources & References'!B82`                            |
| 20  | Volume | units | 8     | 35    | 90    | 171   | 342   | 500   | BP target mix (HW = 7-12% of rev)                        |
| 21  | Growth | %     | 0%    | calc  | calc  | calc  | calc  | calc  | `=IF(C20=0,0,(D20-C20)/C20)`                             |
| 22  | COGS % | %     | 76%   | 76%   | 76%   | 76%   | 76%   | 76%   | [BP 07_Revenue_Model.md - Hardware COGS](#cogs-hardware) |

**COGS Source:** {#cogs-hardware} Per business plan, Hardware gross margin is 24% blended (Fracktal 28% @ arm's-length pricing, Partners 17%). COGS = 76%.

- Vendor Purchase Cost: 66-70% (Fracktal) or 78-82% (Partners)
- Logistics/Shipping: 3-4%
- Installation Support: 2-3%

**Note:** Fracktal Works is a separate company treated at arm's-length. Preferred vendor pricing yields 28% margin vs. 30% vertical integration.

**Volume Calculation (BP Target Mix):**

- Hardware revenue target: 12% (Y0) → 7% (Y5) of total revenue
- Implied attach rate declines as software grows faster
- Y0: $60K HW rev ÷ $7K = 8 printers (40% attach of 20 customers)
- Y1: $250K HW rev ÷ $7K = 35 printers (26% attach of 133 customers)
- Y2: $630K HW rev ÷ $7K = 90 printers (20% attach of 442 customers)
- Y3: $1,200K HW rev ÷ $7K = 171 printers (16% attach of 1,096 customers)
- Y4: $2,400K HW rev ÷ $7K = 342 printers (14% attach of 2,390 customers)
- Y5: $3,500K HW rev ÷ $7K = 500 printers (11% attach of 4,552 customers)

**Why Declining Attach Rate?** Software revenue grows ~20x from Y0→Y5, hardware only ~6x. This reflects:

1. SMB customers (70% at maturity) prefer services over hardware ownership
2. Enterprise customers (high attach) become smaller % of mix
3. Hardware is strategic enabler, not primary revenue driver

### Consumables Materials (Rows 23-26)

| Row | Metric | Unit  | Y0  | Y1   | Y2    | Y3    | Y4    | Y5    | Formula                                         |
| --- | ------ | ----- | --- | ---- | ----- | ----- | ----- | ----- | ----------------------------------------------- |
| 23  | Price  | $     | 60  | 60   | 60    | 60    | 60    | 60    | `='Sources & References'!B83`                   |
| 24  | Volume | units | 166 | 833  | 1,166 | 2,500 | 5,000 | 8,333 | BP target mix (1-2% of rev)                     |
| 25  | Growth | %     | 0%  | calc | calc  | calc  | calc  | calc  | Calculated                                      |
| 26  | COGS % | %     | 67% | 67%  | 67%   | 67%   | 67%   | 67%   | [BP 07_Revenue_Model.md L15](#cogs-consumables) |

**COGS Source:** {#cogs-consumables} Per business plan, Consumables gross margin is 30-35%. Using 33% GM → 67% COGS.

**Volume Calculation (BP Target Mix):**

- Consumables revenue target: 1-2% of total revenue
- Y0: $10K rev ÷ $60 = 166 units
- Y1: $50K rev ÷ $60 = 833 units
- Y2: $70K rev ÷ $60 = 1,166 units
- Y3: $150K rev ÷ $60 = 2,500 units
- Y4: $300K rev ÷ $60 = 5,000 units
- Y5: $500K rev ÷ $60 = 8,333 units

**Volume Calculation:**

- Based on 40 units/printer/year from Sources & References B94
- Cumulative printers in field consumption rate

### AMC Spares (Rows 27-30)

| Row | Metric | Unit      | Y0  | Y1   | Y2   | Y3   | Y4   | Y5   | Formula                       |
| --- | ------ | --------- | --- | ---- | ---- | ---- | ---- | ---- | ----------------------------- |
| 27  | Price  | $         | 500 | 500  | 500  | 500  | 500  | 500  | `='Sources & References'!B69` |
| 28  | Volume | contracts | 3   | 15   | 45   | 100  | 213  | 399  | Cumulative printers 35%       |
| 29  | Growth | %         | 0%  | calc | calc | calc | calc | calc | Calculated                    |
| 30  | COGS % | %         | 60% | 60%  | 60%  | 60%  | 60%  | 60%  | `='Sources & References'!B77` |

**COGS Breakdown (60%):**

- OEM/VAR Revenue Share: 30-40% (Fracktal 30%, third-party OEMs 40%, blended 34%)
- Spare Parts (OEM-sourced): 10-15%
- Technician Time: 8-12%
- Logistics: 3-5%
- Platform/Tracking: 2-3%

**Volume Formula:**

```
=ROUND(SUM($C$20:C20)*'Sources & References'!B95, 0)
```

- Cumulative printer sales 35% AMC attach rate

### Managed Services (Rows 31-34)

| Row | Metric | Unit      | Y0     | Y1     | Y2     | Y3     | Y4     | Y5     | Formula                                            |
| --- | ------ | --------- | ------ | ------ | ------ | ------ | ------ | ------ | -------------------------------------------------- |
| 31  | Price  | $         | 30,000 | 30,000 | 30,000 | 30,000 | 30,000 | 30,000 | `='Sources & References'!B70`                      |
| 32  | Volume | contracts | 0      | 1      | 11     | 40     | 70     | 116    | 5% of customers                                    |
| 33  | Growth | %         | 0%     | calc   | calc   | calc   | calc   | calc   | Calculated                                         |
| 34  | COGS % | %         | 72%    | 72%    | 72%    | 72%    | 72%    | 72%    | [BP 07_Revenue_Model.md L364, L388-394](#cogs-ems) |

**COGS Source:** {#cogs-ems} Per business plan, EMS gross margin is 25-30% (target 28%). Using 72% COGS.

- Staff Costs: 45-55%
- Equipment/Materials: 10-15%
- Software Platform: 5%
- Overhead/Management: 8-12%

**Volume Calculation:**

- Based on 5% managed services rate from Sources & References B98
- Ramp-up in early years, then steady 5% of customer base

### Job Work Services / Tooling Services (Rows 35-38)

| Row | Metric | Unit | Y0    | Y1    | Y2     | Y3     | Y4     | Y5      | Formula                                                           |
| --- | ------ | ---- | ----- | ----- | ------ | ------ | ------ | ------- | ----------------------------------------------------------------- |
| 35  | Price  | $    | 100   | 100   | 100    | 100    | 100    | 100     | `='Sources & References'!B86`                                     |
| 36  | Volume | jobs | 1,500 | 7,500 | 20,290 | 43,500 | 81,000 | 125,000 | BP target mix (25-30% of rev)                                     |
| 37  | Growth | %    | 0%    | calc  | calc   | calc   | calc   | calc    | Calculated                                                        |
| 38  | COGS % | %    | 75%   | 75%   | 75%    | 75%    | 75%    | 75%     | [BP 07_Revenue_Model.md - Third-party fulfillment](#cogs-tooling) |

**COGS Source:** {#cogs-tooling} Per business plan, Job Work uses **third-party fulfillment model**. RapidTools partners with local 3D printing bureaus (including Fracktal as one arm's-length vendor) and takes arbitrage margin. Target gross margin: **25%**.

| Cost Component         | % of Revenue | Description                                              |
| ---------------------- | ------------ | -------------------------------------------------------- |
| **Vendor Invoice**     | 50-60%       | Payment to fulfillment partner (Fracktal, local bureaus) |
| **Platform Fee**       | 3-5%         | Order management, job routing, quality tracking          |
| **Quality Assurance**  | 2-3%         | Spot-check QC, customer issue resolution                 |
| **Shipping/Logistics** | 8-10%        | Delivery from partner to customer                        |
| **Customer Support**   | 2-3%         | Order tracking, issue handling                           |
| **TOTAL COGS**         | **65-81%**   |                                                          |
| **Blended COGS**       | **75%**      | Target **25% gross margin**                              |

**Volume Calculation:**

- **46% blended job work attach rate** (SMB 45% × 70% + Mid-Market 55% × 25% + Enterprise 35% × 5%)
- Source: `='Sources & References'!B96`
- 46% attach × customers × 24 jobs/customer/year
- Higher attach for customers without 3D printers (outsource job work)
- **Note:** Job Work and Hardware are substitutes—customers typically do one or the other

---

## PEOPLE COST (Rows 40-41)

| Row | Cost Category       | Unit | Y0      | Y1        | Y2        | Y3        | Y4        | Y5         | Formula Pattern         |
| --- | ------------------- | ---- | ------- | --------- | --------- | --------- | --------- | ---------- | ----------------------- |
| 41  | Salaries & Benefits | $    | 800,000 | 1,610,000 | 3,290,000 | 5,760,000 | 9,500,000 | 14,040,000 | `='Headcount Plan'!C74` |

**Source:** BP 08_Team_Organization_Fixed_Costs.md L381-391 (Total People Cost by Year)

---

## S&M VARIABLE (Rows 43-48)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L724-732 (Total Operating Costs by Year)

| Row | Cost Category          | Unit | Y0              | Y1              | Y2              | Y3              | Y4              | Y5              | Formula Pattern         |
| --- | ---------------------- | ---- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ----------------------- |
| 44  | Marketing Programs     | $    | 50,000          | 200,000         | 400,000         | 900,000         | 1,600,000       | 2,500,000       | ~5% of revenue at scale |
| 45  | Trade Shows & Events   | $    | 10,000          | 50,000          | 100,000         | 200,000         | 400,000         | 500,000         | ~1% of revenue          |
| 46  | VAR Incentives         | $    | 0               | 0               | 150,000         | 300,000         | 700,000         | 2,000,000       | Starts Y2 with channel  |
| 47  | Sales Commissions      | $    | 0               | 0               | 50,000          | 100,000         | 300,000         | 500,000         | ~15% of direct sales    |
| 48  | **Total S&M Variable** | $    | `=SUM(C44:C47)` | `=SUM(D44:D47)` | `=SUM(E44:E47)` | `=SUM(F44:F47)` | `=SUM(G44:G47)` | `=SUM(H44:H47)` | Sum of components       |

**S&M Variable Totals:** $60K → $250K → $700K → $1,500K → $3,000K → $5,500K

**S&M Variable Scaling Rules:**

- **Marketing Programs**: ~5% of revenue target, includes digital marketing, content, demand gen
- **Trade Shows**: 10-15% of marketing budget, critical for manufacturing industry presence
- **VAR Incentives**: SPIFs, MDF, volume bonuses paid FROM net revenue (starts Y2 with channel)
- **Sales Commissions**: 15-20% of direct sales revenue (AEs start Y2)

---

## FIXED COSTS - G&A (Rows 50-60)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L425-437 (Fixed Cost Scaling by Year) and L454-660 (Year 4 Detail)

| Row | Cost Category                   | Unit | Y0              | Y1              | Y2              | Y3              | Y4              | Y5              | Formula Pattern                 |
| --- | ------------------------------- | ---- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------------- |
| 51  | Facilities (Office + Warehouse) | $    | 15,000          | 38,000          | 70,000          | 264,000         | 410,000         | 590,000         | Step function with expansion    |
| 52  | Technology & Tools              | $    | 45,000          | 90,000          | 160,000         | 378,000         | 580,000         | 840,000         | Cloud, dev tools, security      |
| 53  | R&D Infrastructure              | $    | 25,000          | 50,000          | 75,000          | 168,000         | 300,000         | 440,000         | CAD licenses, ML compute        |
| 54  | R&D Partnerships & IP           | $    | 16,000          | 32,000          | 52,000          | 114,000         | 190,000         | 280,000         | University, patents, prototypes |
| 55  | Professional Services           | $    | 25,000          | 55,000          | 105,000         | 216,000         | 320,000         | 450,000         | Legal, accounting, consulting   |
| 56  | Operations & Travel             | $    | 20,000          | 45,000          | 90,000          | 222,000         | 380,000         | 520,000         | Travel, insurance, localization |
| 57  | Customer Enablement             | $    | 10,000          | 22,000          | 40,000          | 84,000          | 130,000         | 170,000         | LMS, CAB, training              |
| 58  | Employee Development            | $    | 10,000          | 20,000          | 44,000          | 90,000          | 140,000         | 200,000         | L&D, certifications             |
| 59  | Contingency & Reserves          | $    | 14,000          | 18,000          | 44,000          | 66,000          | 50,000          | 110,000         | 3-5% of G&A buffer              |
| 60  | **Total Fixed Costs (G&A)**     | $    | `=SUM(C51:C59)` | `=SUM(D51:D59)` | `=SUM(E51:E59)` | `=SUM(F51:F59)` | `=SUM(G51:G59)` | `=SUM(H51:H59)` | Sum of components               |

**G&A Fixed Totals:** $180K → $370K → $680K → $1,602K → $2,500K → $3,600K

**BP Alignment (08_Team_Organization_Fixed_Costs.md L425-437):**

| Year       | BP Fixed Costs | Model G&A | Model SBC | Model Total | Variance |
| ---------- | -------------- | --------- | --------- | ----------- | -------- |
| Y0 (BP Y1) | $200K          | $180K     | $20K      | $200K       | 0%       |
| Y1 (BP Y2) | $420K          | $370K     | $50K      | $420K       | 0%       |
| Y2 (BP Y3) | $780K          | $680K     | $100K     | $780K       | 0%       |
| Y3 (BP Y4) | $1,750K        | $1,602K   | $150K     | $1,752K     | +0.1%    |
| Y4 (BP Y5) | $2,800K        | $2,500K   | $300K     | $2,800K     | 0%       |
| Y5 (BP Y6) | $4,200K        | $3,600K   | $600K     | $4,200K     | 0%       |

**BP Validation (08_Team_Organization_Fixed_Costs.md Year 4 Detail):**

| Category                  | BP Y4 (L454-660) | Model Y3 | Status |
| ------------------------- | ---------------- | -------- | ------ |
| Facilities                | $264,000         | $264,000 | Match  |
| Technology & Tools        | $378,000         | $378,000 | Match  |
| R&D Infrastructure        | $168,000         | $168,000 | Match  |
| R&D Partnerships & IP     | $114,000         | $114,000 | Match  |
| Professional Services     | $216,000         | $216,000 | Match  |
| Operations & Travel       | $222,000         | $222,000 | Match  |
| Customer Enablement       | $84,000          | $84,000  | Match  |
| Employee Development      | $90,000          | $90,000  | Match  |
| Contingency & Reserves    | $66,000          | $66,000  | Match  |
| **TOTAL G&A (excl. SBC)** | **$1,602,000**   | $1,602K  | Match  |

**Note:** BP Fixed Costs table (L425-437) shows $1,750K for Y4 which includes SBC ($150K). Model separates G&A ($1,602K) from SBC ($150K).

**Fixed Cost Line Item Detail (from BP 08_Team L454-660):**

| Category                     | Components                                                                                |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| **Facilities ($264K)**       | Bangalore HQ $96K, Mumbai $48K, Singapore $96K, Utilities $24K                            |
| **Technology ($378K)**       | Cloud $180K, DevTools $48K, Productivity $30K, Design $12K, Sales $36K, Security $72K     |
| **R&D Infra ($168K)**        | CAD/CAM $60K, ML Compute $48K, Data Platform $30K, Testing $18K, APIs $12K                |
| **R&D Partnerships ($114K)** | University $30K, Patents $36K, Maintenance $18K, Prototypes $18K, Conferences $12K        |
| **Professional ($216K)**     | Legal $60K, Accounting $36K, HR/Recruiting $30K, Consultants $30K, Analyst Relations $60K |
| **Operations ($222K)**       | Insurance $30K, Travel-Sales $72K, Travel-Exec $30K, Localization $42K, Bad Debt $48K     |
| **Enablement ($84K)**        | LMS $24K, Content $30K, Certification $12K, CAB $18K                                      |
| **Employee Dev ($90K)**      | L&D $42K, Certifications $18K, Events $24K, Recognition $6K                               |
| **Contingency ($66K)**       | Operating $42K, Legal/IP Reserve $24K                                                     |

**G&A Fixed Cost Scaling Rules:**

- **Facilities**: Step function with geographic expansion (Bangalore → Mumbai Y2 → Singapore Y3)
- **Technology**: Cloud infra scales with customers + dev tools with headcount + SOC2/ISO compliance at Y3+
- **R&D Infra**: CAD/CAM licenses + ML/AI compute for generative design
- **R&D Partnerships**: University research, patent filings, prototype materials
- **Professional Services**: Scale with complexity (analyst relations for enterprise sales)
- **Professional Services**: Scale with complexity (SOC2/ISO compliance at Y3+)

---

## STOCK-BASED COMPENSATION (Rows 62-63)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L679-682

| Row | Metric                   | Unit | Y0     | Y1     | Y2      | Y3      | Y4      | Y5      | Formula Pattern        |
| --- | ------------------------ | ---- | ------ | ------ | ------- | ------- | ------- | ------- | ---------------------- |
| 63  | Stock-Based Compensation | $    | 20,000 | 50,000 | 100,000 | 150,000 | 300,000 | 600,000 | Non-cash equity grants |

**SBC Scaling:**

- Y0-Y2: ~0.5-1% of revenue (early stage)
- Y3-Y5: ~1-1.2% of revenue (scaling with team)
- Y6+: ~2% of revenue (mature SaaS benchmark)

**Note:** SBC is a non-cash expense. Excluded from EBITDA (industry standard) but included in GAAP operating expenses.

---

## CUSTOMER ACQUISITION (Rows 65-75)

| Row | Metric                | Unit | Y0         | Y1         | Y2         | Y3         | Y4         | Y5         | Formula                                           |
| --- | --------------------- | ---- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ------------------------------------------------- |
| 66  | CAC (per customer)    | $    | 2,000      | 2,100      | 2,200      | 2,300      | 2,400      | 2,500      | [BP 07_Revenue_Model.md L21-31](#cac-source)      |
| 67  | New Customers         | #    | 10         | 76         | 156        | 244        | 422        | 561        | Explicit                                          |
| 68  | Total CAC Spend       | $    | `=C67*C66` | `=D67*D66` | `=E67*E66` | `=F67*F66` | `=G67*G66` | `=H67*H66` | Calculated                                        |
| 69  | Churned Customers     | #    | 0          | 5          | 13         | 26         | 56         | 113        | Prior year × churn rate                           |
| 70  | Customer Growth Rate  | %    | 0%         | 750%       | 173%       | 95%        | 83%        | 57%        | `=(D73-C73)/C73`                                  |
| 71  | Churn Rate            | %    | 15%        | 15%        | 15%        | 15%        | 15%        | 15%        | [BP 07_Revenue_Model.md L24, L801](#churn-source) |
| 72  | Avg Customer Lifetime | yrs  | 6.7        | 6.7        | 6.7        | 6.7        | 6.7        | 6.7        | =1/Churn Rate                                     |
| 73  | Total Customers       | #    | 8          | 35         | 85         | 175        | 375        | 750        | From Sources & References                         |

### Churn Rate Detail (from Business Plan) {#churn-source}

**Source:** [07_Revenue_Model.md](../business_plan/sections/07_Revenue_Model.md#L792-L801)

| Segment     | Churn Rate | Customer Mix | Notes                                   |
| ----------- | ---------- | ------------ | --------------------------------------- |
| SMB         | 17%        | 70%          | Higher churn, lower ARPU                |
| Mid-Market  | 11%        | 25%          | Moderate retention                      |
| Enterprise  | 6%         | 5%           | Strong retention (multi-year contracts) |
| **Blended** | **15%**    | 100%         | Weighted by customer count              |

**Note:** Blended 15% is weighted by customer count (SMB-heavy). Revenue-weighted churn is ~12% because SMB is only 34% of revenue.

### CAC by Segment (from Business Plan) {#cac-source}

**Source:** [07_Revenue_Model.md](../business_plan/sections/07_Revenue_Model.md#L21-31)

| Segment     | CAC        | Notes                           |
| ----------- | ---------- | ------------------------------- |
| SMB         | $2,500     | Inbound + self-serve            |
| Mid-Market  | $12,000    | Inside sales + pilots           |
| Enterprise  | $45,000    | Field sales + multi-stakeholder |
| **Blended** | **$7,000** | Weighted by customer mix        |

**Customer Cohort Calculation:**

```
New Customers = Target Customers - Prior Customers + Churned
Churned = Prior Year Customers × Churn Rate (15%)
Total = Prior + New - Churned
```

---

## GEOGRAPHIC EXPANSION (Rows 77-86)

| Row | Region                 | Y0    | Y1    | Y2          | Y3                  | Y4             | Y5     | Notes                 |
| --- | ---------------------- | ----- | ----- | ----------- | ------------------- | -------------- | ------ | --------------------- |
| 78  | Primary Market         | India | India | India + SEA | India + SEA + Japan | Asia + Germany | Global | Text label            |
| 79  | India Revenue %        | 100%  | 85%   | 60%         | 45%                 | 35%            | 30%    | Home market           |
| 80  | SE Asia Revenue %      | 0%    | 15%   | 30%         | 30%                 | 25%            | 20%    | Y1 entry              |
| 81  | MENA Revenue %         | 0%    | 0%    | 10%         | 15%                 | 15%            | 15%    | Y2 entry              |
| 82  | Europe Revenue %       | 0%    | 0%    | 0%          | 10%                 | 12%            | 20%    | Y3 entry              |
| 83  | Americas Revenue %     | 0%    | 0%    | 0%          | 0%                  | 8%             | 15%    | Y4 entry              |
| 84  | Japan/Taiwan Revenue % | 0%    | 0%    | 10%         | 20%                 | 25%            | 25%    | Y2 entry (high-value) |
| 85  | Germany/EU Revenue %   | 0%    | 0%    | 0%          | 5%                  | 15%            | 20%    | Y3 entry              |
| 86  | China Revenue %        | 0%    | 0%    | 0%          | 0%                  | 0%             | 5%     | Y5 entry (cautious)   |

**Validation:** Sum of regional % should equal 100% each year (allow for overlap adjustments).

---

## INDUSTRY SEGMENTS (Rows 88-94)

| Row | Industry              | Y0  | Y1  | Y2  | Y3  | Y4  | Y5  | Notes                       |
| --- | --------------------- | --- | --- | --- | --- | --- | --- | --------------------------- |
| 89  | Automotive %          | 60% | 55% | 50% | 45% | 40% | 35% | Initial focus, diversifying |
| 90  | Aerospace/Defense %   | 10% | 15% | 20% | 20% | 20% | 20% | High-value, regulated       |
| 91  | Medical Devices %     | 5%  | 10% | 10% | 15% | 15% | 15% | Growing precision need      |
| 92  | Electronics/EV %      | 20% | 15% | 15% | 15% | 20% | 25% | EV transition driver        |
| 93  | Other Manufacturing % | 5%  | 5%  | 5%  | 5%  | 5%  | 5%  | General industrial          |

**Validation:** Sum should equal 100% each year.

---

## KEY RELATIONSHIPS (Rows 96-99)

| Row | Customer           | Y0       | Y1       | Y2       | Y3       | Y4         | Y5     |
| --- | ------------------ | -------- | -------- | -------- | -------- | ---------- | ------ |
| 97  | Honda Pilot Status | Active   | Expanded | Deployed | Scaled   | Multi-site | Global |
| 98  | Toyota Status      | Prospect | Pilot    | Active   | Expanded | Multi-site | Scaled |
| 99  | TVS Motors Status  | Existing | Active   | Expanded | Scaled   | Scaled     | Scaled |

**Status Definitions:**

- **Prospect**: Initial discussions, no contract
- **Pilot**: Paid pilot project underway
- **Active**: Post-pilot, regular usage
- **Expanded**: Additional use cases/sites
- **Scaled**: Major deployment across sites
- **Multi-site**: Multiple facilities using
- **Global**: International deployment

---

## Cross-Sheet Linkages

### From Sources & References

| This Cell                   | Links To                          | Purpose             |
| --------------------------- | --------------------------------- | ------------------- |
| C15:H15 (Software Price)    | `='Sources & References'!B66`     | Pricing consistency |
| C19:H19 (Printer Price)     | `='Sources & References'!B67`     | Pricing consistency |
| C23:H23 (Consumables Price) | `='Sources & References'!B68`     | Pricing consistency |
| C27:H27 (AMC Price)         | `='Sources & References'!B69`     | Pricing consistency |
| C31:H31 (Managed Price)     | `='Sources & References'!B70`     | Pricing consistency |
| C35:H35 (Job Work Price)    | `='Sources & References'!B71`     | Pricing consistency |
| C18:H18 (Software COGS)     | `='Sources & References'!B74`     | COGS consistency    |
| C66:H66 (CAC)               | `='Sources & References'!B82:B87` | CAC by year         |
| C71:H71 (Churn Rate)        | `='Sources & References'!B89`     | Churn consistency   |

### To Other Sheets

| Other Sheet     | Links From                                            | Purpose             |
| --------------- | ----------------------------------------------------- | ------------------- |
| Revenue         | All revenue stream rows                               | Revenue calculation |
| Operating Costs | C41 (People), C44:C47 (S&M), C51:C59 (G&A), C63 (SBC) | OpEx calculation    |
| P&L             | Tax rate, depreciation                                | Net income calc     |
| Cash Flow       | Capex, working capital                                | Cash projection     |
| Headcount Plan  | C41 (Salaries & Benefits)                             | Validation          |

---

## Formula Patterns

### Growth Rate Calculation (Safe Division)

```excel
=IF(C16=0, 0, (D16-C16)/C16)
```

### Inflation Adjustment

```excel
=C42 * (1 + $C$12)^(COLUMN()-3)
```

### CAC Spend

```excel
=C54 * C53
```

### Churned Customers

```excel
=ROUND(B60 * C58, 0)
```

---

## Formatting Standards

| Row Type         | Background Color        | Text Color | Font        |
| ---------------- | ----------------------- | ---------- | ----------- |
| Sheet Title      | `RGB(0.20, 0.30, 0.50)` | White      | Bold 14pt   |
| Section Header   | `RGB(0.20, 0.40, 0.60)` | White      | Bold 12pt   |
| Parameter Labels | White                   | Black      | Normal 10pt |
| Year Headers     | `RGB(0.95, 0.95, 0.95)` | Black      | Bold 10pt   |
| Input Cells      | `RGB(1.0, 1.0, 0.9)`    | Black      | Normal 10pt |
| Formula Cells    | White                   | Black      | Normal 10pt |
| Validation Rows  | `RGB(0.9, 1.0, 0.9)`    | Black      | Normal 10pt |

---

## Revenue Summary (For Quick Reference)

| Stream           | Y0         | Y1         | Y2     | Y3     | Y4     | Y5     |
| ---------------- | ---------- | ---------- | ------ | ------ | ------ | ------ |
| Software         | `=C15*C16` | `=D15*D16` | ...    | ...    | ...    | ...    |
| 3D Printers      | `=C19*C20` | `=D19*D20` | ...    | ...    | ...    | ...    |
| Consumables      | `=C23*C24` | `=D23*D24` | ...    | ...    | ...    | ...    |
| AMC              | `=C27*C28` | `=D27*D28` | ...    | ...    | ...    | ...    |
| Managed Services | `=C31*C32` | `=D31*D32` | ...    | ...    | ...    | ...    |
| Job Work         | `=C35*C36` | `=D35*D36` | ...    | ...    | ...    | ...    |
| **TOTAL**        | =SUM()     | =SUM()     | =SUM() | =SUM() | =SUM() | =SUM() |

**Expected Revenue Totals:**

- Y0: $496K
- Y1: $2.48M
- Y2: $7.00M
- Y3: $15.05M
- Y4: $30.11M
- Y5: $50.18M

---

## Business Plan Alignment Log

### Discrepancies Found & Resolved (2026-01-28)

| Parameter                 | Previous Value  | Corrected Value  | Source Document            | Line Reference |
| ------------------------- | --------------- | ---------------- | -------------------------- | -------------- |
| **CapEx Y2**              | $100,000        | $200,000         | 09_Fundraising_Strategy.md | L313-317       |
| **CapEx Y3**              | $100,000        | $300,000         | 09_Fundraising_Strategy.md | L313-317       |
| **CapEx Y4**              | $100,000        | $500,000         | 09_Fundraising_Strategy.md | L313-317       |
| **CapEx Y5**              | $100,000        | $750,000         | 09_Fundraising_Strategy.md | L313-317       |
| **Seed Round**            | $2,000,000 (Y0) | $3,000,000 (Y0)  | 09_Fundraising_Strategy.md | L56            |
| **Series A**              | $4,000,000 (Y2) | $10,000,000 (Y3) | 09_Fundraising_Strategy.md | L186           |
| **Series B**              | Not modeled     | $25,000,000 (Y5) | 09_Fundraising_Strategy.md | L228           |
| **Churn Rate**            | 10%             | 15% (blended)    | 07_Revenue_Model.md        | L24, L801      |
| **Customer Lifetime**     | 10 years        | 6.7 years        | 07_Revenue_Model.md        | L793           |
| **Software COGS**         | 15%             | 20%              | 07_Revenue_Model.md        | L251-260       |
| **Hardware COGS**         | 60%             | 74%              | 07_Revenue_Model.md        | L14            |
| **Consumables COGS**      | 60%             | 67%              | 07_Revenue_Model.md        | L15            |
| **Managed Services COGS** | 50%             | 72%              | 07_Revenue_Model.md        | L388-394       |
| **Job Work COGS**         | 55%             | 56%              | 07_Revenue_Model.md        | L12            |
| **DSO (Debtor Days)**     | 45 days ✓       | 45 days ✓        | 07_Revenue_Model.md        | L1160          |
| **DPO (Creditor Days)**   | 30 days ✓       | 30 days ✓        | 07_Revenue_Model.md        | L1161          |

### Impact Summary

**Gross Margin Impact:**

- Blended COGS: 41-44% (fixed per stream, no improvement)
- Software: 80% GM (fixed COGS 20%)
- Hardware: 24% GM (fixed COGS 76%)
- Job Work: 25% GM (fixed COGS 75%)
- EMS: 28% GM (fixed COGS 72%)
- Target blended GM: **59%** (stable, not improving)

**Cash Flow Impact:**

- Higher CapEx in later years ($750K vs $100K by Y5)
- More equity infusion ($38M total vs $6M)
- Runway extension from proper funding rounds

**P&L Impact:**

- Higher churn (15% vs 10%) means more customer acquisition cost
- Lower gross margins affect EBITDA trajectory
- Net income targets may need adjustment

### Validation Checklist

- [x] CapEx breakdown documented with justification
- [x] Working capital metrics (DSO/DPO) verified
- [x] Funding rounds aligned with business plan
- [x] Churn rate updated with segment breakdown
- [x] All COGS percentages sourced from business plan
- [ ] P&L sheet needs recalculation with new margins
- [ ] Cash Flow sheet needs recalculation with new CapEx/funding
- [ ] Balance Sheet needs verification after updates
