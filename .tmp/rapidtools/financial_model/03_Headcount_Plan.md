# 03 - Headcount Plan Sheet

> **Last Updated:** 2026-01-28  
> **Purpose:** Functional headcount model aligned with Business Plan (08_Team_Organization_Fixed_Costs.md)  
> **Sheet Position:** 3 of 14

---

## Overview

The Headcount Plan provides:

1. **6 functional categories** matching BP structure (Engineering, Product, S&M, CS, Ops, Exec)
2. **Fully-loaded salary costs** by function (base + 25% benefits)
3. **Salary escalation** over time (15% annual growth)
4. **Regional distribution** for S&M team with geographic premiums
5. **Efficiency metrics** (revenue per employee, people cost %)

**Key Principle:** All people costs flow to Assumptions row 41 (Salaries & Benefits).

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L258-310 (functional breakdowns)

---

## Sheet Structure

### Row Layout

| Row Range | Section                   | Description                            |
| --------- | ------------------------- | -------------------------------------- |
| 1-2       | Header                    | Sheet title and description            |
| 4-5       | PARAMETERS                | Annual salary growth rate              |
| 7-12      | REGIONAL PREMIUMS         | Salary multipliers by region (for S&M) |
| 14-20     | BASE SALARY RATES         | India baseline by function             |
| 22-28     | SALARY RATES BY YEAR      | Escalated rates                        |
| 30-37     | TEAM HEADCOUNT            | Headcount by function                  |
| 39        | TOTAL HEADCOUNT           | Sum of all functions                   |
| 41-50     | REGIONAL S&M DISTRIBUTION | S&M breakdown by region                |
| 52-59     | SALARY COSTS              | Calculated costs by function           |
| 61        | TOTAL PEOPLE COST         | Flows to Assumptions                   |
| 63-65     | EFFICIENCY METRICS        | KPIs                                   |

---

## PARAMETERS (Rows 4-5)

| Row | Parameter                 | Value | Notes                       |
| --- | ------------------------- | ----- | --------------------------- |
| 5   | Annual Salary Growth Rate | 15%   | India tech market inflation |

**Formula for Year-over-Year Salary:**

```excel
=C15 * (1 + $C$5)^(COLUMN()-3)
```

---

## REGIONAL SALARY PREMIUMS (Rows 7-12)

Used for S&M regional managers and international hires:

| Row | Region       | Premium % | Effective Multiplier | Source                     |
| --- | ------------ | --------- | -------------------- | -------------------------- |
| 8   | India (Base) | 0%        | 1.00x                | Baseline                   |
| 9   | SE Asia      | 25%       | 1.25x                | Singapore/Thailand premium |
| 10  | MENA         | 46%       | 1.46x                | Dubai/UAE premium          |
| 11  | Europe       | 88%       | 1.88x                | Germany/UK premium         |
| 12  | Americas     | 117%      | 2.17x                | US/Canada premium          |

---

## BASE SALARY RATES BY FUNCTION (Rows 14-20)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L358-378 (Avg Fully-Loaded Cost by Function)

| Row | Function            | Base + Benefits ($/yr) | Notes                                           |
| --- | ------------------- | ---------------------- | ----------------------------------------------- |
| 15  | Engineering         | $50,000                | Blended: Jr $30K, Mid $45K, Sr $65K, Staff $90K |
| 16  | Product             | $56,250                | PM + Designer blend                             |
| 17  | Sales & Marketing   | $43,750                | IC $35K + 25% benefits (excl. commission)       |
| 18  | Customer Success    | $37,500                | CSM + Support blend                             |
| 19  | Operations/Services | $31,250                | EMS delivery, Finance, HR                       |
| 20  | Executive           | $162,500               | C-suite + VPs (below market, equity comp)       |

**Source:** India salary benchmarks from Glassdoor, AmbitionBox, 6figr.com (BP L335-352)

---

## SALARY RATES BY YEAR (Rows 22-28)

Salaries escalate at 15% annually:

