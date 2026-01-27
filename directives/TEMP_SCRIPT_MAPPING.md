# Temporary Script to Reusable Pattern Mapping

This guide shows which `.tmp/` scripts contain reusable patterns documented in `REUSABLE_PATTERNS.md`.

## High-Value Scripts (Immediately Reusable)

### 1. Sheet Linkage Analysis
**Reusable Pattern:** find_sheet_linkages()  
**Source Scripts:**
- `.tmp/find_linkages.py`  **BEST** - Complete linkage finder with value display
- `.tmp/analyze_sources_sheet.py` - Structure analysis
- `.tmp/trace_dependencies.py` - Formula dependency tracer
- `.tmp/show_links.py` - Simplified linkage viewer

**When to Use:** Before restructuring any sheet that other sheets reference

---

### 2. Business Plan Credibility Audit
**Reusable Pattern:** audit_business_plan()  
**Source Scripts:**
- `.tmp/audit_assumptions.py`  **BEST** - Comprehensive 5-issue credibility audit
- `.tmp/audit_full_assumptions.py` - Extended validation
- `.tmp/audit_assumptions_cac.py` - CAC-specific checks
- `.tmp/audit_customer_economics.py` - Unit economics validation
- `.tmp/audit_revenue_correlation.py` - Revenue logic verification

**When to Use:** After completing business plan, before sharing with investors

**Key Issues It Catches:**
- Math errors (e.g., 800  60%  $1,200 = $960K  should be $576K)
- Unsourced TAM claims (e.g., "+$6B tooling CAD" with no citation)
- Missing timeframes (e.g., "$292B" without "2023-2030" label)
- Point estimates vs ranges (e.g., "$15B"  "$9-15B range")
- Unsub stantiated percentages (e.g., "30% will convert" with no benchmark)

---

### 3. Sheet Restructuring with Preservation
**Reusable Pattern:** restructure_sheet_preserve_formulas()  
**Source Scripts:**
- `.tmp/update_sources_sheet.py`  **BEST** - Full restructure with linkage preservation
- `.tmp/rebuild_sources_complete.py` - Complete sheet rebuild
- `.tmp/restructure_sources.py` - Simpler restructure
- `.tmp/consolidate_customer_economics.py` - Merge duplicate sections

**When to Use:** Changing sheet layout while preserving downstream formulas

**Critical Steps:**
1. Use `find_linkages.py` to identify critical cells
2. Clear sheet but preserve cell positions for linked values
3. Apply all updates in batch with rate limiting
4. Use `verify_linkages.py` to confirm formulas still work

---

### 4. Market Research Consolidation
**Reusable Pattern:** consolidate_market_research()  
**Source Scripts:**
- `.tmp/comprehensive_sources.py`  **BEST** - Aggregates all SERP data into structured sources
- `.tmp/add_market_research_section.py` - Formats for business plan
- `.tmp/market_analysis.py` - TAM/SAM extraction

**Input:** Multiple `.tmp/market_research_*.json` files from SERP API  
**Output:** Structured TAM/SAM data with sources and URLs

**Example:**
```
market_research_jigs.json            TAM: $8.5B (jigs & fixtures)
market_research_vacuum_casting.json  TAM: $2.1B (vacuum casting)
...consolidate_market_research()...
 Total TAM: $35B conservative, $146B with expansion
 35 sources with URLs
```

---

### 5. Formula Verification
**Reusable Pattern:** verify_formulas_still_work()  
**Source Scripts:**
- `.tmp/verify_linkages.py`  **BEST** - Complete verification with error detection
- `.tmp/verify_assumptions.py` - Assumptions sheet check
- `.tmp/verify_complete.py` - All-sheet verification
- `.tmp/verify_sources_direct.py` - Sources & References check
- `.tmp/check_linkage.py` - Simplified linkage test

**When to Use:** After any sheet restructuring or bulk formula updates

**What It Checks:**
- Critical cells have expected values
- No #REF!, #ERROR!, #DIV/0! errors
- Sheet references are valid
- Labels match expected names

---

## Medium-Value Scripts (Patterns Worth Extracting)

### 6. Google Docs Batch Updates
**Source Scripts:**
- `.tmp/fix_credibility_issues.py` - Fixed 5 issues in one batch
- `.tmp/update_business_plan_doc.py` - Expanded to 8 modules
- `.tmp/update_market_expansion.py` - Market expansion narrative
- `.tmp/add_soft_jaws.py` - Added 8th module

**Reusable Pattern:**
```python
def batch_update_document(doc_id, replacements):
    requests = [{'replaceAllText': {...}} for old, new in replacements]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests})
```

**Benefit:** Single API call vs multiple calls = faster + no rate limits

---

### 7. Rate Limit Handling
**Source Scripts:**
- `.tmp/apply_formatting_batched.py` - Batched formatting with delays
- `.tmp/batch_format_sources.py` - Rate-limited formatting
- `.tmp/batch_zebra.py` - Zebra striping with delays

**Key Pattern:** `time.sleep(2)` between batches + `batch_update()` instead of individual calls

**Before (Hit rate limit):**
```python
for row in range(100):
    format_cell_range(sheet, f'A{row}:F{row}', fmt)  # 100 API calls  QUOTA EXCEEDED
```

