# 09 - Summary (KPI Dashboard)

> **Last Updated:** 2026-01-29  
> **Sheet Position:** 9 of 14  
> **Status:** Complete - Aligned with P&L

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
| **Total Revenue**  | $    | $498K | $2,470K | $6,988K | $15,109K | $30,044K | $50,068K |
| **Revenue Growth** | %    | -     | 396%    | 183%    | 116%     | 99%      | 67%      |

### Profitability Section

| Metric                | Unit | Y0     | Y1      | Y2      | Y3      | Y4       | Y5       |
| --------------------- | ---- | ------ | ------- | ------- | ------- | -------- | -------- |
| **Gross Profit**      | $    | $277K  | $1,368K | $3,909K | $8,357K | $17,028K | $29,208K |
| **Gross Margin**      | %    | 56%    | 55%     | 56%     | 55%     | 57%      | 58%      |
| **EBITDA**            | $    | -$763K | -$862K  | -$761K  | -$505K  | $2,028K  | $6,068K  |
| **EBITDA Margin**     | %    | -153%  | -35%    | -11%    | -3%     | 7%       | 12%      |
| **Net Income**        | $    | -$798K | -$932K  | -$901K  | -$715K  | $1,140K  | $3,723K  |
| **Net Profit Margin** | %    | -160%  | -38%    | -13%    | -5%     | 4%       | 7%       |

**Note:** Gross margin stays stable at 56-58% (not improving) — reflects fixed COGS% per stream with services having structural margin limits (materials + labor floor). EBITDA breakeven in Y4, Net Income positive in Y4.

### Cash & Funding Section

| Metric                  | Unit | Y0      | Y1       | Y2      | Y3       | Y4       | Y5       |
| ----------------------- | ---- | ------- | -------- | ------- | -------- | -------- | -------- |
| **Cash Balance**        | $    | $2,073K | $788K    | $9,234K | $7,495K  | $31,800K | $33,053K |
| **Operating Cash Flow** | $    | -$827K  | -$1,085K | -$1,254K| -$1,339K | -$95K    | $2,053K  |

### Customers Section

| Metric                   | Unit | Y0  | Y1   | Y2   | Y3  | Y4  | Y5  |
| ------------------------ | ---- | --- | ---- | ---- | --- | --- | --- |
| **Total Customers**      | #    | 8   | 35   | 85   | 175 | 375 | 750 |
| **New Customers**        | #    | 10  | 76   | 156  | 244 | 422 | 561 |
| **Churned Customers**    | #    | 0   | 1    | 8    | 23  | 45  | 83  |
| **Customer Growth Rate** | %    | 0%  | 750% | 173% | 95% | 83% | 57% |

### Unit Economics Section

**BP Reference:** 07_Revenue_Model.md L24-42 (Unit Economics Summary)

| Metric                    | Unit | Y0       | Y1       | Y2       | Y3       | Y4       | Y5       |
| ------------------------- | ---- | -------- | -------- | -------- | -------- | -------- | -------- |
| **CAC**                   | $    | $2,000   | $2,100   | $2,200   | $2,300   | $2,400   | $2,500   |
| **Total CAC Spend**       | $    | $20K     | $160K    | $343K    | $561K    | $1,013K  | $1,403K  |
| **ARPU (Annual)**         | $    | $62,058  | $70,914  | $82,317  | $85,997  | $80,283  | $66,906  |
| **ARPU (Monthly)**        | $    | $5,171   | $5,909   | $6,860   | $7,166   | $6,690   | $5,575   |
| **Churn Rate (Blended)**  | %    | 15%      | 15%      | 15%      | 15%      | 15%      | 15%      |
| **Avg Customer Lifetime** | yrs  | 6.7      | 6.7      | 6.7      | 6.7      | 6.7      | 6.7      |
| **LTV (Gross)**           | $    | $415,789 | $475,164 | $551,523 | $576,179 | $537,896 | $448,270 |
| **LTV (Net of COGS)**     | $    | $232,841 | $261,590 | $308,853 | $316,898 | $306,200 | $260,397 |
| **LTV:CAC Ratio**         | x    | 11.6x    | 12.5x    | 14.0x    | 13.8x    | 12.8x    | 10.4x    |
| **CAC Payback**           | mo   | 4.6      | 4.3      | 3.9      | 3.9      | 4.3      | 5.4      |

**Note on LTV:CAC (BP 07_Revenue_Model.md L44-60):**
- Ratios of 10-14:1 reflect India cost advantage (CAC 60-70% lower than US)
- Blended churn 15% = SMB 17%, Mid-Market 11%, Enterprise 6% weighted by segment
- As US/EU expansion increases CAC, ratios expected to normalize to 5-8:1
- Industry benchmark minimum: 3:1 (RapidTools exceeds at all stages)

### Revenue Mix Section

| Stream                    | Y0    | Y1      | Y2      | Y3      | Y4       | Y5       |
| ------------------------- | ----- | ------- | ------- | ------- | -------- | -------- |
| **Software Subscription** | $281K | $1,388K | $3,906K | $8,159K | $17,037K | $29,888K |
| **3D Printer Sales**      | $56K  | $245K   | $630K   | $1,197K | $2,394K  | $3,500K  |
| **Consumables Materials** | $10K  | $50K    | $70K    | $150K   | $300K    | $500K    |
| **AMC Spares**            | $1K   | $7K     | $23K    | $53K    | $113K    | $200K    |
| **Managed Services**      | $0K   | $30K    | $330K   | $1,200K | $2,100K  | $3,480K  |
| **Job Work Services**     | $150K | $750K   | $2,029K | $4,350K | $8,100K  | $12,500K |

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

**BP Reference:** 07_Revenue_Model.md L24-42 (churn by segment, lifetime calculation)

```
C25 (CAC) = =Assumptions!C53
C26 (CAC Spend) = =C25*C20
C27 (ARPU Annual) = =C4/C19
C28 (ARPU Monthly) = =C27/12
C29 (Churn Rate) = =Assumptions!C58    // 15% blended (SMB 17%, MM 11%, Ent 6%)
C30 (Lifetime) = =1/C29               // 6.7 years = 1/0.15
C31 (LTV Gross) = =C27*C30
C32 (LTV Net) = =C31*C9               // LTV × Gross Margin
C33 (LTV:CAC) = =C32/C25              // Target: 10-14x (India advantage)
C34 (Payback) = =C25/C28              // Target: 4-6 months
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
| **Revenue**       | $50.1M | Strong growth trajectory |
| **Gross Margin**  | 58%    | Services mix constraint  |
| **EBITDA Margin** | 12%    | Path to 18% by Y8        |
| **Net Margin**    | 7%     | Profitable, reinvesting  |
| **LTV:CAC**       | 10.4x  | 3× industry minimum      |
| **Cash**          | $33.1M | Strong cash position     |

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
