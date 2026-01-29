# 05 - Operating Costs Sheet

> **Last Updated:** 2026-01-29  
> **Purpose:** Calculate all operating expenses aligned with BP 5-layer cost structure  
> **Sheet Position:** 5 of 14

---

## Overview

Operating Costs follows the **5-layer cost structure** defined in BP 08_Team_Organization_Fixed_Costs.md:

1. **Cost of Goods Sold (COGS)** - Variable costs by revenue stream (46% → 36% blended)
2. **People Cost** - All FTE salaries + benefits (~20-28% at scale)
3. **S&M Variable** - Marketing, trade shows, VAR incentives, commissions (~10-14%)
4. **Fixed Costs (G&A)** - Facilities, tools, R&D infra, professional services (~7-8%)
5. **Stock-Based Compensation** - Non-cash equity grants (excluded from EBITDA)

**Key Change:** COGS is now broken out **by revenue stream** with individual COGS percentages, feeding directly into the P&L's stream-level profitability view.

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L724-732 (Total Operating Costs by Year)

---

## Sheet Structure

### Row Layout

| Row Range | Section                  | Description                              |
| --------- | ------------------------ | ---------------------------------------- |
| 1-2       | Header                   | Sheet title and year labels              |
| 3-11      | COST OF GOODS SOLD       | COGS by revenue stream + COGS % column   |
| 13-14     | PEOPLE COST              | All salaries & benefits (from Headcount) |
| 16-22     | S&M VARIABLE             | Marketing, trade shows, VAR, commissions |
| 24-34     | FIXED COSTS (G&A)        | Facilities, tools, R&D infra, compliance |
| 36-37     | STOCK-BASED COMPENSATION | Non-cash equity grants                   |
| 39-40     | TOTAL                    | Total operating costs                    |

---

## COST OF GOODS SOLD BY STREAM (Rows 3-11)

### Stream-Level COGS with Explicit Margins

**Structure:** Column B contains the COGS % for each stream. This enables the P&L to calculate GP by stream.

| Row | Stream                | Col B (COGS%) | Formula           | Y0    | Y1      | Y2      | Y3      | Y4       | Y5       |
| --- | --------------------- | ------------- | ----------------- | ----- | ------- | ------- | ------- | -------- | -------- |
| 4   | Software COGS         | 20%           | `=Revenue!C3*$B4` | $56K  | $280K   | $784K   | $1,620K | $3,420K  | $6,000K  |
| 5   | 3D Printer COGS       | 76%           | `=Revenue!C4*$B5` | $43K  | $186K   | $452K   | $912K   | $1,824K  | $2,660K  |
| 6   | Consumables COGS      | 67%           | `=Revenue!C5*$B6` | $7K   | $34K    | $67K    | $101K   | $201K    | $335K    |
| 7   | AMC COGS              | 60%           | `=Revenue!C6*$B7` | $1K   | $5K     | $14K    | $30K    | $66K     | $120K    |
| 8   | Managed Services COGS | 72%           | `=Revenue!C7*$B8` | $0K   | $22K    | $238K   | $864K   | $1,512K  | $2,520K  |
| 9   | Job Work COGS         | 75%           | `=Revenue!C8*$B9` | $114K | $575K   | $1,524K | $3,225K | $5,993K  | $9,225K  |
| 10  | Blank                 | -             | -                 | -     | -       | -       | -       | -        | -        |
| 11  | **Total COGS**        | -             | `=SUM(C4:C9)`     | $221K | $1,102K | $3,079K | $6,751K | $13,015K | $20,860K |

### COGS % Reference (Column B)

| Cell | Stream           | COGS % | Gross Margin | Source Reference                                             |
| ---- | ---------------- | ------ | ------------ | ------------------------------------------------------------ |
| B4   | Software         | 20%    | **80%**      | BP 07_Revenue_Model.md L251-260 (SaaS margins)               |
| B5   | 3D Printers      | 76%    | **24%**      | BP 07_Revenue_Model.md (Fracktal 28% + Partners 17% blended) |
| B6   | Consumables      | 67%    | **33%**      | BP 07_Revenue_Model.md L15                                   |
| B7   | AMC              | 60%    | **40%**      | BP 07_Revenue_Model.md (OEM share 30-40% + service)          |
| B8   | Managed Services | 72%    | **28%**      | BP 07_Revenue_Model.md L388-394                              |
| B9   | Job Work         | 75%    | **25%**      | BP 07_Revenue_Model.md (Third-party fulfillment)             |

### COGS % Validation (Realistic Stream Math)

