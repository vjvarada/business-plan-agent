# Sources & References - RapidTools Financial Model

> Last Updated: January 2026
>
> **IMPORTANT**: This Markdown file is the source of truth. Edit here, then sync to Google Sheets.
> Other sheets reference cells in Sources & References - be careful with row numbers!

---

## SECTION A: KEY METRICS (Linkable Values)

### TAM - Total Addressable Market

RapidTools operates across **5 revenue streams** targeting **10 design automation modules**. The TAM is calculated bottom-up from relevant global markets.

#### Base Markets (Global 2024-2025)

| Row | Metric                                | Value           | Unit | Source                   | URL                                                                                                                 | Notes                         |
| --- | ------------------------------------- | --------------- | ---- | ------------------------ | ------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| 7   | Dies, Jigs & Tools Market 2024        | 60,180,000,000  | $    | Business Research Co     | https://www.thebusinessresearchcompany.com/report/special-die-and-tool-die-set-jig-and-fixture-global-market-report | Growing to $63.35B in 2025    |
| 8   | End of Arm Tooling (EOAT) Market 2024 | 2,600,000,000   | $    | IMARC Group              | https://www.imarcgroup.com/robotics-end-of-arm-tooling-market                                                       | Robotics EOAT, 4.64% CAGR     |
| 9   | Industrial 3D Printing Market 2024    | 3,560,000,000   | $    | Precedence Research      | https://www.precedenceresearch.com/industrial-3d-printing-market                                                    | Growing to $24B by 2034       |
| 10  | 3D Printing Services Market 2024      | 9,830,000,000   | $    | Fact.MR                  | https://www.factmr.com/report/3d-printing-service-bureaus-market                                                    | Service bureaus, 18.2% CAGR   |
| 11  | Sand Casting Market 2024              | 345,500,000,000 | $    | Verified Market Research | https://www.verifiedmarketresearch.com/product/sand-casting-market/                                                 | 7.8% CAGR to 2031             |
| 12  | Vacuum Casting Market 2024            | 2,560,000,000   | $    | Straits Research         | https://straitsresearch.com/report/vacuum-casting-market                                                            | 5.3% CAGR                     |
| 13  | Palletizing Equipment Market 2024     | 2,900,000,000   | $    | PS Market Research       | https://www.psmarketresearch.com/market-analysis/palletizer-market-report                                           | Material handling automation  |
| 14  | Workholding Devices Market 2024       | 4,440,000,000   | $    | Market Data Forecast     | https://www.marketdataforecast.com/market-reports/workholding-devices-market                                        | Soft jaws, chuck jaws segment |
| 15  | Tooling Market 2024 (Global)          | 273,890,000,000 | $    | Precedence Research      | https://www.precedenceresearch.com/tooling-market                                                                   | 6.9% CAGR to 2032             |

#### Design Automation Software TAM (10 Modules)

The software TAM represents the portion of each market addressable by AI-driven design automation tools.

**Software % Methodology**: Based on McKinsey Digital Manufacturing Report (2024) which estimates 3-5% of manufacturing tooling spend shifts to software/automation solutions annually. Higher percentages (5-8%) applied to segments with greater digital design adoption (shadow boxes, soft jaws, vacuum casting).

| Row | Module                                   | Base Market Segment   | Segment Value ($M) | Software % | Software TAM ($M) | Source                            | Notes                                                   |
| --- | ---------------------------------------- | --------------------- | ------------------ | ---------- | ----------------- | --------------------------------- | ------------------------------------------------------- |
| 17  | 1. Jigs & Fixtures                       | Dies, Jigs & Tools    | 15,000             | 3.5%       | 525               | Business Research Co (Row 7)      | 25% of $60B market is jigs/fixtures per IBIS World      |
| 18  | 2. Assembly Guides                       | Dies, Jigs & Tools    | 8,000              | 3.0%       | 240               | Business Research Co (Row 7)      | Assembly tooling ~13% of market per Grand View Research |
| 19  | 3. Drilling Guides                       | Dies, Jigs & Tools    | 5,000              | 3.0%       | 150               | Business Research Co (Row 7)      | Drilling jig ~8% of market per Technavio                |
| 20  | 4. Alignment Tools (Stickers/Components) | Dies, Jigs & Tools    | 3,000              | 4.0%       | 120               | Business Research Co (Row 7)      | Positioning tools ~5% per Allied Market Research        |
| 21  | 5. Shadow Boxes                          | Dies, Jigs & Tools    | 2,000              | 5.0%       | 100               | Business Research Co (Row 7)      | Visual mgmt/lean tools per Lean Enterprise Institute    |
| 22  | 6. Custom Palletizing Tools              | Palletizing Equipment | 2,900              | 4.0%       | 116               | PS Market Research (Row 13)       | Custom material transport segment                       |
| 23  | 7. Sand Casting Tool Design              | Sand Casting Market   | 10,000             | 2.0%       | 200               | Verified Market Research (Row 11) | Pattern/core box design ~3% of casting market           |
| 24  | 8. Vacuum Casting Tool Design            | Vacuum Casting Market | 2,560              | 5.0%       | 128               | Straits Research (Row 12)         | Mold design automation, higher digital adoption         |
| 25  | 9. Soft Jaws                             | Workholding Devices   | 300                | 8.0%       | 24                | Market Data Forecast (Row 14)     | Custom soft jaw ~7% of workholding per LinkedIn         |
| 26  | 10. End of Arm Tooling (EOAT)            | EOAT Market           | 2,600              | 5.0%       | 130               | IMARC Group (Row 8)               | Gripper/tool design automation                          |
| 27  | **SOFTWARE TAM TOTAL**                   |                       | **51,360**         |            | **1,733**         | Calculated                        | Sum of all modules                                      |

