# Executive Summary

> **Last Updated:** 2025-02-17  
> **Project:** Constellation Aerospace  
> **Status:** Draft

---

## 1. Company at a Glance

**Constellation Aerospace** is a Bangalore-based Earth observation (EO) and geospatial analytics company building a constellation of 3U CubeSats with a proprietary payload — custom Cassegrain optics, hyperspectral imager, and Jetson-based edge compute — enabling on-board AI processing, paired with a cloud-native analytics platform. The company follows a hosted-payload-first strategy: flying its proprietary sensor package on commercial buses (initially Dhruva Aerospace P-DoT 3U) to maximize deployment velocity while retaining full payload IP. Constellation delivers real-time, actionable satellite intelligence to defense, agriculture, infrastructure, and environmental monitoring customers, targeting North America (primary), Europe/Japan/Australia (secondary), and India (tertiary).

| Attribute              | Detail                                                                        |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Founded**            | 2026                                                                          |
| **Headquarters**       | Bangalore, India                                                              |
| **Sector**             | Space Technology / Geospatial Analytics                                       |
| **Architecture**       | 3U CubeSat, survey mode (no tasking)                                          |
| **Satellite Bus**      | Dhruva Aerospace OTS 3U ($200K/unit) — hosted payload model                   |
| **Primary Payload**    | Custom Cassegrain telescope + hyperspectral imager + Jetson edge compute      |
| **Constellation (Y7)** | 22 satellites                                                                 |
| **Analytics Platform** | Cloud-native SaaS with ML/AI layers                                           |
| **Target Verticals**   | Defense, Agriculture, Infrastructure, Environmental                           |
| **Geographies**        | North America (primary), Europe/Japan/Australia (secondary), India (tertiary) |
| **Pre-Seed Investor**  | Bluehill Capital ($1.3M secured)                                              |

---

## 2. Market Opportunity

### Why Now?

Over **$100 billion** in government investment is transforming the Earth observation landscape:

- **US CHIPS and Science Act:** $52.7B funding accelerating satellite and sensor technology
- **India PLI Scheme:** $45B for domestic manufacturing and space tech ecosystem
- **EU Space Programme:** EUR 16.9B driving Copernicus expansion and downstream services
- **Defense spending surge:** Global defense EO procurement growing at 12% CAGR

York Space Systems’ S-1 filing cites Allied Market Research: “the global satellite market [is] projected to grow by approximately $320 billion to over $600 billion from 2023 to 2032 at approximately an 8% CAGR.” India’s space economy alone is projected to grow 5× from $8.4B (2022) to $44B by 2033, with 200+ spacetech startups since 2020 and 100% FDI allowed in satellite manufacturing (IBEF).

The mid-market remains underserved: enterprise customers need better-than-Planet resolution at lower-than-Maxar cost, with AI-driven analytics rather than raw imagery. Constellation fills this gap with edge-processed, ready-to-use geospatial intelligence.

### Market Sizing

| Metric       | Value                                   | Source Confidence |
| ------------ | --------------------------------------- | ----------------- |
| **TAM**      | $7.0B (2025), growing to $14.5B by 2032 | HIGH              |
| **SAM**      | $2.6B (NAM $2.25B + India $0.35B)       | HIGH              |
| **SOM (Y7)** | $30.3M (1.17% SAM penetration)          | MEDIUM            |

Market penetration of 1.17% at Year 7 is conservative relative to industry benchmarks (2–5% typical for well-positioned entrants with proven traction — per SaaS/spacetech industry analysis; see Section 02 for full methodology).

> _Detail: Section 01 - Market Drivers, Section 02 - TAM/SAM/SOM_

---

## 3. Product and Technology

### Edge-AI Satellite Architecture (Hosted Payload Model)

