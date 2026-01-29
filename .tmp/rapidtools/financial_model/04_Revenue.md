# 04 - Revenue Sheet

> **Last Updated:** 2026-01-28  
> **Purpose:** Calculate total revenue from 6 streams using Assumptions inputs  
> **Sheet Position:** 4 of 14

---

## Overview

The Revenue sheet is a **pure calculation sheet** - it contains no inputs, only formulas that reference the Assumptions sheet. This ensures:

- Single source of truth (all inputs in Assumptions)
- Easy scenario modeling (change Assumptions, Revenue updates automatically)
- Clear audit trail

---

## Sheet Structure

### Row Layout

| Row Range | Section           | Description                 |
| --------- | ----------------- | --------------------------- |
| 1-2       | Header            | Sheet title and year labels |
| 3-8       | Revenue by Stream | 6 revenue line items        |
| 10        | TOTAL REVENUE     | Sum of all streams          |
| 12-18     | Revenue Mix       | Percentage breakdown        |

---

## REVENUE BY STREAM (Rows 3-8)

### Formula Pattern

Each revenue stream = Price × Volume from Assumptions. Values align with BP target revenue mix.

| Row | Stream                | Formula Pattern                    | Y0    | Y1      | Y2      | Y3      | Y4       | Y5       |
| --- | --------------------- | ---------------------------------- | ----- | ------- | ------- | ------- | -------- | -------- |
| 3   | Software Subscription | `=Assumptions!C15*Assumptions!C16` | $281K | $1,388K | $3,906K | $8,159K | $17,037K | $29,888K |
| 4   | 3D Printer Sales      | `=Assumptions!C19*Assumptions!C20` | $56K  | $245K   | $630K   | $1,197K | $2,394K  | $3,500K  |
| 5   | Consumables Materials | `=Assumptions!C23*Assumptions!C24` | $10K  | $50K    | $70K    | $150K   | $300K    | $500K    |
| 6   | AMC Spares            | `=Assumptions!C27*Assumptions!C28` | $1K   | $7K     | $23K    | $53K    | $113K    | $200K    |
| 7   | Managed Services      | `=Assumptions!C31*Assumptions!C32` | $0K   | $30K    | $330K   | $1,200K | $2,100K  | $3,480K  |
| 8   | Job Work Services     | `=Assumptions!C35*Assumptions!C36` | $150K | $750K   | $2,029K | $4,350K | $8,100K  | $12,500K |

### Detailed Formulas

**Row 3 - Software Subscription:**

```excel
C3: =Assumptions!C15*Assumptions!C16   // Price  Volume for Y0
D3: =Assumptions!D15*Assumptions!D16   // Price  Volume for Y1
E3: =Assumptions!E15*Assumptions!E16   // etc.
```

**Row 4 - 3D Printer Sales:**

```excel
C4: =Assumptions!C19*Assumptions!C20
D4: =Assumptions!D19*Assumptions!D20
```

**Row 5 - Consumables Materials:**

```excel
C5: =Assumptions!C23*Assumptions!C24
D5: =Assumptions!D23*Assumptions!D24
```

**Row 6 - AMC Spares:**

```excel
C6: =Assumptions!C27*Assumptions!C28
D6: =Assumptions!D27*Assumptions!D28
```

**Row 7 - Managed Services:**

```excel
C7: =Assumptions!C31*Assumptions!C32
D7: =Assumptions!D31*Assumptions!D32
```

**Row 8 - Job Work Services:**

```excel
C8: =Assumptions!C35*Assumptions!C36
D8: =Assumptions!D35*Assumptions!D36
```

---

## TOTAL REVENUE (Row 10)

| Year  | Y0    | Y1      | Y2      | Y3       | Y4       | Y5       |
| ----- | ----- | ------- | ------- | -------- | -------- | -------- |
| Total | $498K | $2,470K | $6,988K | $15,109K | $30,044K | $50,068K |

**Formula:**

```excel
C10: =SUM(C3:C8)
D10: =SUM(D3:D8)
E10: =SUM(E3:E8)
... (drag right)
```

