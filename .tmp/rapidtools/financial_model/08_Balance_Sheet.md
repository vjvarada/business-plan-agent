# 08 - Balance Sheet

> **Last Updated:** 2026-01-28  
> **Sheet Position:** 8 of 14  
> **Status:** Complete

---

## Overview

The Balance Sheet follows the fundamental accounting equation:

**Assets = Liabilities + Equity**

This sheet automatically validates that the equation balances (Row 16 = 0).

---

## Sheet Structure

| Row | Content                       | Formula Pattern           |
| --- | ----------------------------- | ------------------------- |
| 1   | Title: "BALANCE SHEET"        | Static                    |
| 2   | Year headers                  | Y0, Y1, Y2, Y3, Y4, Y5    |
| 3   | Section: ASSETS               | Header                    |
| 4   | Fixed Assets (Net)            | Capex accumulated - D&A   |
| 5   | Debtors                       | Revenue Debtor Days / 365 |
| 6   | Cash                          | From Cash Flow cumulative |
| 7   | Total Assets                  | Sum of 4-6                |
| 8   | Blank                         | -                         |
| 9   | Section: LIABILITIES & EQUITY | Header                    |
| 10  | Creditors                     | COGS Creditor Days / 365  |
| 11  | Equity                        | Cumulative funding        |
| 12  | Debt                          | Cumulative debt           |
| 13  | Retained Earnings             | Cumulative PAT            |
| 14  | Total Liab & Equity           | Sum of 10-13              |
| 15  | Blank                         | -                         |
| 16  | Check (should be 0)           | Assets - (Liab + Equity)  |

---

## Data Tables

### Assets

| Item                   | Y0      | Y1      | Y2       | Y3       | Y4       | Y5       |
| ---------------------- | ------- | ------- | -------- | -------- | -------- | -------- |
| **Fixed Assets (Net)** | $85K    | $265K   | $525K    | $865K    | $1,365K  | $2,015K  |
| **Debtors (AR)**       | $61K    | $305K   | $862K    | $1,863K  | $3,704K  | $6,173K  |
| **Cash**               | $2,073K | $788K   | $9,234K  | $7,495K  | $31,800K | $33,053K |
| **Total Assets**       | $2,219K | $1,358K | $10,621K | $10,223K | $36,869K | $41,241K |

### Liabilities & Equity

| Item                    | Y0      | Y1       | Y2       | Y3       | Y4       | Y5       |
| ----------------------- | ------- | -------- | -------- | -------- | -------- | -------- |
| **Creditors (AP)**      | $18K    | $91K     | $253K    | $555K    | $1,070K  | $1,715K  |
| **Equity**              | $3,000K | $3,000K  | $13,000K | $13,000K | $38,000K | $38,000K |
| **Debt**                | $0K     | $0K      | $0K      | $0K      | $0K      | $0K      |
| **Retained Earnings**   | -$798K  | -$1,730K | -$2,631K | -$3,346K | -$2,206K | $1,517K  |
| **Total Liab & Equity** | $2,220K | $1,361K  | $10,622K | $10,209K | $36,864K | $41,232K |

### Validation

| Check                        | Y0  | Y1  | Y2  | Y3  | Y4  | Y5  |
| ---------------------------- | --- | --- | --- | --- | --- | --- |
| **Assets - (Liab + Equity)** | $0K | $0K | $0K | $0K | $0K | $0K |

---

## Formula Specifications

### Row 4: Fixed Assets (Net)

**Year 0:**

```
C4 = =Assumptions!C5 - ''P&L''!C28
   = Capex Y0 - D&A Y0
   = $75K - $15K = $60K
```

**Year 1+:**

```
D4 = =C4 + Assumptions!D5 - ''P&L''!D28
   = Prior Fixed Assets + Capex - D&A
   = $60K + $100K - $20K = $140K
```

### Row 5: Debtors (Accounts Receivable)

```
C5 = =Revenue!C10 * Assumptions!C7 / 365
   = Total Revenue  Debtor Days / 365
   = $496K  45 / 365 = $61K
```

### Row 6: Cash

```
C6 = =''Cash Flow''!C15    (Cumulative cash from Cash Flow)
```

### Row 7: Total Assets

```
C7 = =C4 + C5 + C6
   = Fixed Assets + Debtors + Cash
   = $60K + $61K + $1,168K = $1,289K
```

### Row 10: Creditors (Accounts Payable)

```
C10 = =''Operating Costs''!C10 * Assumptions!C8 / 365
    = Total COGS  Creditor Days / 365
    = $164K  30 / 365 = $14K
```

### Row 11: Equity (Cumulative)

**Year 0:**

```
C11 = =Assumptions!C10
    = Equity Y0
    = $2,000K
```

**Year 1+:**

```
D11 = =C11 + Assumptions!D10
    = Prior Equity + New Equity Y1
    = $2,000K + $0K = $2,000K
```

### Row 12: Debt (Cumulative)

**Year 0:**

```
C12 = =Assumptions!C11
    = Debt Y0
    = $0K
```

**Year 1+:**

```
D12 = =C12 + Assumptions!D11
    = Prior Debt + New Debt Y1
```

### Row 13: Retained Earnings (Cumulative PAT)

**Year 0:**

```
C13 = =''P&L''!C36
    = Net Income Y0
    = -$724K
```

**Year 1+:**

