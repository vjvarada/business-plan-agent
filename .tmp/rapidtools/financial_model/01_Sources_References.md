# 01 - Sources & References Sheet

> **Last Updated:** 2026-01-28  
> **Purpose:** Single source of truth for all linkable values used across the financial model  
> **Sheet Position:** 1 of 14

---

## Overview

This sheet contains two sections:

1. **Section A: Key Metrics** - Formula-driven values that other sheets link to
2. **Section B: Source Documentation** - Full citations with URLs for audit trail

All pricing, COGS percentages, CAC, churn rates, and market data should be referenced FROM this sheet.

---

## SECTION A: KEY METRICS (Linkable Values)

### A1. TAM - Total Addressable Market (2025)

| Row | Metric                           | Value              | Unit | Calculation/Source                           | Confidence  |
| --- | -------------------------------- | ------------------ | ---- | -------------------------------------------- | ----------- |
| 7   | **SOFTWARE TAM**                 |                    |      |                                              |             |
| 8   | CAD Software (Tooling Subset)    | 6,100              | $M   | Global CAD $12.2B 50% tooling                | HIGH        |
| 9   | CAM Software (Tooling Subset)    | 2,800              | $M   | Global CAM $3.45B 80% tooling                | HIGH        |
| 10  | Other Mfg Software (PLM/Sim)     | 1,100              | $M   | PLM $0.5B + Simulation $0.4B + Tolerance     | MEDIUM      |
| 11  | **Total Software TAM**           | `=B8+B9+B10`       | $M   | Sum of CAD + CAM + Other                     | HIGH        |
| 12  | **HARDWARE TAM**                 |                    |      |                                              |             |
| 13  | Industrial 3D Printing Market    | 18,300             | $M   | Global industrial 3D printing 2025           | HIGH        |
| 14  | Tooling Applications %           | 22%                | %    | Jigs 12% + Molds 7% + Assembly 3%            | HIGH        |
| 15  | **Total Hardware TAM**           | `=B13*B14`         | $M   | 3D Print Market Tooling %                    | HIGH        |
| 16  | **CONSUMABLES TAM**              |                    |      |                                              |             |
| 17  | 3D Printing Materials Market     | 3,880              | $M   | Global 3D printing materials 2025            | HIGH        |
| 18  | Tooling Material Subset          | `=B17*0.22*1.33`   | $M   | Materials 22% 1.33 intensity                 | MEDIUM      |
| 19  | Traditional Tooling Materials    | 6,870              | $M   | CNC $4.2B + Composite $1.5B + Other          | MEDIUM      |
| 20  | **Total Consumables TAM**        | `=B18+B19`         | $M   | 3DP Materials + Traditional                  | MEDIUM-HIGH |
| 21  | **SERVICES TAM**                 |                    |      |                                              |             |
| 22  | Engineering Services Outsourcing | 315,610            | $M   | Global ESO market 2025                       | HIGH        |
| 23  | Mechanical Engineering Subset    | 50,000             | $M   | Mechanical engineering outsourcing           | HIGH        |
| 24  | Tooling Design % of Mech Eng     | 40%                | %    | Jigs/fixtures/molds/dies design work         | MEDIUM      |
| 25  | **Total Services TAM**           | `=B23*B24`         | $M   | Mech Eng Tooling %                           | MEDIUM-HIGH |
| 27  | **TOTAL TAM**                    | `=B11+B15+B20+B25` | $M   | Software + Hardware + Consumables + Services | HIGH        |

### A2. Design Automation Software TAM (10 Modules)