The proprietary payload with on-board edge AI is the core technical differentiator. Constellation follows a **hosted-payload-first strategy** — owning only the sensor package while riding on commercial 3U buses (Dhruva P-DoT). This mirrors OroraTech's approach: "Flying as a hosted payload means [you] can deploy [the] constellation with speed, as integration timelines for payloads are much shorter than building an entire sat" (Payload/OroraTech, 2025).

| Component               | Specification                                    | Y0 Cost                   |
| ----------------------- | ------------------------------------------------ | ------------------------- |
| Satellite Bus           | Dhruva Aerospace OTS 3U (P-DoT, 0.5U–12U, TRL 9) | $200K                     |
| Telescope               | Custom Cassegrain (primary payload)              | $500K (development)       |
| Imager                  | Hyperspectral imager                             | Included in telescope NRE |
| On-board Compute        | NVIDIA Jetson carrier board for edge inference   | $20K                      |
| Thermal System          | Passive management for 3U form factor            | $20K                      |
| Integration and Testing | Assembly, qualification, launch prep             | $260K                     |
| **Total Y0 Hardware**   |                                                  | **$1.0M**                 |

**Edge AI advantage:** Processing imagery on-satellite reduces downlink bandwidth by **80–95%**, enabling near-real-time analytics delivery. Competitors downlink raw imagery, requiring hours-to-days of ground processing.

**Survey mode architecture:** All satellites operate in continuous survey mode (no tasking), reducing operational complexity and enabling systematic coverage at lower cost than on-demand tasking systems.

**Hosted payload benefits:** Dhruva may bundle ground station access if using their bus. Constellation retains full payload IP and can switch bus vendors without redesigning the sensor package.

### Constellation Growth

| Phase              | Timeline   | Satellites         | Capability                                                            |
| ------------------ | ---------- | ------------------ | --------------------------------------------------------------------- |
| Prototype          | Y0–Y1      | 0                  | Payload development, ground validation                                |
| Initial            | Y2–Y3      | 2–6                | First imaging, proof of concept                                       |
| Growth             | Y4–Y5      | 12–16              | Daily revisit for key regions                                         |
| Full               | Y6–Y7      | 20–22              | Near-global coverage                                                  |
| **Phase 3+ (Y5+)** | **Y5–Y8+** | **+6U recon sats** | **Tip-and-cue: 3U survey spots changes, 6U recon images at high res** |

**Tip-and-cue (Phase 3+):** Following the OroraTech model ("as many as two-thirds of the company's sensors might operate on partner satellites"), Constellation plans to add 6U reconnaissance satellites for targeted high-resolution imaging triggered by 3U survey detections. This is a Y5+ capability that multiplies the value of the existing constellation without replacing it.

**CapEx advantage:** Total 8-year constellation CapEx of **~$9.8M** vs ~$31.6M for a comparable 6U–16U fleet — a significant CapEx reduction that fundamentally changes the capital efficiency equation.

> _Detail: Section 03 - Technology Architecture_

---

## 4. Business Model

### Three Revenue Streams + Government Overlay

| Stream                     | Description                              | Y7 Mix           |
| -------------------------- | ---------------------------------------- | ---------------- |
| **Platform Subscriptions** | Annual SaaS analytics access             | ~55%             |
| **Data and Imagery Sales** | Processed imagery and datasets           | ~27%             |
| **Professional Services**  | Custom analysis, consulting              | ~8%              |
| **Government Overlay**     | Defense/gov customers across all streams | ~55-66% of total |

### Revenue Trajectory

| Metric       | Y0  | Y1   | Y2   | Y3   | Y4   | Y5   | Y6   | Y7   |
| ------------ | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Revenue ($M) | 0.2 | 1.1  | 3.0  | 6.4  | 11.3 | 16.4 | 22.0 | 30.3 |
| YoY Growth   | --- | 450% | 173% | 113% | 77%  | 45%  | 34%  | 38%  |
| Customers    | 3   | 12   | 23   | 38   | 58   | 81   | 106  | 133  |
| Avg ACV ($K) | 80  | 90   | 100  | 120  | 130  | 145  | 155  | 165  |
| Gross Margin | 45% | 48%  | 60%  | 65%  | 68%  | 72%  | 72%  | 72%  |

