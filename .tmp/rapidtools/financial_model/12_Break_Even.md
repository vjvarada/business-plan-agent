# 12 - Break-even Analysis

> **Last Updated:** 2026-01-29  
> **Sheet Position:** 12 of 14  
> **Status:** Complete

---

## Overview

The Break-even Analysis calculates:

1. **Contribution Margin** - Revenue minus variable costs
2. **Break-even Revenue** - Fixed Costs Contribution Margin %
3. **Margin of Safety** - Buffer above break-even
4. **Operating Leverage** - Sensitivity to revenue changes

---

## Sheet Structure

| Row   | Section                | Content                                  |
| ----- | ---------------------- | ---------------------------------------- |
| 1     | Title                  | BREAK-EVEN ANALYSIS                      |
| 3-8   | Contribution Margin    | Revenue, Variable Costs, CM, Fixed Costs |
| 10-18 | Break-even Analysis    | BE Revenue, Margin of Safety             |
| 20-22 | Operating Leverage     | DOL calculations                         |
| 24-26 | Margin of Safety       | Detail                                   |
| 28-32 | Profitability Timeline | EBITDA, Net Income milestones            |

---

## Data Tables

### Contribution Margin

| Metric                    | Y0    | Y1      | Y2      | Y3       | Y4       | Y5       |
| ------------------------- | ----- | ------- | ------- | -------- | -------- | -------- |
| **Total Revenue**         | $498K | $2,470K | $6,988K | $15,109K | $30,044K | $50,068K |
| **Variable Costs (COGS)** | $221K | $1,102K | $3,079K | $6,752K  | $13,016K | $20,860K |
| **Contribution Margin**   | $277K | $1,368K | $3,909K | $8,357K  | $17,028K | $29,208K |
| **CM %**                  | 55.6% | 55.4%   | 55.9%   | 55.3%    | 56.7%    | 58.3%    |
| **Fixed Costs**           | $1,040K | $2,230K | $4,670K | $8,862K  | $15,000K | $23,140K |

### Break-even Analysis

| Metric                   | Y0       | Y1       | Y2       | Y3       | Y4       | Y5       |
| ------------------------ | -------- | -------- | -------- | -------- | -------- | -------- |
| **Break-even Revenue**   | $1,871K  | $4,026K  | $8,354K  | $16,026K | $26,455K | $39,693K |
| **Actual Revenue**       | $498K    | $2,470K  | $6,988K  | $15,109K | $30,044K | $50,068K |
| **Margin of Safety ($)** | -$1,373K | -$1,556K | -$1,366K | -$917K   | $3,589K  | $10,375K |
| **Margin of Safety (%)** | -276%    | -63%     | -20%     | -6%      | 12%      | 21%      |
| **Break-even Achieved?** | NO       | NO       | NO       | NO       | YES      | YES      |

### Operating Leverage

| Metric                           | Y0    | Y1    | Y2    | Y3     | Y4   | Y5       |
| -------------------------------- | ----- | ----- | ----- | ------ | ---- | -------- |
| **Degree of Operating Leverage** | -0.4x | -1.6x | -4.6x | -13.5x | 8.6x | 4.9x     |
| **Interpretation**               | Loss  | Loss  | Loss  | Loss   | High | Moderate |

### Profitability Timeline

| Metric                   | Y0     | Y1     | Y2     | Y3     | Y4      | Y5      |
| ------------------------ | ------ | ------ | ------ | ------ | ------- | ------- |
| **EBITDA**               | -$763K | -$862K | -$761K | -$505K | $2,028K | $6,068K |
| **EBITDA Positive?**     | NO     | NO     | NO     | NO     | YES     | YES     |
| **Net Income**           | -$798K | -$932K | -$901K | -$715K | $1,140K | $3,723K |
| **Net Income Positive?** | NO     | NO     | NO     | NO     | YES     | YES     |

---

## Key Formulas

### Contribution Margin

