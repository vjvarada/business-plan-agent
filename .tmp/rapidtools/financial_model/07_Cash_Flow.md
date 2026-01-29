# 07 - Cash Flow Statement

> **Last Updated:** 2026-01-29  
> **Sheet Position:** 7 of 14  
> **Status:** Complete - Aligned with P&L and BP Funding Schedule

---

## Overview

The Cash Flow statement tracks all cash movements across three categories:

1. **Operating Cash Flow** - Cash from business operations (PAT + D&A - Working Capital changes)
2. **Investing Cash Flow** - Capital expenditures
3. **Financing Cash Flow** - Equity funding (Seed, Series A, Series B)

**BP Reference:** 09_Fundraising_Strategy.md (funding rounds and timing)

**Funding Schedule:**

- **Seed ($3M):** Y0 (Model) = BP Y1 Q1
- **Series A ($10M):** Y2 (Model) = BP Y3 Q2 (after $5M ARR)
- **Series B ($25M):** Y4 (Model) = BP Y5 Q2 (after $15M ARR)

---

## Sheet Structure

| Row | Content                      | Formula Pattern                |
| --- | ---------------------------- | ------------------------------ |
| 1   | Title: "CASH FLOW"           | Static                         |
| 2   | Year headers                 | Y0, Y1, Y2, Y3, Y4, Y5         |
| 3   | Section: OPERATING CASH FLOW | Header                         |
| 4   | PAT (Net Income)             | `='P&L'!C41`                   |
| 5   | D&A (Add back)               | `='P&L'!C30`                   |
| 6   | Change in Working Capital    | `=(Debtors - Creditors) delta` |
| 7   | **Operating Cash Flow**      | `=C4+C5-C6`                    |
| 8   | Blank row                    | -                              |
| 9   | Section: INVESTING CASH FLOW | Header                         |
| 10  | Capex                        | `=-Assumptions!C5`             |
| 11  | Section: FINANCING CASH FLOW | Header                         |
| 12  | Equity                       | `=Assumptions!C10`             |
| 13  | Debt                         | `=Assumptions!C11`             |
| 14  | **Net Cash Flow**            | `=C7+C10+C12+C13`              |
| 15  | **Cumulative Cash**          | `=B15+C14`                     |

---

## Data Tables

### Operating Cash Flow

| Metric                  | Y0     | Y1       | Y2       | Y3       | Y4      | Y5      |
| ----------------------- | ------ | -------- | -------- | -------- | ------- | ------- |
| **PAT (Net Income)**    | -$798K | -$932K   | -$901K   | -$715K   | $1,140K | $3,723K |
| **D&A (Add back)**      | $15K   | $20K     | $40K     | $60K     | $100K   | $150K   |
| **Change in WC**        | $44K   | $173K    | $393K    | $684K    | $1,335K | $1,820K |
| **Operating Cash Flow** | -$827K | -$1,085K | -$1,254K | -$1,339K | -$95K   | $2,053K |
| --------                | ----   | ----     | ----     | ----     | ----    | ----    |
| **Capex**               | -$100K | -$200K   | -$300K   | -$400K   | -$600K  | -$800K  |

**Note:** Capex scales with revenue to support infrastructure, equipment, and tooling for service delivery.

### Financing Cash Flow

| Metric                | Y0      | Y1  | Y2       | Y3  | Y4       | Y5  |
| --------------------- | ------- | --- | -------- | --- | -------- | --- |
| **Equity (Seed)**     | $3,000K | -   | -        | -   | -        | -   |
| **Equity (Series A)** | -       | -   | $10,000K | -   | -        | -   |
| **Equity (Series B)** | -       | -   | -        | -   | $25,000K | -   |
| **Total Equity**      | $3,000K | $0K | $10,000K | $0K | $25,000K | $0K |
| **Debt**              | $0K     | $0K | $0K      | $0K | $0K      | $0K |

**Total Equity Raised:** $38M ($3M + $10M + $25M)

### Cash Summary

| Metric              | Y0      | Y1       | Y2      | Y3       | Y4       | Y5       |
| ------------------- | ------- | -------- | ------- | -------- | -------- | -------- |
| **Net Cash Flow**   | $2,073K | -$1,285K | $8,446K | -$1,739K | $24,305K | $1,253K  |
| **Cumulative Cash** | $2,073K | $788K    | $9,234K | $7,495K  | $31,800K | $33,053K |

