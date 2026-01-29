# 11 - Valuation

> **Last Updated:** 2026-01-28  
> **Sheet Position:** 11 of 14  
> **Status:** Complete

---

## Overview

The Valuation sheet calculates company value using three methods:

1. **DCF Valuation** - Discounted cash flow with terminal value
2. **Revenue Multiple** - EV/Revenue comparables
3. **EBITDA Multiple** - EV/EBITDA comparables

Also includes **Investor Returns** projections at exit.

---

## Sheet Structure

| Row   | Section            | Content                         |
| ----- | ------------------ | ------------------------------- |
| 1     | Title              | COMPANY VALUATION               |
| 3-13  | DCF Valuation      | Terminal value, PV calculations |
| 15-25 | Comparables        | Revenue and EBITDA multiples    |
| 27-31 | Valuation Summary  | Combined view                   |
| 33-43 | Investor Returns   | Ownership and MOIC              |
| 45-49 | Investment Metrics | Total invested, returns         |

---

## DCF Valuation

### Inputs

| Parameter                | Value    | Notes                      |
| ------------------------ | -------- | -------------------------- |
| **Year 5 Revenue**       | $50,179K | From P&L                   |
| **Exit Multiple**        | 5.0x     | Conservative SaaS multiple |
| **Discount Rate**        | 20.0%    | VC expected return         |
| **Discount Factor (Y5)** | 0.4x     | 1/(1+20%)^5                |

### Calculation

| Step                 | Formula               | Value                         |
| -------------------- | --------------------- | ----------------------------- |
| Terminal Value       | Revenue Exit Multiple | $50,179K 5.0x = **$250,897K** |
| PV of Terminal Value | TV Discount Factor    | $250,897K 0.4 = **$100,830K** |
| Year 5 FCF           | From Cash Flow        | **$8,914K**                   |
| PV of Y5 FCF         | FCF Discount Factor   | $8,914K 0.4 = **$3,582K**     |
| **Enterprise Value** | PV of TV + PV of FCF  | **$100,830K**                 |

---

## Comparables Valuation

### Revenue Multiple Method

| Metric                  | Low       | Base      | High      |
| ----------------------- | --------- | --------- | --------- |
| **Year 5 Revenue**      | $50,179K  | $50,179K  | $50,179K  |
| **EV/Revenue Multiple** | 5.0x      | 7.0x      | 10.0x     |
| **Implied Valuation**   | $250,897K | $351,256K | $501,795K |

### EBITDA Multiple Method

| Metric                 | Low      | Base     | High     |
| ---------------------- | -------- | -------- | -------- |
| **Year 5 EBITDA**      | $6,000K  | $6,000K  | $6,000K  |
| **EV/EBITDA Multiple** | 10.0x    | 12.0x    | 15.0x    |
| **Implied Valuation**  | $60,000K | $72,000K | $90,000K |

---

## Valuation Summary

| Method               | Conservative  | Base Case     | Upside        |
| -------------------- | ------------- | ------------- | ------------- |
| **DCF (Terminal)**   | $60,498K      | $100,830K     | $141,162K     |
| **Revenue Multiple** | $250,897K     | $351,256K     | $501,795K     |
| **EBITDA Multiple**  | $60,000K      | $72,000K      | $90,000K      |
| **Average**          | **$123,798K** | **$174,695K** | **$244,319K** |

---

## Investor Returns at Exit

### Ownership at Exit (Post Series A)

| Stakeholder            | Ownership % | Base Case Value |
| ---------------------- | ----------- | --------------- |
| **Founders**           | 56.4%       | $98,528K        |
| **Seed Investors**     | 22.6%       | $39,481K        |
| **Series A Investors** | 21.1%       | $36,855K        |
| **Total**              | 100.0%      | $174,695K       |

### Returns by Round

| Round        | Investment | Base Case Return | MOIC      |
| ------------ | ---------- | ---------------- | --------- |
| **Seed**     | $2,000K    | $39,481K         | **19.7x** |
| **Series A** | $4,000K    | $36,855K         | **9.2x**  |
| **Total**    | $6,000K    | $76,336K         | **12.7x** |

