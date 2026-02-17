# Technology Architecture

> **Last Updated:** 2026-02-17
> **Project:** Constellation Aerospace
> **Status:** Draft (v2 — 3U satellite, no tasking)

## Executive Summary

Constellation Aerospace builds a **vertically integrated Earth observation platform** combining multispectral optical satellites with **on-board edge AI processing** — a key differentiator in an industry where most competitors downlink raw data for ground-based analysis. Our **3U CubeSat constellation** operates in **survey mode** (fixed ground track, no agile tasking), designed to deliver **pre-processed, actionable intelligence** directly from orbit at 3–5m resolution. Edge AI reduces downlink bandwidth by up to 80% and enables near-real-time alerts for defense, agriculture, and insurance customers.

The technology stack operates across three layers: (1) **Space Segment** — 3U multispectral optical CubeSats with edge AI payloads, (2) **Ground Segment** — automated ground station network and cloud processing pipeline, and (3) **Platform Layer** — customer-facing analytics SaaS with API-first architecture. Phase 1 (Y0–Y2) deploys the platform layer using third-party imagery (including middleman tasking via partners); Phase 2 (Y2+) integrates own-constellation data through continuous monitoring feeds and archive imagery.

**Key design choice — no tasking:** Constellation's own satellites do NOT perform agile pointing or on-demand tasking. They operate in a fixed survey mode, collecting imagery along their orbital ground track. This simplifies the ADCS (attitude determination and control system), reduces manufacturing cost by 30–40%, increases reliability, and follows the Planet Labs Dove architecture that has proven at scale. During Phase 1, Constellation offers third-party tasking as a middleman using partners like BlackSky and Maxar, but this service is phased out as own-constellation monitoring feeds replace it.

---

## 1. System Architecture Overview

### 1.1 Three-Layer Stack

```

  SPACE SEGMENT
   3U CubeSat with multispectral optical payload (3–5m GSD)
   Edge AI co-processor (on-board inference)
   X-band downlink
   Orbit maintenance (no agile pointing — survey mode)

                        Pre-processed data

  GROUND SEGMENT
   Automated ground station network (AWS Ground Station)
   Raw data ingest and calibration
   Cloud processing pipeline (geometric, radiometric)
   Data archive and catalog

                        Analysis-ready data

  PLATFORM LAYER
   Analytics engine (change detection, classification)
   Customer dashboards and alerting
   API-first architecture (REST + streaming)
   Vertical-specific applications (Ag, Defense, etc.)

```

### 1.2 Phase 1 vs Phase 2 Architecture

| Component                | Phase 1 (Y0–Y2)                                  | Phase 2 (Y2+)                             |
| ------------------------ | ------------------------------------------------ | ----------------------------------------- |
| **Imagery Source**       | Third-party (Planet, Airbus, USGS)               | Own constellation + third-party           |
| **Tasking**              | Middleman via BlackSky/Maxar (resale)            | Not available — survey mode only          |
| **On-board Processing**  | N/A                                              | Edge AI inference on custom payload       |
| **Ground Processing**    | Cloud-only (AWS/GCP)                             | Cloud + on-board pre-processing           |
| **Platform**             | Full SaaS analytics + third-party tasking resale | Full SaaS + continuous monitoring feeds   |
| **Data Products**        | Archive imagery, tasking resale, basic analytics | Monitoring feeds, archive, edge-AI alerts |
| **Data Latency**         | Hours to days (3rd-party pipeline)               | Minutes (on-board alerts) to hours        |
| **Gross Margin on Data** | ~40% (resale)                                    | ~80% (own data)                           |

---

## 2. Space Segment — Satellite Platform

### 2.1 Satellite Design Philosophy

Constellation's satellites follow the **Planet Dove-class design philosophy**: small, standardized, mass-producible 3U CubeSats that prioritize revisit frequency and cost-per-image over maximum spatial resolution or agile pointing.

**Why 3U with no tasking:**

| Design Decision       | Rationale                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **3U form factor**    | Lowest-cost path to constellation scale; proven by Planet (200+ Doves)                                                   |
| **No agile pointing** | Eliminates reaction wheels, complex star trackers, and slew mechanisms — reducing cost 30–40% and increasing reliability |
| **Survey mode**       | Fixed ground track collection maximizes swath coverage; ideal for monitoring and change detection use cases              |
| **Mass-producible**   | Simple ADCS (magnetorquers only) enables $200–400K manufacturing cost per unit                                           |
| **Edge AI payload**   | Differentiator lives in the processing layer, not the pointing mechanism                                                 |