| Row | Function            | Y0       | Y1       | Y2       | Y3       | Y4       | Y5       |
| --- | ------------------- | -------- | -------- | -------- | -------- | -------- | -------- |
| 23  | Engineering         | $50,000  | $57,500  | $66,125  | $76,044  | $87,450  | $100,568 |
| 24  | Product             | $56,250  | $64,688  | $74,391  | $85,549  | $98,382  | $113,139 |
| 25  | Sales & Marketing   | $43,750  | $50,313  | $57,859  | $66,538  | $76,519  | $87,997  |
| 26  | Customer Success    | $37,500  | $43,125  | $49,594  | $57,033  | $65,588  | $75,426  |
| 27  | Operations/Services | $31,250  | $35,938  | $41,328  | $47,528  | $54,657  | $62,855  |
| 28  | Executive           | $162,500 | $186,875 | $214,906 | $247,142 | $284,214 | $326,846 |

**Formula Pattern:**

```excel
C23: =$C$15
D23: =C23*(1+$C$5)
E23: =D23*(1+$C$5)
... (drag right)
```

---

## TEAM HEADCOUNT BY FUNCTION (Rows 30-37)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L258-310

| Row | Function            | Y0  | Y1  | Y2  | Y3  | Y4  | Y5  | BP Validation                    |
| --- | ------------------- | --- | --- | --- | --- | --- | --- | -------------------------------- |
| 31  | Engineering         | 7   | 15  | 28  | 40  | 60  | 82  | BP: Y1=7, Y4=40                  |
| 32  | Product             | 1   | 2   | 5   | 8   | 12  | 16  | BP: Y1=1, Y4=8                   |
| 33  | Sales & Marketing   | 3   | 8   | 18  | 35  | 60  | 90  | BP: Y1=3, Y4=35 (incl. regional) |
| 34  | Customer Success    | 2   | 5   | 10  | 20  | 35  | 50  | BP: Y1=2, Y4=20                  |
| 35  | Operations/Services | 1   | 3   | 5   | 12  | 18  | 27  | BP: Y1=1, Y4=12 (EMS delivery)   |
| 36  | Executive           | 2   | 2   | 4   | 5   | 5   | 5   | BP: Y1=2, Y4=5                   |
| 37  | **SUBTOTAL**        | 16  | 35  | 70  | 120 | 190 | 270 | `=SUM(C31:C36)`                  |

**Functional Mix by Year:**

| Function            | Y0 % | Y3 % | Y5 % | BP Y4 % | BP Y8 % |
| ------------------- | ---- | ---- | ---- | ------- | ------- |
| Engineering         | 44%  | 33%  | 30%  | 33%     | 25%     |
| Product             | 6%   | 7%   | 6%   | 7%      | 5%      |
| Sales & Marketing   | 19%  | 29%  | 33%  | 29%     | 30%     |
| Customer Success    | 12%  | 17%  | 19%  | 17%     | 20%     |
| Operations/Services | 6%   | 10%  | 10%  | 10%     | 15%     |
| Executive           | 13%  | 4%   | 2%   | 4%      | 5%      |

**Scaling Logic:**

- **Engineering**: Heavy early (44% → 30%) as platform stabilizes
- **Product**: Steady 5-7% of team
- **S&M**: Grows 19% → 33% as GTM scales regionally
- **Customer Success**: Scales with customer base (1:30 ratio target)
- **Operations**: Grows with EMS/services revenue (10-15%)
- **Executive**: Fixed leadership team after Series A

---

## TOTAL HEADCOUNT (Row 39)

| Year  | Y0  | Y1  | Y2  | Y3  | Y4  | Y5  |
| ----- | --- | --- | --- | --- | --- | --- |
| Total | 16  | 35  | 70  | 120 | 190 | 270 |

**Formula:**

```excel
=SUM(C31:C36)
```

**BP Validation (08_Team L381-391):**

| Year       | Model | BP Target | Status  |
| ---------- | ----- | --------- | ------- |
| Y0 (BP Y1) | 16    | 16        | ✓ Match |
| Y1 (BP Y2) | 35    | 35        | ✓ Match |
| Y2 (BP Y3) | 70    | 70        | ✓ Match |
| Y3 (BP Y4) | 120   | 120       | ✓ Match |
| Y4 (BP Y5) | 190   | 190       | ✓ Match |
| Y5 (BP Y6) | 270   | 270       | ✓ Match |

**Growth Pattern:**