### Return Scenarios

| Scenario         | Exit Valuation | Seed MOIC | Series A MOIC |
| ---------------- | -------------- | --------- | ------------- |
| **Conservative** | $123,798K      | 14.0x     | 6.5x          |
| **Base Case**    | $174,695K      | 19.7x     | 9.2x          |
| **Upside**       | $244,319K      | 27.6x     | 12.9x         |

---

## Formula Specifications

### DCF Section

```
C4 (Y5 Revenue) = =Revenue!H10
C5 (Exit Multiple) = 5
C6 (Terminal Value) = =C4 * C5
C7 (Discount Rate) = 0.20
C8 (Discount Factor) = =1/(1+C7)^5
C9 (PV of TV) = =C6 * C8
C11 (Y5 FCF) = =''Cash Flow''!H7
C12 (PV of FCF) = =C11 * C8
C13 (EV DCF) = =C9
```

### Comparables Section

```
C18 (Y5 Revenue) = =Revenue!H10
C19 (Multiple Low) = 5
D19 (Multiple Base) = 7
E19 (Multiple High) = 10
C20 (Valuation) = =C18 * C19
D20 (Valuation) = =D18 * D19
E20 (Valuation) = =E18 * E19
```

### Investor Returns

```
C34 (Exit Valuation) = =C31  (Average valuation)
C35 (Founder %) = =1 - C36 - C37  (Residual)
C36 (Seed %) = =Assumptions!C10 / (Assumptions!C10 + Assumptions!E10) * 0.438
C37 (Series A %) = =Assumptions!E10 / (Assumptions!C10 + Assumptions!E10) * 0.438

C39 (Founder Value) = =C34 * C35
C40 (Seed Return) = =C34 * C36
C41 (Seed MOIC) = =C40 / ''Funding Cap Table''!C4
C42 (Series A Return) = =C34 * C37
C43 (Series A MOIC) = =C42 / ''Funding Cap Table''!E4
```

---

## Valuation Benchmarks

### SaaS Revenue Multiples (2024)

| Growth Rate | EV/Revenue Multiple |
| ----------- | ------------------- |
| <20%        | 3-5x                |
| 20-40%      | 5-8x                |
| 40-60%      | 8-12x               |
| >60%        | 12-20x              |

**RapidTools at Y5:**

- Growth: 67%
- Multiple Used: 5-10x (Conservative to Upside)
- **Justification:** Hardware component limits pure SaaS multiples

### EBITDA Multiples

| Profitability | EV/EBITDA Multiple |
| ------------- | ------------------ |
| <10% margin   | 8-10x              |
| 10-20% margin | 10-15x             |
| >20% margin   | 15-20x             |

**RapidTools at Y5:**

- EBITDA Margin: 12%
- Multiple Used: 10-15x
- **Justification:** Early profitability with improving margins justifies mid-range multiple

---

## Cross-Sheet Linkages

| This Sheet         | Links To          | Data            |
| ------------------ | ----------------- | --------------- |
| C4                 | Revenue H10       | Y5 Revenue      |
| C11                | Cash Flow H7      | Y5 Operating CF |
| C23                | P&L H25           | Y5 EBITDA       |
| Ownership %        | Funding Cap Table | Equity stakes   |
| Investment amounts | Assumptions       | Funding         |

---

## Formatting Standards

### Section Headers (Rows 3, 15, 27, 33, 45)

- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Valuation Numbers

- Currency: `$#,##0"K"`
- Multiples: `0.0x`
- Percentages: `0.0%`

### Summary Row

- Background: Light Yellow (#FFFFE6)
- Font: Bold

### MOIC Highlighting

- > 50x: Green (#C6EFCE)
- 20-50x: Light Green
- 10-20x: Yellow (#FFFFE6)
- <10x: Light Red (#FFC7CE)