| Parameter          | Specification                        | Rationale                                                     |
| ------------------ | ------------------------------------ | ------------------------------------------------------------- |
| Form Factor        | 3U CubeSat (101030 cm)               | Minimum viable platform for optical + edge AI payload         |
| Mass               | 4–5 kg                               | Compatible with rideshare launches ($1K–10K/kg) [[1]](#ref-1) |
| Spatial Resolution | 3–5m GSD (multispectral)             | Sufficient for agriculture, change detection, defense ISR     |
| Spectral Bands     | 4–6 bands (visible + NIR + Red Edge) | NDVI, crop health, water analysis, land classification        |
| Swath Width        | 20–40 km                             | Practical for 3U optics; adequate for regional monitoring     |
| Orbit              | LEO, 400–550 km, Sun-synchronous     | Consistent lighting, global coverage                          |
| Pointing Mode      | Survey (fixed nadir or near-nadir)   | No agile tasking; simplifies ADCS to magnetorquers            |
| Design Life        | 3–5 years                            | Standard for LEO CubeSat missions                             |
| Manufacturing Cost | $200–400K per unit                   | 3–5x cheaper than 6U–16U equivalents                          |
| Launch Cost        | $100–250K per unit (rideshare)       | SpaceX Transporter, ISRO PSLV, Rocket Lab [[1]](#ref-1)       |

### 2.2 Multispectral Optical Payload

| Band     | Wavelength (nm) | Application                                    |
| -------- | --------------- | ---------------------------------------------- |
| Blue     | 450–515         | Water body delineation, atmospheric correction |
| Green    | 525–600         | Vegetation vigor, urban mapping                |
| Red      | 630–680         | Chlorophyll absorption, soil discrimination    |
| Red Edge | 705–745         | Crop stress detection, species classification  |
| NIR      | 770–895         | Biomass estimation, NDVI, land/water boundary  |

> **Design choice:** 3–5m resolution with 4–6 bands in a 3U form factor provides the optimal balance of coverage and detail for Constellation's target verticals. The narrower swath (20–40 km vs 150 km for larger sats) is offset by constellation size for adequate revisit rates. Higher resolution (<1m) would require larger optics incompatible with 3U — a trade-off that favors Maxar/BlackSky's architecture, not our high-revisit monitoring model.

### 2.3 Edge AI Co-Processor — Key Differentiator

The on-board AI processing system is Constellation's **core technical moat**. While most EO operators downlink all raw imagery for ground processing, Constellation performs inference at the edge:

| Capability                   | Description                                       | Benefit                                                      |
| ---------------------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| **Cloud Masking**            | ML model identifies cloud-covered frames          | Reduces downlink by 30–50% (avoid transmitting useless data) |
| **Change Detection**         | Compares current pass to baseline                 | Enables real-time alerts for defense and infrastructure      |
| **Object Classification**    | Identifies ships, vehicles, structures            | Supports defense ISR without ground-station latency          |
| **Anomaly Flagging**         | Highlights unusual patterns (crop stress, spills) | Priority alerts delivered within minutes of acquisition      |
| **Compression Optimization** | AI-guided compression preserves areas of interest | 3–5x effective bandwidth improvement                         |

**Technical Implementation (3U-Optimized):**

| Component       | Specification                                                  |
| --------------- | -------------------------------------------------------------- |
| Processor       | Radiation-tolerant GPU/NPU (e.g., Ubotica CogniSAT, Xiphos Q8) |
| Power Budget    | 2–5W dedicated to AI workload (constrained by 3U solar panels) |
| Model Size      | Quantized models (INT8), 5–20MB per model                      |
| Inference Speed | 2–10 seconds per frame                                         |
| Model Updates   | Ground-commanded OTA model deployment                          |
| Framework       | TensorFlow Lite / ONNX Runtime (edge-optimized)                |

> **3U constraint note:** The 2–5W power budget for edge AI is tighter than larger platforms (6U+ can dedicate 10–15W). This means simpler models (cloud masking, change detection) run on-board while complex analytics (multi-temporal classification) run on the ground. This hybrid approach captures 80% of the edge AI value with 30% of the compute budget.

**Market Validation:**

On-board satellite computing is a $2.15B market (2025) growing to $3.50B by 2030 [[2]](#ref-2). CATALYST, MarketsandMarkets, and Analysys Mason all identify edge AI as a critical growth driver for EO [[3]](#ref-3)[[4]](#ref-4)[[5]](#ref-5):

- CATALYST demonstrated in-orbit edge processing achieving "dramatic downlink reduction" [[3]](#ref-3)
- MarketsandMarkets notes AI enables satellites to "pre-process, filter, and interpret data onboard — enabling satellites to prioritize key observations" [[4]](#ref-4)
- Analysys Mason identifies "processing data near to the sensor" as the solution for faster delivery and reduced data volumes [[5]](#ref-5)

### 2.4 Constellation Sizing

| Metric            | Initial (Y2–Y3)            | Growth (Y4–Y5)        | Full Constellation (Y6–Y7) |
| ----------------- | -------------------------- | --------------------- | -------------------------- |
| Satellites        | 4–6                        | 12–16                 | 20–30                      |
| Revisit Frequency | 2–4 days                   | Daily                 | Sub-daily                  |
| Daily Collection  | ~1M km2                    | ~5M km2               | ~15M km2                   |
| Storage/Downlink  | ~100 GB/day                | ~500 GB/day           | ~1.5 TB/day                |
| Global Coverage   | Partial (priority regions) | NAM + India + SE Asia | Near-global                |

> **Survey mode collection:** Without agile tasking, each satellite images a fixed strip along its ground track during each orbit. Coverage builds through constellation size and orbital plane distribution. This is identical to Planet's Dove approach — they achieve daily global coverage with 200+ 3U satellites. Constellation's 20–30 satellite fleet targets **specific high-value regions** rather than global wall-to-wall coverage, reducing CapEx while maintaining competitive revisit rates.

### 2.5 Why No Tasking Is the Right Architecture

| Factor                 | Survey Mode (Constellation)                                | Agile Tasking (BlackSky)                           |
| ---------------------- | ---------------------------------------------------------- | -------------------------------------------------- |
| **ADCS Complexity**    | Magnetorquers only                                         | Reaction wheels + star trackers                    |
| **Manufacturing Cost** | $200–400K per 3U                                           | $2–5M per sat                                      |
| **Reliability**        | Higher (fewer moving parts)                                | Lower (mechanical actuator risk)                   |
| **Time-to-Build**      | 3–6 months                                                 | 12–18 months                                       |
| **Coverage Pattern**   | Systematic, predictable                                    | On-demand, uneven                                  |
| **Best For**           | Monitoring, change detection, trends                       | Ad-hoc collection, urgent imaging                  |
| **Edge AI Synergy**    | High — same areas reimaged regularly, enabling temporal AI | Lower — varied targets reduce model training value |

> **Strategic insight:** Survey mode is ideal for Constellation's core use cases (persistent monitoring, change detection, crop health tracking). These applications benefit from regular temporal revisit of the SAME areas, which is what survey mode provides inherently. Tasking is better for ad-hoc reconnaissance — a market dominated by BlackSky and Maxar with larger, more expensive satellites.

---

## 3. Ground Segment

### 3.1 Ground Station Architecture

| Approach     | Phase 1                      | Phase 2                          |
| ------------ | ---------------------------- | -------------------------------- |
| **Primary**  | AWS Ground Station (managed) | AWS GS + 2–3 dedicated stations  |
| **Backup**   | KSAT network (commercial)    | KSAT + partner stations          |
| **Coverage** | On-demand, pay-per-pass      | Continuous, all-pass capture     |
| **Latency**  | Minutes to hours             | Minutes (pre-processed on-board) |

**AWS Ground Station** provides satellite communication-as-a-service, eliminating the need for dedicated ground infrastructure in Phase 1. As the constellation grows, dedicated stations in strategic locations (e.g., Svalbard, Darwin, McMurdo) reduce latency and increase contact time.

### 3.2 Data Processing Pipeline

```
Downlink > Ingest > Level 0 > Level 1 > Level 2 > Analytics > Delivery
           (raw)   (decoded)  (calibrated) (geocorrected) (derived) (API/dashboard)
```

| Level | Processing                                        | Output                | Cloud Service |
| ----- | ------------------------------------------------- | --------------------- | ------------- |
| L0    | Frame decoding and depacketization                | Raw digital numbers   | S3 ingest     |
| L1A   | Radiometric calibration (sensor corrections)      | Calibrated radiance   | EC2/Lambda    |
| L1B   | Geometric correction (orthorectification)         | Georeferenced imagery | EC2 (GPU)     |
| L2    | Atmospheric correction, mosaicking                | Surface reflectance   | EC2 (GPU)     |
| L3    | Analytics products (NDVI, classification, change) | Derived intelligence  | SageMaker     |
| L4    | Customer-specific alerts and reports              | Actionable insights   | API Gateway   |

---

## 4. Platform Layer — Analytics SaaS

### 4.1 Core Platform Capabilities

| Feature                           | Description                                                 | Target Users       |
| --------------------------------- | ----------------------------------------------------------- | ------------------ |
| **Monitoring Dashboard**          | Automated change detection over areas of interest           | All verticals      |
| **Third-Party Tasking** (Phase 1) | Order new collections from partner satellites (middleman)   | Defense, Energy    |
| **Monitoring Feed Subscription**  | Continuous imagery updates from own constellation (Phase 2) | All verticals      |
| **Analytics Engine**              | Pre-built models for crop health, infrastructure, maritime  | Ag, Insurance      |
| **Custom Model Builder**          | Train and deploy custom models on Constellation data        | Enterprise         |
| **Alert System**                  | Real-time notifications for detected changes (edge AI)      | Defense, Insurance |
| **Historical Archive**            | Access to multi-year imagery archive for trend analysis     | All verticals      |
| **API Access**                    | RESTful APIs for programmatic data retrieval and analysis   | Enterprise, Gov    |

> **Phase transition:** Third-party tasking (middleman) is available in Phase 1 (Y0–Y2) as a revenue bridge. Once own constellation is operational (Y2+), monitoring feed subscriptions replace tasking as the primary data product — offering higher margins and better alignment with survey-mode architecture.

### 4.2 Vertical-Specific Applications

| Vertical        | Application                                  | Key Analytics                                       |
| --------------- | -------------------------------------------- | --------------------------------------------------- |
| **Defense**     | Persistent surveillance, activity monitoring | Object detection, change detection, pattern-of-life |
| **Agriculture** | Crop health monitoring, yield estimation     | NDVI time series, stress mapping, moisture indices  |
| **Energy**      | Pipeline/infrastructure monitoring           | Encroachment detection, construction progress       |
| **Insurance**   | Pre/post-disaster assessment                 | Damage classification, flood extent, wind damage    |

### 4.3 Technical Stack

| Layer        | Technology           | Rationale                                    |
| ------------ | -------------------- | -------------------------------------------- |
| Frontend     | React + MapLibre GL  | High-performance geospatial visualization    |
| Backend API  | Python (FastAPI)     | Async processing, ML ecosystem compatibility |
| ML/AI        | PyTorch + ONNX       | Training (cloud) + inference (edge + cloud)  |
| Data Store   | PostgreSQL + PostGIS | Spatial queries, metadata catalog            |
| Object Store | AWS S3               | Imagery archive (petabyte-scale)             |
| Compute      | EC2 (GPU) + Lambda   | GPU for processing, serverless for APIs      |
| Streaming    | Kafka                | Real-time data pipeline for alerts           |
| Auth         | OAuth 2.0 + RBAC     | Enterprise SSO, role-based access            |

---

## 5. Technical Moats

### 5.1 Defensibility Analysis

| Moat                       | Description                                                                           | Time to Replicate                 | Strength |
| -------------------------- | ------------------------------------------------------------------------------------- | --------------------------------- | -------- |
| **Edge AI IP**             | On-board inference models tuned for EO workloads                                      | 2–3 years                         | HIGH     |
| **Training Data Flywheel** | Own-constellation data improves models > better products > more customers > more data | Accelerates with scale            | HIGH     |
| **Vertical Domain Models** | Pre-built analytics for defense, agriculture, insurance                               | 1–2 years per vertical            | MEDIUM   |
| **Cost Structure**         | Own satellites provide data at ~80% gross margin vs ~40% for resale                   | Requires constellation investment | HIGH     |
| **3U Unit Economics**      | $300–600K per satellite enables rapid iteration and replacement                       | Architecture decision             | MEDIUM   |
| **Government Clearances**  | FCC licensing, ITAR compliance, defense procurement credentials                       | 1–3 years                         | HIGH     |

### 5.2 Edge AI vs. Ground Processing — Competitive Advantage

| Metric                    | Traditional (Ground)        | Constellation (Edge AI)     | Advantage                  |
| ------------------------- | --------------------------- | --------------------------- | -------------------------- |
| Downlink bandwidth needed | 100% of raw data            | 20–50% (filtered at source) | 2–5x bandwidth savings     |
| Alert latency             | Hours to days               | Minutes                     | 10–100x faster             |
| Ground processing cost    | $0.10–0.50/km2              | $0.02–0.10/km2              | 3–5x cheaper               |
| Cloud compute required    | High (all data)             | Low (pre-filtered)          | 60–80% reduction           |
| Useful data ratio         | ~30% (rest is clouds/ocean) | ~90% (filtered on-board)    | 3x more value per downlink |

---

## 6. Development Roadmap

| Phase                           | Timeline | Milestones                                                                                                                                  | Investment                |
| ------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| **Phase 1: Platform**           | Y0–Y1    | Launch analytics SaaS with third-party data (incl. tasking resale), onboard 10+ enterprise customers, validate edge AI models in simulation | $1–2M (software dev)      |
| **Phase 2A: Pathfinder**        | Y1–Y2    | Book rideshare launch, manufacture 2 pathfinder 3U sats with edge AI payload, ground testing                                                | $1–2M (hardware + launch) |
| **Phase 2B: Initial Ops**       | Y2–Y3    | Launch pathfinders, validate on-orbit edge AI, first monitoring feed products, phase out third-party tasking resale                         | $2–3M (operations + MFG)  |
| **Phase 3: Scale**              | Y3–Y5    | Scale to 12–16 satellites, daily revisit for priority regions, India ground station, defense contract portfolio                             | $4–6M (expansion)         |
| **Phase 4: Full Constellation** | Y5–Y7    | 20–30 satellites, near-global coverage, on-board model marketplace, next-gen payload development                                            | $5–8M (full scale)        |

### CapEx Schedule (Estimated)

| Category                    | Y0         | Y1         | Y2         | Y3         | Y4         | Y5         | Y6         | Y7         | Total       |
| --------------------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------- |
| Satellite Mfg / Bus (3U)    | $0.22M†    | $0.40M     | $1.00M     | $1.50M     | $1.80M     | $1.00M     | $0.70M     | $0.45M     | $7.07M      |
| Launch Services             | —          | $0.15M     | $0.50M     | $0.50M     | $0.60M     | $0.40M     | $0.30M     | $0.25M     | $2.70M      |
| Ground Segment              | —          | $0.30M     | $0.80M     | $0.80M     | $0.50M     | $0.30M     | $0.20M     | $0.10M     | $3.00M      |
| Payload Dev & Lab/Equipment | $0.78M†    | $0.50M     | $0.30M     | $0.30M     | $0.50M     | $0.30M     | $0.30M     | $0.40M     | $3.38M      |
| Software/Licenses           | —          | $0.50M     | $0.40M     | $0.40M     | $0.50M     | $0.50M     | $0.50M     | $0.50M     | $3.30M      |
| **Total CapEx**             | **$1.00M** | **$1.85M** | **$3.00M** | **$3.50M** | **$3.90M** | **$2.50M** | **$2.00M** | **$1.70M** | **$19.45M** |

> **† Y0 CapEx detail:** Satellite Mfg/Bus $0.22M = Dhruva Aerospace 3U OTS bus ($200K) + compute/electronics ($20K). Payload Dev $0.78M = Cassegrain telescope optics & imaging ($500K) + thermal management ($20K) + integration/testing/GSE ($260K). No software CapEx in Y0 (tools in OpEx). No launch in Y0.
>
> **3U cost advantage:** Total constellation CapEx of ~$19.5M over 8 years is roughly half what a 6U–16U fleet of equivalent size would cost (~$41M). The savings come primarily from satellite manufacturing (60–70% cheaper) and launch costs (lighter sats = cheaper rideshare slots). This dramatically improves the company's capital efficiency and reduces funding requirements.

---

## 7. Key Insights

- **Edge AI is the differentiator, not tasking**: On-board processing reduces downlink costs by 50–80%, enables minute-latency alerts, and creates a data flywheel — this is where the IP lives, not in pointing mechanisms [[3]](#ref-3)[[4]](#ref-4)[[5]](#ref-5)
- **3U survey-mode architecture is proven**: Planet's 200+ Dove fleet validates this approach at massive scale; reliability and unit economics favor simplicity
- **No tasking = lower cost, higher reliability**: Eliminating agile pointing saves 30–40% per satellite and removes the primary mechanical failure mode
- **Phase 1 middleman tasking bridges the gap**: Third-party tasking resale generates revenue in Y0–Y2 while own constellation is built
- **Monitoring feeds replace tasking**: Survey mode naturally produces continuous coverage data — ideal for subscriptions, change detection, and temporal analytics
- **Own-constellation economics are compelling**: Gross margins improve from ~40% (resale) to ~80% (own data), fundamentally changing unit economics at scale
- **3U CapEx of ~$19.5M** (vs ~$41M for 6U–16U) means the company can be fully funded with $16.3M equity and no structural capital gap
- **The satellite onboard computing market ($2.15B) validates demand** for edge AI capabilities in space [[2]](#ref-2)

---

## 8. Investment Implications

1. **Technology is proven** — 3U CubeSats and edge computing are mature technologies being applied in a novel combination; no unproven physics required
2. **Phase 1 de-risks execution** — revenue generation before satellite build validates market demand with minimal hardware risk; middleman tasking generates revenue immediately
3. **Edge AI creates switching costs** — customers build workflows around Constellation's near-real-time monitoring and alert capabilities, increasing retention
4. **3U architecture is capital-efficient** — total CapEx of ~$19.5M is fully covered by $16.3M equity + operating cash flow; no structural funding gap
5. **No tasking simplifies operations** — survey-mode satellites require minimal ground-station commanding and scheduling complexity
6. **The architecture scales linearly** — adding 3U satellites is incremental ($300–600K each), with each satellite contributing ~$1M/year in data revenue at maturity

---

## References & Sources

### Satellite Manufacturing & Launch Economics

<a name="ref-1"></a>

1. **Market Research Future — Small Satellite Launch Economics (2025)**
   - Launch costs: $1,000–10,000/kg
   - Manufacturing cost as low as $200K for 3U CubeSats
   - Small satellite market growing rapidly
   - Source: Market Research Future
   - URL: https://www.marketresearchfuture.com/reports/small-satellite-market-6007

### On-Board Computing & Edge AI

<a name="ref-2"></a> 2. **Mordor Intelligence — Satellite Onboard Computing System Market (2025–2030)**

- Market Size: $2.15B (2025) > $3.50B (2030)
- Growth driven by edge AI processing demand
- Source: Mordor Intelligence
- URL: https://www.mordorintelligence.com/industry-reports/satellite-onboard-computing-system-market

<a name="ref-3"></a> 3. **CATALYST — In-Orbit Edge Data Processing (2025)**

- Demonstrated dramatic downlink reduction through on-board processing
- Bandwidth optimization by filtering data in orbit
- Source: CATALYST
- URL: https://catalyst.earth/catalyst-optimizes-satellite-performance-with-in-orbit-edge-data-processing/

<a name="ref-4"></a> 4. **MarketsandMarkets — AI Impact on Small Satellite Industry (2025)**

- AI enables on-board pre-processing, filtering, and interpretation
- Satellites can prioritize key observations and reduce downlink congestion
- Source: MarketsandMarkets
- URL: https://www.marketsandmarkets.com/ResearchInsight/ai-impact-analysis-small-satellite-industry.asp

<a name="ref-5"></a> 5. **Analysys Mason — Edge Computing in Space (2025)**

- Processing data near sensor reduces delivery time and downlink volumes
- Identified as a necessity, not luxury, for competitive EO operations
- Source: Analysys Mason
- URL: https://www.analysysmason.com/research/content/articles/edge-computing-in-space-necessity-or-luxury/