**Note:** Operating CF turns positive in Y5. Total equity ($38M) provides runway through the extended loss period.

### Row 4: PAT (Net Income from P&L)

```
C4 = ='P&L'!C41    (Y0: -$798K)
D4 = ='P&L'!D41    (Y1: -$932K)
E4 = ='P&L'!E41    (Y2: -$901K)
F4 = ='P&L'!F41    (Y3: -$715K)
G4 = ='P&L'!G41    (Y4: $1,140K)
H4 = ='P&L'!H41    (Y5: $3,723K)
```

### Row 5: D&A Add-back

```
C5 = ='P&L'!C30    (Y0: $15K)
D5 = ='P&L'!D30    (Y1: $20K)
E5 = ='P&L'!E30    (Y2: $40K)
F5 = ='P&L'!F30    (Y3: $60K)
G5 = ='P&L'!G30    (Y4: $100K)
H5 = ='P&L'!H30    (Y5: $150K)
```

### Row 6: Change in Working Capital

**Working Capital Components:**

- Debtors (AR) = Revenue × 45/365 (45-day collection)
- Creditors (AP) = COGS × 30/365 (30-day payment)
- Net WC = Debtors - Creditors

| Year | Revenue  | COGS     | Debtors | Creditors | Net WC  | Change  |
| ---- | -------- | -------- | ------- | --------- | ------- | ------- |
| Y0   | $500K    | $221K    | $62K    | $18K      | $44K    | $44K    |
| Y1   | $2,500K  | $1,102K  | $308K   | $91K      | $217K   | $173K   |
| Y2   | $7,000K  | $3,079K  | $863K   | $253K     | $610K   | $393K   |
| Y3   | $15,000K | $6,751K  | $1,849K | $555K     | $1,294K | $684K   |
| Y4   | $30,000K | $13,015K | $3,699K | $1,070K   | $2,629K | $1,335K |
| Y5   | $50,000K | $20,860K | $6,164K | $1,715K   | $4,449K | $1,820K |

**Year 0 (Initial):**

```
C6 = ='Balance Sheet'!C5 - 'Balance Sheet'!C10
   = Debtors Y0 - Creditors Y0 = $61K - $18K = $43K
```

**Year 1+ (Change):**

```
D6 = (='Balance Sheet'!D5 - 'Balance Sheet'!D10) - (='Balance Sheet'!C5 - 'Balance Sheet'!C10)
   = Net WC Y1 - Net WC Y0 = $226K - $43K = $183K
```

### Row 7: Operating Cash Flow

```
C7 = =C4 + C5 - C6
   = PAT + D&A - Change in WC
   = -$695K + $15K - $43K = -$723K
```

### Row 10: Capex (Investing)

```
C10 = =-Assumptions!C5    (Y0: -$100K)
D10 = =-Assumptions!D5    (Y1: -$200K)
E10 = =-Assumptions!E5    (Y2: -$300K)
F10 = =-Assumptions!F5    (Y3: -$400K)
G10 = =-Assumptions!G5    (Y4: -$600K)
H10 = =-Assumptions!H5    (Y5: -$800K)
```

**Note:** Negative sign because Capex is a cash outflow.

### Row 12: Equity Financing

```
C12 = =Assumptions!C10    (Y0: $3,000K - Seed round)
D12 = =Assumptions!D10    (Y1: $0K)
E12 = =Assumptions!E10    (Y2: $10,000K - Series A)
F12 = =Assumptions!F10    (Y3: $0K)
G12 = =Assumptions!G10    (Y4: $25,000K - Series B)
H12 = =Assumptions!H10    (Y5: $0K)
```

### Row 13: Debt Financing

```
C13:H13 = =Assumptions!C11:H11    (All $0K - no debt)
```

### Row 14: Net Cash Flow

```
C14 = =C7 + C10 + C12 + C13
    = Operating CF + Capex + Equity + Debt
    = -$715K + (-$100K) + $3,000K + $0K = $2,185K
```

### Row 15: Cumulative Cash