| Metric             | Y0    | Y1      | Y2      | Y3       | Y4       | Y5       |
| ------------------ | ----- | ------- | ------- | -------- | -------- | -------- |
| **Blended COGS %** | 44%   | 44%     | 44%     | 45%      | 43%      | 42%      |
| Revenue            | $500K | $2,500K | $7,000K | $15,000K | $30,000K | $50,000K |
| Total COGS         | $221K | $1,102K | $3,079K | $6,751K  | $13,015K | $20,860K |
| **Gross Margin**   | 56%   | 56%     | 56%     | 55%      | 57%      | 58%      |

**Margin Reality:** With fixed COGS% per stream, blended margin stays ~56-58% (not 54-64%). This reflects realistic stream economics where Services margins (25-28%) are constrained by labor and materials costs.

---

## PEOPLE COST (Rows 12-13)

### Linked from Headcount Plan Sheet

| Row | Metric                | Formula                 | Y0    | Y1      | Y2      | Y3      | Y4      | Y5       |
| --- | --------------------- | ----------------------- | ----- | ------- | ------- | ------- | ------- | -------- |
| 13  | **Total People Cost** | `='Headcount Plan'!C61` | $800K | $1,610K | $3,290K | $5,760K | $9,500K | $14,040K |

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L381-391 (Total People Cost by Year)

| Metric                   | Y0   | Y1   | Y2   | Y3   | Y4   | Y5   |
| ------------------------ | ---- | ---- | ---- | ---- | ---- | ---- |
| Headcount                | 16   | 35   | 70   | 120  | 190  | 270  |
| Avg Cost/FTE             | $50K | $46K | $47K | $48K | $50K | $52K |
| People Cost % of Revenue | 160% | 64%  | 47%  | 38%  | 32%  | 28%  |

**Headcount Plan uses 6 functional categories (aligned with BP):**

- Engineering, Product, Sales & Marketing, Customer Success, Operations/Services, Executive

---

## S&M VARIABLE (Rows 15-21)

### Marketing, Trade Shows, VAR Incentives, Sales Commissions

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L724-732 shows S&M Variable scaling from $50K (Y1) to $5,500K (Y6)

| Row | Cost Category          | Formula            | Y0   | Y1    | Y2    | Y3      | Y4      | Y5      |
| --- | ---------------------- | ------------------ | ---- | ----- | ----- | ------- | ------- | ------- |
| 16  | Marketing Programs     | `=Assumptions!C61` | $50K | $200K | $400K | $900K   | $1,600K | $2,500K |
| 17  | Trade Shows & Events   | `=Assumptions!C62` | $10K | $50K  | $100K | $200K   | $400K   | $500K   |
| 18  | VAR Incentives         | `=Assumptions!C63` | $0K  | $0K   | $150K | $300K   | $700K   | $2,000K |
| 19  | Sales Commissions      | `=Assumptions!C64` | $0K  | $0K   | $50K  | $100K   | $300K   | $500K   |
| 20  | **Total S&M Variable** | `=SUM(C16:C19)`    | $60K | $250K | $700K | $1,500K | $3,000K | $5,500K |

**BP Validation (08_Team_Organization_Fixed_Costs.md L724-732):**

| Year    | BP S&M Variable | Model S&M Variable | Match  |
| ------- | --------------- | ------------------ | ------ |
| Y1 (Y0) | $50K            | $60K               | Approx |
| Y2 (Y1) | $250K           | $250K              | Yes    |
| Y3 (Y2) | $700K           | $700K              | Yes    |
| Y4 (Y3) | $1,500K         | $1,500K            | Yes    |
| Y5 (Y4) | $3,000K         | $3,000K            | Yes    |
| Y6 (Y5) | $5,500K         | $5,500K            | Yes    |

---

## FIXED COSTS - G&A (Rows 23-33)

### Facilities, Tools, R&D Infra, Professional Services (EXCLUDES People Cost & S&M)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L425-437 (Scaling) and L454-660 (Year 4 Detail)

| Row | Cost Category                        | Formula            | Y0    | Y1    | Y2    | Y3      | Y4      | Y5      |
| --- | ------------------------------------ | ------------------ | ----- | ----- | ----- | ------- | ------- | ------- |
| 24  | Facilities (Office + Warehouse)      | `=Assumptions!C51` | $15K  | $38K  | $70K  | $264K   | $410K   | $590K   |
| 25  | Technology & Tools (Cloud, Software) | `=Assumptions!C52` | $45K  | $90K  | $160K | $378K   | $580K   | $840K   |
| 26  | R&D Infrastructure                   | `=Assumptions!C53` | $25K  | $50K  | $75K  | $168K   | $300K   | $440K   |
| 27  | R&D Partnerships & IP                | `=Assumptions!C54` | $16K  | $32K  | $52K  | $114K   | $190K   | $280K   |
| 28  | Professional Services                | `=Assumptions!C55` | $25K  | $55K  | $105K | $216K   | $320K   | $450K   |
| 29  | Operations & Travel                  | `=Assumptions!C56` | $20K  | $45K  | $90K  | $222K   | $380K   | $520K   |
| 30  | Customer Enablement                  | `=Assumptions!C57` | $10K  | $22K  | $40K  | $84K    | $130K   | $170K   |
| 31  | Employee Development                 | `=Assumptions!C58` | $10K  | $20K  | $44K  | $90K    | $140K   | $200K   |
| 32  | Contingency & Reserves               | `=Assumptions!C59` | $14K  | $18K  | $44K  | $66K    | $50K    | $110K   |
| 33  | **Total Fixed Costs (G&A)**          | `=SUM(C24:C32)`    | $180K | $370K | $680K | $1,602K | $2,500K | $3,600K |