| Row | Module                  | Software TAM ($M) | Base Market           | Share %           | Source                   |
| --- | ----------------------- | ----------------- | --------------------- | ----------------- | ------------------------ |
| 29  | 1. Jigs & Fixtures      | 181               | Dies, Jigs & Tools    | 0.30%             | Business Research Co     |
| 30  | 2. Assembly Guides      | 60                | Dies, Jigs & Tools    | 0.10%             | Business Research Co     |
| 31  | 3. Drilling Guides      | 48                | Dies, Jigs & Tools    | 0.08%             | Business Research Co     |
| 32  | 4. Alignment Tools      | 30                | Dies, Jigs & Tools    | 0.05%             | Business Research Co     |
| 33  | 5. Shadow Boxes         | 18                | Dies, Jigs & Tools    | 0.03%             | Business Research Co     |
| 34  | 6. Custom Palletizing   | 44                | Palletizing Equipment | 1.50%             | PS Market Research       |
| 35  | 7. Sand Casting Tools   | 69                | Sand Casting Market   | 0.02%             | Verified Market Research |
| 36  | 8. Vacuum Casting Tools | 51                | Vacuum Casting        | 2.00%             | Straits Research         |
| 37  | 9. Soft Jaws            | 9                 | Workholding Devices   | 0.20%             | Market Data Forecast     |
| 38  | 10. EOAT                | 52                | EOAT Market           | 2.00%             | IMARC Group              |
| 39  | **SOFTWARE TAM TOTAL**  | `=SUM(B29:B38)`   | $M                    | Sum of 10 modules |                          |

### A3. SAM - Regional Breakdown (Formula-Driven)

| Row | Region                  | Total Mfg | Target Seg | Digital-Ready % | SAM Companies   |
| --- | ----------------------- | --------- | ---------- | --------------- | --------------- |
| 42  | **INDIA**               | 680,000   | 58,500     | 10%             | `=C42*D42`      |
| 43  | **SE ASIA**             | 250,000   | 24,200     | 12%             | `=C43*D43`      |
| 44  | **JAPAN**               | 180,000   | 26,400     | 25%             | `=C44*D44`      |
| 45  | **GERMANY/EU**          | 200,000   | 30,600     | 20%             | `=C45*D45`      |
| 46  | **OTHERS**              | -         | 8,000      | -               | 8,000           |
| 47  | **TOTAL SAM Companies** |           |            |                 | `=SUM(E42:E46)` |

**Calculated SAM Values:**

- India SAM: 5,850 companies
- SE Asia SAM: 2,904 companies
- Japan SAM: 6,600 companies
- Germany/EU SAM: 6,120 companies
- Others: 8,000 companies
- **Total SAM: 29,474 companies**

### A4. SOM - Customer Projections (Linked to Assumptions)

| Row | Year | Penetration % | Customers | Seats  | Seats/Cust | Calculation                     |
| --- | ---- | ------------- | --------- | ------ | ---------- | ------------------------------- |
| 50  | Y0   | 0.07%         | 20        | 123    | 6.0        | Pilot phase, enterprise-heavy   |
| 51  | Y1   | 0.45%         | 133       | 669    | 5.0        | Early adopter, building channel |
| 52  | Y2   | 1.50%         | 442       | 1,990  | 4.5        | Product-market fit, VAR ramp    |
| 53  | Y3   | 3.72%         | 1,096     | 4,385  | 4.0        | Growth phase, SMB via VARs      |
| 54  | Y4   | 8.11%         | 2,390     | 9,082  | 3.8        | Scaling, channel dominant       |
| 55  | Y5   | 15.44%        | 4,552     | 15,933 | 3.5        | Market expansion, 70% SMB mix   |

### A5. Seats per Customer Model (by Segment)

**Segment Mix Evolution:**
| Segment | Seats Avg | Y0 Mix | Y5 Mix | Notes |
| ------------ | --------- | ------ | ------ | ---------------------------------- |
| SMB | 2.0 | 30% | 70% | 1-4 operators per company |
| Mid-Market | 5.0 | 40% | 25% | 3-8 operators, multi-department |
| Enterprise | 15.0 | 30% | 5% | 10-30 operators, multi-site |

**Blended Seats per Customer by Year:**
| Row | Year | Seats/Customer | Segment Mix Driver |
| --- | ---- | -------------- | ------------------------------------- |
| 58 | Y0 | 6.0 | Enterprise pilots (Honda, TVS) |
| 59 | Y1 | 5.0 | More mid-market, building VAR channel |
| 60 | Y2 | 4.5 | SMB growing via VARs |
| 61 | Y3 | 4.0 | SMB dominant, VAR-led growth |
| 62 | Y4 | 3.8 | 65% VAR channel, SMB-heavy |
| 63 | Y5 | 3.5 | Mature mix: 70% SMB, 25% MM, 5% Ent |