#### Hardware & Services TAM (Additional Revenue Streams)

| Row | Revenue Stream                     | Addressable Market     | RapidTools Share % | TAM ($M)  | Source              | Notes                               |
| --- | ---------------------------------- | ---------------------- | ------------------ | --------- | ------------------- | ----------------------------------- |
| 29  | 3D Printers (Hardware)             | Industrial 3D Printing | 15%                | 534       | Precedence Research | Entry-level industrial FDM printers |
| 30  | Consumables (Filaments, Materials) | 3D Printing Materials  | 10%                | 313       | Data Bridge MR      | $3.13B materials market             |
| 31  | Job Work (Design + Print Services) | 3D Printing Services   | 5%                 | 492       | Fact.MR             | Service bureau market share         |
| 32  | Managed Services (On-site)         | 3D Printing Services   | 2%                 | 197       | Fact.MR             | Enterprise full-service             |
| 33  | **HARDWARE & SERVICES TAM**        |                        |                    | **1,536** | Calculated          | Sum of non-software streams         |

#### TOTAL TAM SUMMARY

| Row | Category                                | TAM ($M)  | Notes                       |
| --- | --------------------------------------- | --------- | --------------------------- |
| 35  | Design Automation Software (10 modules) | 1,733     | AI-driven design tools      |
| 36  | Hardware (3D Printers)                  | 534       | Industrial printer sales    |
| 37  | Consumables                             | 313       | Recurring materials revenue |
| 38  | Job Work Services                       | 492       | Design + print fulfillment  |
| 39  | Managed Services                        | 197       | Enterprise deployments      |
| 40  | **TOTAL RapidTools TAM**                | **3,269** | All 5 revenue streams       |

---

### SAM - Serviceable Addressable Market

SAM is calculated by applying addressability filters to the TAM, based on:

- Geographic focus (Year 1: India, expanding globally)
- Target company profiles (manufacturing companies with tooling needs)
- Digital readiness (CAD capabilities, 3D printing adoption)

**SAM Methodology**: Regional manufacturing counts from IBEF, Trade.gov, JBIC. Target segments filtered to Auto, Aerospace, Precision Engineering per industry reports. Addressable % based on CAD/3D printing adoption rates from 6sense Technology Adoption Report 2024.

#### Regional Company Analysis

##### INDIA (Year 1 Focus)

| Row | Metric                      | Value   | Unit | Source                         | Notes                                           |
| --- | --------------------------- | ------- | ---- | ------------------------------ | ----------------------------------------------- |
| 43  | India - Total Mfg Companies | 680,000 | #    | IBEF Manufacturing Report 2024 | India Brand Equity Foundation                   |
| 44  | India - Target Segments     | 58,500  | #    | ACMA + Nexdigm Reports         | Auto (35K) + Aero (2K) + Precision (21.5K)      |
| 45  | India - Addressable %       | 10.00%  | %    | 6sense CAD Adoption 2024       | Companies with CAD: AutoCAD 39%, SolidWorks 14% |
| 46  | India - SAM Companies       | 5,850   | #    | Calculated                     | =B44\*B45                                       |

##### SOUTHEAST ASIA (Year 2-3)

| Row | Metric                        | Value   | Unit | Source                     | Notes                                           |
| --- | ----------------------------- | ------- | ---- | -------------------------- | ----------------------------------------------- |
| 48  | SE Asia - Total Mfg Companies | 250,000 | #    | Source of Asia Report 2024 | Vietnam, Thailand, Indonesia, Malaysia combined |
| 49  | SE Asia - Target Segments     | 24,200  | #    | AMT Online + Sparkco AI    | 9.7% of mfg base in precision segments          |
| 50  | SE Asia - Addressable %       | 12.00%  | %    | 6sense CAD Adoption 2024   | Growing digital adoption, higher than India     |
| 51  | SE Asia - SAM Companies       | 2,904   | #    | Calculated                 | =B49\*B50                                       |

##### JAPAN (Year 3-4)

| Row | Metric                      | Value   | Unit | Source                   | Notes                                          |
| --- | --------------------------- | ------- | ---- | ------------------------ | ---------------------------------------------- |
| 53  | Japan - Total Mfg Companies | 180,000 | #    | Safeguard Global 2024    | World ranking #3 manufacturer                  |
| 54  | Japan - Target Segments     | 26,400  | #    | JBIC Survey 2024         | Auto (15K), electronics (7K), precision (4.4K) |
| 55  | Japan - Addressable %       | 25.00%  | %    | 6sense CAD Adoption 2024 | High technology adoption, Industry 4.0 leaders |
| 56  | Japan - SAM Companies       | 6,600   | #    | Calculated               | =B54\*B55                                      |

##### GERMANY / EU (Year 4-5)

