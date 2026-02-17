# Executive Summary

> **Last Updated:** 2025-02-17  
> **Project:** Constellation Aerospace  
> **Status:** Draft

---

## 1. Company at a Glance

**Constellation Aerospace** is a Bangalore-based Earth observation (EO) and geospatial analytics company building a vertically integrated stack: a proprietary constellation of 3U CubeSats with on-board edge-AI processing, paired with a cloud-native analytics platform. The company delivers real-time, actionable satellite intelligence to defense, agriculture, infrastructure, and environmental monitoring customers across North America and India.

| Attribute | Detail |
|-----------|--------|
| **Founded** | 2026 |
| **Headquarters** | Bangalore, India |
| **Sector** | Space Technology / Geospatial Analytics |
| **Architecture** | 3U CubeSat, survey mode (no tasking) |
| **Satellite Bus** | Dhruva Aerospace OTS 3U ($200K/unit) |
| **Primary Payload** | Custom Cassegrain telescope + edge compute |
| **Constellation (Y7)** | 22 satellites |
| **Analytics Platform** | Cloud-native SaaS with ML/AI layers |
| **Target Verticals** | Defense, Agriculture, Infrastructure, Environmental |
| **Geographies** | North America (primary), India (secondary) |
| **Pre-Seed Investor** | Bluehill Capital ($1.3M secured) |

---

## 2. Market Opportunity

### Why Now?

Over **$100 billion** in government investment is transforming the Earth observation landscape:

- **US CHIPS and Science Act:** $52.7B funding accelerating satellite and sensor technology
- **India PLI Scheme:** $45B for domestic manufacturing and space tech ecosystem
- **EU Space Programme:** EUR 16.9B driving Copernicus expansion and downstream services
- **Defense spending surge:** Global defense EO procurement growing at 12% CAGR

The mid-market remains underserved: enterprise customers need better-than-Planet resolution at lower-than-Maxar cost, with AI-driven analytics rather than raw imagery. Constellation fills this gap with edge-processed, ready-to-use geospatial intelligence.

### Market Sizing

| Metric | Value | Source Confidence |
|--------|-------|-------------------|
| **TAM** | $7.0B (2025), growing to $14.5B by 2032 | HIGH |
| **SAM** | $2.6B (NAM $2.25B + India $0.35B) | HIGH |
| **SOM (Y7)** | $30.3M (1.17% SAM penetration) | MEDIUM |

Market penetration of 1.17% at Year 7 is conservative relative to industry benchmarks (2-5% typical for well-positioned entrants with proven traction).

> *Detail: Section 01 - Market Drivers, Section 02 - TAM/SAM/SOM*

---

## 3. Product and Technology

### Edge-AI Satellite Architecture

The 3U CubeSat with on-board edge AI is the core technical differentiator:

| Component | Specification | Y0 Cost |
|-----------|--------------|---------|
| Satellite Bus | Dhruva Aerospace OTS 3U | $200K |
| Telescope | Custom Cassegrain (primary payload) | $500K (development) |
| On-board Compute | AI inference chip for edge processing | $20K |
| Thermal System | Passive management for 3U form factor | $20K |
| Integration and Testing | Assembly, qualification, launch prep | $260K |
| **Total Y0 Hardware** | | **$1.0M** |

**Edge AI advantage:** Processing imagery on-satellite reduces downlink bandwidth by **80-95%**, enabling near-real-time analytics delivery. Competitors downlink raw imagery, requiring hours-to-days of ground processing.

**Survey mode architecture:** All satellites operate in continuous survey mode (no tasking), reducing operational complexity and enabling systematic coverage at lower cost than on-demand tasking systems.

### Constellation Growth

| Phase | Timeline | Satellites | Capability |
|-------|----------|------------|------------|
| Prototype | Y0-Y1 | 0 | Payload development, ground validation |
| Initial | Y2-Y3 | 2-6 | First imaging, proof of concept |
| Growth | Y4-Y5 | 12-16 | Daily revisit for key regions |
| Full | Y6-Y7 | 20-22 | Near-global coverage |