**BP Alignment (08_Team_Organization_Fixed_Costs.md L425-437):**

| Year       | BP Fixed Costs | Model G&A | Model SBC | Model Total | Variance |
| ---------- | -------------- | --------- | --------- | ----------- | -------- |
| Y0 (BP Y1) | $200K          | $180K     | $20K      | $200K       | 0%       |
| Y1 (BP Y2) | $420K          | $370K     | $50K      | $420K       | 0%       |
| Y2 (BP Y3) | $780K          | $680K     | $100K     | $780K       | 0%       |
| Y3 (BP Y4) | $1,750K        | $1,602K   | $150K     | $1,752K     | +0.1%    |
| Y4 (BP Y5) | $2,800K        | $2,500K   | $300K     | $2,800K     | 0%       |
| Y5 (BP Y6) | $4,200K        | $3,600K   | $600K     | $4,200K     | 0%       |

**Note:** BP Fixed Costs include SBC. Model correctly separates G&A from SBC for clearer reporting.

---

## STOCK-BASED COMPENSATION (Rows 35-36)

### Non-Cash Equity Grants (Excluded from EBITDA)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L679-682

| Row | Metric                   | Formula            | Y0   | Y1   | Y2    | Y3    | Y4    | Y5    |
| --- | ------------------------ | ------------------ | ---- | ---- | ----- | ----- | ----- | ----- |
| 36  | Stock-Based Compensation | `=Assumptions!C81` | $20K | $50K | $100K | $150K | $300K | $600K |

**Note:** SBC is a non-cash expense. Excluded from EBITDA (industry standard) but included in GAAP operating expenses.

**BP Validation (08_Team_Organization_Fixed_Costs.md L724-732):**

| Year    | BP SBC | Model SBC | Match |
| ------- | ------ | --------- | ----- |
| Y1 (Y0) | $20K   | $20K      | Yes   |
| Y2 (Y1) | $50K   | $50K      | Yes   |
| Y3 (Y2) | $100K  | $100K     | Yes   |
| Y4 (Y3) | $150K  | $150K     | Yes   |
| Y5 (Y4) | $300K  | $300K     | Yes   |
| Y6 (Y5) | $600K  | $600K     | Yes   |

---

## TOTAL OPERATING COSTS (Row 39)

| Year                      | Y0      | Y1      | Y2      | Y3       | Y4       | Y5       |
| ------------------------- | ------- | ------- | ------- | -------- | -------- | -------- |
| COGS                      | $220K   | $1,100K | $3,080K | $6,750K  | $13,020K | $20,860K |
| People Cost               | $680K   | $1,610K | $3,290K | $5,760K  | $9,500K  | $14,040K |
| S&M Variable              | $50K    | $250K   | $700K   | $1,500K  | $3,000K  | $5,500K  |
| Fixed (G&A)               | $200K   | $420K   | $780K   | $1,600K  | $2,500K  | $3,600K  |
| **Sub-Total (Cash)**      | $1,150K | $3,380K | $7,850K | $15,610K | $28,020K | $44,000K |
| SBC (Non-Cash)            | $20K    | $50K    | $100K   | $150K    | $300K    | $600K    |
| **Total Operating Costs** | $1,170K | $3,430K | $7,950K | $15,760K | $28,320K | $44,600K |

**Formula:**

```excel
C39: =C10 + C13 + C20 + C33 + C36  // COGS + People + S&M + G&A + SBC
```

**BP Alignment (08_Team_Organization_Fixed_Costs.md L724-732):**

| Year    | BP COGS | Model COGS | BP Total Costs | Model Total | Variance |
| ------- | ------- | ---------- | -------------- | ----------- | -------- |
| Y1 (Y0) | $0.22M  | $0.22M     | $1.15M         | $1.17M      | +2%      |
| Y2 (Y1) | $1.10M  | $1.10M     | $3.38M         | $3.43M      | +1%      |
| Y3 (Y2) | $3.08M  | $3.08M     | $7.85M         | $7.95M      | +1%      |
| Y4 (Y3) | $6.75M  | $6.75M     | $15.61M        | $15.76M     | +1%      |
| Y5 (Y4) | $13.02M | $13.02M    | $28.02M        | $28.32M     | +1%      |
| Y6 (Y5) | $20.86M | $20.86M    | $44.00M        | $44.60M     | +1%      |