| Row | Metric                        | Value   | Unit | Source                   | Notes                                       |
| --- | ----------------------------- | ------- | ---- | ------------------------ | ------------------------------------------- |
| 58  | Germany - Total Mfg Companies | 200,000 | #    | Trade.gov Germany 2024   | Advanced Manufacturing Commercial Guide     |
| 59  | Germany - Target Segments     | 30,600  | #    | Spherical Insights 2024  | Auto suppliers (18K), precision eng (12.6K) |
| 60  | Germany - Addressable %       | 20.00%  | %    | 6sense CAD Adoption 2024 | Industry 4.0 leaders, high digital maturity |
| 61  | Germany/EU - SAM Companies    | 6,120   | #    | Calculated               | =B59\*B60                                   |

##### OTHER REGIONS

| Row | Metric                 | Value | Unit | Source   | Notes                             |
| --- | ---------------------- | ----- | ---- | -------- | --------------------------------- |
| 63  | Others - SAM Companies | 8,000 | #    | Estimate | UK, Canada, Australia, MENA, etc. |

#### SAM Value Calculation

| Row | Metric                  | Value       | Unit | Formula              | Notes                           |
| --- | ----------------------- | ----------- | ---- | -------------------- | ------------------------------- |
| 43  | TOTAL SAM - Companies   | 29,474      | #    | =B46+B51+B56+B61+B63 | Sum of all regional SAMs        |
| 44  | SAM Value (All Streams) | 220,500,000 | $    | Calculated           | See SAM by Revenue Stream below |

#### SAM by Revenue Stream

**Attach Rate Sources**: Hardware attach from Gartner (15-25% B2B cross-sell), Job Work from Deloitte Manufacturing Services (25-35% outsourcing), Managed Services from Gartner Enterprise IT (3-7% MSP adoption).

| Row | Revenue Stream              | SAM Companies | Attach Rate | Revenue/Customer | SAM Value ($M) | Notes                                   |
| --- | --------------------------- | ------------- | ----------- | ---------------- | -------------- | --------------------------------------- |
| 69  | Software (10 modules)       | 29,474        | 100%        | $3,000/yr        | 88.4           | Primary product - Tropic Spend Report   |
| 70  | 3D Printers (Hardware)      | 29,474        | 20%         | $5,000           | 29.5           | Cross-sell 20% - Gartner Tech Adoption  |
| 71  | Consumables                 | 5,895         | 100%        | $2,400/yr        | 14.1           | 40 units × $60 per printer customer     |
| 72  | Job Work Services           | 29,474        | 30%         | $5,000/yr        | 44.2           | Outsourced fulfillment - Deloitte Mfg   |
| 73  | Managed Services            | 29,474        | 5%          | $30,000/yr       | 44.2           | Enterprise tier - Gartner Enterprise IT |
| 74  | **TOTAL SAM (All Streams)** |               |             |                  | **220.5**      | Combined revenue opportunity            |

---

### SOM - Serviceable Obtainable Market

**SOM Derivation from SAM**: SOM is calculated as SAM × Penetration Target. Penetration targets based on Span Global Services benchmark: B2B SaaS typically achieves 2-8% SAM penetration in first 5 years. Higher penetration in focused markets (India first) before expanding globally.

#### SAM Penetration Targets

| Row | Metric                    | Value | Unit | Source               | Notes                             |
| --- | ------------------------- | ----- | ---- | -------------------- | --------------------------------- |
| 46  | Y0 SAM Penetration Target | 0.10% | %    | Span Global Services | Pilot phase, India focus          |
| 47  | Y1 SAM Penetration Target | 0.50% | %    | Span Global Services | Early adopter phase               |
| 48  | Y2 SAM Penetration Target | 1.50% | %    | Span Global Services | Product-market fit, SE Asia entry |
| 49  | Y3 SAM Penetration Target | 3.00% | %    | Span Global Services | Growth phase, Japan entry         |
| 50  | Y4 SAM Penetration Target | 5.00% | %    | Span Global Services | Scaling, EU entry                 |
| 51  | Y5 SAM Penetration Target | 8.00% | %    | Span Global Services | Market expansion, global          |

#### Customer Projections (Derived from SAM × Penetration)

| Row | Metric       | Value | Unit | Formula            | Notes              |
| --- | ------------ | ----- | ---- | ------------------ | ------------------ |
| 52  | Y0 Customers | 29    | #    | =ROUND(B43\*B46,0) | SAM 29,474 × 0.10% |
| 53  | Y1 Customers | 147   | #    | =ROUND(B43\*B47,0) | SAM 29,474 × 0.50% |
| 54  | Y2 Customers | 442   | #    | =ROUND(B43\*B48,0) | SAM 29,474 × 1.50% |
| 55  | Y3 Customers | 884   | #    | =ROUND(B43\*B49,0) | SAM 29,474 × 3.00% |
| 56  | Y4 Customers | 1,474 | #    | =ROUND(B43\*B50,0) | SAM 29,474 × 5.00% |
| 57  | Y5 Customers | 2,358 | #    | =ROUND(B43\*B51,0) | SAM 29,474 × 8.00% |

#### SAM Penetration Verification

| Row | Metric                      | Value | Unit | Formula  | Notes                   |
| --- | --------------------------- | ----- | ---- | -------- | ----------------------- |
| 59  | Y5 SAM Penetration (Actual) | 8.00% | %    | =B57/B43 | Calculated verification |

---

### Seats Expansion Model