**CapEx advantage:** Total 8-year constellation CapEx of **~$19.5M** vs ~$41M for a comparable 6U-16U fleet --- a **53% CapEx reduction** that fundamentally changes the capital efficiency equation.

> *Detail: Section 03 - Technology Architecture*

---

## 4. Business Model

### Three Revenue Streams + Government Overlay

| Stream | Description | Y7 Mix |
|--------|-------------|--------|
| **Platform Subscriptions** | Annual SaaS analytics access | ~55% |
| **Data and Imagery Sales** | Processed imagery and datasets | ~27% |
| **Professional Services** | Custom analysis, consulting | ~8% |
| **Government Overlay** | Defense/gov customers across all streams | ~55-66% of total |

### Revenue Trajectory

| Metric | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | Y7 |
|--------|-----|-----|-----|-----|-----|-----|-----|-----|
| Revenue ($M) | 0.4 | 1.1 | 3.0 | 6.4 | 11.3 | 16.4 | 22.0 | 30.3 |
| YoY Growth | --- | 175% | 173% | 113% | 77% | 45% | 34% | 38% |
| Customers | 5 | 12 | 23 | 38 | 58 | 81 | 106 | 133 |
| Avg ACV ($K) | 80 | 90 | 100 | 120 | 130 | 145 | 155 | 165 |
| Gross Margin | 45% | 48% | 60% | 65% | 68% | 72% | 72% | 72% |

### Unit Economics

| Metric | Y1 | Y3 | Y5 | Y7 |
|--------|-----|-----|-----|-----|
| LTV:CAC | 4.8x | 9.2x | 17.9x | 23.8x |
| CAC Payback | 8.3 mo | 6.5 mo | 5.6 mo | 5.0 mo |

> *Detail: Section 07 - Revenue Model*

---

## 5. Competitive Positioning

| Factor | Planet Labs | BlackSky | Constellation |
|--------|------------|----------|---------------|
| Revenue (Latest) | $244M | ~$100M | $0.4M (Y0) |
| Architecture | 200+ Doves, 3U | 6-8 sats, 55cm | 3U CubeSats, edge AI |
| Edge Processing | No (ground only) | No (ground only) | Yes (on-satellite) |
| Tasking | Limited | Yes | No (survey mode) |
| Analytics | Basic overlays | Monitoring alerts | Full ML/AI platform |
| OpEx Base | San Francisco | Herndon, VA | Bangalore, India |

**Competitive moat:** Edge AI + India cost base + vertically integrated analytics creates a differentiated position that US-based competitors cannot replicate at equivalent unit economics.

> *Detail: Section 04 - Competitive Analysis*

---

## 6. Traction and Customer Validation

Constellation is pre-revenue at plan creation. The validation framework targets:

| Milestone | Timeline | Status |
|-----------|----------|--------|
| Cassegrain telescope prototype | Y0 Q1-Q2 | In progress |
| Analytics MVP with sample imagery | Y0 Q2-Q3 | Planned |
| First pilot agreements (3-5 customers) | Y0 Q3-Q4 | Target |
| First satellite launch | Y1 | Target |
| $1.1M ARR | Y1 | Target |

Target initial customers: Indian defense agencies, agricultural monitoring programs, infrastructure developers, and US commercial EO data consumers.

> *Detail: Section 05 - Customer Validation*

---

## 7. Team and India Cost Advantage

### Headcount Plan

| Department | Y0 | Y1 | Y3 | Y5 | Y7 |
|------------|-----|-----|-----|-----|-----|
| Engineering | 10 | 12 | 22 | 35 | 46 |
| Operations | 1 | 3 | 12 | 24 | 38 |
| Sales and Marketing | --- | 4 | 10 | 18 | 26 |
| G&A | 3 | 3 | 5 | 7 | 10 |
| Leadership | 1 | --- | 7 | 8 | 10 |
| **Total** | **15** | **22** | **56** | **92** | **130** |