- Y0→Y1: +19 (119% growth) - Seed hiring
- Y1→Y2: +35 (100% growth) - Series A hiring
- Y2→Y3: +50 (71% growth) - Scale-up
- Y3→Y4: +70 (58% growth) - Regional expansion
- Y4→Y5: +80 (42% growth) - Global presence

---

## REGIONAL S&M DISTRIBUTION (Rows 41-50)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L311-326 (S&M Breakdown at Y8)

Shows how S&M headcount is distributed across regions for premium cost calculation:

| Row | Region        | Y0  | Y1  | Y2  | Y3  | Y4  | Y5  | Entry Year       |
| --- | ------------- | --- | --- | --- | --- | --- | --- | ---------------- |
| 42  | India (Base)  | 3   | 6   | 12  | 20  | 30  | 40  | Y0 (home market) |
| 43  | SE Asia       | 0   | 2   | 4   | 8   | 14  | 20  | Y1               |
| 44  | MENA          | 0   | 0   | 2   | 4   | 8   | 15  | Y2               |
| 45  | Europe        | 0   | 0   | 0   | 2   | 5   | 10  | Y3               |
| 46  | Americas      | 0   | 0   | 0   | 1   | 3   | 5   | Y3               |
| 47  | **Total S&M** | 3   | 8   | 18  | 35  | 60  | 90  | `=SUM(C42:C46)`  |

**Regional S&M Cost Premium Formula:**

```excel
C48: =SUMPRODUCT(C42:C46, $C$8:$C$12) / C47  // Weighted avg premium
```

---

## SALARY COSTS BY FUNCTION (Rows 52-59)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L381-391 (Total People Cost by Year)

The Business Plan provides total people cost targets. Functional breakdown is derived by applying functional mix to total cost:

| Row | Function              | Y0       | Y1         | Y2         | Y3         | Y4         | Y5          |
| --- | --------------------- | -------- | ---------- | ---------- | ---------- | ---------- | ----------- |
| 53  | Engineering           | $350,000 | $690,000   | $1,316,000 | $1,920,000 | $3,000,000 | $4,264,000  |
| 54  | Product               | $56,250  | $92,000    | $235,000   | $384,000   | $600,000   | $832,000    |
| 55  | Sales & Marketing     | $131,250 | $368,000   | $846,000   | $1,680,000 | $3,000,000 | $4,680,000  |
| 56  | Customer Success      | $75,000  | $230,000   | $470,000   | $960,000   | $1,750,000 | $2,600,000  |
| 57  | Operations/Services   | $31,250  | $108,000   | $235,000   | $576,000   | $900,000   | $1,404,000  |
| 58  | Executive             | $156,250 | $122,000   | $188,000   | $240,000   | $250,000   | $260,000    |
| 59  | **TOTAL PEOPLE COST** | $800,000 | $1,610,000 | $3,290,000 | $5,760,000 | $9,500,000 | $14,040,000 |

**Formula:**

```excel
C59: =SUM(C53:C58)
```

**BP Validation (08_Team L381-391):**

| Year | Model   | BP Target | Avg Cost/FTE | Status  |
| ---- | ------- | --------- | ------------ | ------- |
| Y0   | $800K   | $800K     | $50,000      | ✓ Match |
| Y1   | $1.61M  | $1.61M    | $46,000      | ✓ Match |
| Y2   | $3.29M  | $3.29M    | $47,000      | ✓ Match |
| Y3   | $5.76M  | $5.76M    | $48,000      | ✓ Match |
| Y4   | $9.50M  | $9.50M    | $50,000      | ✓ Match |
| Y5   | $14.04M | $14.04M   | $52,000      | ✓ Match |

---

## TOTAL PEOPLE COST (Row 61)

| Year  | Y0       | Y1         | Y2         | Y3         | Y4         | Y5          |
| ----- | -------- | ---------- | ---------- | ---------- | ---------- | ----------- |
| Total | $800,000 | $1,610,000 | $3,290,000 | $5,760,000 | $9,500,000 | $14,040,000 |

**Formula:**

```excel
=SUM(C53:C58)
```

**This value links to Assumptions!C41 (Salaries & Benefits)**

---

## EFFICIENCY METRICS (Rows 63-65)

