# Team, Organization & Fixed Costs

> **Last Updated:** 2026-02-17
> **Project:** Constellation Aerospace
> **Status:** Draft (v3 — Y0 budget itemized)

## Executive Summary

Constellation Aerospace operates with **core operations in Bangalore, India**. One co-founder — an Australian passport holder and US green-card holder — maintains a base in the US for direct North American business development, supplemented by travel from India. This India-first approach delivers a **dramatic cost advantage**: a 14-person founding team (8 FTE + 6 interns) costs approximately **₹1.56 Cr ($0.17M) in Y0** — vs $2.38M for an equivalent US-based team at $170K average CTC. The $1.3M pre-seed is allocated as **$1.0M for satellite payload development** (monolithic Cassegrain telescope + Dhruva 3U bus integration) and **$0.3M for people + operations**.

The Y0 team is **payload-engineering focused**: 2 FTE + 1 PTE engineer work on the Cassegrain telescope, imager integration, and Jetson carrier board, with a CV/ML engineer building the analytics platform in parallel. The organization grows from **14 people (Y0) to ~121 (Y7)**, with headcount cost scaling from **$0.17M to $3.1M**. Total fixed operating costs (headcount + non-headcount) reach **$5.4M by Y7**, supporting **$30.3M in revenue** and yielding a **revenue-per-employee of ~$250K**.

---

## 1. Organization Structure

### 1.1 Founding Team (Y0 — 14 People, Bangalore)

| Role                           | Count  | Department           | Annual CTC (₹ LPA) | USD Cost   |
| ------------------------------ | ------ | -------------------- | ------------------ | ---------- |
| Chief Architect / Co-Founder   | 1      | Executive            | ₹30L               | $33K       |
| Chief Operations / Co-Founder  | 1      | Executive            | ₹30L               | $33K       |
| Mechatronics / System Engineer | 2      | Payload Engineering  | ₹15L each          | $33K total |
| CV/ML Engineer                 | 1      | Software Engineering | ₹15L               | $16K       |
| Optics + Jetson Engineer (PTE) | 1      | Payload Engineering  | ₹12L               | $13K       |
| EA + Admin                     | 1      | G&A                  | ₹14L               | $15K       |
| HR / People Ops                | 1      | G&A                  | ₹10L               | $11K       |
| Interns (cross-functional)     | 6      | Engineering / Ops    | ₹2.5L each         | $16K total |
| **Total Y0**                   | **14** |                      | **₹1.56 Cr**       | **$171K**  |

> **CTC = Cost to Company** (Indian standard), including base salary, PF, gratuity, and variable pay. USD at ₹91 = $1.
> **Y0 team is payload-focused:** 2 FTE Mechatronics/System engineers + 1 PTE Optics/Jetson engineer are dedicated to the Cassegrain telescope + imager + Jetson carrier board build. The CV/ML engineer builds the analytics platform in parallel using third-party imagery. 6 interns (5–7 range) support across engineering and operations.

### 1.2 Y0 Pre-Seed Budget Allocation ($1.3M)

| Category                         | Amount      | Details                                                                             |
| -------------------------------- | ----------- | ----------------------------------------------------------------------------------- |
| **Optics & Imaging Systems**     | **$500K**   | Monolithic Cassegrain telescope: OTS optics, R&D, machinery, outsourced fabrication |
| **3U Satellite Bus (OTS)**       | **$200K**   | Off-the-shelf bus from Dhruva Aerospace; Constellation integrates own payload       |
| **Compute & Electronics**        | **$20K**    | Edge compute, sensors, power electronics                                            |
| **Thermal Management**           | **$20K**    | Thermal design, development, testing, materials                                     |
| **Integration, Testing & Other** | **$260K**   | Assembly, environmental testing, GSE, ADCS, comms subsystems                        |
| **Subtotal — Hardware/CapEx**    | **$1,000K** | Payload qualification + bus integration (no launch in Y0)                           |
|                                  |             |                                                                                     |
| **People / HR**                  | **$171K**   | 14-person team (see Section 1.1 above)                                              |
| **Operations & Overhead**        | **$129K**   | Office, cloud, legal, travel, insurance, tools, India local transport (see Sec 3.1) |
| **Subtotal — OpEx**              | **$300K**   |                                                                                     |
|                                  |             |                                                                                     |
| **Total Pre-Seed**               | **$1,300K** | Fully allocated; no unallocated buffer                                              |

