# 10 - Sensitivity Analysis

> **Last Updated:** 2026-01-28  
> **Sheet Position:** 10 of 14  
> **Status:** Complete

---

## Overview

The Sensitivity Analysis sheet models different scenarios and shows how key metrics change with variations in assumptions. This helps investors understand risk and upside potential.

---

## Sheet Structure

| Row   | Section                | Content                 |
| ----- | ---------------------- | ----------------------- |
| 1     | Title                  | SENSITIVITY ANALYSIS    |
| 3-12  | Scenario Analysis      | Bear/Base/Bull cases    |
| 14-20 | Revenue Sensitivity    | Price Volume matrix     |
| 22-28 | EBITDA Sensitivity     | Revenue Cost matrix     |
| 30-35 | Key Assumptions Impact | Variable impact ratings |

---

## Data Tables

### Scenario Analysis

| Parameter              | Bear Case | Base Case | Bull Case |
| ---------------------- | --------- | --------- | --------- |
| **Revenue Growth Adj** | -20%      | 0%        | +20%      |
| **Cost Adjustment**    | +10%      | 0%        | -10%      |
| **Price Adjustment**   | -10%      | 0%        | +10%      |

### Scenario Outputs (Year 5)

| Metric         | Bear Case | Base Case | Bull Case |
| -------------- | --------- | --------- | --------- |
| **Revenue**    | $36,000K  | $50,000K  | $66,000K  |
| **EBITDA**     | $2,300K   | $6,000K   | $10,000K  |
| **Net Income** | $500K     | $3,675K   | $8,500K   |

### Revenue Sensitivity Table (Price × Volume)

|                | -20% Vol | -10% Vol | Base     | +10% Vol | +20% Vol |
| -------------- | -------- | -------- | -------- | -------- | -------- |
| **-20% Price** | $32,000K | $36,000K | $40,000K | $44,000K | $48,000K |
| **-10% Price** | $36,000K | $40,500K | $45,000K | $49,500K | $54,000K |
| **Base Price** | $40,000K | $45,000K | $50,000K | $55,000K | $60,000K |
| **+10% Price** | $44,000K | $49,500K | $55,000K | $60,500K | $66,000K |
| **+20% Price** | $48,000K | $54,000K | $60,000K | $66,000K | $72,000K |

### EBITDA Sensitivity Table (Revenue × Cost)

|              | -10% Cost | -5% Cost | Base     | +5% Cost | +10% Cost |
| ------------ | --------- | -------- | -------- | -------- | --------- |
| **-20% Rev** | $2,588K   | $2,430K  | $2,271K  | $2,113K  | $1,954K   |
| **-10% Rev** | $4,276K   | $4,138K  | $4,000K  | $3,862K  | $3,724K   |
| **Base Rev** | $6,315K   | $6,158K  | $6,000K  | $5,843K  | $5,685K   |
| **+10% Rev** | $8,354K   | $8,177K  | $8,000K  | $7,823K  | $7,646K   |
| **+20% Rev** | $10,393K  | $10,197K | $10,000K | $9,803K  | $9,606K   |

### Key Assumptions Impact

| Variable           | Base Value | -20% | -10%     | +10%     | +20% | Impact     |
| ------------------ | ---------- | ---- | -------- | -------- | ---- | ---------- |
| **Revenue Growth** | 67% (Y5)   | Low  | Med-Low  | Med-High | High | **High**   |
| **COGS %**         | 42%        | High | Med-High | Med-Low  | Low  | **High**   |
| **Fixed Costs**    | $23M       | High | Med-High | Med-Low  | Low  | **Medium** |
| **CAC**            | $2,500     | High | Med-High | Med-Low  | Low  | **Medium** |

---

## Formula Specifications

### Scenario Revenue (Y5)

```
C10 (Bear) = =Revenue!H10 * (1 + C5) * (1 + C7)
           = Base Revenue  (1 - 0.20)  (1 - 0.10)
           = $50,179K  0.80  0.90 = $36,129K

D10 (Base) = =Revenue!H10
           = $50,179K

E10 (Bull) = =Revenue!H10 * (1 + E5) * (1 + E7)
           = $50,179K  1.20  1.10 = $66,237K
```