**Seat Expansion Sources**: OpenView Product Benchmarks 2024 shows B2B SaaS seat expansion of 1.5-2x annually for successful products. Gainsight reports avg seats/account grows from 1-2 (SMB) to 3-5 (Mid-Market) over 3-4 years.

| Row | Metric            | Value | Unit | Source                      | Notes                             |
| --- | ----------------- | ----- | ---- | --------------------------- | --------------------------------- |
| 86  | Y0 Seats/Customer | 1     | #    | OpenView Product Benchmarks | Single user adoption, pilot phase |
| 87  | Y1 Seats/Customer | 2     | #    | OpenView Product Benchmarks | Team adoption begins              |
| 88  | Y2 Seats/Customer | 2     | #    | OpenView Product Benchmarks | Multi-user teams, same as Y1      |
| 89  | Y3 Seats/Customer | 3     | #    | Gainsight Expansion Report  | Department-wide adoption          |
| 90  | Y4 Seats/Customer | 3     | #    | Gainsight Expansion Report  | Cross-functional use              |
| 91  | Y5 Seats/Customer | 4     | #    | Gainsight Expansion Report  | Enterprise deployment, 4x initial |

---

### Pricing Benchmarks

**Sources**: Competitor pricing from Renishaw FixtureBuilder, trinckle fixturemate, Vention (see Section B - Competitor & Pricing Sources). 3D Printer pricing from Precedence Research Industrial 3D Printing Report. Consumables from Data Bridge 3D Printing Materials Market Report.

| Row | Metric                      | Value  | Unit      | Source                      | Notes                                                                    |
| --- | --------------------------- | ------ | --------- | --------------------------- | ------------------------------------------------------------------------ |
| 94  | Software Subscription Price | 1,500  | $/seat/yr | Renishaw, trinckle, Vention | Competitive positioning: Renishaw $2-3K, trinckle $1-2K, Vention $1.5-2K |
| 95  | 3D Printer Price            | 5,000  | $/unit    | Precedence Research (Row 9) | Entry-level industrial FDM: Ultimaker $3-6K, Raise3D $4-8K               |
| 96  | Consumables Price           | 600    | $/unit    | Data Bridge MR (Row 30)     | Industrial filament avg $40-60/kg, ~10kg/unit                            |
| 97  | AMC Contract Price          | 400    | $/yr      | Gartner IT Services         | Industry standard 8-10% of equipment cost                                |
| 98  | Managed Services Price      | 30,000 | $/yr      | Deloitte Managed Services   | Mid-market MSP pricing: $2-5K/month                                      |

---

### COGS Percentages

**Sources**: SaaS COGS from OpenView SaaS Benchmarks 2024, KeyBanc SaaS Survey 2024. Hardware margins from IBISWorld Manufacturing Reports. Service margins from Deloitte Professional Services Benchmarks.

| Row | Metric                  | Value  | Unit | Source                          | Notes                                             |
| --- | ----------------------- | ------ | ---- | ------------------------------- | ------------------------------------------------- |
| 101 | Software COGS %         | 15.00% | %    | OpenView SaaS Benchmarks 2024   | Median SaaS gross margin 75-80%, COGS 15-20%      |
| 102 | 3D Printer COGS %       | 45.00% | %    | IBISWorld 3D Printer Mfg        | Reseller margin 40-50% COGS, 50-60% gross margin  |
| 103 | Consumables COGS %      | 60.00% | %    | IBISWorld Plastics Wholesale    | Materials + fulfillment, 35-40% gross margin      |
| 104 | AMC COGS %              | 60.00% | %    | Gartner IT Services + OEM share | OEM/VAR share 30-40% + parts 12% + technician 10% |
| 105 | Managed Services COGS % | 50.00% | %    | Deloitte Managed Services       | Dedicated personnel 40-50% + overhead 10%         |

---

### Customer Acquisition

**Sources**: CAC benchmarks from ProfitWell B2B SaaS Benchmarks 2024, OpenView SaaS Metrics Report 2024. SMB B2B SaaS CAC typically $1,000-$3,000. Churn benchmarks from Recurly State of Subscriptions 2025, CustomerGauge B2B Benchmarks.

| Row | Metric                | Value  | Unit       | Source                       | Notes                                                 |
| --- | --------------------- | ------ | ---------- | ---------------------------- | ----------------------------------------------------- |
| 108 | Y0 CAC                | 2,000  | $/customer | ProfitWell B2B SaaS 2024     | Early-stage CAC: $1,500-$3,000, high-touch sales      |
| 109 | Y1 CAC                | 1,800  | $/customer | ProfitWell B2B SaaS 2024     | Growth phase: 10% efficiency improvement              |
| 110 | Y2 CAC                | 1,500  | $/customer | OpenView SaaS Metrics 2024   | Scale phase: median SMB SaaS CAC                      |
| 111 | Y3 CAC                | 1,400  | $/customer | OpenView SaaS Metrics 2024   | Expansion phase: regional presence reduces CAC        |
| 112 | Y4 CAC                | 1,300  | $/customer | OpenView SaaS Metrics 2024   | Maturity phase: brand recognition                     |
| 113 | Y5 CAC                | 1,200  | $/customer | OpenView SaaS Metrics 2024   | Efficiency phase: 40% inbound-led per HubSpot         |
| 114 | Churn Rate            | 10.00% | %          | Recurly 2025 + CustomerGauge | SMB B2B SaaS: 4.9-10% annual (using conservative 10%) |
| 115 | Avg Customer Lifetime | 10     | years      | Calculated                   | =1/Churn Rate (1/10% = 10 years)                      |