### Unit Economics

| Metric      | Y1     | Y3     | Y5     | Y7     |
| ----------- | ------ | ------ | ------ | ------ |
| LTV:CAC     | 4.5x   | 8.6x   | 13.9x  | 15.8x  |
| CAC Payback | 22 mo  | 12 mo  | 9 mo   | 8 mo   |

> _Detail: Section 07 - Revenue Model_

---

## 5. Competitive Positioning

| Factor           | Planet Labs      | BlackSky          | Constellation        |
| ---------------- | ---------------- | ----------------- | -------------------- |
| Revenue (Latest) | $244M            | ~$100M            | $0.2M (Y0)           |
| Architecture     | 200+ Doves, 3U   | 6-8 sats, 55cm    | 3U CubeSats, edge AI |
| Edge Processing  | No (ground only) | No (ground only)  | Yes (on-satellite)   |
| Tasking          | Limited          | Yes               | No (survey mode)     |
| Analytics        | Basic overlays   | Monitoring alerts | Full ML/AI platform  |
| OpEx Base        | San Francisco    | Herndon, VA       | Bangalore, India     |

**Competitive moat:** Edge AI + India cost base + vertically integrated analytics creates a differentiated position that US-based competitors cannot replicate at equivalent unit economics.

> _Detail: Section 04 - Competitive Analysis_

---

## 6. Traction and Customer Validation

Constellation is pre-revenue at plan creation. The validation framework targets:

| Milestone                              | Timeline | Status      |
| -------------------------------------- | -------- | ----------- |
| Cassegrain telescope prototype         | Y0 Q1-Q2 | In progress |
| Analytics MVP with sample imagery      | Y0 Q2-Q3 | In Progress |
| First pilot agreements (3-5 customers) | Y0 Q3-Q4 | Target      |
| First satellite launch                 | Y1       | Target      |
| $1.1M ARR                              | Y1       | Target      |

Target initial customers: Indian defense agencies, agricultural monitoring programs, infrastructure developers, and US commercial EO data consumers.

> _Detail: Section 05 - Customer Validation_

---

## 7. Team and India Cost Advantage

### Headcount Plan

| Department          | Y0     | Y1     | Y3     | Y5     | Y7      |
| ------------------- | ------ | ------ | ------ | ------ | ------- |
| Engineering         | 8      | 9      | 25     | 37     | 47      |
| Operations          | 1      | 3      | 11     | 22     | 35      |
| Sales and Marketing | —      | 4      | 9      | 17     | 24      |
| G&A                 | 5      | 5      | 7      | 10     | 15      |
| **Total**           | **14** | **21** | **52** | **86** | **121** |

### India Cost Advantage

| Metric               | Constellation (India) | US Equivalent ($170K CTC) | Savings |
| -------------------- | --------------------- | ------------------------- | ------- |
| Y0 Team (14 people)  | $171K                 | $2.38M                    | **93%** |
| Y7 Team (121 people) | $3.06M                | $20.57M                   | **85%** |

**Y0 team composition:** 8 FTE (2 co-founders, 2 mechatronics/systems engineers, 1 CV/ML engineer, 1 optics+Jetson PTE, 1 EA+Admin, 1 HR/People Ops) + 6 paid interns = 14 people. Exchange rate: ₹91/$1.

**Y0 budget:** $1.0M CapEx (satellite hardware) + $0.171M headcount + $0.129M operations (including India local travel) = **$1.3M total** (exactly matches Pre-Seed round).

> _Detail: Section 08 - Team, Organization, and Fixed Costs_

---

## 8. Financial Highlights

### Profitability Milestones

