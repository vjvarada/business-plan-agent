# Financial Model Editing Decision Tree

> **For Agents: Use this decision tree to choose the right editing approach**

## Scope Clarification

- This decision tree applies to **existing** Google Sheets models that need edits.
- For **new model creation from scratch**, use the step-gated workflow in `directives/business_planning.md` (Create Local → Validate Local → Upload → Audit).

## The Central Question

**"What type of change is the user requesting?"**

```
USER WANTS TO EDIT FINANCIAL MODEL
    ↓
    Decision Point 1: Scope of Change
    ├─ MINOR EDIT (values, single formula fix)
    │   → Use Local-First Workflow
    │
    ├─ STRUCTURAL CHANGE (add/remove revenue streams, change TAM methodology)
    │   → Use Config-Based Rebuild
    │
    └─ BULK UPDATE (many cells, same pattern)
        → Use Local-First Workflow
```

## Decision Point 1: Scope Assessment

### Use **Local-First Workflow** when:

✅ **Updating values without changing structure:**

- Change funding amounts ($500K → $1.6M)
- Update growth rates (40% → 50%)
- Fix pricing (€2,500 → €3,000)
- Correct COGS percentages

✅ **Fixing individual formulas:**

- Replace hard-coded value with formula
- Fix broken reference (#REF! error)
- Update single cross-sheet reference

✅ **Making consistent bulk updates:**

- Update all Year 1 growth rates
- Change tax rate across all years
- Fix formatting (percentages showing as decimals)

**Command:**

```bash
python execution/edit_financial_model.py --sheet-id "ID" --prepare
# Edit CSV files
python execution/edit_financial_model.py --sheet-id "ID" --validate
python execution/edit_financial_model.py --sheet-id "ID" --apply
```

---

### Use **Config-Based Rebuild** when:

✅ **Adding/removing business lines (revenue streams):**

- Add "Training Services" as 6th revenue stream
- Remove "Job Work Services"
- Split "Software Subscription" into two tiers
- Add geographic expansion streams (India, SE Asia, Americas)

✅ **Changing financial model structure:**

- Extend from 5 years to 10 years
- Add new cost categories (R&D, Marketing)
- Restructure TAM/SAM/SOM methodology
- Change headcount planning approach

✅ **Major business model pivots:**

- Switch from B2B to B2C pricing
- Change from subscription to transaction model
- Add multi-currency support
- Implement tiered pricing

**Command:**

```bash
# 1. Update config
# Edit .tmp/rapidtools_config.json - add/remove revenue streams, change structure

# 2. Rebuild model
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json \
  --output-id "EXISTING_SHEET_ID"

# This overwrites the existing model with new structure
# All formulas automatically regenerated with correct linkages
```

---

## Decision Point 2: Row Insertion Impact

**Question:** "Will this change require adding/removing rows?"

### If NO (rows stay the same):

→ **Local-First is safe**

- Formulas won't break
- Row references stay valid
- Quick and clean

### If YES (rows will shift):

→ **Config-Based Rebuild is safer**

**Why?** Adding row 25 breaks ALL formulas that reference rows 25+:

```
Before: =Revenue!C30    (refers to Total Revenue)
After:  =Revenue!C30    (now refers to wrong row - off by 1!)
```

Manual fix would require updating hundreds of formulas across all sheets.

---

## Real-World Scenarios

### Scenario 1: "Change Seed Round from $500K to $1.6M"

**Analysis:**

- ✅ Value change only
- ✅ No rows added/removed
- ✅ No structure change

**Decision:** **Local-First Workflow**

```bash
python execution/edit_financial_model.py --sheet-id "ID" --prepare
# Edit Cash_Flow_formulas.csv: Row 12, Col C: 500000 → 1600000
python execution/edit_financial_model.py --sheet-id "ID" --apply
```

**Time:** 3 minutes

---

### Scenario 2: "Add 'Training Services' as 6th revenue stream"

**Analysis:**

- ❌ Adds new rows to Revenue sheet
- ❌ Adds new rows to Assumptions sheet
- ❌ Total Revenue formula needs updating
- ❌ P&L needs new revenue line
- ❌ Operating Costs needs new COGS line
- ❌ All downstream formulas shift

**Decision:** **Config-Based Rebuild**

```bash
# Edit .tmp/rapidtools_config.json
# Add to revenue_streams array:
{
    "name": "Training Services",
    "description": "On-site and virtual training",
    "price": 5000,
    "volume": 10,
    "growth": 0.30,
    "cogs_pct": 0.40
}

# Rebuild
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json \
  --output-id "1-Ss62..."
```

**Time:** 2 minutes (automated formula regeneration)

---

### Scenario 3: "Change TAM calculation methodology"

**Analysis:**

- ❌ Affects Sources & References sheet structure
- ❌ May add/remove rows for new TAM segments
- ❌ Assumptions sheet references need updating
- ❌ Multiple interconnected changes

**Decision:** **Config-Based Rebuild**

**Alternative (if just updating formulas):**

- If TAM rows stay at same positions → Local-First
- If TAM structure changes → Config-Based Rebuild

---

### Scenario 4: "Update all growth rates to be 10% lower"

**Analysis:**

- ✅ Multiple value changes
- ✅ No structure change
- ✅ No rows added/removed
- ✅ Same formula pattern

**Decision:** **Local-First Workflow**

```bash
python execution/edit_financial_model.py --sheet-id "ID" --prepare
# Bulk edit Assumptions_formulas.csv:
#   Find all growth values, reduce by 10%
#   Or use find-replace in text editor
python execution/edit_financial_model.py --sheet-id "ID" --apply
```

**Time:** 5 minutes

---

### Scenario 5: "Remove 'Job Work Services' revenue stream"

**Analysis:**

- ❌ Removes rows from Revenue sheet
- ❌ All formulas below shift up
- ❌ Total Revenue formula needs updating
- ❌ Cross-sheet references break

**Decision:** **Config-Based Rebuild**

```bash
# Edit .tmp/rapidtools_config.json
# Remove from revenue_streams array

# Rebuild
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json \
  --output-id "1-Ss62..."
```

---

## Comparison Table

| Change Type               | Examples                                | Recommended Approach | Time     | Risk |
| ------------------------- | --------------------------------------- | -------------------- | -------- | ---- |
| **Value updates**         | Funding amounts, growth rates, prices   | Local-First          | 3-5 min  | Low  |
| **Formula fixes**         | Fix #REF!, convert hardcoded to formula | Local-First          | 3-5 min  | Low  |
| **Bulk updates**          | Update all tax rates, all year 1 values | Local-First          | 5-10 min | Low  |
| **Add revenue stream**    | New product line, new service           | Config Rebuild       | 2 min    | None |
| **Remove revenue stream** | Discontinue product                     | Config Rebuild       | 2 min    | None |
| **Restructure TAM/SAM**   | Change methodology, add segments        | Config Rebuild       | 2-5 min  | None |
| **Extend timeline**       | 5 years → 10 years                      | Config Rebuild       | 2 min    | None |
| **Add cost categories**   | New fixed cost line items               | Config Rebuild       | 2 min    | None |

---

## Agent Decision Flowchart

```
START: User requests financial model edit
    ↓
Q1: Does it add/remove revenue streams?
    YES → Config-Based Rebuild
    NO  ↓
Q2: Does it add/remove rows anywhere?
    YES → Config-Based Rebuild
    NO  ↓
Q3: Does it change sheet structure/layout?
    YES → Config-Based Rebuild
    NO  ↓
Q4: Is it updating values or fixing formulas?
    YES → Local-First Workflow
    NO  ↓
Q5: Is it bulk find-replace operation?
    YES → Local-First Workflow
    NO  ↓
→ ASK USER FOR CLARIFICATION
```

---

## Configuration File Structure

For **Config-Based Rebuild**, the agent edits `.tmp/rapidtools_config.json`:

```json
{
    "company": "RapidTools",
    "general": {
        "tax_rate": 0.25,
        "capex_y0": 150000,
        "equity_y0": 500000,
        ...
    },
    "revenue_streams": [
        {
            "name": "Software Subscription",
            "price": 2500,
            "volume": 25,
            "growth": 0.60,
            "cogs_pct": 0.15
        },
        {
            "name": "Training Services",  // ← ADD NEW STREAM HERE
            "price": 5000,
            "volume": 10,
            "growth": 0.30,
            "cogs_pct": 0.40
        }
    ],
    "fixed_costs": [
        {"name": "Salaries and Benefits", "value": 216000},
        {"name": "R&D", "value": 50000}  // ← ADD NEW COST HERE
    ],
    "customer_acquisition": {
        "cac": 500,
        "churn_rate": 0.08,
        ...
    }
}
```

**What gets auto-regenerated:**

- All 14 sheets
- All 1,418+ formulas
- All cross-sheet references
- All linkages preserved
- Formatting applied

**Time:** ~30 seconds for full rebuild

---

## Key Principles

### 1. **Local-First = Surgical Edits**

- Like using a scalpel
- Precise, targeted changes
- Requires understanding of impact
- Best for value updates and formula fixes

### 2. **Config-Based = Architectural Changes**

- Like using blueprints to rebuild
- Comprehensive, structural changes
- Automatic formula regeneration
- Best for adding/removing business lines

### 3. **When in Doubt:**

If the change involves:

- ❌ Adding rows
- ❌ Removing rows
- ❌ Changing TAM/SAM structure
- ❌ New revenue streams
- ❌ New cost categories

→ **Use Config-Based Rebuild**

It's faster, safer, and guarantees no broken formulas.

---

## Summary for Agents

**ASK YOURSELF:**

1. **"Will rows shift?"** → Config Rebuild
2. **"Is this a business model change?"** → Config Rebuild
3. **"Just updating values?"** → Local-First
4. **"Fixing a formula?"** → Local-First

**DEFAULT RULE:**

- Changes to **structure/business model** → Config Rebuild
- Changes to **values/parameters** → Local-First

**NEVER:**

- Don't use Local-First to add/remove revenue streams
- Don't use Config Rebuild for simple value updates
- Don't edit Google Sheets directly via API calls