> **Note:** The $1M hardware budget is dedicated to building and qualifying the satellite payload (Cassegrain telescope + imager + Jetson carrier board, integrated with Dhruva 3U bus). No satellite launch in Y0 — first launch target is Y1. The CV/ML Engineer uses this year to build the initial analytics platform using third-party data, generating $0.2M Y0 revenue (partial year, 3 paying clients) with minimal COGS. India local travel (Uber commute, lab visits at ~₹2,000/day) is included in Operations & Overhead.

> **Hardware contingency:** The $500K optics budget follows a dual-path strategy: primary development of the custom monolithic Cassegrain telescope, with a commercial off-the-shelf (COTS) telescope assembly as a fallback within the same budget. If custom optics development exceeds budget or schedule, the team can pivot to a COTS unit ($50–100K), allocating the remaining funds to payload integration and testing. This ensures the Y0 hardware milestone is met within the $1.0M CapEx envelope regardless of the optical path chosen. Custom optics development resumes in subsequent satellite builds if needed.

### 1.3 Headcount Growth Plan

| Department             | Y0     | Y1     | Y2     | Y3     | Y4     | Y5     | Y6      | Y7      |
| ---------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------- | ------- |
| **Engineering**        | 8      | 9      | 18     | 25     | 33     | 37     | 42      | 47      |
| - Software             | 2      | 5      | 8      | 11     | 15     | 17     | 19      | 21      |
| - Satellite/Hardware   | 5      | 3      | 7      | 9      | 12     | 14     | 16      | 18      |
| - ML/AI                | 1      | 1      | 3      | 5      | 6      | 6      | 7       | 8       |
| **Sales & Marketing**  | —      | 4      | 7      | 9      | 13     | 17     | 21      | 24      |
| - Sales/BD             | —      | 3      | 6      | 8      | 11     | 14     | 18      | 21      |
| - Marketing            | —      | 1      | 1      | 1      | 2      | 3      | 3       | 3       |
| **Operations**         | 1      | 3      | 7      | 11     | 17     | 22     | 28      | 35      |
| - Satellite Operations | —      | 1      | 4      | 7      | 10     | 14     | 18      | 22      |
| - Customer Success     | —      | 1      | 1      | 2      | 4      | 5      | 6       | 8       |
| - Data Operations      | 1      | 1      | 2      | 2      | 3      | 3      | 4       | 5       |
| **G&A**                | 5      | 5      | 3      | 7      | 7      | 10     | 12      | 15      |
| - Executive/Founders   | 2      | 2      | 2      | 3      | 3      | 3      | 3       | 3       |
| - Finance/Legal        | —      | 1      | 1      | 2      | 2      | 4      | 5       | 7       |
| - HR/Admin/EA          | 3      | 2      | —      | 2      | 2      | 3      | 4       | 5       |
| **Total Headcount**    | **14** | **21** | **35** | **52** | **70** | **86** | **103** | **121** |

> **Y0 includes 6 interns** distributed across Satellite/Hardware (2), Software (1), ML/AI (1), Data Ops (1), and HR/Admin (1). Interns are short-term roles supporting payload development and platform bootstrapping. From Y0→Y1: interns depart (−6) but 13 FTE hires join, netting +7 to reach 21. **HR/Admin/EA** drops from 3→2 (intern leaves; EA+Admin + HR continue as FTEs). **Satellite/Hardware** drops from 5→3 (2 interns leave; PTE Optics/Jetson transitions as payload completes CAD phase); hardware ramps again from Y2 with constellation manufacturing. Software hiring accelerates from Y1 as the platform becomes the growth priority.

---

## 2. Compensation Structure (Indian Market)

### 2.1 Salary Bands — Bangalore Tech Market

