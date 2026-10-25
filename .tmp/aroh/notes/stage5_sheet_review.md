# Aroh — Stage 5 sheet-by-sheet review

> **Status:** Prepared for owner approval. No sheet is approved yet (A-092: approvals are the owner's).
> **Model:** `.tmp/aroh/financial_model/aroh_financial_model.xlsx` (base), `..._downside.xlsx`
> **Automated checks (rerun after the sheet fixes):** formulas compute with no errors; balance check 0 in all four periods; cash ≥ 0 (₹14.96 / 32.53 / 66.07 / 121.28 Cr); EBITDA ties to the revenue and cost calculators at 0.00% (−2.70 / 9.93 / 20.35 / 41.67 Cr); RapidTools models rebuild identically.

**Pre-launch presentation:** Period 1 is a **five-month stub (Nov 2026–Mar 2027), not annualised**. Fifty customers are onboarded in March and billed annually upfront, so billings are large but recognised revenue is small; the rest sits in deferred revenue (a liability) and is recognised in FY2027–28. Cash is therefore ahead of profit. Growth in the first full year is shown as "n/m".

| # | Sheet | Check result | Caveat for the owner |
|---|---|---|---|
| 1 | Sources & References | Units now ₹ M; Section B lists 10 real sources | SOM target is recognised FY2029–30 revenue |
| 2 | Assumptions | Ties to register | Churn/price are founder-stated, unproven |
| 3 | Headcount Plan | Per-year plans (4→4→6→10 devs; FDEs 2→4→6→12) | Delivery salaries sit in COGS |
| 4 | Revenue | Anniversary-aware cohorts, no double count | 70% pilot conversion untested |
| 5 | Operating Costs | Dev cloud, production floor ₹4L/mo + ₹3,000/org/month | Infra per org is a chosen value (measured ≈ ₹880) |
| 6 | P&L | Pre-launch loss; profitable from FY2027–28 | ~45% FY2029–30 EBITDA margin needs owner acceptance |
| 7 | Cash Flow | Δ deferred revenue included | Depends on March receipts arriving on time |
| 8 | Balance Sheet | Balances; deferred revenue shown as liability | — |
| 9 | Summary | First-period growth "n/m" | — |
| 10 | Sensitivity Analysis | Runs | Crude: it does not replace the scripted stress tests in Section 10 |
| 11 | Valuation | Shows "n/a — no outside capital" return in base case | WACC and terminal growth are set but the template DCF barely uses them; exit-multiple value is the headline |
| 12 | Break-even Analysis | Delivery salaries counted fixed | — |
| 13 | Funding Cap Table | DEWiN ₹5 Cr marked existing shareholders, 0 dilution | Seed terms are illustrative |
| 14 | Charts Data | Populates | — |

## Open owner confirmations
1. ₹1.2L laptops for non-engineers (A-083).
2. ₹2 Cr standby shareholder loan (A-091).
3. Pre-launch team (A-066).
4. Whether the ~45% FY2029–30 EBITDA margin may be headlined.
5. Re-approval of Sections 05, 06, 09, 10, 11 after the changes.

## To record approvals
`python execution/run_stepwise_workflow.py --project aroh --stage 5 --execute --local-first --approve-sheet "<sheet name>"` — only on the owner's instruction.