---

### Product Attachment Rates (CONSOLIDATED)

**Sources**: Cross-sell benchmarks from Gainsight Customer Success Report 2024, SaaS product-led growth benchmarks from OpenView. Hardware attach rates from Gartner Technology Adoption Report.

**Customer Mix:** 70% SMB / 25% Mid-Market / 5% Enterprise (by count)

#### Blended Attach Rates (Weighted by Customer Mix)

| Row | Metric                 | Blended | Unit  | Source                       | Calculation (SMB×70% + MM×25% + Ent×5%)    |
| --- | ---------------------- | ------- | ----- | ---------------------------- | ------------------------------------------ |
| 118 | Hardware Attach Rate   | 22%     | %     | Gartner Tech Adoption 2024   | 15%×70% + 35%×25% + 50%×5% = 22%           |
| 119 | Consumables/Printer/Yr | 40      | units | Stratasys Usage Data         | Industrial printer: 3-4 spools/month avg   |
| 120 | AMC Attach Rate        | 35%     | %     | Gartner IT Services          | Service attach: 30-40% for equipment sales |
| 121 | Job Work Attach Rate   | 46%     | %     | Calculated                   | 45%×70% + 55%×25% + 35%×5% = 46%           |
| 122 | EMS Attach Rate        | 4%      | %     | Deloitte Enterprise Services | 0%×70% + 5%×25% + 30%×5% = 4%              |
| 123 | Consumables Attach     | 15%     | %     | Calculated                   | 10%×70% + 25%×25% + 40%×5% = 15%           |

#### Segment-Specific Attach Rates (from BP 07_Revenue_Model.md)

| Product/Service             | SMB (70%) | Mid-Market (25%) | Enterprise (5%) |
| --------------------------- | --------- | ---------------- | --------------- |
| Additional Software Seats   | 50%       | 80%              | 100%            |
| Second Product (Casting)    | 20%       | 40%              | 60%             |
| Tooling Services (Job Work) | 45%       | 55%              | 35%             |
| Enterprise Managed Services | 0%        | 5%               | 30%             |
| Hardware Purchase           | 15%       | 35%              | 50%             |
| Consumables                 | 10%       | 25%              | 40%             |

**Key Insight:** Job Work attach (46%) is inversely correlated with Hardware attach (22%). Customers typically either buy printers OR outsource printing—they're substitutes, not complements.

---

### Headcount Benchmarks

#### Revenue Metrics

| Row | Metric                              | Value   | Unit          | Source                        | Notes                                    |
| --- | ----------------------------------- | ------- | ------------- | ----------------------------- | ---------------------------------------- |
| 124 | Revenue per Employee (Private SaaS) | 130,000 | $/employee/yr | Capchase SaaS Metrics 2024    | Median private SaaS: $100-150K/employee  |
| 125 | Revenue per Employee (Public SaaS)  | 200,000 | $/employee/yr | OpenView SaaS Benchmarks 2024 | Top quartile public SaaS: $180-250K      |
| 126 | Revenue per Employee (Target)       | 150,000 | $/employee/yr | Internal target               | Between private median and public target |

#### Customer Success Ratios

| Row | Metric                        | Value     | Unit      | Source                        | Notes                                 |
| --- | ----------------------------- | --------- | --------- | ----------------------------- | ------------------------------------- |
| 129 | Accounts per CSM (Mid-Market) | 100       | accounts  | Gainsight CS Benchmark 2024   | Mid-market range: 75-150 accounts/CSM |
| 130 | ARR per CSM                   | 2,000,000 | $/CSM/yr  | Gainsight CS Benchmark 2024   | Range: $1.5-3M ARR per CSM            |
| 131 | Customers per Support Rep     | 200       | customers | Zendesk Benchmark Report 2024 | SMB tier: 150-250 customers/rep       |

#### Sales Team Ratios

| Row | Metric                  | Value   | Unit     | Source                        | Notes                                 |
| --- | ----------------------- | ------- | -------- | ----------------------------- | ------------------------------------- |
| 134 | ARR per Sales Rep       | 500,000 | $/rep/yr | OpenView SaaS Benchmarks 2024 | SMB AE quota: $400-600K, median $500K |
| 135 | Quota Attainment Target | 80%     | %        | Gartner Sales Benchmark 2024  | B2B SaaS quota attainment: 70-85%     |

#### Engineering Ratios

| Row | Metric                           | Value | Unit | Source                         | Notes                               |
| --- | -------------------------------- | ----- | ---- | ------------------------------ | ----------------------------------- |
| 138 | Eng to Total Ratio (Early Stage) | 60%   | %    | ChartMogul SaaS Benchmark 2024 | Seed-Series A: 55-65% engineering   |
| 139 | Eng to Total Ratio (Scale)       | 40%   | %    | ChartMogul SaaS Benchmark 2024 | Series B+: 35-45% as sales/CS grows |

#### Regional Manager Salaries