| Department      | Role               | Y0 CTC (₹ LPA) | Y3 CTC (₹ LPA) | Y7 CTC (₹ LPA) | Notes                   |
| --------------- | ------------------ | -------------- | -------------- | -------------- | ----------------------- |
| **Engineering** | Junior Engineer    | ₹8–12L         | ₹10–14L        | ₹12–18L        | Fresh–2yr exp           |
|                 | Mid Engineer       | ₹14–20L        | ₹16–24L        | ₹20–30L        | 3–5yr exp               |
|                 | Senior Engineer    | ₹22–35L        | ₹25–40L        | ₹30–50L        | 6+ yr exp               |
|                 | ML/AI Engineer     | ₹18–30L        | ₹22–35L        | ₹28–45L        | Premium for AI talent   |
|                 | Satellite Engineer | ₹15–25L        | ₹18–30L        | ₹22–38L        | Aerospace-specific      |
|                 | VP Engineering     | ₹28–40L        | ₹35–50L        | ₹45–65L        | Leadership              |
| **Sales**       | BD Executive       | ₹8–15L         | ₹10–18L        | ₹14–22L        | India-based BD          |
|                 | BD Manager         | ₹18–28L        | ₹22–35L        | ₹28–42L        | Defense/gov focus       |
|                 | VP Sales           | ₹25–40L        | ₹30–50L        | ₹40–60L        | Founder-level initially |
| **Operations**  | Sat Ops Technician | ₹6–12L         | ₹8–15L         | ₹10–18L        | 24/7 rotation           |
|                 | Customer Success   | ₹8–15L         | ₹10–18L        | ₹14–22L        |                         |
|                 | Data Ops Analyst   | ₹6–12L         | ₹8–15L         | ₹10–18L        |                         |
| **G&A**         | Finance Manager    | ₹12–20L        | ₹15–25L        | ₹20–35L        |                         |
|                 | HR Manager         | ₹8–15L         | ₹10–18L        | ₹14–25L        |                         |
|                 | Admin/Office       | ₹4–8L          | ₹5–10L         | ₹6–12L         |                         |
| **Executive**   | CEO/CTO            | ₹25–30L        | ₹40L           | ₹60–80L        | Below market (equity)   |

### 2.2 Average CTC by Department

| Department           | Y0 Avg (₹ LPA) | Y0 Avg (USD) | Y3 Avg (₹ LPA) | Y3 Avg (USD) | Y7 Avg (₹ LPA) | Y7 Avg (USD) |
| -------------------- | -------------- | ------------ | -------------- | ------------ | -------------- | ------------ |
| Engineering (FTE)    | ₹14L           | $15K         | ₹22L           | $24K         | ₹30L           | $33K         |
| Sales & Marketing    | —              | —            | ₹20L           | $22K         | ₹25L           | $27K         |
| Operations           | —              | —            | ₹12L           | $13K         | ₹15L           | $16K         |
| G&A (incl. Founders) | ₹21L           | $23K         | ₹15L           | $16K         | ₹18L           | $20K         |
| Interns              | ₹2.5L          | $3K          | —              | —            | —              | —            |
| **Blended Average**  | **₹11L**       | **$12K**     | **₹19L**       | **$21K**     | **₹23L**       | **$25K**     |

> Y0 blended average is lower than Y1+ because 6 interns (₹2.5L each) pull the average down. FTE-only average is ₹18L ($19K).

### 2.3 Total Headcount Cost

**CTC in India includes PF, gratuity, and employer contributions (~20% statutory loading).**

| Year                     | Y0         | Y1         | Y2         | Y3         | Y4         | Y5         | Y6         | Y7         |
| ------------------------ | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Headcount                | 14         | 21         | 35         | 52         | 70         | 86         | 103        | 121        |
| Avg CTC (₹ LPA)          | ₹11L       | ₹17L       | ₹18L       | ₹19L       | ₹20L       | ₹21L       | ₹22L       | ₹23L       |
| Total CTC (₹ Cr)         | ₹1.56 Cr   | ₹3.6 Cr    | ₹6.3 Cr    | ₹9.9 Cr    | ₹14.0 Cr   | ₹18.1 Cr   | ₹22.7 Cr   | ₹27.8 Cr   |
| **Total CTC (USD)**      | **$0.17M** | **$0.39M** | **$0.69M** | **$1.09M** | **$1.54M** | **$1.98M** | **$2.49M** | **$3.06M** |
| US Equivalent Cost       | $2.38M     | $3.57M     | $5.95M     | $8.84M     | $11.90M    | $14.62M    | $17.51M    | $20.57M    |
| **India Cost Advantage** | **93%**    | **89%**    | **88%**    | **88%**    | **87%**    | **86%**    | **86%**    | **85%**    |