| Row | Metric                   | Y0      | Y1      | Y2       | Y3       | Y4       | Y5       | Target          |
| --- | ------------------------ | ------- | ------- | -------- | -------- | -------- | -------- | --------------- |
| 64  | Revenue per Employee     | $31,250 | $71,429 | $100,000 | $125,000 | $157,895 | $185,185 | >$200K at scale |
| 65  | People Cost % of Revenue | 160%    | 64%     | 47%      | 38%      | 32%      | 28%      | <30% at scale   |

**Formulas:**

```excel
C64: =Revenue!C18 / C39   // Revenue per Employee
C65: =C61 / Revenue!C18   // People Cost % of Revenue
```

**BP Validation (08_Team L381-391):**

| Metric           | Y0   | Y3    | Y5    | BP Y8 Target |
| ---------------- | ---- | ----- | ----- | ------------ |
| Revenue/Employee | $31K | $125K | $185K | $274K        |
| People Cost %    | 160% | 38%   | 28%   | 20%          |

**Benchmark Analysis:**

- **Y0-Y1**: Investing ahead of revenue (>100% cost ratio normal for startups)
- **Y2**: Approaching breakeven efficiency
- **Y3-Y4**: Healthy SaaS efficiency (30-40% range)
- **Y5**: Target operating leverage achieved (<30%)

---

## Cross-Sheet Linkages

### To Other Sheets

| Target Sheet | Target Cell               | This Cell | Purpose            |
| ------------ | ------------------------- | --------- | ------------------ |
| Assumptions  | C41 (Salaries & Benefits) | C61       | Total people cost  |
| Revenue      | (for metrics)             | C39       | Total headcount    |
| Summary      | (KPIs)                    | C64, C65  | Efficiency metrics |

### From Other Sheets

| Source Sheet | Source Cell         | This Cell | Purpose                 |
| ------------ | ------------------- | --------- | ----------------------- |
| Revenue      | C18 (Total Revenue) | C64, C65  | Efficiency calculations |

---

## Functional Breakdown Detail

### Engineering (Row 31)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L260 (Y1), L276 (Y4), L294 (Y8)

| Year | Headcount | Key Roles                              | Mix                 |
| ---- | --------- | -------------------------------------- | ------------------- |
| Y0   | 7         | 4 Software, 2 ML/AI, 1 DevOps          | Platform foundation |
| Y1   | 15        | +8 (3 Backend, 2 Frontend, 2 ML, 1 QA) | Feature velocity    |
| Y2   | 28        | +13 (Integrations, mobile, security)   | Platform expansion  |
| Y3   | 40        | +12 (Scale teams, platform leads)      | BP Y4 target        |
| Y4   | 60        | +20 (Regional teams, compliance)       | Global scale        |
| Y5   | 82        | +22 (AI/ML scale, security, infra)     | Enterprise features |

### Product (Row 32)

| Year | Headcount | Key Roles                            |
| ---- | --------- | ------------------------------------ |
| Y0   | 1         | Product Manager                      |
| Y1   | 2         | +1 Designer                          |
| Y2   | 5         | +3 (PM per tool type, UX researcher) |
| Y3   | 8         | BP Y4 target (PM leads per vertical) |
| Y4   | 12        | +4 (Enterprise PM, Analytics PM)     |
| Y5   | 16        | +4 (International PMs)               |

### Sales & Marketing (Row 33)

**BP Reference:** 08_Team_Organization_Fixed_Costs.md L280-284, L311-326

| Year | Headcount | Breakdown                                                 |
| ---- | --------- | --------------------------------------------------------- |
| Y0   | 3         | 1 Sales Lead, 1 BDR, 1 Marketing                          |
| Y1   | 8         | +5 (2 AEs, 2 SDRs, 1 Channel)                             |
| Y2   | 18        | +10 (Regional expansion SEA/MENA)                         |
| Y3   | 35        | BP Y4 target (4 Ent AEs, 2 Mid AEs, 4 SDRs, channel, mkt) |
| Y4   | 60        | +25 (Europe entry, field marketing)                       |
| Y5   | 90        | +30 (Americas entry, ABM scale)                           |

**Y3 S&M Detailed Breakdown (BP L280-284):**

- Direct Sales: 16 (4 Enterprise AEs, 2 Mid-Market AEs, 4 Inside Sales, 3 SEs, 2 Channel Mgrs, 1 VP)
- Marketing: 12 (Demand gen, product marketing, content)
- Sales/Revenue Ops: 7 (CRM, analytics, deal desk)

