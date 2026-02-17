# Revenue Model

> **Last Updated:** 2026-07-10
> **Project:** Constellation Aerospace
> **Status:** Draft

## Executive Summary

Constellation Aerospace generates revenue through **three complementary streams**: (1) Platform Subscriptions — recurring analytics SaaS at $80K–175K ACV, (2) Data & Imagery Sales — archive imagery and continuous monitoring feeds on a consumption basis, and (3) Professional Services — custom analytics projects and consulting engagements. A fourth revenue category, **Government Contracts**, spans all three streams but is tracked separately due to its distinct procurement and billing structure.

Total revenue grows from **$0.4M in Y0 to $30.3M in Y7**, driven by customer acquisition (5 133 total clients), ACV expansion ($80K $165K), and the transition from third-party data resale (~40% gross margin) to own-constellation data (~80% gross margin) starting in Y2–Y3. Unit economics reach maturity by Y5 with **LTV:CAC >4.0 and CAC payback <14 months**.

---

## 1. Revenue Stream Architecture

### 1.1 Three Streams + Government Overlay

```
PLATFORM SUBSCRIPTIONS (Recurring)
   Analytics SaaS (monitoring, dashboards, alerts, API)
   55–60% of total revenue at maturity

DATA & IMAGERY SALES (Consumption + Recurring)
   Archive access (pay-per-image)
   Continuous monitoring feeds (scheduled collection along orbit)
   Third-party tasking resale (Phase 1 middleman only)
   25–30% of total revenue at maturity

PROFESSIONAL SERVICES (Project-Based)
   Custom analytics development
   Consulting and implementation
   10–15% of total revenue at maturity

GOVERNMENT CONTRACTS (Cross-Stream)
   IDIQ, SBIR, OTA vehicles
   May include platform + data + services bundled
   Tracked as separate revenue line
```

### 1.2 Revenue Mix Evolution

| Stream                      | Y0  | Y1  | Y2  | Y3  | Y5  | Y7  |
| --------------------------- | --- | --- | --- | --- | --- | --- |
| Platform Subscriptions      | 50% | 45% | 40% | 42% | 50% | 55% |
| Data & Imagery Sales        | 10% | 15% | 25% | 30% | 28% | 27% |
| Professional Services       | 40% | 30% | 20% | 13% | 10% | 8%  |
| Government (included above) | 20% | 30% | 45% | 55% | 60% | 55% |

> **Note:** Government revenue is an overlay — it flows through Platform, Data, and Services streams. In Y3–Y5, government contracts dominate as defense IDIQ vehicles ramp; by Y7, commercial revenue catches up through agricultural and energy verticals.

---

## 2. Pricing Strategy

### 2.1 Platform Subscription Tiers

| Tier             | ACV            | Target Customer                         | Features                                                    |
| ---------------- | -------------- | --------------------------------------- | ----------------------------------------------------------- |
| **Starter**      | $5K–$20K/yr    | Researchers, NGOs, small firms          | Limited AOIs, standard imagery, basic analytics             |
| **Professional** | $50K–$120K/yr  | Mid-market (agriculture co-ops, energy) | 10+ AOIs, change detection, custom alerts, API              |
| **Enterprise**   | $120K–$300K/yr | Large enterprise, government agencies   | Unlimited AOIs, priority monitoring, SLA, dedicated support |
| **Defense/Gov**  | $200K–$2M+/yr  | Defense, intelligence community         | Classified capabilities, on-prem option, bespoke analytics  |

**Blended ACV trajectory:**

| Year    | Y0   | Y1   | Y2    | Y3    | Y4    | Y5    | Y6    | Y7    |
| ------- | ---- | ---- | ----- | ----- | ----- | ----- | ----- | ----- |
| Avg ACV | $80K | $90K | $100K | $120K | $130K | $145K | $155K | $165K |

ACV expansion driven by: (1) customer migration to Enterprise tier, (2) data product upsell when own constellation comes online, (3) adding monitored AOIs over time.

### 2.2 Data & Imagery Pricing