> **India operations cost ~85–93% less than US equivalent** at comparable headcount (1:1 comparison at $170K average US CTC). This is Constellation's structural cost advantage. Y0 advantage is 93%: $171K India vs $2.38M US for the same 14-person team. The advantage narrows slightly at scale as India salaries inflate faster than US rates, but remains above 85% through Y7.

---

## 3. Fixed Operating Costs (Non-Headcount)

### 3.1 Fixed Cost Categories (India-Optimized)

| Category                  | Y0       | Y1        | Y2         | Y3         | Y5         | Y7         | Notes                                               |
| ------------------------- | -------- | --------- | ---------- | ---------- | ---------- | ---------- | --------------------------------------------------- |
| **Office (Bangalore)**    | $12K     | $30K      | $50K       | $80K       | $120K      | $180K      | Coworking own space                                 |
| **Cloud Infrastructure**  | $8K      | $120K     | $250K      | $400K      | $600K      | $800K      | Minimal Y0; scales with platform                    |
| **Ground Station Ops**    | —        | $30K      | $100K      | $200K      | $350K      | $450K      | AWS GS + KSAT; Dhruva may bundle if using their bus |
| **Insurance**             | $3K      | $25K      | $50K       | $80K       | $120K      | $150K      | Basic D&O Y0; expands with launches                 |
| **Legal & Regulatory**    | $15K     | $60K      | $100K      | $150K      | $200K      | $250K      | IP filings, basic ITAR consult Y0                   |
| **US Travel (BD)**        | $18K     | $100K     | $150K      | $180K      | $200K      | $200K      | 3–4 trips Y0; ramps with BD activity                |
| **India Local Travel**    | $5K      | $10K      | $15K       | $20K       | $25K       | $30K       | Uber commute, lab visits (~₹2,000/day)              |
| **Marketing Programs**    | $3K      | $40K      | $80K       | $120K      | $200K      | $250K      | Website + basic presence Y0                         |
| **Software & Tools**      | $8K      | $40K      | $60K       | $80K       | $120K      | $150K      | SaaS licenses                                       |
| **R&D Consumables**       | $6K      | $80K      | $150K      | $100K      | $50K       | —          | Bench supplies (separate from $1M CapEx)            |
| **India Statutory Costs** | $5K      | $15K      | $25K       | $35K       | $50K       | $60K       | GST compliance, RoC filings                         |
| **Contingency**           | $8K      | $20K      | $30K       | $30K       | $40K       | $40K       |                                                     |
| **Total Fixed Costs**     | **$91K** | **$570K** | **$1.07M** | **$1.48M** | **$2.08M** | **$2.56M** |                                                     |

> **Y0 fixed costs are deliberately lean ($91K)** because the pre-seed is concentrated on hardware/payload development ($1M). Cloud, travel, insurance, and marketing are kept minimal since Y0 is an R&D/build year. India local travel (₹2,000/day Uber commute) is a minor but recurring cost. Ground station access via Dhruva Space may be bundled if using their P-DoT bus, reducing Y1+ ground station costs (vs. standalone KSAT/AWS). Costs ramp sharply in Y1 as the platform launches, BD travel increases, and ground station operations begin.

### 3.2 US Travel Budget Detail

Founders will handle North American BD through regular travel. One co-founder (Australian passport + US green-card holder) maintains a US base for direct client engagement:

| Purpose                                    | Y0 (Pre-Seed)        | Y1+ (Growth Phase)            |
| ------------------------------------------ | -------------------- | ----------------------------- |
| Defense BD meetings (DC, Colorado Springs) | 1–2 trips, $8K       | 6–8 trips/yr, $50K            |
| Industry conferences (GEOINT, SmallSat)    | 1 conference, $5K    | 4–6/yr, $35K                  |
| Customer site visits                       | —                    | 6–10/yr, $40K                 |
| Investor meetings                          | 1 trip, $5K          | 4–6/yr, $25K                  |
| **Total**                                  | **$18K (3–4 trips)** | **$100K–$200K (20–40 trips)** |

