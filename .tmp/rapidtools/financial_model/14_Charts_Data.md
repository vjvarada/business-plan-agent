# 14 - Charts Data

> **Last Updated:** 2026-01-28  
> **Sheet Position:** 14 of 14  
> **Status:** Complete

---

## Overview

The Charts Data sheet provides **pre-formatted data for visualizations**. Each section is designed to feed a specific chart type in presentations or dashboards.

This sheet contains **10 chart data series** covering:

- Revenue trends
- Profitability metrics
- Customer growth
- Unit economics
- Cash position
- Cap table
- Break-even analysis

---

## Sheet Structure

| Row   | Chart                     | Data Type       |
| ----- | ------------------------- | --------------- |
| 1-3   | Chart 1: Revenue Growth   | Line chart      |
| 5-12  | Chart 2: Revenue Mix      | Pie/Bar chart   |
| 14-18 | Chart 3: Profitability    | Multi-line      |
| 20-23 | Chart 4: Customer Growth  | Bar/Line        |
| 25-28 | Chart 5: Unit Economics   | Dual axis       |
| 30-32 | Chart 6: Cash Position    | Area chart      |
| 34-38 | Chart 7: Margin Trends    | Multi-line      |
| 40-44 | Chart 8: Cap Table        | Pie chart       |
| 46-49 | Chart 9: Funding Timeline | Stacked bar     |
| 51-54 | Chart 10: Break-even      | Line comparison |

---

## Data Tables

### Chart 1: Revenue Growth

| Year             | Y0  | Y1    | Y2    | Y3     | Y4     | Y5     |
| ---------------- | --- | ----- | ----- | ------ | ------ | ------ |
| **Revenue ($K)** | 496 | 2,482 | 6,997 | 15,050 | 30,106 | 50,179 |

**Chart Type:** Line chart with data labels
**Recommended:** Include growth % as secondary series

---

### Chart 2: Revenue Mix (Year 5)

| Stream                    | Revenue ($K) | % of Total |
| ------------------------- | ------------ | ---------- |
| **Software Subscription** | 30,000       | 59.8%      |
| **Job Work Services**     | 12,500       | 24.9%      |
| **Managed Services**      | 3,480        | 6.9%       |
| **3D Printer Sales**      | 3,500        | 7.0%       |
| **Consumables**           | 500          | 1.0%       |
| **AMC Spares**            | 200          | 0.4%       |

**Chart Type:** Pie chart or horizontal bar
**Note:** Software is dominant revenue stream (60%)

---

### Chart 3: Profitability Trend

| Year                  | Y0   | Y1    | Y2    | Y3    | Y4     | Y5     |
| --------------------- | ---- | ----- | ----- | ----- | ------ | ------ |
| **Gross Profit ($K)** | 280  | 1,400 | 3,920 | 8,250 | 16,980 | 29,140 |
| **EBITDA ($K)**       | -650 | -880  | -850  | -610  | 1,980  | 6,000  |
| **Net Income ($K)**   | -685 | -950  | -990  | -820  | 1,106  | 3,675  |

**Chart Type:** Multi-line with zero baseline
**Note:** Highlight Y4 as profitability inflection point

---

### Chart 4: Customer Growth

| Year                | Y0  | Y1  | Y2  | Y3  | Y4  | Y5  |
| ------------------- | --- | --- | --- | --- | --- | --- |
| **Total Customers** | 8   | 35  | 85  | 175 | 375 | 750 |
| **New Customers**   | 10  | 76  | 156 | 244 | 422 | 561 |

**Chart Type:** Stacked bar or dual-axis line
**Note:** Net adds = New - Churned

---

### Chart 5: Unit Economics

| Year                 | Y0     | Y1     | Y2     | Y3     | Y4     | Y5     |
| -------------------- | ------ | ------ | ------ | ------ | ------ | ------ |
| **LTV:CAC Ratio**    | 207.5x | 226.5x | 251.5x | 248.8x | 226.4x | 184.5x |
| **CAC Payback (mo)** | 0.6    | 0.5    | 0.5    | 0.5    | 0.5    | 0.7    |

**Chart Type:** Dual-axis (LTV:CAC left, Payback right)
**Note:** Exceptionally strong unit economics

---

### Chart 6: Cash Position

| Year                  | Y0    | Y1  | Y2    | Y3    | Y4    | Y5     |
| --------------------- | ----- | --- | ----- | ----- | ----- | ------ |
| **Cash Balance ($K)** | 1,168 | 342 | 3,977 | 4,457 | 7,962 | 16,776 |

**Chart Type:** Area chart (shows cumulative)
**Note:** Series A at Y2 visible as step-up

---

### Chart 7: Margin Trends

| Year              | Y0      | Y1     | Y2    | Y3    | Y4    | Y5    |
| ----------------- | ------- | ------ | ----- | ----- | ----- | ----- |
| **Gross Margin**  | 66.9%   | 67.1%  | 67.2% | 66.5% | 67.7% | 68.9% |
| **EBITDA Margin** | -142.9% | -21.6% | 3.1%  | 11.9% | 22.5% | 29.0% |
| **Net Margin**    | -145.9% | -22.4% | 2.1%  | 8.8%  | 16.8% | 21.7% |