### A6. Pricing & Channel Economics (LINKED TO ASSUMPTIONS)

#### Software Pricing Structure

| Row | Metric                | Value | Unit      | Notes                         |
| --- | --------------------- | ----- | --------- | ----------------------------- |
| 66  | **List Price**        | 2,400 | $/seat/yr | What customer pays (SMB tier) |
| 67  | Volume Discount (MM)  | 10%   | %         | Mid-Market (5-19 seats)       |
| 68  | Volume Discount (Ent) | 20%   | %         | Enterprise (20+ seats)        |

#### Channel Mix & Commissions (by Year)

**Source:** [BP 06_Go_To_Market_Strategy.md L821-835](../business_plan/sections/06_Go_To_Market_Strategy.md#L821-L835)

| Row | Channel      | Margin | Y0 Mix | Y5 Mix | Notes                                  |
| --- | ------------ | ------ | ------ | ------ | -------------------------------------- |
| 70  | Direct       | 0%     | 80%    | 15%    | Enterprise sales, 100% retained        |
| 71  | VAR          | 27%    | 15%    | 65%    | Primary channel, 25-30% tiered blended |
| 72  | Distributor  | 25%    | 5%     | 15%    | Geographic expansion (BP: 20-25%)      |
| 73  | OEM Partners | 10%    | 0%     | 5%     | Stratasys, HP bundles (BP: 10% fee)    |

**Blended Channel Cost by Year:**
| Row | Year | Direct | VAR | Dist | OEM | Blended Cost | Net Price |
| --- | ---- | ------ | ---- | ---- | --- | ------------ | --------- |
| 75 | Y0 | 80% | 15% | 5% | 0% | 5.3% | $2,272 |
| 76 | Y1 | 50% | 40% | 8% | 2% | 13.0% | $2,088 |
| 77 | Y2 | 30% | 55% | 12% | 3% | 18.2% | $1,964 |
| 78 | Y3 | 20% | 60% | 15% | 5% | 20.5% | $1,909 |
| 79 | Y4 | 15% | 65% | 15% | 5% | 21.8% | $1,876 |
| 80 | Y5 | 15% | 65% | 15% | 5% | 21.8% | $1,876 |

**Note:** Net Price = List Price × (1 - Blended Channel Cost). This is the revenue RapidTools recognizes per seat.

#### Other Product Pricing

| Row | Revenue Stream    | Price  | Unit   | Competitive Range           | Source                    |
| --- | ----------------- | ------ | ------ | --------------------------- | ------------------------- |
| 82  | 3D Printer Sales  | 7,000  | $/unit | $5,000-15,000               | Precedence Research       |
| 83  | Consumables       | 60     | $/unit | $40-100                     | Data Bridge MR            |
| 84  | AMC Contract      | 500    | $/yr   | 8-10% of equipment          | Gartner IT Services       |
| 85  | Managed Services  | 30,000 | $/yr   | $20K-50K                    | Deloitte Managed Services |
| 86  | Job Work Services | 100    | $/job  | COGS incl materials + labor | Internal                  |

### A7. COGS Percentages (LINKED TO ASSUMPTIONS)

| Row | Revenue Stream   | COGS % | Gross Margin | Source                                           | Notes                                                    |
| --- | ---------------- | ------ | ------------ | ------------------------------------------------ | -------------------------------------------------------- |
| 88  | Software         | 20%    | 80%          | [BP 07_Revenue_Model.md L251-260]                | Cloud 8-10%, APIs 2-3%, CS 5-7%, Payments 2-3%           |
| 89  | 3D Printers      | 76%    | 24%          | [BP 07_Revenue_Model.md Hardware COGS]           | Blended: Fracktal 28% GM (arm's-length), Partners 17% GM |
| 90  | Consumables      | 67%    | 33%          | [BP 07_Revenue_Model.md L15]                     | Materials markup 30-35% GM                               |
| 91  | AMC              | 60%    | 40%          | [BP 07_Revenue_Model.md OEM share]               | OEM share 34% + Parts 12% + Tech 10% + Logistics 4%      |
| 92  | Managed Services | 72%    | 28%          | [BP 07_Revenue_Model.md L388-394]                | Staff 50%, Equip 12%, Platform 5%, OH 10%                |
| 93  | Job Work         | 75%    | 25%          | [BP 07_Revenue_Model.md Third-party fulfillment] | Vendor 55% + Platform 5% + Shipping 10% + Support 5%     |

**Note:** COGS updated 2026-01-28 to reflect third-party fulfillment and OEM revenue share:

- **Job Work (75% COGS):** RapidTools partners with local 3D printing bureaus (including Fracktal as arm's-length vendor) and takes 25% arbitrage margin
- **Hardware (76% COGS):** Fracktal treated as preferred vendor with arm's-length pricing (28% margin vs. 30% vertical integration)
- **AMC (60% COGS):** OEM/VAR revenue share 30-40% (Fracktal 30%, third-party 40%) + service delivery costs

### A8. Customer Acquisition (LINKED TO ASSUMPTIONS)

| Row | Year | CAC ($/customer) | Source                   | Notes                |
| --- | ---- | ---------------- | ------------------------ | -------------------- |
| 96  | Y0   | 2,000            | ProfitWell B2B SaaS 2024 | Early-stage: $1.5-3K |
| 97  | Y1   | 2,100            | ProfitWell B2B SaaS 2024 | 10% efficiency gain  |
| 98  | Y2   | 2,200            | OpenView SaaS Metrics    | Scale phase median   |
| 99  | Y3   | 2,300            | OpenView SaaS Metrics    | Regional presence    |
| 100 | Y4   | 2,400            | OpenView SaaS Metrics    | Brand recognition    |
| 101 | Y5   | 2,500            | OpenView SaaS Metrics    | 40% inbound-led      |

| Row | Metric                | Value | Unit  | Source                                   |
| --- | --------------------- | ----- | ----- | ---------------------------------------- |
| 103 | Churn Rate (Blended)  | 15%   | %     | [BP 07_Revenue_Model.md L24, L801]       |
| 104 | Avg Customer Lifetime | 6.7   | years | =1/15% per [BP 07_Revenue_Model.md L793] |

**Churn Rate by Segment (from Business Plan):**

- SMB: 17% (70% of customers)
- Mid-Market: 11% (25% of customers)
- Enterprise: 6% (5% of customers)
- **Blended: 15%** (weighted by customer count)

### A9. Product Attachment Rates (LINKED TO ASSUMPTIONS)

#### Blended Attach Rates (for Financial Model)

| Row | Metric                   | Blended | Unit  | Source                       | Calculation                         |
| --- | ------------------------ | ------- | ----- | ---------------------------- | ----------------------------------- |
| 93  | Hardware Attach Rate     | 22%     | %     | Gartner Tech Adoption        | 70%×15% + 25%×35% + 5%×50% = 22%    |
| 94  | Consumables/Printer/Year | 40      | units | Stratasys Usage Data         | 3-4 spools/month industrial average |
| 95  | AMC Attach Rate          | 35%     | %     | Gartner IT Services          | 30-40% service attach (equipment)   |
| 96  | Job Work Attach Rate     | 46%     | %     | Calculated                   | 70%×45% + 25%×55% + 5%×35% = 46%    |
| 97  | Jobs/Customer/Year       | 24      | jobs  | Internal                     | ~2 jobs per month                   |
| 98  | EMS Attach Rate          | 4%      | %     | Deloitte Enterprise Services | 70%×0% + 25%×5% + 5%×30% = 4%       |
| 99  | Consumables Attach Rate  | 15%     | %     | Calculated                   | 70%×10% + 25%×25% + 5%×40% = 15%    |

#### Segment-Specific Attach Rates (Reference from BP 07_Revenue_Model.md)

| Product/Service               | SMB (70%) | Mid-Market (25%) | Enterprise (5%) | Blended |
| ----------------------------- | --------- | ---------------- | --------------- | ------- |
| Additional Software Seats     | 50%       | 80%              | 100%            | 59%     |
| Second Product (e.g. Casting) | 20%       | 40%              | 60%             | 27%     |
| Tooling Services (Job Work)   | 45%       | 55%              | 35%             | 46%     |
| Enterprise Managed Services   | 0%        | 5%               | 30%             | 3.8%    |
| Hardware Purchase             | 15%       | 35%              | 50%             | 22%     |
| Consumables                   | 10%       | 25%              | 40%             | 15%     |

**Customer Mix Assumption:** 70% SMB / 25% Mid-Market / 5% Enterprise (by customer count)

**Blended Formula:** `= (SMB% × 70%) + (MidMkt% × 25%) + (Ent% × 5%)`

#### Attach Rate Sources

| Source                         | Report                    | Key Data                 | Relevance                  |
| ------------------------------ | ------------------------- | ------------------------ | -------------------------- |
| Gartner Tech Adoption 2024     | B2B Hardware Cross-Sell   | 15-25% typical           | Hardware attach benchmarks |
| Gartner IT Services 2024       | Equipment Service Attach  | 30-40% for industrial    | AMC attach rate            |
| Gainsight CS Benchmark 2024    | SaaS Cross-Sell           | 20-35% product expansion | Second product attach      |
| Deloitte Managed Services 2024 | Enterprise IT Outsourcing | 3-7% MSP adoption        | EMS attach rate            |
| OpenView SaaS Metrics 2024     | PLG Expansion             | 40-60% seat expansion    | Software seat attach       |

**Note:** Job Work attach rate (46%) is higher than hardware (22%) because customers who don't buy hardware often outsource 3D printing entirely. These are complementary, not additive—a customer typically does one or the other.

### A10. Industry Growth Rates (CAGR 2024-2030)

| Row | Market Segment                   | CAGR  | Source                 |
| --- | -------------------------------- | ----- | ---------------------- |
| 101 | CAD Software Market              | 6.2%  | Future Market Insights |
| 102 | CAM Software Market              | 5.8%  | Mordor Intelligence    |
| 103 | Industrial 3D Printing           | 10.6% | GM Insights            |
| 104 | 3D Printing Materials            | 13.5% | Grand View Research    |
| 105 | Engineering Services Outsourcing | 8.9%  | Mordor Intelligence    |
| 106 | Industrial Robotics              | 12.0% | IFR World Robotics     |

---

## SECTION B: SOURCE DOCUMENTATION

### B1. TAM Market Research Sources

| Ref# | Source Name             | Report                     | Year | URL                      | Key Data                   |
| ---- | ----------------------- | -------------------------- | ---- | ------------------------ | -------------------------- |
| [1]  | Future Market Insights  | Global CAD Software Market | 2024 | futuremarketinsights.com | $12.2B in 2025, 6.2% CAGR  |
| [2]  | Mordor Intelligence     | Global CAM Software Market | 2024 | mordorintelligence.com   | $3.45B in 2025, 7.1% CAGR  |
| [3]  | Mordor Intelligence     | India CAD Market           | 2024 | mordorintelligence.com   | $620M in 2025              |
| [6]  | GM Insights             | Industrial 3D Printing     | 2024 | gminsights.com           | $18.3B in 2025             |
| [7]  | GM Insights             | India 3D Printing Market   | 2024 | gminsights.com           | $1.24B in 2025             |
| [8]  | Grand View Research     | 3D Printing Materials      | 2024 | grandviewresearch.com    | $3.88B in 2025, 21.2% CAGR |
| [9]  | MarketsandMarkets       | CAM Software Market        | 2024 | marketsandmarkets.com    | $3.40B in 2024             |
| [10] | Stratasys Annual Report | Tooling Applications       | 2024 | investors.stratasys.com  | 20-25% of market           |

### B2. Services TAM Validation

| Ref# | Source Name              | Data Point                       | Value           | URL                        |
| ---- | ------------------------ | -------------------------------- | --------------- | -------------------------- |
| [32] | Mordor Intelligence      | Engineering Services Outsourcing | $315.61B (2025) | mordorintelligence.com     |
| [33] | Market Report Analytics  | Mechanical Eng Outsourcing       | $50B (2025)     | marketreportanalytics.com  |
| [34] | SNS Insider              | Contract Mfg & Design Services   | $621.36B (2024) | snsinsider.com             |
| [35] | Verified Market Research | Engineering Design Services      | $148.62B (2032) | verifiedmarketresearch.com |

### B3. SaaS Benchmark Sources

| Ref# | Source Name       | Report                  | Year | URL                  | Key Data                 |
| ---- | ----------------- | ----------------------- | ---- | -------------------- | ------------------------ |
| [20] | ProfitWell        | B2B SaaS CAC Benchmarks | 2024 | profitwell.com       | SMB CAC: $1-3K           |
| [21] | OpenView Partners | SaaS Metrics Report     | 2024 | openviewpartners.com | Revenue/employee, quotas |
| [22] | SaaS Capital      | Growth Benchmarks       | 2024 | saas-capital.com     | Median SaaS metrics      |
| [23] | ChartMogul        | Churn by Segment        | 2024 | chartmogul.com       | SMB 17%, MM 11%, Ent 6%  |
| [24] | Recurly           | Churn Report            | 2025 | vitally.io           | B2B SaaS avg: 3.5%       |
| [25] | CustomerGauge     | Churn by Industry       | 2024 | customergauge.com    | B2B SaaS: 4.67%          |
| [26] | Gainsight         | CS Benchmark Report     | 2024 | gainsight.com        | CSM ratios, ARR/CSM      |

### B4. Regional Manufacturing Sources

| Ref# | Source Name      | Report                     | Year | URL                 | Key Data               |
| ---- | ---------------- | -------------------------- | ---- | ------------------- | ---------------------- |
| [13] | IBEF             | India Manufacturing Report | 2024 | ibef.org            | $490B output (2025)    |
| [14] | ASEAN Statistics | SE Asia Manufacturing      | 2024 | aseanstats.org      | $100B+ (2025)          |
| [15] | Safeguard Global | World Rankings             | 2024 | safeguardglobal.com | Top 10 manufacturers   |
| [16] | Trade.gov        | Germany Manufacturing      | 2024 | trade.gov           | Advanced manufacturing |
| [17] | JBIC Survey      | Japan Manufacturing        | 2024 | jbic.go.jp          | Japan industry data    |

### B5. Government Policy Investment

| Ref# | Policy/Initiative            | Investment | Region  | Sector              | URL                           |
| ---- | ---------------------------- | ---------- | ------- | ------------------- | ----------------------------- |
| [40] | U.S. CHIPS Act               | $52.7B     | USA     | Semiconductor       | commerce.gov/chips            |
| [41] | U.S. Inflation Reduction Act | $369B      | USA     | Clean Energy/EV     | whitehouse.gov                |
| [42] | India PLI Scheme             | $26B       | India   | 14 Sectors          | investindia.gov.in            |
| [43] | India Semiconductor Mission  | $10B       | India   | Fab + ATMP          | meity.gov.in                  |
| [44] | EU Chips Act                 | 43B        | EU      | Semiconductor       | digital-strategy.ec.europa.eu |
| [45] | EU Green Deal                | 1T         | EU      | Clean Energy        | ec.europa.eu                  |
| [46] | Germany Industry 4.0         | 20B        | Germany | Smart Manufacturing | plattform-i40.de              |

### B6. Competitor Benchmarks

| Ref# | Company                | Revenue     | Segment           | Key Metric       | Source                  |
| ---- | ---------------------- | ----------- | ----------------- | ---------------- | ----------------------- |
| [50] | Trinckle (FixtureMate) | Est. $5-10M | Generative Design | 12yr head start  | trinckle.com            |
| [51] | Zoo/KittyCAD           | -           | AI CAD            | $20M Series A    | zoo.dev                 |
| [52] | Autodesk               | $5.5B       | Incumbent CAD     | 80% gross margin | investors.autodesk.com  |
| [53] | Dassault Systèmes      | $6.2B       | SOLIDWORKS        | 85% gross margin | 3ds.com                 |
| [54] | PTC                    | $2.1B       | Creo + IoT        | SaaS transition  | investor.ptc.com        |
| [55] | Stratasys              | $630M       | Industrial 3DP    | 45% gross margin | investors.stratasys.com |
| [56] | 3D Systems             | $490M       | Industrial 3DP    | 40% gross margin | sec.gov                 |

### B7. Funding Comparables

| Ref# | Source                  | Data Point                  | Value    | URL            |
| ---- | ----------------------- | --------------------------- | -------- | -------------- |
| [60] | CB Insights Q3 2024     | Median Seed Deal Size       | $3.0M    | cbinsights.com |
| [61] | CB Insights Q3 2024     | Median Seed Valuation       | $13.5M   | cbinsights.com |
| [62] | Bessemer State of Cloud | B2B SaaS Series A Median    | $10-12M  | bvp.com        |
| [63] | Bessemer State of Cloud | Series A Valuation Multiple | 5-7x ARR | bvp.com        |

---

## Cross-Sheet Linkage Map

Other sheets should reference this sheet using these cell addresses:

| Data Point              | Cell Reference                    | Used By                      |
| ----------------------- | --------------------------------- | ---------------------------- |
| Software Price          | `='Sources & References'!B66`     | Assumptions, Revenue         |
| 3D Printer Price        | `='Sources & References'!B67`     | Assumptions, Revenue         |
| Consumables Price       | `='Sources & References'!B68`     | Assumptions, Revenue         |
| AMC Price               | `='Sources & References'!B69`     | Assumptions, Revenue         |
| Managed Services Price  | `='Sources & References'!B70`     | Assumptions, Revenue         |
| Job Work Price          | `='Sources & References'!B71`     | Assumptions, Revenue         |
| Software COGS %         | `='Sources & References'!B74`     | Assumptions, Operating Costs |
| 3D Printer COGS %       | `='Sources & References'!B75`     | Assumptions, Operating Costs |
| Consumables COGS %      | `='Sources & References'!B76`     | Assumptions, Operating Costs |
| AMC COGS %              | `='Sources & References'!B77`     | Assumptions, Operating Costs |
| Managed Services COGS % | `='Sources & References'!B78`     | Assumptions, Operating Costs |
| Job Work COGS %         | `='Sources & References'!B79`     | Assumptions, Operating Costs |
| Y0-Y5 CAC               | `='Sources & References'!B82:B87` | Assumptions                  |
| Churn Rate              | `='Sources & References'!B89`     | Assumptions                  |
| Customer Lifetime       | `='Sources & References'!B90`     | Assumptions                  |
| Y0-Y5 Customers         | `='Sources & References'!B50:B55` | Assumptions, Summary         |
| Y0-Y5 Seats/Customer    | `='Sources & References'!B58:B63` | Assumptions                  |

---

## Formatting Standards

### Section A (Key Metrics)

- Main Title (Row 1): Dark blue BG `RGB(0.20, 0.30, 0.50)`, white bold 14pt
- Section Headers: Dark blue BG `RGB(0.20, 0.40, 0.60)`, white bold 12pt
- Category Headers: Medium blue BG `RGB(0.30, 0.50, 0.70)`, white bold 11pt
- Data Rows: White / Light blue zebra `RGB(0.85, 0.92, 0.98)`

### Section B (Source Documentation)

- Section Header: Dark blue BG `RGB(0.20, 0.40, 0.60)`, white bold 12pt
- Column Headers: Light gray BG `RGB(0.95, 0.95, 0.95)`, bold black
- URLs: Blue text `RGB(0.10, 0.30, 0.70)`