> Y0 travel is minimal — founders are heads-down on payload build. BD activity ramps dramatically from Y1 when the platform and first data products are ready for demonstration.

---

## 4. Total Operating Cost Summary

| Component                   | Y0         | Y1         | Y2         | Y3         | Y5         | Y7         |
| --------------------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Headcount Cost (India)      | $0.17M     | $0.39M     | $0.69M     | $1.09M     | $1.98M     | $3.06M     |
| Fixed Costs                 | $0.09M     | $0.57M     | $1.07M     | $1.48M     | $2.08M     | $2.56M     |
| **Total OpEx (excl. COGS)** | **$0.26M** | **$0.96M** | **$1.76M** | **$2.57M** | **$4.06M** | **$5.62M** |
| Revenue                     | $0.2M      | $1.1M      | $3.0M      | $6.4M      | $16.4M     | $30.3M     |
| **OpEx / Revenue**          | 130%       | 87%        | 59%        | 40%        | 25%        | 19%        |

> Y0 OpEx / Revenue of 130% reflects partial-year revenue recognition — only $0.2M in revenue against $0.26M OpEx. Most of the $1.3M pre-seed goes to hardware CapEx ($1.0M), not operating expenses. OpEx is only 19% of revenue by Y7. Note: the pre-seed budget allocates $300K to operations (including ~$40K in one-time setup costs not in the recurring fixed cost table).

### 4.1 Including COGS and CapEx

| Category                          | Y0          | Y1          | Y2          | Y3          | Y5          | Y7          |
| --------------------------------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| OpEx (above)                      | $0.26M      | $0.96M      | $1.76M      | $2.57M      | $4.06M      | $5.62M      |
| COGS (data procurement + sat ops) | $0.11M      | $0.57M      | $1.20M      | $2.24M      | $4.59M      | $8.48M      |
| CapEx (payload dev + sat mfg)     | $1.00M      | $1.85M      | $3.00M      | $3.50M      | $2.50M      | $1.70M      |
| **Total Cash Required**           | **$1.37M**  | **$3.38M**  | **$5.96M**  | **$8.31M**  | **$11.15M** | **$15.80M** |
| Revenue                           | $0.2M       | $1.1M       | $3.0M       | $6.4M       | $16.4M      | $30.3M      |
| **Net Cash Flow**                 | **-$1.17M** | **-$2.28M** | **-$2.96M** | **-$1.91M** | **$5.25M**  | **$14.50M** |

> **Cash flow turns positive in Y4** on an annual basis. Y0 CapEx of $1.0M is the monolithic Cassegrain telescope build + Dhruva 3U bus procurement. Total satellite-specific CapEx (mfg + launch) of ~$9.8M over 8 years vs ~$31.6M for a 6U–16U fleet.

---

## 5. Efficiency Metrics

### 5.1 Revenue per Employee

| Metric                | Y0   | Y1   | Y3    | Y5    | Y7    | Benchmark            |
| --------------------- | ---- | ---- | ----- | ----- | ----- | -------------------- |
| Revenue / Employee    | $14K | $52K | $123K | $191K | $250K | Planet Labs ~$270K   |
| Cost/Employee (India) | $12K | $19K | $21K  | $23K  | $25K  | US ~$170K            |
| Revenue/Cost Multiple | 1.2  | 2.7  | 5.9   | 8.3   | 10.0  | Exceptional leverage |

**Revenue-per-employee of $250K at Y7** approaches Planet Labs' benchmark, but at **85% lower cost per employee** — this is the India cost arbitrage in action. Y0 cost/employee is especially low ($12K) due to intern-heavy team composition (6 of 14).

### 5.2 Cost Efficiency vs US Competitor

| Y7 Metric        | Constellation (India) | US Competitor (equivalent) | Advantage   |
| ---------------- | --------------------- | -------------------------- | ----------- |
| 121 employees    | $3.06M headcount      | $20.57M headcount          | 85% savings |
| Fixed costs      | $2.56M                | $6.50M                     | 61% savings |
| Total OpEx       | $5.62M                | $27.07M                    | 79% savings |
| Operating margin | 81%                   | 11%                        | 70pp better |