**Chart Type:** Multi-line with 0% baseline
**Note:** Clip Y-axis at -50% for readability

---

### Chart 8: Cap Table (Post Series A)

| Stakeholder            | Ownership % |
| ---------------------- | ----------- |
| **Founders**           | 56.4%       |
| **Seed Investors**     | 22.6%       |
| **Series A Investors** | 21.1%       |

**Chart Type:** Pie chart or donut
**Note:** Founders retain majority control

---

### Chart 9: Funding Timeline

| Year                       | Y0    | Y1    | Y2    | Y3    | Y4    | Y5    |
| -------------------------- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Equity Raised ($K)**     | 2,000 | 0     | 4,000 | 0     | 0     | 0     |
| **Cumulative Equity ($K)** | 2,000 | 2,000 | 6,000 | 6,000 | 6,000 | 6,000 |

**Chart Type:** Bar for raised, line for cumulative
**Note:** Show round labels (Seed, Series A)

---

### Chart 10: Break-even Analysis

| Year                        | Y0    | Y1    | Y2    | Y3     | Y4     | Y5     |
| --------------------------- | ----- | ----- | ----- | ------ | ------ | ------ |
| **Break-even Revenue ($K)** | 1,527 | 3,042 | 6,158 | 11,516 | 18,623 | 27,060 |
| **Actual Revenue ($K)**     | 496   | 2,482 | 6,997 | 15,050 | 30,106 | 50,179 |

**Chart Type:** Dual line comparison
**Note:** Highlight crossover at Y2 (break-even achieved)

---

## Formula Specifications

### All chart data references Summary or underlying sheets:

```
Chart 1 Revenue:
B3 = =Summary!C4/1000  (convert to $K)

Chart 2 Revenue Mix:
B7 = =Revenue!H3/1000  (Y5 Software)
B8 = =Revenue!H4/1000  (Y5 Printers)
...

Chart 3 Profitability:
B16 = =Summary!C8/1000  (Gross Profit)
B17 = =Summary!C10/1000  (EBITDA)
B18 = =Summary!C12/1000  (Net Income)

Chart 4 Customers:
B22 = =Summary!C19  (Total Customers)
B23 = =Summary!C20  (New Customers)

Chart 5 Unit Economics:
B27 = =Summary!C33  (LTV:CAC)
B28 = =Summary!C34  (CAC Payback)

Chart 6 Cash:
B32 = =Summary!C15/1000  (Cash Balance)

Chart 7 Margins:
B36 = =Summary!C9  (Gross Margin %)
B37 = =Summary!C11  (EBITDA Margin %)
B38 = =Summary!C13  (Net Margin %)

Chart 8 Cap Table:
B42 = =''Funding Cap Table''!E15  (Founders %)
B43 = =''Funding Cap Table''!E16  (Seed %)
B44 = =''Funding Cap Table''!E17  (Series A %)

Chart 9 Funding:
B48 = =''Funding Cap Table''!C4/1000  (Equity Raised)
B49 = =''Funding Cap Table''!C5/1000  (Cumulative)

Chart 10 Break-even:
B53 = =''Break-even Analysis''!C11/1000  (BE Revenue)
B54 = =''Break-even Analysis''!C12/1000  (Actual Revenue)
```

---

## Recommended Chart Styles

### Color Palette for Charts

| Series               | Color           | Hex     |
| -------------------- | --------------- | ------- |
| **Revenue/Positive** | Blue            | #336699 |
| **EBITDA**           | Green           | #339966 |
| **Net Income**       | Dark Green      | #006600 |
| **Costs/Negative**   | Red             | #CC3333 |
| **Break-even Line**  | Orange (dashed) | #FF9900 |
| **Target/Threshold** | Gray (dashed)   | #999999 |

### Chart Formatting Guidelines

1. **Titles:** Bold, 14pt, above chart
2. **Axis Labels:** 10pt, rotated if needed
3. **Data Labels:** Inside bars, or end of lines
4. **Legend:** Bottom or right, 10pt
5. **Gridlines:** Light gray, horizontal only
6. **Zero Line:** Emphasized for margin charts

---

## Cross-Sheet Linkages

| Chart | Primary Source                  | Secondary     |
| ----- | ------------------------------- | ------------- |
| 1     | Summary C4:H4                   | Revenue       |
| 2     | Revenue H3:H8                   | -             |
| 3     | Summary C8:H8, C10:H10, C12:H12 | P&L           |
| 4     | Summary C19:H19, C20:H20        | Assumptions   |
| 5     | Summary C33:H33, C34:H34        | -             |
| 6     | Summary C15:H15                 | Balance Sheet |
| 7     | Summary C9:H9, C11:H11, C13:H13 | -             |
| 8     | Funding Cap Table E15:E17       | -             |
| 9     | Funding Cap Table C4:H4, C5:H5  | Assumptions   |
| 10    | Break-even C11:H11, C12:H12     | -             |

---

## Formatting Standards

### Section Headers (Rows 1, 5, 14, 20, 25, 30, 34, 40, 46, 51)

- Background: Light Gray (#F2F2F2)
- Font: Bold, 11pt

### Data Values

- Numbers: Right-aligned
- Currency: No symbol (chart will format)
- Percentages: As decimal in formulas, display as %