```
C6 (Contribution Margin) = =C4 - C5
                         = Revenue - Variable Costs
                         = $500K - $220K = $280K

C7 (CM %) = =C6 / C4
          = $280K / $500K = 56.0%
```

### Break-even Revenue

```
C11 (BE Revenue) = =C8 / C7
                 = Fixed Costs / CM%
                 = $930K / 56.0% = $1,661K
```

### Margin of Safety

```
C13 (MOS $) = =C12 - C11
            = Actual Revenue - BE Revenue
            = $500K - $1,661K = -$1,161K

C14 (MOS %) = =C13 / C12
            = MOS$ / Actual Revenue
            = -$1,161K / $500K = -232%
```

### Degree of Operating Leverage

```
C21 (DOL) = =C6 / (C6 - C8)
          = CM / Operating Income
          = $280K / ($280K - $930K)
          = $280K / -$650K = -0.4x
```

### Months to Break-even

```
C15 = =IF(C13<0, "N/A", ROUND(12*(C11/C4)/12, 1))
    = If profitable, calculate months within year
```

---

## Cross-Sheet Linkages

| This Sheet | Links To            | Data              |
| ---------- | ------------------- | ----------------- |
| C4         | Revenue C10         | Total Revenue     |
| C5         | Operating Costs C10 | Total COGS        |
| C8         | Operating Costs C14 | Total Fixed Costs |
| C29        | P&L C25             | EBITDA            |
| C31        | P&L C36             | Net Income        |

---

## Analysis Insights

### Break-even Timeline

| Milestone                   | Year Achieved | Revenue at BE                    |
| --------------------------- | ------------- | -------------------------------- |
| **Contribution Positive**   | Y0            | $0 (always positive with 56% CM) |
| **Cash Flow Break-even**    | Y4            | $26.5M                           |
| **EBITDA Positive**         | Y4            | $30.0M                           |
| **Net Income Positive**     | Y4            | $30.0M                           |
| **Fully Funded Operations** | Y5            | $50.0M                           |

### Operating Leverage Interpretation

| DOL      | Meaning        | Implication                                |
| -------- | -------------- | ------------------------------------------ |
| Negative | Operating loss | Revenue below break-even                   |
| >10x     | Very High      | Small revenue change = large profit change |
| 5-10x    | High           | Significant sensitivity                    |
| 2-5x     | Moderate       | Balanced risk                              |
| <2x      | Low            | Stable, less sensitive                     |

**RapidTools DOL at Y5: 4.9x**

- 10% revenue increase → ~49% EBITDA increase
- Moderate leverage reflecting balanced cost structure

### Margin of Safety Assessment

| MOS %  | Risk Level | Assessment       |
| ------ | ---------- | ---------------- |
| <0%    | Very High  | Below break-even |
| 0-15%  | High       | Thin margin      |
| 15-30% | Moderate   | Acceptable       |
| 30-50% | Low        | Comfortable      |
| >50%   | Very Low   | Very safe        |

**RapidTools at Y5: 21%**

- Revenue could decline 21% before hitting break-even
- Acceptable margin of safety in early profitable years

---

## Sensitivity: Break-even Revenue

| If Fixed Costs | Break-even Revenue (Y5) | MOS% |
| -------------- | ----------------------- | ---- |
| -20% ($18.5M)  | $31.8M                  | 36%  |
| -10% ($20.8M)  | $35.7M                  | 29%  |
| Base ($23.1M)  | $39.7M                  | 21%  |
| +10% ($25.5M)  | $43.7M                  | 13%  |
| +20% ($27.8M)  | $47.6M                  | 5%   |

---

## Formatting Standards

### Section Headers (Rows 3, 10, 20, 24, 28)

- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Break-even Status

- YES: Green background (#C6EFCE)
- NO: Red background (#FFC7CE)

### Margin of Safety

- Positive: Green text
- Negative: Red text

### Contribution Margin Row

- Background: Light Gray (#F2F2F2)
- Font: Bold