**Note:** COGS now matches BP exactly. Total within 2% due to SBC inclusion.

---

## Cost Structure Analysis

### Cost Breakdown by Category (BP 5-Layer Structure)

| Category     | Y0      | Y5       | % of Total Y5 | % of Revenue |
| ------------ | ------- | -------- | ------------- | ------------ |
| COGS         | $220K   | $20,860K | 46.8%         | 42%          |
| People Cost  | $680K   | $14,040K | 31.5%         | 28%          |
| S&M Variable | $50K    | $5,500K  | 12.3%         | 11%          |
| Fixed (G&A)  | $200K   | $3,600K  | 8.1%          | 7%           |
| SBC          | $20K    | $600K    | 1.3%          | 1%           |
| **Total**    | $1,170K | $44,600K | 100%          | 89% of Rev   |

### Operating Leverage

| Metric             | Y0   | Y1   | Y2   | Y3   | Y4  | Y5  |
| ------------------ | ---- | ---- | ---- | ---- | --- | --- |
| Total Cost/Revenue | 234% | 137% | 114% | 105% | 94% | 89% |
| COGS/Revenue       | 44%  | 44%  | 44%  | 45%  | 43% | 42% |
| People/Revenue     | 136% | 64%  | 47%  | 38%  | 32% | 28% |
| S&M/Revenue        | 10%  | 10%  | 10%  | 10%  | 10% | 11% |
| G&A/Revenue        | 40%  | 17%  | 11%  | 11%  | 8%  | 7%  |

**Insight:** Operating leverage improves as fixed costs (People + G&A) become smaller % of revenue. COGS stays stable at 42-45% (fixed % per stream). At Y5: 89% cost/revenue = 11% EBITDA margin potential (actual 12% per BP).

---

## Cross-Sheet Linkages

### From Other Sheets

| Source Sheet   | Source Cell | This Cell | Data                              |
| -------------- | ----------- | --------- | --------------------------------- |
| Revenue        | C3:H8       | C4:H9     | Revenue by stream (for COGS calc) |
| Assumptions    | C18-C38     | C4:H9     | COGS percentages                  |
| Headcount Plan | C74         | C13       | Total People Cost                 |
| Assumptions    | C61-C64     | C16:C19   | S&M Variable components           |
| Assumptions    | C71-C79     | C24:C32   | Fixed Cost (G&A) components       |
| Assumptions    | C81         | C36       | Stock-Based Compensation          |

### To Other Sheets

| Target Sheet | Target Cell          | This Cell       | Purpose                      |
| ------------ | -------------------- | --------------- | ---------------------------- |
| P&L          | COGS line            | C10             | Gross profit calc            |
| P&L          | Operating expenses   | C13+C20+C33     | Operating income calc        |
| P&L          | SBC                  | C36             | GAAP OpEx (below EBITDA)     |
| Cash Flow    | Operating activities | C10+C13+C20+C33 | Cash outflows (excludes SBC) |

---

## Formatting Standards

| Row Type        | Background Color        | Text Color | Font        | Number Format |
| --------------- | ----------------------- | ---------- | ----------- | ------------- |
| Sheet Title     | `RGB(0.20, 0.30, 0.50)` | White      | Bold 14pt   | -             |
| Section Header  | `RGB(0.20, 0.40, 0.60)` | White      | Bold 12pt   | -             |
| Category Header | `RGB(0.30, 0.50, 0.70)` | White      | Bold 11pt   | -             |
| Year Headers    | `RGB(0.95, 0.95, 0.95)` | Black      | Bold 10pt   | -             |
| Cost Rows       | White                   | Black      | Normal 10pt | `$#,##0"K"`   |
| Total Rows      | `RGB(0.9, 0.95, 1.0)`   | Black      | Bold 10pt   | `$#,##0"K"`   |
| GRAND TOTAL Row | `RGB(0.85, 0.9, 0.95)`  | Black      | Bold 11pt   | `$#,##0"K"`   |

---

## Validation Checks

1. **COGS % Validation**: Each COGS should equal Revenue x COGS %
2. **People Cost Match**: Row 13 should equal `='Headcount Plan'!C74`
3. **S&M Variable**: Sum should match BP table (within 5%)
4. **G&A Fixed**: Sum should match BP table (within 5%)
5. **Total Validation**: Row 39 = Sum of all categories
6. **BP Alignment**: Total Operating Costs should be less than 85% of revenue at Y5+ (EBITDA positive)