| Milestone                     | Year  | Value                                |
| ----------------------------- | ----- | ------------------------------------ |
| EBITDA Positive               | Y2–Y3 | $0.04M (Y2), $1.6M / 25% margin (Y3) |
| Net Income Positive           | Y4    | $1.7M (15% margin)                   |
| Operating CF Positive         | Y3    | $1.4M                                |
| Net CF Positive (after CapEx) | Y4    | $0.17M; Y5 = $4.0M                   |

### Key Financial Metrics (Y7)

| Metric               | Y7 Value               |
| -------------------- | ---------------------- |
| Revenue              | $30.3M                 |
| Gross Margin         | 72%                    |
| EBITDA               | $16.2M (53% margin)    |
| Net Income           | $10.1M (33% margin)    |
| Total OpEx           | $5.6M (19% of revenue) |
| Revenue per Employee | $250K                  |
| Cumulative Cash      | $29.1M                 |
| Satellite CapEx (mfg+launch) | ~$9.8M          |
| Total Equity Raised  | $16.3M                 |

### Capital Efficiency Comparison

| Metric                  | Constellation | US EO Competitor |
| ----------------------- | ------------- | ---------------- |
| Equity Raised           | $16.3M        | $40-60M          |
| Satellite CapEx (mfg+launch) | ~$9.8M   | ~$31.6M          |
| Revenue / Employee (Y7) | $250K         | $150-200K        |
| OpEx / Revenue (Y7)     | 19%           | 40-60%           |

**Cash position:** Cumulative cash remains **positive throughout** the entire projection period. The lowest cash point is $7.6M at Y3 --- a comfortable buffer. Y7 cumulative cash reaches $29.1M.

> _Detail: Section 10 - Financial Projections_

---

## 9. Fundraising Strategy

### Planned Rounds

| Round            | Amount     | Timing | Pre-Money | Dilution | Status                     |
| ---------------- | ---------- | ------ | --------- | -------- | -------------------------- |
| Pre-Seed         | $1.3M      | Y0     | $5M       | ~21%     | Secured (Bluehill Capital) |
| Seed             | $3M        | Y1     | $12-15M   | ~17-20%  | Planned                    |
| Series A         | $12M       | Y3     | $40-55M   | ~21-27%  | Planned                    |
| **Total Equity** | **$16.3M** |        |           |          |                            |

### Use of Funds (Pre-Seed --- $1.3M)

| Category                                     | Amount    | %        |
| -------------------------------------------- | --------- | -------- |
| Satellite Hardware (Cassegrain + Dhruva bus) | $1.0M     | 77%      |
| Headcount (14 people, 12 months)             | $0.169M   | 13%      |
| Operations and Infrastructure                | $0.131M   | 10%      |
| **Total**                                    | **$1.3M** | **100%** |

### Return Profile (MOIC, Pre-Downstream Dilution)

| Exit Scenario | Exit Value | Pre-Seed | Seed   | Series A |
| ------------- | ---------- | -------- | ------ | -------- |
| Conservative  | $150M      | 24x      | 9x     | 2.5-3.0x |
| Base          | $240-250M  | 39-40x   | 14-17x | 4.0-4.8x |
| Aggressive    | $370-500M  | 60-79x   | 22-33x | 6.2-9.3x |

_Note: Exit value ranges reflect two valuation approaches --- DCF/multiples analysis (Section 10: $150-370M) and fundraising narrative (Section 09: $150-500M). Returns are pre-downstream dilution; fully diluted returns after all rounds would be ~35-40% lower._

> _Detail: Section 09 - Fundraising Strategy_

---

## 10. Investment Thesis

1. **$7B market, 1% penetration** --- Constellation targets only $30M of a $7B TAM. Even 50% underperformance yields a viable business at $15M revenue.

2. **3U architecture = fraction of the CapEx** --- satellite CapEx ~$9.8M (mfg + launch) vs $31.6M for larger form factors. Every dollar of equity goes further.