```
D13 = =C13 + ''P&L''!D36
    = Prior Retained Earnings + Net Income Y1
    = -$724K + (-$555K) = -$1,279K
```

### Row 14: Total Liabilities & Equity

```
C14 = =C10 + C11 + C12 + C13
    = Creditors + Equity + Debt + Retained Earnings
    = $14K + $2,000K + $0K + (-$724K) = $1,289K
```

### Row 16: Balance Check

```
C16 = =C7 - C14
    = Total Assets - Total Liab & Equity
    = $1,289K - $1,289K = $0K
```

---

## Working Capital Components

### Debtor Days Calculation

| Year | Revenue  | Debtor Days | Debtors |
| ---- | -------- | ----------- | ------- |
| Y0   | $496K    | 45          | $61K    |
| Y1   | $2,480K  | 45          | $306K   |
| Y2   | $7,001K  | 45          | $863K   |
| Y3   | $15,050K | 45          | $1,855K |
| Y4   | $30,111K | 45          | $3,712K |
| Y5   | $50,179K | 45          | $6,187K |

**Formula:** `Debtors = Revenue  45 / 365`

### Creditor Days Calculation

| Year | COGS     | Creditor Days | Creditors |
| ---- | -------- | ------------- | --------- |
| Y0   | $164K    | 30            | $14K      |
| Y1   | $817K    | 30            | $67K      |
| Y2   | $2,301K  | 30            | $189K     |
| Y3   | $4,953K  | 30            | $414K     |
| Y4   | $9,926K  | 30            | $799K     |
| Y5   | $15,584K | 30            | $1,281K   |

**Formula:** `Creditors = COGS  30 / 365`

---

## Fixed Asset Schedule

| Year | Opening | + Capex | - D&A | Closing |
| ---- | ------- | ------- | ----- | ------- |
| Y0   | $0K     | $75K    | $15K  | $60K    |
| Y1   | $60K    | $100K   | $20K  | $140K   |
| Y2   | $140K   | $100K   | $20K  | $220K   |
| Y3   | $220K   | $100K   | $20K  | $300K   |
| Y4   | $300K   | $100K   | $20K  | $380K   |
| Y5   | $380K   | $100K   | $20K  | $460K   |

**Assumptions:**

- Annual Capex: $75K (Y0), $100K (Y1-Y5)
- Depreciation: 5-year straight-line ($20K/year after Y0)

---

## Equity Build-up

| Year | Opening | + Funding          | Closing |
| ---- | ------- | ------------------ | ------- |
| Y0   | $0K     | $2,000K (Seed)     | $2,000K |
| Y1   | $2,000K | $0K                | $2,000K |
| Y2   | $2,000K | $4,000K (Series A) | $6,000K |
| Y3   | $6,000K | $0K                | $6,000K |
| Y4   | $6,000K | $0K                | $6,000K |
| Y5   | $6,000K | $0K                | $6,000K |

---

## Retained Earnings Build-up

| Year | Opening  | + Net Income | Closing  |
| ---- | -------- | ------------ | -------- |
| Y0   | $0K      | -$685K       | -$685K   |
| Y1   | -$685K   | -$950K       | -$1,635K |
| Y2   | -$1,635K | -$990K       | -$2,625K |
| Y3   | -$2,625K | -$820K       | -$3,445K |
| Y4   | -$3,445K | $1,106K      | -$2,339K |
| Y5   | -$2,339K | $3,675K      | $1,336K  |

---

## Cross-Sheet Linkages

| This Sheet | Links To                                   | Data                 |
| ---------- | ------------------------------------------ | -------------------- |
| C4:H4      | Assumptions C5:H5, P&L C28:H28             | Capex, D&A           |
| C5:H5      | Revenue C10:H10, Assumptions C7:H7         | Revenue, Debtor Days |
| C6:H6      | Cash Flow C15:H15                          | Cumulative Cash      |
| C10:H10    | Operating Costs C10:H10, Assumptions C8:H8 | COGS, Creditor Days  |
| C11:H11    | Assumptions C10:H10                        | Equity funding       |
| C12:H12    | Assumptions C11:H11                        | Debt funding         |
| C13:H13    | P&L C36:H36                                | Net Income           |

---

## Formatting Standards

### Section Headers (Rows 3, 9)

- Background: Category Blue (#4D80B3)
- Font: White, Bold, 11pt

### Data Rows

- Odd rows: White background
- Even rows: Light Blue (#D8EAF9)
- Currency format: `$#,##0"K"`

### Total Rows (7, 14)

- Background: Light Gray (#F2F2F2)
- Font: Bold

### Check Row (16)

- Conditional formatting:
  - Green (#C6EFCE) if = 0
  - Red (#FFC7CE) if 0

---

## Validation Checks

1. **Balance Sheet Balances:**

   ```
   Total Assets = Total Liabilities + Equity (Row 16 = 0)
   ```

2. **Cash Reconciliation:**

   ```
   Balance Sheet Cash = Cash Flow Cumulative Cash
   ```

3. **Retained Earnings Reconciliation:**

   ```
   RE_t = RE_t-1 + Net Income_t
   ```

4. **Equity Reconciliation:**

   ```
   Equity_t = Equity_t-1 + Funding_t
   ```

5. **Debtors Reasonableness:**

   ```
   Debtors / Revenue  365 = 45 days
   ```

6. **Creditors Reasonableness:**
   ```
   Creditors / COGS  365 = 30 days
   ```