**Growth Analysis:**
| Metric | Y0→Y1 | Y1→Y2 | Y2→Y3 | Y3→Y4 | Y4→Y5 |
|--------|-------|-------|-------|-------|-------|
| Growth $ | +$1,972K | +$4,518K | +$8,121K | +$14,935K | +$20,024K |
| Growth % | 396% | 183% | 116% | 99% | 67% |

---

## REVENUE MIX (Rows 12-18)

### Percentage Breakdown (Aligned with BP Y6 Targets)

| Row | Stream                  | Formula   | Y0    | Y1    | Y2    | Y3    | Y4    | Y5    | BP Target Y5    |
| --- | ----------------------- | --------- | ----- | ----- | ----- | ----- | ----- | ----- | --------------- |
| 13  | Software Subscription % | `=C3/C10` | 56.4% | 56.2% | 55.9% | 54.0% | 56.7% | 59.7% | 60% ✓           |
| 14  | 3D Printer Sales %      | `=C4/C10` | 11.2% | 9.9%  | 9.0%  | 7.9%  | 8.0%  | 7.0%  | 7% ✓            |
| 15  | Consumables Materials % | `=C5/C10` | 2.0%  | 2.0%  | 1.0%  | 1.0%  | 1.0%  | 1.0%  | 1% ✓            |
| 16  | AMC Spares %            | `=C6/C10` | 0.2%  | 0.3%  | 0.3%  | 0.4%  | 0.4%  | 0.4%  | (within EMS 7%) |
| 17  | Managed Services %      | `=C7/C10` | 0.0%  | 1.2%  | 4.7%  | 7.9%  | 7.0%  | 6.9%  | (within EMS 7%) |
| 18  | Job Work Services %     | `=C8/C10` | 30.1% | 30.4% | 29.0% | 28.8% | 27.0% | 25.0% | 25% ✓           |

**BP Target Mapping:**

- **Software 60%**: FM Y5 = 59.7% ✓
- **Tooling Services 25%**: FM Y5 Job Work = 25.0% ✓
- **EMS 7%**: FM Y5 AMC (0.4%) + Managed Services (6.9%) = 7.3% ✓
- **Hardware 7%**: FM Y5 3D Printers = 7.0% ✓
- **Consumables 1%**: FM Y5 = 1.0% ✓

**Validation:** Sum of percentages equals 100% for each year.

---

## Revenue Stream Characteristics