3. **Edge AI is the moat** --- On-satellite processing (80-95% bandwidth reduction) enables real-time analytics that competitors cannot replicate without redesigning their entire constellation.

4. **India cost base is a weapon** --- 85–93% lower team costs (at $170K US benchmark) mean profitability at revenue levels where US competitors are still burning cash. EBITDA positive at just $6.4M revenue (Y3).

5. **Government revenue = stability** --- 55-66% of revenue from defense/government contracts provides predictable, multi-year revenue streams with high switching costs.

6. **Pre-Seed fully allocated, Seed launches the business** --- Bluehill Capital's $1.3M buys a qualified satellite payload + working analytics platform + $0.2M revenue (partial year), all within 12 months. Seed ($3M) funds the first satellite launch and growth.

7. **Hosted payload model = deployment speed** --- By flying on commercial buses (Dhruva P-DoT), Constellation can scale its constellation faster than competitors building proprietary satellites. Per-satellite payload cost of ~$200K after NRE amortization.

8. **Multiple exit pathways at $150-370M+** --- Defense prime acquisition (L3Harris, Northrop Grumman), EO major consolidation (Planet Labs), or IPO.

---

## 11. Key Risks and Mitigations

| #   | Risk                                    | Likelihood | Mitigation                                                                                       |
| --- | --------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------ |
| 1   | Satellite launch failure or delay       | Medium     | Phased 3U builds (low per-unit risk); insurance; "no-satellite" path viable at $14M Y7 revenue   |
| 2   | Cassegrain payload execution            | Medium     | Proven optical design; India manufacturing ecosystem; entire Y0 dedicated to qualification       |
| 3   | Government contract concentration       | Medium     | Diversify across defense/civil/agriculture/commercial; no single customer >20% of revenue        |
| 4   | US market access as India-based company | Low-Medium | ITAR-compliant data handling; US subsidiary for defense contracts; strong partnerships           |
| 5   | CapEx timing vs revenue ramp            | Medium     | 3U per-unit cost ($300-600K) allows pause-and-assess; satellite CapEx ~$9.8M (mfg+launch) within $16.3M equity |

**Downside protection:** Even under a "No Satellites" scenario (analytics platform only, using third-party imagery), the company achieves $14M Y7 revenue with 62% gross margin --- a viable standalone business.

> _Detail: Section 11 - Risk Analysis_

---

## 12. Business Plan Section Index

| #   | Section                 | Status        | Key Takeaway                                              |
| --- | ----------------------- | ------------- | --------------------------------------------------------- |
| 00  | Executive Summary       | This document | Overview of all sections                                  |
| 01  | Market Drivers          | Final         | $100B+ government investment driving EO demand            |
| 02  | TAM/SAM/SOM Calculation | Final         | $7.0B TAM, $2.6B SAM, $30.3M SOM (Y7)                     |
| 03  | Technology Architecture | Final         | 3U CubeSat + edge AI + hosted payload; ~$9.8M sat CapEx   |
| 04  | Competitive Analysis    | Final         | Edge AI + India cost = unique positioning                 |
| 05  | Customer Validation     | Final         | Pre-revenue validation framework                          |
| 06  | Go-To-Market Strategy   | Final         | Defense-first, phased geographic expansion                |
| 07  | Revenue Model           | Final         | 3 streams + gov overlay; $0.2M to $30.3M                  |
| 08  | Team and Costs          | Final         | 14 to 121 people; India 85–93% cost advantage             |
| 09  | Fundraising Strategy    | Final         | $16.3M equity; Pre-Seed secured                           |
| 10  | Financial Projections   | Final         | EBITDA+ Y3; Net income+ Y4; Cash always positive          |
| 11  | Risk Analysis           | Final         | 5 key risks identified with mitigations                   |

---

_This executive summary synthesizes findings from all 11 business plan sections. For detailed analysis, methodology, and source citations, refer to the individual section documents. All financial projections are in USD unless otherwise noted._