### India Cost Advantage

| Metric | Constellation (India) | US Equivalent | Savings |
|--------|----------------------|---------------|---------|
| Y0 Team (15 people) | $212K | ~$1.3M | **83%** |
| Y7 Team (130 people) | $3.6M | ~$21M | **83%** |

**Y0 team composition:** 10 FTE engineers + 1 Mission Ops analyst + 1 EA + 1 Admin + 1 HR/People Ops + 1 Chief Architect (Founder) = 15 people, supplemented by 5 paid interns.

**Y0 budget:** $1.0M CapEx (satellite hardware) + $0.212M headcount + $0.088M operations = **$1.3M total** (exactly matches Pre-Seed round).

> *Detail: Section 08 - Team, Organization, and Fixed Costs*

---

## 8. Financial Highlights

### Profitability Milestones

| Milestone | Year | Value |
|-----------|------|-------|
| EBITDA Positive | Y3 | $1.4M (22% margin) |
| Net Income Positive | Y4 | $1.5M (13% margin) |
| Operating CF Positive | Y3 | $1.2M |
| Net CF Positive (after CapEx) | ~Y4-Y5 | Y4 approximately break-even; Y5 = $3.9M |

### Key Financial Metrics (Y7)

| Metric | Y7 Value |
|--------|----------|
| Revenue | $30.3M |
| Gross Margin | 72% |
| EBITDA | $15.7M (52% margin) |
| Net Income | $12.2M (40% margin) |
| Total OpEx | $6.1M (20% of revenue) |
| Revenue per Employee | $233K |
| Cumulative Cash | $27.8M |
| Total CapEx (8yr) | ~$19.5M |
| Total Equity Raised | $16.3M |

### Capital Efficiency Comparison

| Metric | Constellation | US EO Competitor |
|--------|--------------|-----------------|
| Equity Raised | $16.3M | $40-60M |
| Total CapEx | ~$19.5M | ~$41M |
| Revenue / Employee (Y7) | $233K | $150-200K |
| OpEx / Revenue (Y7) | 20% | 40-60% |

**Cash position:** Cumulative cash remains **positive throughout** the entire projection period. The lowest cash point is $7.3M at Y3-Y4 --- a comfortable buffer. Y7 cumulative cash reaches $27.8M.

> *Detail: Section 10 - Financial Projections*

---

## 9. Fundraising Strategy

### Planned Rounds

| Round | Amount | Timing | Pre-Money | Dilution | Status |
|-------|--------|--------|-----------|----------|--------|
| Pre-Seed | $1.3M | Y0 | $5M | ~21% | Secured (Bluehill Capital) |
| Seed | $3M | Y1 | $12-15M | ~17-20% | Planned |
| Series A | $12M | Y3 | $40-55M | ~21-27% | Planned |
| **Total Equity** | **$16.3M** | | | | |

### Use of Funds (Pre-Seed --- $1.3M)

| Category | Amount | % |
|----------|--------|---|
| Satellite Hardware (Cassegrain + Dhruva bus) | $1.0M | 77% |
| Headcount (15 people, 12 months) | $0.212M | 16% |
| Operations and Infrastructure | $0.088M | 7% |
| **Total** | **$1.3M** | **100%** |

### Return Profile (MOIC, Pre-Downstream Dilution)

| Exit Scenario | Exit Value | Pre-Seed | Seed | Series A |
|---------------|-----------|----------|------|----------|
| Conservative | $150M | 24x | 9x | 2.5-3.0x |
| Base | $240-250M | 39-40x | 14-17x | 4.0-4.8x |
| Aggressive | $370-500M | 60-79x | 22-33x | 6.2-9.3x |

*Note: Exit value ranges reflect two valuation approaches --- DCF/multiples analysis (Section 10: $150-370M) and fundraising narrative (Section 09: $150-500M). Returns are pre-downstream dilution; fully diluted returns after all rounds would be ~35-40% lower.*

