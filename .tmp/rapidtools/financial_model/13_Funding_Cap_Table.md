# 13 - Funding & Cap Table

> **Last Updated:** 2026-01-28  
> **Sheet Position:** 13 of 14  
> **Status:** Complete

---

## Overview

The Funding & Cap Table sheet tracks:
1. **Funding Rounds** - Equity and debt raised per year
2. **Round Details** - Valuation and ownership dilution
3. **Cap Table** - Ownership percentages over time
4. **Investor Returns** - Exit values and MOIC

---

## Sheet Structure

| Row | Section | Content |
|-----|---------|---------|
| 1 | Title | FUNDING & CAP TABLE |
| 3-7 | Funding Rounds | Equity/Debt raised, cumulative |
| 9-12 | Round Details | Pre/Post money, dilution |
| 14-19 | Cap Table | Ownership % by stakeholder |
| 21-27 | Investor Returns | Exit values, MOIC |

---

## Data Tables

### Funding Rounds

| Metric | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 |
|--------|----|----|----|----|----|----|
| **Equity Raised** | $2,000K | $0K | $4,000K | $0K | $0K | $0K |
| **Cumulative Equity** | $2,000K | $2,000K | $6,000K | $6,000K | $6,000K | $6,000K |
| **Debt Raised** | $0K | $0K | $0K | $0K | $0K | $0K |
| **Cumulative Debt** | $0K | $0K | $0K | $0K | $0K | $0K |

### Round Details

| Metric | Seed (Y0) | Series A (Y2) |
|--------|-----------|---------------|
| **Pre-money Valuation** | $5,000K | $15,000K |
| **Post-money Valuation** | $7,000K | $19,000K |
| **Round Ownership %** | 28.6% | 21.1% |
| **Amount Raised** | $2,000K | $4,000K |

### Cap Table (Ownership %)

| Stakeholder | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 |
|-------------|----|----|----|----|----|----|
| **Founders** | 71.4% | 71.4% | 56.4% | 56.4% | 56.4% | 56.4% |
| **Seed Investors** | 28.6% | 28.6% | 22.6% | 22.6% | 22.6% | 22.6% |
| **Series A Investors** | 0.0% | 0.0% | 21.1% | 21.1% | 21.1% | 21.1% |
| **Series B Investors** | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Total** | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

### Investor Returns (Conservative - 5x Revenue Exit)

| Metric | Exit Y5 |
|--------|---------|
| **Exit Valuation (5x Rev)** | $250,897K |
| **Seed Investor Return** | $56,593K |
| **Seed MOIC** | 28.3x |
| **Series A Return** | $52,821K |
| **Series A MOIC** | 13.2x |
| **Founder Value** | $141,483K |

---

## Dilution Waterfall

### Seed Round (Y0)

| | Before | After |
|---|--------|-------|
| Founders | 100.0% | 71.4% |
| Seed | 0.0% | 28.6% |
| Total | 100.0% | 100.0% |

**Calculation:**
- Pre-money: $5.0M
- Investment: $2.0M
- Post-money: $7.0M
- Seed Ownership: $2M / $7M = **28.6%**

### Series A (Y2)

| | Before | After |
|---|--------|-------|
| Founders | 71.4% | 56.4% |
| Seed | 28.6% | 22.6% |
| Series A | 0.0% | 21.1% |
| Total | 100.0% | 100.0% |

**Calculation:**
- Pre-money: $15.0M
- Investment: $4.0M
- Post-money: $19.0M
- Series A Ownership: $4M / $19M = **21.1%**
- Dilution Factor: $15M / $19M = 78.9%
- Existing Owners  78.9%

---

## Formula Specifications

### Funding Section
```
C4 (Equity Y0) = =Assumptions!C10
C5 (Cumulative) = =C4
D5 = =C5 + D4
```

### Round Details
```
C10 (Pre-money Seed) = 5000000  (input)
C11 (Post-money) = =C10 + C4
C12 (Round %) = =C4 / C11
```

### Cap Table Calculations
```
C15 (Founders Y0) = =1 - C16  (residual after Seed)
C16 (Seed Y0) = =C12  (Round ownership %)

E15 (Founders Y2) = =D15 * (E10 / E11)  (diluted)
E16 (Seed Y2) = =D16 * (E10 / E11)  (diluted)
E17 (Series A Y2) = =E12  (new round ownership)
```

### Investor Returns
```
C22 (Exit Val) = =Valuation!C31  (5x revenue multiple)
C23 (Seed Return) = =C22 * C16
C24 (Seed MOIC) = =C23 / C4
C25 (Series A Return) = =C22 * C17
C26 (Series A MOIC) = =C25 / E4
C27 (Founder Value) = =C22 * C15
```

---

## Return Scenarios

### At 5x Revenue Exit ($250.9M)

| Stakeholder | Investment | Return | MOIC |
|-------------|------------|--------|------|
| **Founders** | - | $141.5M | - |
| **Seed** | $2.0M | $56.6M | **28.3x** |
| **Series A** | $4.0M | $52.8M | **13.2x** |

### At 7x Revenue Exit ($351.3M)

| Stakeholder | Investment | Return | MOIC |
|-------------|------------|--------|------|
| **Founders** | - | $198.1M | - |
| **Seed** | $2.0M | $79.2M | **39.6x** |
| **Series A** | $4.0M | $73.9M | **18.5x** |

### At 10x Revenue Exit ($501.8M)

| Stakeholder | Investment | Return | MOIC |
|-------------|------------|--------|------|
| **Founders** | - | $283.0M | - |
| **Seed** | $2.0M | $113.2M | **56.6x** |
| **Series A** | $4.0M | $105.6M | **26.4x** |

---

## Implied Valuations

### Step-up Analysis

| Round | Valuation | Multiple of Previous |
|-------|-----------|---------------------|
| Seed (Y0) | $7.0M post | - |
| Series A (Y2) | $19.0M post | **2.7x** step-up |
| Exit (Y5) | $250.9M | **13.2x** step-up |

### Revenue-Based Milestones

| Stage | Revenue | Implied Multiple | Valuation |
|-------|---------|------------------|-----------|
| Seed | $0.5M (Y0) | 14x ARR | $7M |
| Series A | $7M (Y2) | 2.7x ARR | $19M |
| Exit | $50M (Y5) | 5x Revenue | $251M |

---

## Cross-Sheet Linkages

| This Sheet | Links To | Data |
|------------|----------|------|
| C4, E4 | Assumptions C10, E10 | Equity funding |
| C6, etc | Assumptions C11, etc | Debt funding |
| C22 | Valuation C31 | Exit valuation |

---

## Formatting Standards

### Section Headers (Rows 3, 9, 14, 21)
- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Ownership Percentages
- Format: `0.0%`
- Total row: Bold, should always = 100%

### MOIC Values
- Format: `0.0x`
- >20x: Green (#C6EFCE)
- 10-20x: Light Green
- 5-10x: Yellow
- <5x: Light Red

### Funding Cells (Non-zero)
- Background: Light Yellow (#FFFFE6)
- Indicates active funding rounds