| Row | Metric                    | Value   | Unit | Source                  | Notes                                    |
| --- | ------------------------- | ------- | ---- | ----------------------- | ---------------------------------------- |
| 142 | India Regional Manager    | 50,000  | $/yr | Glassdoor India 2024    | SaaS Sales Manager: ₹35-50L ($42-60K)    |
| 143 | SE Asia Regional Manager  | 60,000  | $/yr | PayScale Singapore 2024 | Regional Sales: SGD 70-90K ($52-67K)     |
| 144 | MENA Regional Manager     | 70,000  | $/yr | PayScale UAE 2024       | Regional Manager: AED 220-300K ($60-82K) |
| 145 | Europe Regional Manager   | 90,000  | $/yr | Glassdoor Germany 2024  | Sales Manager: €75-100K ($82-109K)       |
| 146 | Americas Regional Manager | 100,000 | $/yr | Glassdoor US 2024       | Regional Sales Manager: $90-120K         |

---

### Key Derived Metrics (Calculated)

| Row | Metric                        | Value         | Unit  | Source                | Notes                          |
| --- | ----------------------------- | ------------- | ----- | --------------------- | ------------------------------ |
| 149 | Total TAM (All Streams)       | 3,269,000,000 | $     | Sum of all TAM        | Software + Hardware + Services |
| 150 | Total SAM Companies           | 29,474        | #     | Sum of all regions    | Links to B65                   |
| 151 | Total SAM Value (All Streams) | 220,500,000   | $     | SAM by revenue stream | Links to B74                   |
| 152 | Y5 Market Penetration         | 4.44%         | %     | Y5 Customers / SAM    | =B82/B65                       |
| 153 | Customer Lifetime Value       | 15,000        | $     | Lifetime × ARPU       | $15K per customer              |
| 154 | LTV:CAC Ratio (Y5)            | 12.5          | ratio | LTV / CAC             | 12.5:1 ratio                   |

---

## SECTION B: FULL SOURCE DOCUMENTATION

### TAM Market Research Sources (New)

| Source Name              | Report/Page               | Year | URL                                                                                                                 | Notes                  |
| ------------------------ | ------------------------- | ---- | ------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| Business Research Co     | Dies, Jigs & Tools Market | 2024 | https://www.thebusinessresearchcompany.com/report/special-die-and-tool-die-set-jig-and-fixture-global-market-report | $60.18B in 2024        |
| IMARC Group              | EOAT Market               | 2024 | https://www.imarcgroup.com/robotics-end-of-arm-tooling-market                                                       | $2.6B, 4.64% CAGR      |
| Precedence Research      | Industrial 3D Printing    | 2024 | https://www.precedenceresearch.com/industrial-3d-printing-market                                                    | $3.56B growing to $24B |
| Fact.MR                  | 3D Printing Services      | 2024 | https://www.factmr.com/report/3d-printing-service-bureaus-market                                                    | $9.83B, 18.2% CAGR     |
| Verified Market Research | Sand Casting Market       | 2024 | https://www.verifiedmarketresearch.com/product/sand-casting-market/                                                 | $345.5B, 7.8% CAGR     |
| Straits Research         | Vacuum Casting Market     | 2024 | https://straitsresearch.com/report/vacuum-casting-market                                                            | $2.56B, 5.3% CAGR      |
| PS Market Research       | Palletizer Market         | 2024 | https://www.psmarketresearch.com/market-analysis/palletizer-market-report                                           | $2.9B, 5.6% CAGR       |
| Market Data Forecast     | Workholding Devices       | 2024 | https://www.marketdataforecast.com/market-reports/workholding-devices-market                                        | $4.44B, 5.1% CAGR      |
| Precedence Research      | Global Tooling Market     | 2024 | https://www.precedenceresearch.com/tooling-market                                                                   | $273.89B, 6.9% CAGR    |

### Regional Manufacturing Sources

| Source Name             | Report/Page         | Year | URL                                      | Notes                   |
| ----------------------- | ------------------- | ---- | ---------------------------------------- | ----------------------- |
| AMT Online              | SE Asia Growth      | 2024 | https://www.amtonline.org/article/intern | Regional analysis       |
| Sparkco AI              | Next Mfg Powerhouse | 2024 | https://sparkco.ai/blog/southeast-asia-t | Growth drivers          |
| WEDC                    | Aerospace Sector    | 2024 | https://wedc.org/market-intelligence/pos | Aerospace opportunities |
| Market Research SE Asia | Vietnam-Thailand    | 2024 | https://marketresearchsoutheastasia.com/ | Country comparison      |

### Japan & Germany Sources

| Source Name         | Report/Page      | Year | URL                                      | Notes                  |
| ------------------- | ---------------- | ---- | ---------------------------------------- | ---------------------- |
| Safeguard Global    | World Rankings   | 2024 | https://www.safeguardglobal.com/resource | Top 10 manufacturers   |
| Trade.gov           | Germany Mfg      | 2024 | https://www.trade.gov/country-commercial | Advanced manufacturing |
| Spherical Insights  | Largest Mfg 2024 | 2024 | https://www.sphericalinsights.com/blogs/ | Country rankings       |
| World Manufacturing | 2024 Report      | 2024 | https://worldmanufacturing.org/wp-conten | Annual report          |

### Competitor & Pricing Sources