| Product                                     | Pricing Model        | Price Range        | Margin |
| ------------------------------------------- | -------------------- | ------------------ | ------ |
| **Archive Imagery** (3rd-party)             | Per-image or area    | $5–$50/km²         | ~40%   |
| **Archive Imagery** (own constellation)     | Per-image or area    | $2–$20/km²         | ~80%   |
| **Third-Party Tasking** (Phase 1 middleman) | Per-collection       | $500–$5,000/task   | ~30%   |
| **Monitoring Feed** (own constellation)     | Monthly subscription | $1K–$10K/month/AOI | ~80%   |
| **Monitoring Feed** (3rd-party blend)       | Monthly subscription | $2K–$15K/month/AOI | ~50%   |

> **Note:** Constellation's own 3U satellites operate in survey mode (fixed ground track, no agile tasking). Revenue from own data comes through archive imagery and continuous monitoring feeds. Third-party tasking is offered as a middleman service during Phase 1 (Y0–Y2) only, using partners like BlackSky and Maxar.

> **Key insight:** Own-constellation data has 2 the margin of resold data. This is the fundamental economic driver for building the satellite fleet.

### 2.3 Professional Services Pricing

| Service                      | Pricing      | Typical Engagement                    |
| ---------------------------- | ------------ | ------------------------------------- |
| Custom Analytics Development | $150K–$500K  | 3–6 months; build bespoke models      |
| Implementation / Integration | $50K–$150K   | 1–3 months; connect to client systems |
| Consulting                   | $200–$350/hr | Ad-hoc advisory, data interpretation  |
| Training                     | $5K–$15K     | 1–3 day workshops                     |

---

## 3. Revenue Build-Up (8-Year Model)

### 3.1 Revenue by Stream

| Stream                           | Y0        | Y1        | Y2        | Y3        | Y4         | Y5         | Y7         |
| -------------------------------- | --------- | --------- | --------- | --------- | ---------- | ---------- | ---------- |
| Platform Subscriptions           | $0.2M     | $0.5M     | $0.9M     | $1.9M     | $3.9M      | $5.9M      | $8.3M      |
| Data & Imagery                   | $0.05M    | $0.2M     | $0.6M     | $1.4M     | $2.1M      | $3.3M      | $5.1M      |
| Professional Services            | $0.15M    | $0.3M     | $0.5M     | $0.6M     | $0.8M      | $1.2M      | $1.2M      |
| Government Contracts (IDIQ/SBIR) | —         | $0.1M     | $1.0M     | $2.5M     | $4.5M      | $6.0M      | $8.0M      |
| Gov. overlay via streams¹        | —         | —         | —         | —         | —          | —          | $7.7M      |
| **Total Revenue**                | **$0.4M** | **$1.1M** | **$3.0M** | **$6.4M** | **$11.3M** | **$16.4M** | **$30.3M** |

> ¹ As government share grows from ~27% (Y1) to ~66% (Y7), an increasing volume of government spend flows through Platform/Data/Services contracts rather than separate IDIQ vehicles. At Y0–Y5, the IDIQ line captures substantially all incremental government revenue (totals match Table 3.2). By Y7, $7.7M of additional government revenue is embedded in the three stream lines above. **Table 3.2 below is the authoritative Commercial vs Government split.**

### 3.2 Alternative View — Total Revenue with Overlap Removed

| Year                   | Y0        | Y1        | Y2        | Y3        | Y4         | Y5         | Y6         | Y7         |
| ---------------------- | --------- | --------- | --------- | --------- | ---------- | ---------- | ---------- | ---------- |
| **Commercial Revenue** | $0.4M     | $0.8M     | $1.2M     | $2.2M     | $3.8M      | $5.8M      | $8.2M      | $10.3M     |
| **Government Revenue** | —         | $0.3M     | $1.8M     | $4.2M     | $7.5M      | $10.6M     | $13.8M     | $20.0M     |
| **Total Revenue**      | **$0.4M** | **$1.1M** | **$3.0M** | **$6.4M** | **$11.3M** | **$16.4M** | **$22.0M** | **$30.3M** |

### 3.3 Revenue Growth Rates

| Year        | Y0Y1 | Y1Y2 | Y2Y3 | Y3Y4 | Y4Y5 | Y5Y6 | Y6Y7 |
| ----------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Growth Rate | 175% | 173% | 113% | 77%  | 45%  | 34%  | 38%  |