---

## 6. Key Insights

- **India-based operations are the structural cost moat** — 93% cheaper than US equivalent at Y0, maintaining 85% advantage at scale (1:1 headcount comparison at $170K US CTC)
- **Pre-seed of $1.3M is tightly allocated:** $1.0M hardware/CapEx (Cassegrain telescope + Dhruva 3U bus) + $0.17M HR (14-person payload-focused team: 8 FTE + 6 interns) + $0.13M operations (including India local travel) — zero slack
- **Y0 is an R&D/build year:** 2 FTE + 1 PTE focus on the Cassegrain optics, hyperspectral imager, and Jetson carrier board; platform generates $0.2M from third-party data resale (partial year, 3 clients) with just 2 software engineers
- **Cash flow turns positive Y4** — the 3U architecture keeps total CapEx at ~$9.8M vs ~$31.6M for 6U–16U, preserving cash throughout
- **121 people by Y7** supports $30.3M revenue at only $5.6M total OpEx (19% of revenue) — SaaS-like operating leverage
- **US travel budget of $18K (Y0) $200K (Y7)** is the primary non-India cost — one co-founder (Australian passport + US green-card holder) maintains a US base for BD

---

## 7. Cross-Section Alignment

| Metric                       | Previous Sections    | This Section                   | Aligned? |
| ---------------------------- | -------------------- | ------------------------------ | -------- |
| Y7 Revenue (Sec 07)          | $30.3M               | $30.3M (for efficiency calcs)  | ✅       |
| Pre-seed amount (Sec 09)     | $1.3M                | $1.3M (fully allocated in 1.2) | ✅       |
| Y0 CapEx allocation (Sec 03) | $1.0M                | $1.0M (payload + bus)          | ✅       |
| 3U Sat Bus source (Sec 03)   | Dhruva Aerospace OTS | $200K Dhruva bus               | ✅       |
| Y0 OpEx                      | $0.26M (Sec 10)      | $0.26M                         | ✅       |

> ✅ **Cascade complete (v4):** Updated headcount (14→121), costs at ₹91/$, US benchmark at $170K CTC. Sections 03 and 10 may need minor updates to reflect $0.26M OpEx (vs prior $0.30M). Fixed costs updated with India local travel and Dhruva ground station note.

---

## 8. Investment Implications

1. **India cost base is a competitive weapon** — Constellation runs a 14-person team for $171K (Y0), scaling to 121 people for $3.06M (Y7), vs $20.57M for a US competitor at $170K average CTC. That’s 85–93% structural savings.
2. **Pre-seed of $1.3M is fully allocated** with zero slack — $1M goes directly into Cassegrain telescope + Dhruva 3U bus, $0.30M covers lean operations (including $171K headcount for 8 FTE + 6 interns) for 12 months
3. **Y0 is an R&D year by design** — the team builds the payload (Cassegrain + imager + Jetson carrier board) and bootstraps the platform; first satellite launch is a Y1 milestone funded by the Seed round
4. **Tightly scoped Y0 reduces pre-seed risk** — Bluehill's $1.3M buys a qualified satellite payload, a working analytics platform, and $0.2M in revenue (partial year), all within 12 months
5. **Per-satellite payload cost of ~$200K** (after amortizing NRE) gives Constellation a 3–5× cost advantage on constellation scaling vs competitors building proprietary buses
6. **Cash flow positive by ~Y4–Y5** means Series A may be the last equity round needed (Series B optional for acceleration)
7. **Founder-led BD** from a US base (one co-founder holds Australian passport + US green card) keeps customer access high while maintaining India cost structure

---

## References & Sources

This section relies on:

- Glassdoor India / Levels India for Bangalore tech compensation benchmarks
- CoWorkIndia for Bangalore coworking/office costs ($800–1,200/desk/month)
- AWS pricing for cloud infrastructure (global pricing applies)
- KSAT / AWS Ground Station pricing for satellite operations
- Dhruva Aerospace catalog pricing for 3U satellite bus ($200K OTS)
- Internal projections aligned with Sections 02, 03, 06, and 07
- Pre-seed term sheet from Bluehill Capital ($1.3M)