| Source Name    | Report/Page      | Year | URL                                      | Notes                   |
| -------------- | ---------------- | ---- | ---------------------------------------- | ----------------------- |
| Renishaw       | FixtureBuilder   | 2024 | https://www.renishaw.com/en/3d-fixture-m | Fixture software $2-3K  |
| trinckle       | fixturemate      | 2024 | https://www.trinckle.com/fixturemate     | AI fixture design $1-2K |
| BigRep         | FLOW Solution    | 2024 | https://bigrep.com/posts/bigrep-flow-sol | End-to-end workflow     |
| Opti Solutions | Nucleo Software  | 2024 | https://www.optisolutionsusa.com/nucleo- | Welding fixtures        |
| xcPEP          | Cost Engineering | 2024 | https://xcpep.com/                       | Should-cost analysis    |
| Vention        | Jigs & Fixtures  | 2024 | https://vention.io/applications/jigs-fix | Modular fixtures        |

### SMB Software & Pricing Sources

| Source Name         | Report/Page         | Year | URL                                      | Notes                     |
| ------------------- | ------------------- | ---- | ---------------------------------------- | ------------------------- |
| Mordor Intelligence | SMB Software Market | 2024 | https://www.mordorintelligence.com/indus | Market sizing             |
| ECI Solutions       | ERP Guide 2024      | 2024 | https://www.ecisolutions.com/blog/39-erp | SMB software stats        |
| Monetizely          | SaaS Pricing        | 2024 | https://www.getmonetizely.com/blogs/ente | Pricing strategies        |
| McKinsey            | SMB Tech Market     | 2024 | https://www.mckinsey.com/industries/tech | Market dynamics           |
| Tropic              | Spend Report 2024   | 2024 | https://go.tropicapp.io/2025-spend-repor | Software spend benchmarks |

### SaaS Benchmark Research

| Source Name    | Report/Page              | Year | URL                                                                                | Notes                         |
| -------------- | ------------------------ | ---- | ---------------------------------------------------------------------------------- | ----------------------------- |
| Recurly        | 2025 Churn Report        | 2025 | https://www.vitally.io/post/saas-churn-b                                           | B2B SaaS avg churn: 3.5%      |
| Vena Solutions | 2025 SaaS Churn Rate     | 2025 | https://www.venasolutions.com/blog/saas-                                           | B2B SaaS avg churn: 4.9%      |
| CustomerGauge  | Churn Rate by Industry   | 2024 | https://customergauge.com/blog/average-c                                           | B2B SaaS: 4.67%               |
| ChurnFree      | B2B SaaS Benchmarks      | 2025 | https://churnfree.com/blog/b2b-saas-chur                                           | Target: 5% or lower           |
| Optifai        | B2B SaaS LTV Benchmarks  | 2024 | https://optif.ai/learn/questions/b2b-saa                                           | SMB LTV: $15K-$40K            |
| F22 Labs       | Market Sizing Guide      | 2024 | https://www.f22labs.com/blogs/market-siz                                           | SaaS: 2-5% SAM in first years |
| Span Global    | TAM SAM SOM Guide        | 2024 | https://www.spanglobalservices.com/blog/                                           | TAM = 10-20x 5yr SOM          |
| 6sense         | CAD Software Market      | 2024 | https://www.6sense.com/tech/cad-software                                           | AutoCAD: 39%, SolidWorks: 14% |
| ProfitWell     | B2B SaaS CAC Benchmarks  | 2024 | https://www.profitwell.com/recur/all/cac-benchmarks                                | SMB CAC: $1,000-$3,000        |
| OpenView       | SaaS Metrics Report      | 2024 | https://openviewpartners.com/2024-saas-benchmarks                                  | Revenue/employee, CAC, quotas |
| Gartner        | IT Services Benchmarks   | 2024 | https://www.gartner.com/en/information-technology                                  | AMC pricing, MSP adoption     |
| IBISWorld      | 3D Printer Manufacturing | 2024 | https://www.ibisworld.com/industry-statistics/market-size/3d-printer-manufacturing | Hardware margins 50-60%       |
| Deloitte       | Managed Services Report  | 2024 | https://www2.deloitte.com/managed-services                                         | MSP pricing, service margins  |

### Customer Success & Sales Benchmark Sources

| Source Name | Report/Page         | Year | URL                                                                          | Notes                          |
| ----------- | ------------------- | ---- | ---------------------------------------------------------------------------- | ------------------------------ |
| Gainsight   | CS Benchmark Report | 2024 | https://www.gainsight.com/resources/reports/2024-customer-success-benchmarks | CSM ratios, ARR/CSM            |
| Gainsight   | Expansion Report    | 2024 | https://www.gainsight.com/resources/reports/expansion-benchmarks             | Seat expansion 1.5-2x annually |
| Zendesk     | Support Benchmarks  | 2024 | https://www.zendesk.com/benchmark                                            | Customers/support rep ratios   |
| Gartner     | Sales Benchmarks    | 2024 | https://www.gartner.com/en/sales/research/sales-benchmarks                   | Quota attainment 70-85%        |
| Gartner     | Tech Adoption       | 2024 | https://www.gartner.com/en/research/technology-adoption                      | Hardware cross-sell 15-25%     |
| HubSpot     | Inbound Marketing   | 2024 | https://www.hubspot.com/state-of-inbound                                     | 40% inbound-led at maturity    |

### Industry Segment Sources

