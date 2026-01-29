# 13 - Funding & Cap Table

> **Last Updated:** 2026-01-29  
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
| **Equity Raised** | $3,000K | $0K | $10,000K | $0K | $25,000K | $0K |
| **Cumulative Equity** | $3,000K | $3,000K | $13,000K | $13,000K | $38,000K | $38,000K |
| **Debt Raised** | $0K | $0K | $0K | $0K | $0K | $0K |
| **Cumulative Debt** | $0K | $0K | $0K | $0K | $0K | $0K |

### Round Details

| Metric | Seed (Y0) | Series A (Y2) | Series B (Y4) |
|--------|-----------|---------------|---------------|
| **Pre-money Valuation** | $12,000K | $40,000K | $100,000K |
| **Post-money Valuation** | $15,000K | $50,000K | $125,000K |
| **Round Ownership %** | 20.0% | 20.0% | 20.0% |
| **Amount Raised** | $3,000K | $10,000K | $25,000K |

### Cap Table (Ownership %)

| Stakeholder | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 |
|-------------|----|----|----|----|----|----|
| **Founders** | 80.0% | 80.0% | 64.0% | 64.0% | 51.2% | 51.2% |
| **Seed Investors** | 20.0% | 20.0% | 16.0% | 16.0% | 12.8% | 12.8% |
| **Series A Investors** | 0.0% | 0.0% | 20.0% | 20.0% | 16.0% | 16.0% |
| **Series B Investors** | 0.0% | 0.0% | 0.0% | 0.0% | 20.0% | 20.0% |
| **Total** | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

### Investor Returns (Conservative - 5x Revenue Exit)

| Metric | Exit Y5 |
|--------|---------|
| **Exit Valuation (5x Rev)** | $250,340K |
| **Seed Investor Return** | $32,044K |
| **Seed MOIC** | 10.7x |
| **Series A Return** | $40,054K |
| **Series A MOIC** | 4.0x |
| **Series B Return** | $50,068K |
| **Series B MOIC** | 2.0x |
| **Founder Value** | $128,174K |

---

## Dilution Waterfall

### Seed Round (Y0)

| | Before | After |
|---|--------|-------|
| Founders | 100.0% | 80.0% |
| Seed | 0.0% | 20.0% |
| Total | 100.0% | 100.0% |

**Calculation:**
- Pre-money: $12.0M
- Investment: $3.0M
- Post-money: $15.0M
- Seed Ownership: $3M / $15M = **20.0%**

### Series A (Y2)

| | Before | After |
|---|--------|-------|
| Founders | 80.0% | 64.0% |
| Seed | 20.0% | 16.0% |
| Series A | 0.0% | 20.0% |
| Total | 100.0% | 100.0% |

**Calculation:**
- Pre-money: $40.0M
- Investment: $10.0M
- Post-money: $50.0M
- Series A Ownership: $10M / $50M = **20.0%**
- Dilution Factor: $40M / $50M = 80.0%
- Existing Owners × 80.0%

### Series B (Y4)

| | Before | After |
|---|--------|-------|
| Founders | 64.0% | 51.2% |
| Seed | 16.0% | 12.8% |
| Series A | 20.0% | 16.0% |
| Series B | 0.0% | 20.0% |
| Total | 100.0% | 100.0% |

**Calculation:**
- Pre-money: $100.0M
- Investment: $25.0M
- Post-money: $125.0M
- Series B Ownership: $25M / $125M = **20.0%**
- Dilution Factor: $100M / $125M = 80.0%
- Existing Owners × 80.0%

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

### At 5x Revenue Exit ($250.3M)

| Stakeholder | Investment | Return | MOIC |
|-------------|------------|--------|------|
| **Founders** | - | $128.2M | - |
| **Seed** | $3.0M | $32.0M | **10.7x** |
| **Series A** | $10.0M | $40.1M | **4.0x** |
| **Series B** | $25.0M | $50.1M | **2.0x** |

### At 7x Revenue Exit ($350.5M)

| Stakeholder | Investment | Return | MOIC |
|-------------|------------|--------|------|
| **Founders** | - | $179.5M | - |
| **Seed** | $3.0M | $44.9M | **15.0x** |
| **Series A** | $10.0M | $56.1M | **5.6x** |
| **Series B** | $25.0M | $70.1M | **2.8x** |

### At 10x Revenue Exit ($500.7M)

| Stakeholder | Investment | Return | MOIC |
|-------------|------------|--------|------|
| **Founders** | - | $256.4M | - |
| **Seed** | $3.0M | $64.1M | **21.4x** |
| **Series A** | $10.0M | $80.1M | **8.0x** |
| **Series B** | $25.0M | $100.1M | **4.0x** |

---

## Implied Valuations

### Step-up Analysis

| Round | Valuation | Multiple of Previous |
|-------|-----------|---------------------|
| Seed (Y0) | $15.0M post | - |
| Series A (Y2) | $50.0M post | **3.3x** step-up |
| Series B (Y4) | $125.0M post | **2.5x** step-up |
| Exit (Y5) | $250.3M | **2.0x** step-up |

### Revenue-Based Milestones

| Stage | Revenue | Implied Multiple | Valuation |
|-------|---------|------------------|-----------|
| Seed | $0.5M (Y0) | 30x ARR | $15M |
| Series A | $7M (Y2) | 7.1x ARR | $50M |
| Series B | $30M (Y4) | 4.2x ARR | $125M |
| Exit | $50M (Y5) | 5x Revenue | $250M |

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