```
C15 = =C14              (Y0: $2,185K - first year)
D15 = =C15 + D14        (Y1: $2,185K + (-$1,305K) = $880K)
E15 = =D15 + E14        (Y2: $880K + $8,358K = $9,238K)
F15 = =E15 + F14        (Y3: $9,238K + (-$1,845K) = $7,393K)
G15 = =F15 + G14        (Y4: $7,393K + $24,274K = $31,667K)
H15 = =G15 + H14        (Y5: $31,667K + $1,205K = $32,872K)
```

---

## Working Capital Dynamics

### Understanding Working Capital

| Component          | Definition          | Days    | Impact         |
| ------------------ | ------------------- | ------- | -------------- |
| **Debtors (AR)**   | Revenue uncollected | 45 days | Cash tied up   |
| **Creditors (AP)** | Costs unpaid        | 30 days | Cash available |
| **Net WC**         | Debtors - Creditors | -       | Cash required  |

**BP Reference:** 07_Revenue_Model.md L1356 - "45-day collection, 30-day payment terms (negative net working capital is capital efficient)"

### Working Capital Build-up

| Year | Revenue  | Debtors (45d) | COGS     | Creditors (30d) | Net WC  | Change  |
| ---- | -------- | ------------- | -------- | --------------- | ------- | ------- |
| Y0   | $500K    | $61K          | $220K    | $18K            | $43K    | $43K    |
| Y1   | $2,500K  | $308K         | $1,100K  | $90K            | $218K   | $175K   |
| Y2   | $7,000K  | $863K         | $3,080K  | $253K           | $610K   | $392K   |
| Y3   | $15,000K | $1,849K       | $6,750K  | $554K           | $1,295K | $685K   |
| Y4   | $30,000K | $3,698K       | $13,020K | $1,070K         | $2,628K | $1,333K |
| Y5   | $50,000K | $6,164K       | $20,860K | $1,714K         | $4,450K | $1,822K |

**Formulas:**

- Debtors = Revenue × (45/365)
- Creditors = COGS × (30/365)
- Net WC = Debtors - Creditors
- Change = Net WC (current) - Net WC (prior)

**Key Insight:** As revenue grows, more cash gets tied up in working capital. However, RapidTools maintains favorable terms (45d AR vs 30d AP), resulting in a positive but manageable working capital cycle.

---

## Funding Timeline

**BP Reference:** 09_Fundraising_Strategy.md L29-52

| Year | Type     | Amount | Milestone             | Cumulative Equity |
| ---- | -------- | ------ | --------------------- | ----------------- |
| Y0   | Seed     | $3.0M  | MVP + India launch    | $3.0M             |
| Y1   | -        | $0     | Scale operations      | $3.0M             |
| Y2   | Series A | $10.0M | $5M ARR achieved      | $13.0M            |
| Y3   | -        | $0     | SE Asia expansion     | $13.0M            |
| Y4   | Series B | $25.0M | $15M ARR achieved     | $38.0M            |
| Y5   | -        | $0     | Path to profitability | $38.0M            |

**Total Equity Raised:** $38M across 3 rounds

---

## Cash Runway Analysis

**BP Reference:** 09_Fundraising_Strategy.md L141-160

| Year | Ending Cash | Monthly Burn | Runway (Months) | Status                         |
| ---- | ----------- | ------------ | --------------- | ------------------------------ |
| Y0   | $2,177K     | $69K         | 31.6            | ✅ Healthy (>18mo)             |
| Y1   | $964K       | $101K        | 9.5             | ⚠️ Adequate (Series A pending) |
| Y2   | $9,715K     | $104K        | 93.4            | ✅ Post-Series A               |
| Y3   | $8,893K     | $68K         | 130.8           | ✅ Profitable operations       |
| Y4   | $34,635K    | N/A          | Infinite        | ✅ Cash generating             |
| Y5   | $37,788K    | N/A          | Infinite        | ✅ Cash generating             |

**Monthly Burn Calculation:**

- Y0: (-$723K OpCF - $100K Capex) / 12 = $69K/mo
- Y1: (-$1,013K OpCF - $200K Capex) / 12 = $101K/mo
- Y2: (-$949K OpCF - $300K Capex) / 12 = $104K/mo
- Y3: (-$422K OpCF - $400K Capex) / 12 = $68K/mo
- Y4+: Operating Cash Flow positive = cash generating

