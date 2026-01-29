# 09 - Summary (KPI Dashboard)

> **Last Updated:** 2026-01-28  
> **Sheet Position:** 9 of 14  
> **Status:** Complete

---

## Overview

The Summary sheet provides a **KPI Dashboard** consolidating key metrics from all other sheets. This is the primary view for investors and management.

---

## Sheet Structure

| Row   | Section        | Content                          |
| ----- | -------------- | -------------------------------- |
| 1     | Title          | KEY METRICS SUMMARY              |
| 2     | Headers        | Unit, Y0-Y5                      |
| 3-5   | Revenue        | Total Revenue, Growth %          |
| 7-13  | Profitability  | GP, EBITDA, Net Income + Margins |
| 14-16 | Cash & Funding | Cash Balance, Operating CF       |
| 18-22 | Customers      | Total, New, Churned, Growth      |
| 24-34 | Unit Economics | CAC, ARPU, LTV, Ratios           |
| 36-46 | Revenue Mix    | Breakdown by stream              |

---

## Data Tables

### Revenue Section

| Metric             | Unit | Y0    | Y1      | Y2      | Y3       | Y4       | Y5       |
| ------------------ | ---- | ----- | ------- | ------- | -------- | -------- | -------- |
| **Total Revenue**  | $    | $496K | $2,482K | $7,001K | $15,050K | $30,111K | $50,179K |
| **Revenue Growth** | %    | -     | 400%    | 182%    | 115%     | 100%     | 67%      |

### Profitability Section

| Metric                | Unit | Y0     | Y1      | Y2      | Y3      | Y4       | Y5       |
| --------------------- | ---- | ------ | ------- | ------- | ------- | -------- | -------- |
| **Gross Profit**      | $    | $280K  | $1,400K | $3,920K | $8,250K | $16,980K | $29,140K |
| **Gross Margin**      | %    | 56%    | 56%     | 56%     | 55%     | 57%      | 58%      |
| **EBITDA**            | $    | -$650K | -$880K  | -$850K  | -$610K  | $1,980K  | $6,000K  |
| **EBITDA Margin**     | %    | -130%  | -35%    | -12%    | -4%     | 7%       | 12%      |
| **Net Income**        | $    | -$685K | -$950K  | -$990K  | -$820K  | $1,106K  | $3,675K  |
| **Net Profit Margin** | %    | -137%  | -38%    | -14%    | -5%     | 4%       | 7%       |

**Note:** Gross margin stays stable at 56-58% (not improving) — reflects fixed COGS% per stream with services having structural margin limits (materials + labor floor). EBITDA breakeven in Y4, Net Income positive in Y4.

### Cash & Funding Section

| Metric                  | Unit | Y0      | Y1     | Y2      | Y3      | Y4      | Y5       |
| ----------------------- | ---- | ------- | ------ | ------- | ------- | ------- | -------- |
| **Cash Balance**        | $    | $1,168K | $342K  | $3,977K | $4,457K | $7,962K | $16,776K |
| **Operating Cash Flow** | $    | -$757K  | -$726K | -$265K  | $580K   | $3,605K | $8,914K  |

### Customers Section

| Metric                   | Unit | Y0  | Y1   | Y2   | Y3  | Y4  | Y5  |
| ------------------------ | ---- | --- | ---- | ---- | --- | --- | --- |
| **Total Customers**      | #    | 8   | 35   | 85   | 175 | 375 | 750 |
| **New Customers**        | #    | 10  | 76   | 156  | 244 | 422 | 561 |
| **Churned Customers**    | #    | 0   | 1    | 8    | 23  | 45  | 83  |
| **Customer Growth Rate** | %    | 0%  | 750% | 173% | 95% | 83% | 57% |

### Unit Economics Section

| Metric                    | Unit | Y0       | Y1       | Y2       | Y3       | Y4       | Y5       |
| ------------------------- | ---- | -------- | -------- | -------- | -------- | -------- | -------- |
| **CAC**                   | $    | $2,000   | $2,100   | $2,200   | $2,300   | $2,400   | $2,500   |
| **Total CAC Spend**       | $    | $20K     | $160K    | $343K    | $561K    | $1,013K  | $1,403K  |
| **ARPU (Annual)**         | $    | $62,058  | $70,914  | $82,317  | $85,997  | $80,283  | $66,906  |
| **ARPU (Monthly)**        | $    | $5,171   | $5,909   | $6,860   | $7,166   | $6,690   | $5,575   |
| **Churn Rate**            | %    | 10%      | 10%      | 10%      | 10%      | 10%      | 10%      |
| **Avg Customer Lifetime** | yrs  | 10.0     | 10.0     | 10.0     | 10.0     | 10.0     | 10.0     |
| **LTV (Gross)**           | $    | $620,575 | $709,137 | $823,172 | $859,971 | $802,827 | $669,060 |
| **LTV (Net of COGS)**     | $    | $415,011 | $475,698 | $553,257 | $572,310 | $543,477 | $461,262 |
| **LTV:CAC Ratio**         | x    | 207.5x   | 226.5x   | 251.5x   | 248.8x   | 226.4x   | 184.5x   |
| **CAC Payback**           | mo   | 0.6      | 0.5      | 0.5      | 0.5      | 0.5      | 0.7      |

