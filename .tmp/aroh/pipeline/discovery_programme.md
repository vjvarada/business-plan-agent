# Aroh Discovery Programme — 50–100 owner interviews

> **Purpose:** turn the plan's founder-stated conviction into evidence before 31 March 2027.
> **Status:** Draft for owner review. All plan figures remain unproven until these interviews and the pilots report.

## What each interview must settle

| Plan assumption | Interview question | Evidence that supports it | Evidence that kills it |
|---|---|---|---|
| Owner is the integration layer (the enemy) | "Walk me through how you learned last week's number that mattered." | Owner names ≥3 sources they stitch by hand | Owner has a trusted dashboard already |
| SAM filter: ₹100–5,000 Cr, manufacturing / distribution / B2B services | Revenue, sector, systems in use | In band, ≥3 systems | Single ERP covers everything |
| Budget migration (Layer 2) | "What do you pay today for the people and tools that do this?" | Names a CoS/EA/MIS/analyst cost ≥ ₹20L | No budget line, "I do it myself" |
| Price ₹1.5L/month org fee (A-026; ₹10K/seat extras) | Van Westendorp: too cheap / cheap / expensive / too expensive | Median "expensive" above the price | Price at or above "too expensive" for >40% |
| Adoption easier than CRM/ERP | "What stopped your last tool rollout?" | Failure was effort/training | Failure was trust/data quality |
| Free 6-week pilot converts at 70% | "If it showed X by week 6, would you sign on the spot?" | Names who signs and when | "Need board / committee" |

## Process
1. Source from DEWiN relationships first (P01–P10, D01–D50 in `prospect_tracker.csv`), then second-degree introductions.
2. 30-minute call; record in the tracker (stage, probability, ACV, objections, next step) the same day.
3. Do not pitch the product first; ask the starting-loop question, then show the Owner Intelligence one-pager.
4. Weekly: run `python execution/pipeline_summary.py --file .tmp/aroh/pipeline/prospect_tracker.csv`.

## Gates
- **By 31 Dec 2026:** 10 pilots live; ≥30 interviews logged.
- **By 31 Jan 2027:** ≥50 named direct prospects with probability set; weighted expected signings ≥35, else revisit the 50-by-March milestone.
- **By 31 Mar 2027:** ≥25 paid contracts is the minimum to stay on the base path (Section 11 early warning).