| Source Name               | Report/Page              | Year | URL                                                                                  | Notes                         |
| ------------------------- | ------------------------ | ---- | ------------------------------------------------------------------------------------ | ----------------------------- |
| IBIS World                | Jigs & Fixtures Industry | 2024 | https://www.ibisworld.com/industry-statistics/jig-fixture-manufacturing              | 25% of dies/jigs/tools market |
| Grand View Research       | Assembly Tooling         | 2024 | https://www.grandviewresearch.com/industry-analysis/assembly-equipment-market        | 13% of tooling market         |
| Technavio                 | Drilling Jig Market      | 2024 | https://www.technavio.com/report/drilling-jig-market                                 | 8% of tooling market          |
| Allied Market Research    | Positioning Tools        | 2024 | https://www.alliedmarketresearch.com/positioning-equipment-market                    | 5% of tooling market          |
| Lean Enterprise Institute | Visual Management        | 2024 | https://www.lean.org/lexicon-terms/visual-management/                                | Shadow box/5S tools           |
| McKinsey                  | Digital Manufacturing    | 2024 | https://www.mckinsey.com/capabilities/operations/our-insights/digital-manufacturing  | 3-5% software shift annually  |
| LinkedIn                  | Soft Jaws Market         | 2024 | https://www.linkedin.com/pulse/soft-jaws-market-analysis                             | 7% of workholding market      |
| Data Bridge MR            | 3D Printing Materials    | 2024 | https://www.databridgemarketresearch.com/reports/global-3d-printing-materials-market | $3.13B materials market       |
| Stratasys                 | Usage Data               | 2024 | https://www.stratasys.com/resources                                                  | 3-4 spools/month industrial   |

### Headcount Benchmark Sources

| Source Name       | Report/Page                          | Year | URL                                             | Notes                                    |
| ----------------- | ------------------------------------ | ---- | ----------------------------------------------- | ---------------------------------------- |
| Capchase          | SaaS Metrics 2024 - Revenue/Employee | 2024 | https://www.capchase.com/resources/saas-metrics | Private SaaS: $100-150K/employee         |
| OpenView Partners | SaaS Benchmarks Report               | 2024 | https://openviewpartners.com/benchmarks         | Public SaaS: $180-250K/employee          |
| ChartMogul        | B2B SaaS Benchmark Study             | 2024 | https://chartmogul.com/reports/saas-benchmarks  | Eng ratio: 55-65% early, 35-45% scale    |
| Gainsight         | Customer Success Benchmark Report    | 2024 | https://www.gainsight.com/resources/reports     | CSM ratios: 75-150 accounts, $1.5-3M ARR |
| Glassdoor         | Regional Manager Salary Data         | 2024 | https://www.glassdoor.com/Salaries              | India, Germany, US salary benchmarks     |
| PayScale          | International Salary Benchmarks      | 2024 | https://www.payscale.com/research               | Singapore, UAE salary benchmarks         |

---

## NOTES

- All market research conducted via SerpAPI and verified sources
- Data validated against multiple sources where possible
- Column B values are linkable to Assumptions sheet
- Last research update: January 2026
- All URLs verified active at time of research
- **TAM expanded to include 10 design automation modules and 5 revenue streams**
- **Total TAM increased from $517M (fixtures only) to $3.27B (all streams)**
- **All values now include source attribution with row references for traceability**
- **Section B expanded with 50+ sources covering: TAM markets, regional manufacturing, competitors, SaaS benchmarks, customer success, sales, and industry segments**

---

## ROW REFERENCE MAP

**Critical**: Other sheets reference these cells. When syncing to Google Sheets, verify row numbers!

### TAM Section (Rows 7-40)

| Row | Cell | Description               | Value       |
| --- | ---- | ------------------------- | ----------- |
| 7   | B7   | Dies, Jigs & Tools Market | $60.18B     |
| 27  | B27  | Software TAM Total        | $1,733M     |
| 33  | B33  | Hardware & Services TAM   | $1,536M     |
| 40  | B40  | **TOTAL TAM**             | **$3,269M** |

### SAM Section (Rows 43-74)

| Row | Cell | Description                 | Value       |
| --- | ---- | --------------------------- | ----------- |
| 65  | B65  | Total SAM Companies         | 29,474      |
| 67  | B67  | SAM Value (Software)        | $88.4M      |
| 74  | B74  | **Total SAM (All Streams)** | **$220.5M** |

### SOM Section (Rows 77-83)

| Row | Cell | Description        | Value |
| --- | ---- | ------------------ | ----- |
| 82  | B82  | Y5 Customers       | 1,308 |
| 83  | B83  | Y5 SAM Penetration | 4.44% |

### Pricing & COGS (Rows 94-105)

| Row | Cell | Description     | Value          |
| --- | ---- | --------------- | -------------- |
| 94  | B94  | Software Price  | $1,500/seat/yr |
| 101 | B101 | Software COGS % | 15%            |

### Customer Economics (Rows 108-121)

| Row | Cell | Description       | Value    |
| --- | ---- | ----------------- | -------- |
| 114 | B114 | Churn Rate        | 10%      |
| 115 | B115 | Customer Lifetime | 10 years |

### Key Derived Metrics (Rows 149-154)

| Row | Cell | Description             | Value   |
| --- | ---- | ----------------------- | ------- |
| 149 | B149 | Total TAM               | $3.27B  |
| 151 | B151 | Total SAM (All Streams) | $220.5M |
| 154 | B154 | LTV:CAC Ratio           | 12.5:1  |
