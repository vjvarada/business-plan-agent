# 11 - Valuation

> **Last Updated:** 2026-01-29  
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
| **Year 5 Revenue**       | $50,068K | From P&L                   |
| **Exit Multiple**        | 5.0x     | Conservative SaaS multiple |
| **Discount Rate**        | 20.0%    | VC expected return         |
| **Discount Factor (Y5)** | 0.4x     | 1/(1+20%)^5                |

### Calculation

| Step                 | Formula               | Value                         |
| -------------------- | --------------------- | ----------------------------- |
| Terminal Value       | Revenue Exit Multiple | $50,068K 5.0x = **$250,340K** |
| PV of Terminal Value | TV Discount Factor    | $250,340K 0.4 = **$100,607K** |
| Year 5 FCF           | From Cash Flow        | **$2,053K**                   |
| PV of Y5 FCF         | FCF Discount Factor   | $2,053K 0.4 = **$825K**       |
| **Enterprise Value** | PV of TV + PV of FCF  | **$100,607K**                 |

---

## Comparables Valuation

### Revenue Multiple Method

| Metric                  | Low       | Base      | High      |
| ----------------------- | --------- | --------- | --------- |
| **Year 5 Revenue**      | $50,068K  | $50,068K  | $50,068K  |
| **EV/Revenue Multiple** | 5.0x      | 7.0x      | 10.0x     |
| **Implied Valuation**   | $250,340K | $350,476K | $500,680K |

### EBITDA Multiple Method

| Metric                 | Low      | Base     | High      |
| ---------------------- | -------- | -------- | --------- |
| **Year 5 EBITDA**      | $6,068K  | $6,068K  | $6,068K   |
| **EV/EBITDA Multiple** | 10.0x    | 12.0x    | 15.0x     |
| **Implied Valuation**  | $60,680K | $72,816K | $91,020K  |

---

## Valuation Summary

| Method               | Conservative  | Base Case     | Upside        |
| -------------------- | ------------- | ------------- | ------------- |
| **DCF (Terminal)**   | $60,364K      | $100,607K     | $140,850K     |
| **Revenue Multiple** | $250,340K     | $350,476K     | $500,680K     |
| **EBITDA Multiple**  | $60,680K      | $72,816K      | $91,020K      |
| **Average**          | **$123,795K** | **$174,633K** | **$244,183K** |

---

## Investor Returns at Exit

### Ownership at Exit (Post Series B)

**BP Reference:** 09_Fundraising_Strategy.md L319-340 (Cap Table Evolution)

| Stakeholder            | Ownership % | Base Case Value |
| ---------------------- | ----------- | --------------- |
| **Founders**           | 40.5%       | $70,727K        |
| **ESOP Pool**          | 4.0%        | $6,985K         |
| **Seed Investors**     | 13.5%       | $23,575K        |
| **Series A Investors** | 17.0%       | $29,687K        |
| **Series B Investors** | 25.0%       | $43,658K        |
| **Total**              | 100.0%      | $174,633K       |

**Note:** BP targets 48% founder ownership post-Series B. The 40.5% here reflects slightly higher dilution per round. ESOP (4%) reserved for key hires.

### Returns by Round

| Round        | Investment | Base Case Return | MOIC      |
| ------------ | ---------- | ---------------- | --------- |
| **Seed**     | $3,000K    | $23,575K         | **7.9x**  |
| **Series A** | $10,000K   | $29,687K         | **3.0x**  |
| **Series B** | $25,000K   | $43,658K         | **1.7x**  |
| **Total**    | $38,000K   | $96,921K         | **2.6x**  |

**Note:** Base case uses average valuation of $174.6M. At strategic exit ($400-600M per BP L466-470), Seed MOIC would be 18-27x.

### Return Scenarios

| Scenario         | Exit Valuation | Seed MOIC | Series A MOIC | Series B MOIC |
| ---------------- | -------------- | --------- | ------------- | ------------- |
| **Conservative** | $123,795K      | 5.6x      | 2.1x          | 1.2x          |
| **Base Case**    | $174,633K      | 7.9x      | 3.0x          | 1.7x          |
| **Upside**       | $244,183K      | 11.0x     | 4.2x          | 2.4x          |
| **Strategic**    | $500,000K      | 22.5x     | 8.5x          | 5.0x          |

**Note:** Strategic exit ($400-600M) is BP's most likely scenario (60% probability per L466). Conservative/Base/Upside reflect model-calculated valuations.

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
