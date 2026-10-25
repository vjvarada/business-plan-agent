# Aroh — Financial Model Tooling Gaps (found 2026-10-24, before Stage 4)

Stage 4 `--local-first` runs `execution/build_financial_model.py` (`run_stepwise_workflow.py:309-330`).

| Need for Aroh | Supported today? | Fix | Risk |
| ------------- | ---------------- | --- | ---- |
| 3-year horizon | Yes, via `--years` CLI flag (default 11); workflow doesn't pass it; `num_years` config key ignored (doc says it's read — `SHEET_BUILD_GUIDE.md:45`) | Read `config["num_years"]` as default + pass through workflow (~5 lines) | Low |
| Org-level recurring fee × live customers | Partial — generic price × volume with fixed growth | Customer-cohort revenue (new, churned, live) | Medium |
| One-time setup fee per **new** org | No | Setup stream driven by new customers | Medium |
| Customer cohorts / churn | Display-only (`customer_acquisition` never referenced) | Wire into revenue | Medium |
| Per-role hiring plan (FDEs hired ahead of demand) | Department × growth % only | Per-year hire counts by role | Medium |
| FX (₹95/US$ for AI costs) | No — single currency label | Convert USD inputs to ₹ in config prep | Low |
| Monthly Year 1 | No | Out of scope unless asked | High |

**Stage 2 extraction (found 2026-10-24):** `extract_config_from_plan.py` starts from RapidTools template defaults and its regexes didn't match Aroh's sections, so the first `aroh_config.json` was 100% RapidTools values (software/hardware TAM, SE Asia SAM, $3M seed) yet passed `validate_config.py`. Fixed: the extractor now writes `_provenance` and exits 2 when core keys (tam, sam, som, revenue_streams, funding) fall back to defaults. The invalid config was deleted. **Aroh's model config will be built from the assumption register and `revenue_calc.py` / `sizing_calc.py` outputs, not extracted from prose.**

**Resolved 2026-10-25 (A-058):** `build_financial_model.py` now supports per-year plans (`*_by_year`, `year_labels`, `period_months`, `in_cogs`, `capex_by_year`, `tax_loss_carryforward`) — see `directives/SHEET_BUILD_GUIDE.md` → "Per-Year Plans". Regression: three RapidTools configs rebuild cell-for-cell identical. Aroh base and upside models tie out to the calculation scripts within 0.5%, balance every period and keep cash ≥ 0.

**Avoid:** `create_financial_model.py` (Google Sheets) and `create_financial_model_local.py` for 3-year — hardwired 11 columns.

**Quirk:** Assumptions volume cells sit one column right of other sheets (`:661` vs `:849-850`); consistent but check at small year counts.

**Decision needed at Stage 4:** extend `build_financial_model.py` (cohort revenue, setup fee, per-role hiring) vs a dedicated SaaS model builder.
