# 01 - Sources & References Sheet

> **Last Updated:** 2026-01-29  
> **Purpose:** Single source of truth for all linkable values used across the financial model  
> **Sheet Position:** 1 of 14

---

## Overview

This sheet contains two sections:

1. **Section A: Key Metrics** - Formula-driven values that other sheets link to
2. **Section B: Source Documentation** - Full citations with URLs for audit trail

All pricing, COGS percentages, CAC, churn rates, and market data should be referenced FROM this sheet.

### TAM/SAM/SOM Summary

| Metric | Value | Description |
| ------ | ----- | ----------- |
| **TAM** | $42.0B | Software $10B + Hardware $4B + Consumables $8B + Services $20B |
| **SAM (Phase 1-2)** | $2.88B | India + SE Asia addressable market |
| **SAM (Phase 3)** | $5.76B | + Global VAR network (2× regional SAM) |
| **SOM (Year 8)** | $104M | 1.81% penetration, 5,500 customers |
| **Revenue Mix** | 62/30/7/1 | Software/Services/Hardware/Consumables |

---

## SECTION A: KEY METRICS (Linkable Values)

### A1. TAM - Total Addressable Market (2025): $42.0 Billion

**Source:** [BP 02_TAM_SAM_SOM_Calculation.md](../business_plan/sections/02_TAM_SAM_SOM_Calculation.md)