### Scenario EBITDA (Y5)

```
C11 (Bear) = =''P&L''!H25 * (1 + C5) + (''P&L''!H20 * C6)
           = Adjusted EBITDA with revenue reduction and cost increase

D11 (Base) = =''P&L''!H25
           = $6,000K

E11 (Bull) = Adjusted for higher revenue and lower costs
```

### Revenue Sensitivity Table

```
D16 = =Revenue!H10 * (1 + $C16) * (1 + D$15)
    = Base Revenue  Row Adjustment  Column Adjustment

Example: C16 = $50,179K  (1-0.20)  (1-0.20)
       = $50,179K  0.80  0.80 = $32,115K
```

### EBITDA Sensitivity Table

```
D24 = =''P&L''!H25 + (Revenue!H10 * $C24) - (''Operating Costs''!H14 * D$23)
    = Base EBITDA + Revenue Delta - Cost Delta
```

---

## Sensitivity Ranges

### Revenue Range

| Scenario | Adjustment | Revenue Y5 | Change |
| -------- | ---------- | ---------- | ------ |
| Bear     | -28%       | $36.1M     | -28%   |
| Base     | 0%         | $50.2M     | -      |
| Bull     | +32%       | $66.2M     | +32%   |

### EBITDA Range

| Scenario | EBITDA Y5 | Margin |
| -------- | --------- | ------ |
| Bear     | $2.3M     | 6%     |
| Base     | $6.0M     | 12%    |
| Bull     | $10.0M    | 15%    |

---

## Risk Assessment

### High Impact Variables

1. **Revenue Growth Rate** - Direct 1:1 impact on revenue
2. **COGS %** - Affects gross margin and profitability
3. **Churn Rate** - Affects customer base and recurring revenue

### Medium Impact Variables

1. **Fixed Costs** - Operating leverage
2. **CAC** - Customer acquisition efficiency
3. **Price** - Revenue per customer

### Low Impact Variables

1. **Debtor Days** - Working capital timing
2. **Creditor Days** - Working capital timing
3. **Capex** - Balance sheet impact only

---

## Scenario Narratives

### Bear Case (-20% Revenue, +10% Costs, -10% Price)

**Assumptions:**

- Slower market adoption
- Increased competition driving prices down
- Higher costs due to inflation/supply chain
- 10% higher churn rate

**Outcome:**

- Revenue Y5: $36.1M (vs $50.0M base)
- Still marginally profitable: $0.5M net income
- Cash positive: No additional funding needed

### Base Case

**Assumptions:**

- Current trajectory maintained
- Market grows as projected
- Costs scale as planned

**Outcome:**

- Revenue Y5: $50.0M
- Net Income: $3.7M
- Cash: $16.8M

### Bull Case (+20% Revenue, -10% Costs, +10% Price)

**Assumptions:**

- Faster market adoption
- Premium pricing accepted
- Operating efficiencies achieved
- Lower churn (8%)

**Outcome:**

- Revenue Y5: $66.2M (+32% vs base)
- Net Income: $8.5M
- Cash: $25M+

---

## Cross-Sheet Linkages

| This Sheet       | Links To            | Data     |
| ---------------- | ------------------- | -------- |
| Revenue Base     | Revenue H10         | $50,000K |
| EBITDA Base      | P&L H25             | $6,000K  |
| Net Income Base  | P&L H36             | $3,675K  |
| COGS Base        | Operating Costs H10 | $20,860K |
| Fixed Costs Base | Operating Costs H14 | $23,140K |

---

## Formatting Standards

### Section Headers (Rows 3, 14, 22, 30)

- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Sensitivity Tables

- Row/Column headers: Light Gray (#F2F2F2)
- Base case intersection: Yellow highlight (#FFFFE6)
- Positive variance: Light green (#C6EFCE)
- Negative variance: Light red (#FFC7CE)

### Impact Ratings

- High: Red background
- Medium: Yellow background
- Low: Green background