> *Detail: Section 09 - Fundraising Strategy*

---

## 10. Investment Thesis

1. **$7B market, 1% penetration** --- Constellation targets only $30M of a $7B TAM. Even 50% underperformance yields a viable business at $15M revenue.

2. **3U architecture = half the CapEx** --- ~$19.5M total constellation cost vs $41M for larger form factors. Every dollar of equity goes further.

3. **Edge AI is the moat** --- On-satellite processing (80-95% bandwidth reduction) enables real-time analytics that competitors cannot replicate without redesigning their entire constellation.

4. **India cost base is a weapon** --- 83% lower team costs mean profitability at revenue levels where US competitors are still burning cash. EBITDA positive at just $6.4M revenue (Y3).

5. **Government revenue = stability** --- 55-66% of revenue from defense/government contracts provides predictable, multi-year revenue streams with high switching costs.

6. **Pre-Seed fully allocated, Seed launches the business** --- Bluehill Capital's $1.3M buys a qualified satellite payload + working analytics platform + $0.4M revenue, all within 12 months. Seed ($3M) funds the first satellite launch and growth.

7. **Multiple exit pathways at $150-370M+** --- Defense prime acquisition (L3Harris, Northrop Grumman), EO major consolidation (Planet Labs), or IPO.

---

## 11. Key Risks and Mitigations

| # | Risk | Likelihood | Mitigation |
|---|------|-----------|------------|
| 1 | Satellite launch failure or delay | Medium | Phased 3U builds (low per-unit risk); insurance; "no-satellite" path viable at $14M Y7 revenue |
| 2 | Cassegrain payload execution | Medium | Proven optical design; India manufacturing ecosystem; entire Y0 dedicated to qualification |
| 3 | Government contract concentration | Medium | Diversify across defense/civil/agriculture/commercial; no single customer >20% of revenue |
| 4 | US market access as India-based company | Low-Medium | ITAR-compliant data handling; US subsidiary for defense contracts; strong partnerships |
| 5 | CapEx timing vs revenue ramp | Medium | 3U per-unit cost ($300-600K) allows pause-and-assess; ~$19.5M CapEx fully funded by $16.3M equity |

**Downside protection:** Even under a "No Satellites" scenario (analytics platform only, using third-party imagery), the company achieves $14M Y7 revenue with 62% gross margin --- a viable standalone business.

> *Detail: Section 11 - Risk Analysis*

---

## 12. Business Plan Section Index

| # | Section | Status | Key Takeaway |
|---|---------|--------|--------------|
| 00 | Executive Summary | This document | Overview of all sections |
| 01 | Market Drivers | Final | $100B+ government investment driving EO demand |
| 02 | TAM/SAM/SOM Calculation | Final | $7.0B TAM, $2.6B SAM, $30.3M SOM (Y7) |
| 03 | Technology Architecture | Final | 3U CubeSat + edge AI; ~$19.5M total CapEx |
| 04 | Competitive Analysis | Final | Edge AI + India cost = unique positioning |
| 05 | Customer Validation | Final | Pre-revenue validation framework |
| 06 | Go-To-Market Strategy | Final | Defense-first, phased geographic expansion |
| 07 | Revenue Model | Final | 3 streams + gov overlay; $0.4M to $30.3M |
| 08 | Team and Costs | Final | 15 to 130 people; India 83% cost advantage |
| 09 | Fundraising Strategy | Final | $16.3M equity; Pre-Seed secured |
| 10 | Financial Projections | Final | EBITDA+ Y3; Net income+ Y4; Cash always positive |
| 11 | Risk Analysis | Final | 5 key risks identified with mitigations |

---

*This executive summary synthesizes findings from all 11 business plan sections. For detailed analysis, methodology, and source citations, refer to the individual section documents. All financial projections are in USD unless otherwise noted.*