### Revenue Mix Section

| Stream                    | Y0    | Y1      | Y2      | Y3      | Y4       | Y5       |
| ------------------------- | ----- | ------- | ------- | ------- | -------- | -------- |
| **Software Subscription** | $279K | $1,400K | $3,920K | $8,100K | $17,100K | $30,000K |
| **3D Printer Sales**      | $56K  | $245K   | $595K   | $1,197K | $2,394K  | $3,500K  |
| **Consumables Materials** | $10K  | $50K    | $100K   | $150K   | $300K    | $500K    |
| **AMC Spares**            | $2K   | $8K     | $23K    | $53K    | $112K    | $200K    |
| **Managed Services**      | $0K   | $30K    | $330K   | $1,200K | $2,100K  | $3,480K  |
| **Job Work Services**     | $150K | $750K   | $2,030K | $4,350K | $8,100K  | $12,500K |

---

## Formula Specifications

### Revenue Metrics

```
C4 (Total Revenue) = =Revenue!C10
C5 (Revenue Growth) = =(D4-C4)/C4  [D5 onwards]
```

### Profitability Metrics

```
C8 (Gross Profit) = =''P&L''!C16
C9 (Gross Margin) = =C8/C4
C10 (EBITDA) = =''P&L''!C25
C11 (EBITDA Margin) = =C10/C4
C12 (Net Income) = =''P&L''!C36
C13 (Net Margin) = =C12/C4
```

### Cash Metrics

```
C15 (Cash Balance) = =''Balance Sheet''!C6
C16 (Operating CF) = =''Cash Flow''!C7
```

### Customer Metrics

```
C19 (Total Customers) = =Assumptions!C60
C20 (New Customers) = =Assumptions!C54
C21 (Churned) = =Assumptions!C55
C22 (Growth Rate) = =(D19-C19)/C19  [D22 onwards]
```

### Unit Economics

```
C25 (CAC) = =Assumptions!C53
C26 (CAC Spend) = =C25*C20
C27 (ARPU Annual) = =C4/C19
C28 (ARPU Monthly) = =C27/12
C29 (Churn Rate) = =Assumptions!C58
C30 (Lifetime) = =1/C29
C31 (LTV Gross) = =C27*C30
C32 (LTV Net) = =C31*C9
C33 (LTV:CAC) = =C32/C25
C34 (Payback) = =C25/C28
```

### Revenue Mix

```
C37:C42 = =Revenue!C3:C8
```

---

## Cross-Sheet Linkages

| Metric            | Source Sheet  | Source Cell |
| ----------------- | ------------- | ----------- |
| Total Revenue     | Revenue       | C10         |
| Gross Profit      | P&L           | C16         |
| EBITDA            | P&L           | C25         |
| Net Income        | P&L           | C36         |
| Cash Balance      | Balance Sheet | C6          |
| Operating CF      | Cash Flow     | C7          |
| Total Customers   | Assumptions   | C60         |
| New Customers     | Assumptions   | C54         |
| Churned Customers | Assumptions   | C55         |
| CAC               | Assumptions   | C53         |
| Churn Rate        | Assumptions   | C58         |
| Revenue by Stream | Revenue       | C3:C8       |

---

## Investor Highlights

### Key Metrics (Year 5)

| Metric            | Value  | Assessment               |
| ----------------- | ------ | ------------------------ |
| **Revenue**       | $50.2M | Strong growth trajectory |
| **Gross Margin**  | 68.9%  | SaaS-like margins        |
| **EBITDA Margin** | 29.0%  | Highly profitable        |
| **Net Margin**    | 21.7%  | Excellent bottom line    |
| **LTV:CAC**       | 184.5x | Very efficient CAC       |
| **Cash**          | $16.8M | Strong cash position     |

### Growth Profile

| Metric    | CAGR (Y0-Y5)            |
| --------- | ----------------------- |
| Revenue   | 150%                    |
| EBITDA    | N/A (turns positive Y2) |
| Customers | 147%                    |

---

## Formatting Standards

### Section Headers (Rows 3, 7, 14, 18, 24, 36)

- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Data Labels (Column A)

- Font: Bold
- Alignment: Left

### Metric Values

- Currency: `$#,##0"K"` or `$#,##0`
- Percentage: `0.0%`
- Ratio: `0.0x`
- Count: `#,##0`

### Negative Values

- Font color: Red
- Currency: `($#,##0"K")`

### Highlight Cells

- Total Revenue row: Light blue background
- Net Income row: Yellow background if positive, red if negative