> **Growth deceleration** is natural: from startup hypergrowth (>100%) to sustainable scale (30–40%). By Y6–Y7, growth is driven by constellation capacity expansion and India market ramp. B2B SaaS median growth rate is ~25% [[1]](#ref-1) — Constellation exceeds this through Y7 due to multi-vector growth (new geos + new data products + new verticals).

---

## 4. Unit Economics

### 4.1 Customer Acquisition

| Metric              | Y0    | Y1    | Y3    | Y5   | Y7   | Notes                                                    |
| ------------------- | ----- | ----- | ----- | ---- | ---- | -------------------------------------------------------- |
| Blended CAC         | $80K  | $75K  | $65K  | $55K | $50K | Declines with brand + inbound growth                     |
| Enterprise CAC      | $120K | $110K | $100K | $90K | $80K | Long sales cycles, dedicated reps                        |
| SMB/Self-Serve CAC  | $5K   | $5K   | $4K   | $3K  | $3K  | Product-led growth, minimal touch                        |
| New Customers/Year  | 5     | 8     | 18    | 30   | 40   | Per Section 02 SOM build                                 |
| Churn Rate (Annual) | 10%   | 12%   | 12%   | 10%  | 10%  | Enterprise retention improves [[2]](#ref-2)[[3]](#ref-3) |

### 4.2 Lifetime Value

| Metric               | Y1      | Y3      | Y5     | Y7     | Benchmark                |
| -------------------- | ------- | ------- | ------ | ------ | ------------------------ |
| Average ACV          | $90K    | $120K   | $145K  | $165K  | —                        |
| Gross Margin         | 48%     | 60%     | 68%    | 72%    | Improves with own data   |
| Customer Lifetime    | 8.3 yrs | 8.3 yrs | 10 yrs | 10 yrs | =1/churn                 |
| LTV (Gross Margin)   | $358K   | $598K   | $986K  | $1.19M | —                        |
| LTV:CAC Ratio        | 4.8     | 9.2     | 17.9   | 23.8   | >3 healthy [[2]](#ref-2) |
| CAC Payback (months) | 20      | 13      | 9      | 7      | <18 months target        |

> **LTV:CAC** appears exceptionally strong from Y3+ because own-constellation data dramatically improves gross margins while CAC decreases with brand maturity. Planet Labs' economics validate this pattern — once satellites are operational, incremental data revenue has minimal COGS.

### 4.3 Gross Margin Breakdown

| Revenue Source            | COGS Components                        | Gross Margin |
| ------------------------- | -------------------------------------- | ------------ |
| Platform Subscriptions    | Cloud hosting, ML compute, support     | 75–85%       |
| Data — Own Constellation  | Satellite ops, ground station, storage | 75–85%       |
| Data — Third-Party Resale | Data procurement, processing           | 35–45%       |
| Professional Services     | Personnel, tools                       | 45–55%       |
| **Blended (Y0)**          | Heavy 3rd-party data reliance          | **~45%**     |
| **Blended (Y7)**          | Own data dominant                      | **~72%**     |

**The margin transformation story:**

- Y0–Y2: Blended ~45–55% (reselling third-party data)
- Y3–Y4: Blended ~60–65% (own satellites begin contributing)
- Y5–Y7: Blended ~68–72% (own data dominates, SaaS scales)

---

## 5. Revenue Model Assumptions

### 5.1 Key Assumptions Register

| Assumption             | Value     | Source/Basis                                                                   | Confidence |
| ---------------------- | --------- | ------------------------------------------------------------------------------ | ---------- |
| Starting ACV           | $80K      | Below Planet Enterprise ($100K+), above SkyFi self-serve                       | MEDIUM     |
| ACV Growth Rate        | ~10%/yr   | Feature expansion + data upsell + inflation                                    | MEDIUM     |
| Annual Logo Churn      | 10–12%    | B2B SaaS benchmark: 3.5–5% enterprise, 12.5% median [[2]](#ref-2)[[3]](#ref-3) | HIGH       |
| Net Revenue Retention  | 110–120%  | Account expansion offsets churn                                                | MEDIUM     |
| Own-Data Gross Margin  | 80%       | Planet Labs analog: own-satellite data is high-margin                          | HIGH       |
| Resale Gross Margin    | 40%       | Standard data resale markup                                                    | HIGH       |
| Services Gross Margin  | 50%       | People-intensive but high-value                                                | HIGH       |
| Gov Revenue Share Peak | 60% (Y5)  | Planet Labs is 80%+ gov; we diversify earlier                                  | MEDIUM     |
| First Gov Contract     | Y1 (SBIR) | 6–12 month SBIR cycle; defense BD hire in Y0                                   | MEDIUM     |

### 5.2 Revenue Sensitivity

| Scenario          | Key Changes                                   | Y7 Revenue | Y7 Margin |
| ----------------- | --------------------------------------------- | ---------- | --------- |
| **Base Case**     | As modeled                                    | $30.3M     | 72%       |
| **Conservative**  | 20% fewer clients, 10% lower ACV, 14% churn   | $18.2M     | 65%       |
| **Aggressive**    | 25% more clients, 15% higher ACV, own sats Y2 | $45.0M     | 75%       |
| **No Satellites** | Pure analytics/resale, no CapEx               | $14.0M     | 50%       |

> **The "No Satellites" scenario** shows that even without building a constellation, Constellation can build a $14M analytics business — but margins remain compressed without proprietary data. The constellation investment is justified by the margin expansion from ~50% to ~72%.

---

## 6. Cross-Section Alignment Check

| Metric             | Section 02 (TAM/SOM) | This Section (Revenue)          | Aligned? |
| ------------------ | -------------------- | ------------------------------- | -------- |
| Y7 Revenue (Base)  | $30.3M               | $30.3M                          |          |
| Total Clients Y7   | 133                  | 133 (5 new Y0 + growth - churn) |          |
| Avg ACV Y7         | $165K                | $165K                           |          |
| SAM Penetration Y7 | 1.17%                | $30.3M / $2,600M = 1.17%        |          |
| Annual Churn       | 12%                  | 12% (10% at maturity)           |          |
| Revenue Streams    | 3 + gov overlay      | 3 + gov overlay                 |          |

---

## 7. Key Insights

- **Three-stream model** with government overlay provides revenue diversification while maintaining focus
- **Own-constellation data is the margin catalyst**: gross margin expands from ~45% to ~72% as own data replaces third-party resale
- **Government revenue dominates early** (60% at Y5) but commercial catches up by Y7 (45% gov) — healthier long-term mix
- **LTV:CAC reaches >4 by Y1** and continues improving — indicating strong unit economics even with enterprise sales cycles
- **"No Satellites" scenario** validates the analytics-only model at $14M by Y7 — the constellation is a margin play, not a survival requirement

---

## 8. Investment Implications

1. **Revenue model is staged**: platform subscriptions provide baseline, own-constellation data accelerates growth and margins
2. **Government contracts provide predictable, large-ticket revenue** — but require 12–18 month sales cycles, justifying early investment in defense BD
3. **Gross margin expansion from 45% 72%** is the strongest argument for constellation investment
4. **Net revenue retention >110%** means existing customers grow faster than churn erodes the base — a hallmark of healthy B2B SaaS
5. **Y3–Y4 is the inflection point** where own-satellite revenue begins and the margin profile fundamentally shifts

---

## References & Sources

### SaaS Benchmarks

<a name="ref-1"></a>

1. **SaaS Capital — 2025 Private B2B SaaS Growth Rate Benchmarks**
   - Median growth rate: 25%
   - Source: SaaS Capital
   - URL: https://www.saas-capital.com/research/private-saas-company-growth-rate-benchmarks/

<a name="ref-2"></a> 2. **Lighter Capital — 2025 B2B SaaS Startup Benchmarks**

- Median revenue churn: 12.50% (2025)
- CAC payback target: <18 months
- LTV:CAC healthy threshold: >3.0x
- Source: Lighter Capital
- URL: https://www.lightercapital.com/blog/2025-b2b-saas-startup-benchmarks

<a name="ref-3"></a> 3. **Vena Solutions — SaaS Churn Rate Benchmarks (2025)**

- Average annual B2B SaaS churn: ~4.9%
- Enterprise (high ARPA): 3.5–5%
- Source: Vena Solutions
- URL: https://www.venasolutions.com/blog/saas-churn-rate