**After (Works):**
```python
requests = [{'repeatCell': {...}} for row in range(100)]
sheet.spreadsheet.batch_update({'requests': requests})  # 1 API call
time.sleep(2)
```

---

### 8. Standardized Formatting
**Source Scripts:**
- `.tmp/final_format.py` - Applied standard color scheme
- `.tmp/format_sources_complete.py` - Complete Sources & References formatting
- `.tmp/apply_zebra_formatting.py` - Zebra stripe pattern

**Reusable Asset:** `execution/format_sheets.py` + `Colors` class

**Usage:**
```python
from format_sheets import SheetFormatter, Colors
formatter = SheetFormatter(spreadsheet)
formatter.format_assumptions_sheet()  # Standard colors, fonts, borders
```

---

### 9. Number Format Application
**Source Scripts:**
- `.tmp/apply_number_formats.py` - Currency, percentages, numbers
- `.tmp/fix_pct.py` - Fixed percentage formatting bug
- `.tmp/fix_number_format.py` - Corrected number patterns

**Key Learning:** Always specify pattern, not just type

```python
# WRONG - shows 0.1 instead of 10%
sheet.format('B70', {'numberFormat': {'type': 'PERCENT'}})

# CORRECT - shows 10.00%
sheet.format('B70', {'numberFormat': {'type': 'PERCENT', 'pattern': '0.00%'}})
```

---

## Low-Value Scripts (One-Off / Debugging)

### Debugging Scripts (Not Reusable)
- `.tmp/debug.py` through `.tmp/debug7.py` - One-off troubleshooting
- `.tmp/check_*.py` (80+ files) - Specific issue investigation
- `.tmp/fix_*.py` (120+ files) - Targeted bug fixes

**Learning:** These are valuable for **understanding the problem**, not for reuse.

**Example:** `.tmp/check_sources_values.py` revealed that TAM was $517.5M (old fixture-only model), which led to creating `.tmp/update_sources_sheet.py` to update to $35B-$146B.

---

### Analysis Scripts (Informative but not Reusable)
- `.tmp/analyze_*.py` - One-time analyses
- `.tmp/review_*.py` - Quality checks
- `.tmp/audit_*.py` - Specific audits

**Value:** These identified issues but aren't reusable as-is. Extract the **pattern**, not the script.

---

## Extraction Recommendations

### Scripts to Convert to Reusable Tools

1. **`.tmp/find_linkages.py`**  `execution/analyze_sheet_linkages.py`  DONE
   - Generalize to work with any source/target sheet pair
   - Add CLI args: --sheet-id, --source, --target

2. **`.tmp/audit_assumptions.py`**  `execution/audit_business_plan.py`
   - Generalize to check any business plan document
   - Add CLI args: --doc-id, --mode [tam|sam|math|timeframe|all]

3. **`.tmp/verify_linkages.py`**  `execution/verify_sheet_integrity.py`
   - Check any sheet for formula errors
   - Add CLI args: --sheet-id, --sheet [name or 'all']

4. **`.tmp/comprehensive_sources.py`**  `execution/consolidate_market_research.py`
   - Aggregate any set of market_research_*.json files
   - Add CLI args: --research-dir, --output, --format [json|markdown]

### Functions to Extract into execution/utils.py

```python
# execution/utils.py

def batch_update_with_rate_limiting(sheet, requests, batch_size=10, delay=2):
    """Execute sheet updates in batches to avoid rate limits"""
    ...

def apply_standard_colors(sheet, row_ranges):
    """Apply standard color palette to sheet ranges"""
    ...

def validate_math_in_doc(doc_content):
    """Find calculation errors in document text"""
    ...

def extract_tam_sam_from_serp(serp_results):
    """Extract market size data from SERP API results"""
    ...
```

---

## Summary: Top Scripts Worth Preserving

| Priority | Script | Reusable As | Value |
|----------|--------|-------------|-------|
|  HIGH | `.tmp/find_linkages.py` | analyze_sheet_linkages.py | Critical before restructures |
|  HIGH | `.tmp/audit_assumptions.py` | audit_business_plan.py | Ensures investor credibility |
|  HIGH | `.tmp/update_sources_sheet.py` | restructure_sheet() pattern | Safe restructuring |
|  HIGH | `.tmp/verify_linkages.py` | verify_sheet_integrity.py | Post-change validation |
|  MED | `.tmp/comprehensive_sources.py` | consolidate_market_research.py | TAM/SAM aggregation |
|  MED | `.tmp/fix_credibility_issues.py` | batch_doc_update() pattern | Efficient doc edits |
|  MED | `.tmp/apply_formatting_batched.py` | batch_format() pattern | Avoid rate limits |
|  LOW | `.tmp/check_*.py` (80 files) | Debugging reference only | One-off investigations |
|  LOW | `.tmp/fix_*.py` (120 files) | Debugging reference only | Specific bug fixes |

**Total Scripts Created:** ~350  
**Reusable Patterns Identified:** 10  
**High-Value Scripts to Preserve:** 7

**Recommendation:** Move top 7 scripts from `.tmp/` to `execution/` with generalized parameters and CLI interfaces. Keep others in `.tmp/` as reference for similar future issues.