| Row | Metric                           | Value              | Unit | Calculation/Source                           | Confidence  |
| --- | -------------------------------- | ------------------ | ---- | -------------------------------------------- | ----------- |
| 7   | **SOFTWARE TAM**                 |                    |      |                                              |             |
| 8   | CAD Software (Tooling Subset)    | 6,100              | $M   | Global CAD $12.2B × 50% tooling [[1]](#ref-1)| HIGH        |
| 9   | CAM Software (Tooling Subset)    | 2,800              | $M   | Global CAM $3.45B × 80% tooling [[2]](#ref-2)| HIGH        |
| 10  | Other Mfg Software (PLM/Sim)     | 1,100              | $M   | PLM $0.5B + Simulation $0.4B + Tolerance     | MEDIUM      |
| 11  | **Total Software TAM**           | `=B8+B9+B10`       | $M   | Sum of CAD + CAM + Other = **$10.0B**        | HIGH        |
| 12  | **HARDWARE TAM**                 |                    |      |                                              |             |
| 13  | Industrial 3D Printing Market    | 18,300             | $M   | Global industrial 3D printing 2025 [[6]](#ref-6) | HIGH    |
| 14  | Tooling Applications %           | 22%                | %    | Jigs 12% + Molds 7% + Assembly 3% [[10]](#ref-10) | HIGH   |
| 15  | **Total Hardware TAM**           | `=B13*B14`         | $M   | 3D Print × Tooling % = **$4.0B**             | HIGH        |
| 16  | **CONSUMABLES TAM**              |                    |      |                                              |             |
| 17  | 3D Printing Materials Market     | 3,880              | $M   | Global 3D printing materials 2025 [[8]](#ref-8) | HIGH     |
| 18  | Tooling Material Subset          | `=B17*0.22*1.33`   | $M   | Materials × 22% × 1.33 intensity = $1.13B    | MEDIUM      |
| 19  | Traditional Tooling Materials    | 6,870              | $M   | CNC $4.2B + Composite $1.5B + Other          | MEDIUM      |
| 20  | **Total Consumables TAM**        | `=B18+B19`         | $M   | 3DP Materials + Traditional = **$8.0B**      | MEDIUM-HIGH |
| 21  | **SERVICES TAM**                 |                    |      |                                              |             |
| 22  | Engineering Services Outsourcing | 315,610            | $M   | Global ESO market 2025 [[32]](#ref-32)       | HIGH        |
| 23  | Mechanical Engineering Subset    | 50,000             | $M   | Mechanical engineering outsourcing [[33]](#ref-33) | HIGH   |
| 24  | Tooling Design % of Mech Eng     | 40%                | %    | Jigs/fixtures/molds/dies design work         | MEDIUM      |
| 25  | **Total Services TAM**           | `=B23*B24`         | $M   | Mech Eng × Tooling % = **$20.0B**            | MEDIUM-HIGH |
| 27  | **TOTAL TAM**                    | `=B11+B15+B20+B25` | $M   | Software + Hardware + Consumables + Services = **$42.0B** | HIGH |

**TAM Summary:**
| Revenue Stream  | TAM (2025) | Confidence | Primary Source |
| --------------- | ---------- | ---------- | -------------- |
| Software        | $10.0B     | HIGH       | Future Market Insights (CAD $12.2B), Mordor (CAM $3.45B) |
| Hardware        | $4.0B      | HIGH       | GM Insights (3D Printing $18.3B × 22% tooling) |
| Consumables     | $8.0B      | MEDIUM-HIGH| Grand View ($3.88B materials) + traditional tooling |
| Services        | $20.0B     | MEDIUM-HIGH| Mordor Intelligence (ESO $315.61B), MRA ($50B mech. eng.) |
| **TOTAL TAM**   | **$42.0B** | **HIGH**   | All streams validated with tier-1 research |

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

### A3. SAM - Serviceable Addressable Market: $2.88B → $5.76B (Phased)

**Source:** [BP 02_TAM_SAM_SOM_Calculation.md](../business_plan/sections/02_TAM_SAM_SOM_Calculation.md)

#### Geographic Expansion Phases

| Row | Phase       | Years | Geography            | SAM ($M)  | Cumulative SAM | Multiplier |
| --- | ----------- | ----- | -------------------- | --------- | -------------- | ---------- |
| 42  | **Phase 1** | Y1-Y2 | India                | 1,800     | $1.80B         | 1.0×       |
| 43  | **Phase 2** | Y3-Y4 | + SE Asia            | 1,080     | $2.88B         | 1.6×       |
| 44  | **Phase 3** | Y5-Y8 | + Global VARs        | 2,880     | $5.76B         | 2.0×       |

#### SAM by Revenue Stream (India + SE Asia = Phase 1-2)

| Row | Revenue Stream  | SAM ($M) | % of TAM | Calculation                                               |
| --- | --------------- | -------- | -------- | --------------------------------------------------------- |
| 46  | Software        | 336      | 3.4%     | Regional CAD ($1.01B) × Addressability (40.9%) × Tooling  |
| 47  | Hardware        | 366      | 9.2%     | Regional 3DP ($1.66B) × Addressability (24%) × Tooling × Growth |
| 48  | Consumables     | 440      | 5.5%     | Materials ($103M) + Traditional ($1.77B) with filters     |
| 49  | Services        | 1,740    | 8.7%     | **BOTTOMS-UP** (650K companies × $1K-15K avg spend/tier)  |
| 50  | **TOTAL SAM**   | `=SUM(B46:B49)` | 6.9% | India + SE Asia addressable market = **$2.88B**           |

#### Regional Company Base (for Penetration Calculation)

| Row | Region                  | Total Mfg | Target Seg | Digital-Ready % | SAM Companies   |
| --- | ----------------------- | --------- | ---------- | --------------- | --------------- |
| 52  | **INDIA**               | 680,000   | 58,500     | 10%             | `=C52*D52`      |
| 53  | **SE ASIA**             | 250,000   | 24,200     | 12%             | `=C53*D53`      |
| 54  | **JAPAN**               | 180,000   | 26,400     | 25%             | `=C54*D54`      |
| 55  | **GERMANY/EU**          | 200,000   | 30,600     | 20%             | `=C55*D55`      |
| 56  | **OTHERS**              | -         | 8,000      | -               | 8,000           |
| 57  | **TOTAL SAM Companies** |           |            |                 | `=SUM(E52:E56)` |

**Calculated SAM Company Values:**

- India SAM: 5,850 companies (58,500 × 10%)
- SE Asia SAM: 2,904 companies (24,200 × 12%)
- Japan SAM: 6,600 companies (26,400 × 25%)
- Germany/EU SAM: 6,120 companies (30,600 × 20%)
- Others: 8,000 companies
- **Total SAM: 29,474 companies**

#### SAM Addressability Filters

| Filter                           | Software | Hardware | Consumables | Services |
| -------------------------------- | -------- | -------- | ----------- | -------- |
| Digital maturity (CAD-ready)     | 40.9%    | -        | -           | -        |
| Infrastructure ready             | 95%      | 60%      | 60%         | -        |
| Investment capacity ($80K+)      | -        | 40%      | -           | -        |
| Outsource tooling design         | -        | -        | -           | 65%      |
| **Combined Addressability**      | 40.9%    | 24%      | 17%         | 65%      |

### A4. SOM - Serviceable Obtainable Market: $104M (Year 8)

**Source:** [BP 02_TAM_SAM_SOM_Calculation.md](../business_plan/sections/02_TAM_SAM_SOM_Calculation.md)

#### 8-Year SOM Growth Trajectory

| Row | Year | Geography     | Active SAM | Revenue ($M) | Customers | Avg ARPU   | YoY Growth | SAM Penetration |
| --- | ---- | ------------- | ---------- | ------------ | --------- | ---------- | ---------- | --------------- |
| 60  | Y1*  | India         | $1.80B     | 0.5          | 8         | $62,500    | -          | 0.03%           |
| 61  | Y2   | India         | $1.80B     | 2.5          | 30        | $83,333    | 400%       | 0.14%           |
| 62  | Y3   | + SE Asia     | $2.88B     | 7.0          | 85        | $82,353    | 180%       | 0.24%           |
| 63  | Y4   | + SE Asia     | $2.88B     | 15.0         | 220       | $68,182    | 114%       | 0.52%           |
| 64  | Y5   | + Global VARs | $4.32B     | 30.0         | 550       | $54,545    | 100%       | 0.69%           |
| 65  | Y6   | + Global VARs | $4.80B     | 50.0         | 1,350     | $37,037    | 67%        | 1.04%           |
| 66  | Y7   | + Global VARs | $5.28B     | 77.0         | 2,900     | $26,552    | 54%        | 1.46%           |
| 67  | Y8   | Global        | $5.76B     | 104.0        | 5,500     | $18,909    | 35%        | 1.81%           |

*Y1 is an 18-month PMF validation period. Early customers are enterprise pilots at high ARPU.

#### Revenue Mix by Stream (Year 8 = $104M)

| Row | Revenue Stream              | Revenue ($M) | Mix %  | Penetration vs SAM |
| --- | --------------------------- | ------------ | ------ | ------------------ |
| 69  | Software Subscriptions      | 64.0         | 61.5%  | 9.5% of $672M      |
| 70  | Tooling Services (Job Work) | 24.2         | 23.3%  | 0.7% of $3.48B     |
| 71  | Enterprise Managed Services | 7.4          | 7.1%   | 0.2% of $3.48B     |
| 72  | Hardware (3D Printers)      | 7.4          | 7.1%   | 1.0% of $732M      |
| 73  | Consumables                 | 1.1          | 1.1%   | 0.1% of $880M      |
| 74  | **TOTAL**                   | `=SUM(B69:B73)` | 100% | **1.81%** blended  |

#### Customer Segment Mix (Year 8)

| Row | Segment        | Customers | Mix % | ARPU    | Revenue ($M) | Penetration |
| --- | -------------- | --------- | ----- | ------- | ------------ | ----------- |
| 76  | SMB            | 3,850     | 70%   | $9,300  | 35.8         | 0.77%       |
| 77  | Mid-Market     | 1,375     | 25%   | $37,200 | 51.2         | 2.75%       |
| 78  | Enterprise     | 275       | 5%    | $62,000 | 17.1         | 5.50%       |
| 79  | **TOTAL**      | 5,500     | 100%  | $18,909 | 104.0        | 1.81%       |

**ARPU Decline Explanation:** Intentional "land enterprise, scale SMB" strategy.
- Y1-Y2: Enterprise pilots (Honda, TVS, Toyota) at $62K-$83K ARPU
- Y3-Y4: Mid-market + SMB entry at $68K-$82K ARPU  
- Y5-Y8: SMB-dominant (70% of customers) at $19K-$55K ARPU

### A5. Seats per Customer Model (by Segment)

**Segment Mix Evolution:**
| Segment      | Seats Avg | Y1 Mix | Y8 Mix | Notes                              |
| ------------ | --------- | ------ | ------ | ---------------------------------- |
| SMB          | 2.0       | 30%    | 70%    | 1-4 operators per company          |
| Mid-Market   | 5.0       | 40%    | 25%    | 3-8 operators, multi-department    |
| Enterprise   | 15.0      | 30%    | 5%     | 10-30 operators, multi-site        |

**Blended Seats per Customer by Year:**
| Row | Year | Seats/Customer | Segment Mix Driver                    |
| --- | ---- | -------------- | ------------------------------------- |
| 82  | Y1   | 6.0            | Enterprise pilots (Honda, TVS)        |
| 83  | Y2   | 5.5            | More mid-market, building VAR channel |
| 84  | Y3   | 5.0            | SMB growing via VARs                  |
| 85  | Y4   | 4.5            | SMB dominant, VAR-led growth          |
| 86  | Y5   | 4.0            | 55% VAR channel                       |
| 87  | Y6   | 3.8            | 65% VAR channel, SMB-heavy            |
| 88  | Y7   | 3.6            | 70% SMB mix                           |
| 89  | Y8   | 3.5            | Mature mix: 70% SMB, 25% MM, 5% Ent   |

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

### A8a. Unit Economics by Segment (Year 8 - Mature State)

**Source:** [BP 07_Revenue_Model.md](../business_plan/sections/07_Revenue_Model.md)

| Row | Metric             | SMB        | Mid-Market | Enterprise  | Blended        |
| --- | ------------------ | ---------- | ---------- | ----------- | -------------- |
| 106 | **Blended ARPU**   | $9,300     | $37,200    | $62,000     | **$18,909**    |
| 107 | **CAC**            | $2,500     | $12,000    | $45,000     | $7,000         |
| 108 | **Churn Rate**     | 17%        | 11%        | 6%          | 15%            |
| 109 | **Lifetime**       | 5.9 yrs    | 9.1 yrs    | 16.7 yrs    | 6.7 yrs        |
| 110 | **LTV**            | $38,400    | $220,000   | $621,000    | $82,000        |
| 111 | **LTV:CAC**        | **15.4:1** | **18.3:1** | **13.8:1**  | **11.7:1**     |
| 112 | **Payback Period** | 4.6 months | 5.5 months | 12.1 months | **6.0 months** |
| 113 | **Gross Margin**   | 65%        | 60%        | 55%         | **59%**        |

**Note on LTV:CAC Ratios:** Our ratios (12-18:1) exceed the 3:1 industry minimum. Two structural advantages:
1. **India cost advantage:** Sales/marketing costs are 60-70% lower than US equivalents
2. **Multi-product stickiness:** Customers using software + services + hardware face 5× switching costs

**Segment Gross Margins:** Enterprise has lower GM (55%) than SMB (65%) because enterprise deals include more services and EMS (lower margin) alongside software.

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

### TAM/SAM/SOM Data

| Data Point              | Cell Reference                    | Used By                      |
| ----------------------- | --------------------------------- | ---------------------------- |
| Total TAM               | `='Sources & References'!B27`     | Summary, Pitch Deck          |
| Software TAM            | `='Sources & References'!B11`     | Summary                      |
| Hardware TAM            | `='Sources & References'!B15`     | Summary                      |
| Consumables TAM         | `='Sources & References'!B20`     | Summary                      |
| Services TAM            | `='Sources & References'!B25`     | Summary                      |
| Total SAM ($M)          | `='Sources & References'!B50`     | Summary                      |
| SAM by Phase (Y1-8)     | `='Sources & References'!B42:B44` | Summary, Geographic          |
| Total SAM Companies     | `='Sources & References'!E57`     | Summary                      |
| Y1-Y8 Revenue           | `='Sources & References'!D60:D67` | Assumptions, P&L             |
| Y1-Y8 Customers         | `='Sources & References'!E60:E67` | Assumptions, Summary         |
| Y1-Y8 ARPU              | `='Sources & References'!F60:F67` | Assumptions                  |
| Y1-Y8 Penetration       | `='Sources & References'!H60:H67` | Summary                      |

### Pricing Data

| Data Point              | Cell Reference                    | Used By                      |
| ----------------------- | --------------------------------- | ---------------------------- |
| Software List Price     | `='Sources & References'!B92`     | Assumptions, Revenue         |
| 3D Printer Price        | `='Sources & References'!B98`     | Assumptions, Revenue         |
| Consumables Price       | `='Sources & References'!B99`     | Assumptions, Revenue         |
| AMC Price               | `='Sources & References'!B100`    | Assumptions, Revenue         |
| Managed Services Price  | `='Sources & References'!B101`    | Assumptions, Revenue         |
| Job Work Price          | `='Sources & References'!B102`    | Assumptions, Revenue         |

### COGS Data

| Data Point              | Cell Reference                    | Used By                      |
| ----------------------- | --------------------------------- | ---------------------------- |
| Software COGS %         | `='Sources & References'!B105`    | Assumptions, Operating Costs |
| 3D Printer COGS %       | `='Sources & References'!B106`    | Assumptions, Operating Costs |
| Consumables COGS %      | `='Sources & References'!B107`    | Assumptions, Operating Costs |
| AMC COGS %              | `='Sources & References'!B108`    | Assumptions, Operating Costs |
| Managed Services COGS % | `='Sources & References'!B109`    | Assumptions, Operating Costs |
| Job Work COGS %         | `='Sources & References'!B110`    | Assumptions, Operating Costs |

### Customer Metrics

| Data Point              | Cell Reference                    | Used By                      |
| ----------------------- | --------------------------------- | ---------------------------- |
| Y1-Y8 CAC               | `='Sources & References'!B113:B120` | Assumptions                |
| Churn Rate (Blended)    | `='Sources & References'!B122`    | Assumptions                  |
| Customer Lifetime       | `='Sources & References'!B123`    | Assumptions                  |
| Y1-Y8 Seats/Customer    | `='Sources & References'!B82:B89` | Assumptions                  |

### Unit Economics

| Data Point              | Cell Reference                    | Used By                      |
| ----------------------- | --------------------------------- | ---------------------------- |
| SMB ARPU                | `='Sources & References'!B127`    | Summary, Valuation           |
| Mid-Market ARPU         | `='Sources & References'!C127`    | Summary, Valuation           |
| Enterprise ARPU         | `='Sources & References'!D127`    | Summary, Valuation           |
| Blended ARPU            | `='Sources & References'!E127`    | Summary, Valuation           |
| Blended LTV             | `='Sources & References'!E131`    | Summary, Valuation           |
| Blended LTV:CAC         | `='Sources & References'!E132`    | Summary, Valuation           |

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