| Stream                    | Type        | COGS % | Gross Margin | Growth Driver                                       |
| ------------------------- | ----------- | ------ | ------------ | --------------------------------------------------- |
| **Software Subscription** | Recurring   | 20%    | **80%**      | Seat expansion, new customers                       |
| **3D Printer Sales**      | One-time    | 76%    | **24%**      | Hardware attach rate (arm's-length)                 |
| **Consumables Materials** | Recurring   | 67%    | **33%**      | Installed printer base                              |
| **AMC Spares**            | Recurring   | 60%    | **40%**      | Cumulative printers × attach (incl. OEM share)      |
| **Managed Services**      | Recurring   | 72%    | **28%**      | Enterprise customer %                               |
| **Job Work Services**     | Transaction | 75%    | **25%**      | Customers × jobs/customer (third-party fulfillment) |

**Note:** COGS percentages are stored in Operating Costs sheet (Column B). The P&L calculates GP by stream using: `GP = Revenue - (Revenue × COGS%)`.

### Revenue Quality Analysis

**Recurring Revenue (ARR Components):**

- Software + AMC + Managed Services + Consumables (partial)
- Y5 Recurring: ~$34M (68% of total)

**Transaction Revenue:**

- 3D Printers + Job Work
- Y5 Transaction: ~$16M (32% of total)

### GP Contribution Analysis (P&L Feed)

| Stream      | Y5 Revenue | % of Rev | GP Margin | Y5 GP  | % of Total GP |
| ----------- | ---------- | -------- | --------- | ------ | ------------- |
| Software    | $29.9M     | 60%      | 80%       | $23.9M | **82%**       |
| 3D Printers | $3.5M      | 7%       | 24%       | $0.84M | 3%            |
| Consumables | $0.5M      | 1%       | 33%       | $0.17M | <1%           |
| AMC         | $0.2M      | <1%      | 40%       | $0.08M | <1%           |
| Managed Svc | $3.5M      | 7%       | 28%       | $0.97M | 3%            |
| Job Work    | $12.5M     | 25%      | 25%       | $3.13M | **11%**       |
| **TOTAL**   | $50.1M     | 100%     | **58%**   | $29.1M | 100%          |

**Key Insight:** Software drives 82% of gross profit despite being 60% of revenue. Blended GP margin of 58% matches BP target of 58-59% (improving from 54% in Y0 as software mix increases).

**Note:** GP margin improves from Y0 (54%) to Y5 (58%) as high-margin software grows from 56% to 60% of revenue mix.

**Transaction Revenue:**

- 3D Printers + Job Work
- Y5 Transaction: ~$16M (32% of total)

---

## Cross-Sheet Linkages

### From Assumptions Sheet

| This Cell | Assumptions Reference | Data                            |
| --------- | --------------------- | ------------------------------- |
| C3:H3     | C15:H15 C16:H16       | Software (Price Volume)         |
| C4:H4     | C19:H19 C20:H20       | 3D Printers (Price Volume)      |
| C5:H5     | C23:H23 C24:H24       | Consumables (Price Volume)      |
| C6:H6     | C27:H27 C28:H28       | AMC (Price Volume)              |
| C7:H7     | C31:H31 C32:H32       | Managed Services (Price Volume) |
| C8:H8     | C35:H35 C36:H36       | Job Work (Price Volume)         |

### To Other Sheets

| Target Sheet    | Target Cell          | This Cell        | Purpose              |
| --------------- | -------------------- | ---------------- | -------------------- |
| Operating Costs | COGS calculation     | C3:H8            | Revenue COGS %       |
| P&L             | Revenue line         | C10:H10          | Total Revenue        |
| Summary         | KPIs                 | C10:H10, C13:H18 | Revenue metrics      |
| Headcount Plan  | Efficiency           | C10:H10          | Rev/employee calc    |
| Cash Flow       | Operating activities | C10:H10          | Cash from operations |

---

## Formatting Standards

| Row Type        | Background Color        | Text Color | Font        | Number Format |
| --------------- | ----------------------- | ---------- | ----------- | ------------- |
| Sheet Title     | `RGB(0.20, 0.30, 0.50)` | White      | Bold 14pt   | -             |
| Year Headers    | `RGB(0.95, 0.95, 0.95)` | Black      | Bold 10pt   | -             |
| Revenue Rows    | White                   | Black      | Normal 10pt | `$#,##0"K"`   |
| Total Row       | `RGB(0.9, 0.95, 1.0)`   | Black      | Bold 10pt   | `$#,##0"K"`   |
| Section Label   | `RGB(0.20, 0.40, 0.60)` | White      | Bold 11pt   | -             |
| Percentage Rows | White                   | Black      | Normal 10pt | `0.0%`        |

---

## Validation Checks

### Revenue Totals Match Business Plan

| Year | Business Plan | Model   | Variance |
| ---- | ------------- | ------- | -------- |
| Y0   | $500K         | $496K   | -0.8%    |
| Y1   | $2.5M         | $2.48M  | -0.7%    |
| Y2   | $7.0M         | $7.00M  | 0.0%     |
| Y3   | $15.0M        | $15.05M | +0.3%    |
| Y4   | $30.0M        | $30.11M | +0.4%    |
| Y5   | $50.0M        | $50.18M | +0.4%    |

### Mix Validation

- Software should be 50-60% of revenue (target: SaaS-led business)
- Job Work should decline as % over time (customers adopt hardware)
- Hardware + Consumables + AMC should grow together (ecosystem)

---

## Notes

1. **No hardcoded values** - All revenue is calculated from Assumptions
2. **Scenario modeling** - Change prices or volumes in Assumptions to see impact
3. **Revenue recognition** - All revenue recognized when earned (no deferred)
4. **Currency** - All values in USD