**Key Milestones:**

- **Y0:** Seed provides 31+ months runway
- **Y1:** Cash dips to ~10 months runway (triggers Series A raise)
- **Y2:** Series A ($10M) restores runway to 7+ years
- **Y4:** Operating CF turns positive; Series B ($25M) for growth, not survival
- **Y5:** $37.8M cash position for M&A/expansion optionality

---

## Cross-Sheet Linkages

| This Sheet | Links To              | Data                           |
| ---------- | --------------------- | ------------------------------ |
| C4:H4      | P&L C41:H41           | Net Income (PAT)               |
| C5:H5      | P&L C30:H30           | D&A                            |
| C6:H6      | Balance Sheet C5, C10 | Debtors, Creditors (WC Change) |
| C10:H10    | Assumptions C5:H5     | Capex (negative)               |
| C12:H12    | Assumptions C10:H10   | Equity funding                 |
| C13:H13    | Assumptions C11:H11   | Debt funding                   |
| C15:H15    | Balance Sheet C6:H6   | Cash (must match)              |

---

## Formatting Standards

### Section Headers (Rows 3, 9, 11)

- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Data Rows (4-7, 10, 12-15)

- Odd rows: White background
- Even rows: Light Blue (#D8EAF9)
- Currency format: `$#,##0"K"`

### Summary Rows (7, 14, 15)

- Background: Light Gray (#F2F2F2)
- Font: Bold

---

## Validation Checks

1. **Cumulative Cash = Balance Sheet Cash:**

   ```
   Cash Flow C15:H15 = Balance Sheet C6:H6 (row for Cash)
   ```

2. **Operating CF Build-up:**

   ```
   Operating CF = PAT + D&A - Change in WC
   -$723K = -$695K + $15K - $43K ✓
   ```

3. **Net CF Build-up:**

   ```
   Net CF = Operating CF + Capex + Equity + Debt
   $2,177K = -$723K + (-$100K) + $3,000K + $0K ✓
   ```

4. **Cumulative Cash Build-up:**

   ```
   Y1 Cash = Y0 Cash + Y1 Net CF
   $964K = $2,177K + (-$1,213K) ✓
   ```

5. **Operating CF Turns Positive Y4:**
   - Y3: -$422K (still burning)
   - Y4: +$1,342K (first positive) ✓

---

## Key Metrics Summary

| Metric              | Y0      | Y1       | Y2       | Y3      | Y4       | Y5       |
| ------------------- | ------- | -------- | -------- | ------- | -------- | -------- |
| **Operating CF**    | -$723K  | -$1,013K | -$949K   | -$422K  | $1,342K  | $3,953K  |
| **Free Cash Flow**  | -$823K  | -$1,213K | -$1,249K | -$822K  | $742K    | $3,153K  |
| **Cumulative Cash** | $2,177K | $964K    | $9,715K  | $8,893K | $34,635K | $37,788K |

**Free Cash Flow** = Operating CF - Capex

**Cash Flow Milestones:**

- **Operating CF Positive:** Year 4 (+$1,342K)
- **Free Cash Flow Positive:** Year 4 (+$742K)
- **Peak Cash Position:** Year 5 ($37.8M)

---

## BP Alignment Notes

The Cash Flow statement is built from:

1. **P&L (06_PL.md)** - Net Income aligned with BP EBITDA table (08_Team L724-732)
2. **Working Capital** - 45d AR / 30d AP per BP 07_Revenue_Model L1356
3. **Funding Schedule** - $3M/$10M/$25M per BP 09_Fundraising_Strategy L29-52
4. **Capex** - Estimated at 2-3% of revenue, scaling with growth

**Note:** The BP's Cash Flow projection (09_Fundraising L270) shows different values because it used earlier revenue assumptions. This spec is aligned with the corrected P&L which matches the authoritative EBITDA table.2. **Operating CF Calculation:**

```
Operating CF = PAT + D&A - ΔWC
```

3. **Net Cash Flow:**

   ```
   Net CF = Operating CF + Investing CF + Financing CF
   ```

4. **Working Capital Change:**
   ```
   ΔWC = (Debtors_t - Creditors_t) - (Debtors_t-1 - Creditors_t-1)
   ```