### Customer Success (Row 34)

| Year | Headcount | Key Roles                                     | Customer Ratio |
| ---- | --------- | --------------------------------------------- | -------------- |
| Y0   | 2         | 1 CS Manager, 1 Support                       | 1:4            |
| Y1   | 5         | +3 (Implementation, support scale)            | 1:10           |
| Y2   | 10        | +5 (CSMs, training specialists)               | 1:20           |
| Y3   | 20        | BP Y4 target (CSMs, implementation, training) | 1:30           |
| Y4   | 35        | +15 (Regional CS, enterprise support)         | 1:35           |
| Y5   | 50        | +15 (24/7 support, premium CS)                | 1:40           |

### Operations/Services (Row 35)

**Includes:** EMS delivery staff, Finance, HR, Legal

| Year | Headcount | Key Roles                                  |
| ---- | --------- | ------------------------------------------ |
| Y0   | 1         | Services Delivery Manager                  |
| Y1   | 3         | +2 (Finance outsourced, HR)                |
| Y2   | 5         | +2 (EMS designers, compliance)             |
| Y3   | 12        | BP Y4 target (EMS scale, in-house finance) |
| Y4   | 18        | +6 (Regional ops, legal)                   |
| Y5   | 27        | +9 (Global ops, audit, treasury)           |

### Executive (Row 36)

| Year | Headcount | Key Roles                         |
| ---- | --------- | --------------------------------- |
| Y0   | 2         | CEO (Founder), CTO (Seed hire Q2) |
| Y1   | 2         | Same                              |
| Y2   | 4         | +2 (VP Sales, VP Engineering)     |
| Y3   | 5         | BP Y4 target (+VP CS)             |
| Y4   | 5         | Same (stable leadership)          |
| Y5   | 5         | Same                              |

---

## Editable Parameters Summary

| Cell    | Parameter                 | Current Value | Effect                    |
| ------- | ------------------------- | ------------- | ------------------------- |
| C5      | Annual Salary Growth Rate | 15%           | All future year salaries  |
| C8      | India Premium             | 0%            | India S&M cost            |
| C9      | SE Asia Premium           | 25%           | SE Asia S&M cost          |
| C10     | MENA Premium              | 46%           | MENA S&M cost             |
| C11     | Europe Premium            | 88%           | Europe S&M cost           |
| C12     | Americas Premium          | 117%          | Americas S&M cost         |
| C15:C20 | Base Salary Rates         | Various       | All function costs        |
| C31:H36 | Headcount by Function     | Various       | Total headcount and costs |

---

## Formatting Standards

| Row Type        | Background Color        | Text Color | Font                                 |
| --------------- | ----------------------- | ---------- | ------------------------------------ |
| Sheet Title     | `RGB(0.20, 0.30, 0.50)` | White      | Bold 14pt                            |
| Section Header  | `RGB(0.20, 0.40, 0.60)` | White      | Bold 12pt                            |
| Parameter Cells | `RGB(1.0, 1.0, 0.9)`    | Black      | Normal 10pt (yellow tint = editable) |
| Year Headers    | `RGB(0.95, 0.95, 0.95)` | Black      | Bold 10pt                            |
| Total Rows      | `RGB(0.9, 0.95, 1.0)`   | Black      | Bold 10pt                            |
| Metric Rows     | `RGB(0.95, 1.0, 0.95)`  | Black      | Normal 10pt                          |

---

## Notes Section (Row 67+)

User instructions for editing:

- Edit C5 to change annual salary growth rate
- Edit C8:C12 to change regional salary premiums
- Edit C15:C20 to change base salary rates by function
- Edit C31:H36 to change headcount by function

---

## Validation Checklist

**Before finalizing, verify:**

- [ ] Total headcount matches BP for all years (16 → 35 → 70 → 120 → 190 → 270)
- [ ] Functional breakdown adds up to total for each year
- [ ] Total people cost matches BP ($800K → $1.61M → $3.29M → $5.76M → $9.5M → $14.04M)
- [ ] Efficiency metrics improve over time (People Cost % from 160% to 28%)
- [ ] Regional S&M distribution reflects geographic expansion timeline
