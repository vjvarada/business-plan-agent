# Agent Decision Checklist - Financial Model Editing

> **Use this checklist EVERY TIME before editing a Google Sheets financial model**

## Pre-Edit Checklist

### Step 1: Identify the Change Type

**User wants to edit the financial model. What kind of change is it?**

- [ ] Read user request carefully
- [ ] Identify specific changes requested
- [ ] Classify as **Structural** or **Value Update**

### Step 2: Apply Decision Logic

**Answer these questions in order:**

#### Q1: Does it add or remove revenue streams?

- [ ] YES → **USE CONFIG-BASED REBUILD** (stop here)
- [ ] NO → Continue to Q2

#### Q2: Does it add or remove any rows in any sheet?

- [ ] YES → **USE CONFIG-BASED REBUILD** (stop here)
- [ ] NO → Continue to Q3

#### Q3: Does it change the structure/methodology of TAM/SAM/SOM?

- [ ] YES → **USE CONFIG-BASED REBUILD** (stop here)
- [ ] NO → Continue to Q4

#### Q4: Does it add or remove cost categories?

- [ ] YES → **USE CONFIG-BASED REBUILD** (stop here)
- [ ] NO → Continue to Q5

#### Q5: Does it extend the timeline (e.g., 5yr → 10yr)?

- [ ] YES → **USE CONFIG-BASED REBUILD** (stop here)
- [ ] NO → Continue to Q6

#### Q6: Is it a business model pivot or major restructuring?

- [ ] YES → **USE CONFIG-BASED REBUILD** (stop here)
- [ ] NO → Continue to Q7

#### Q7: Is it updating values (funding, growth, pricing)?

- [ ] YES → **USE LOCAL-FIRST WORKFLOW** ✅

#### Q8: Is it fixing/updating formulas (no structure change)?

- [ ] YES → **USE LOCAL-FIRST WORKFLOW** ✅

#### Q9: Is it a bulk value update (same structure)?

- [ ] YES → **USE LOCAL-FIRST WORKFLOW** ✅

#### Q10: Still unclear?

- [ ] **ASK USER FOR CLARIFICATION**
- [ ] **CONSULT: `directives/DECISION_TREE.md`**

---

## Execution Checklist

### If Using **Config-Based Rebuild**:

- [ ] Explain to user why rebuild is necessary
- [ ] Locate config file: `.tmp/<project>_config.json`
- [ ] Make requested changes to config JSON
- [ ] Run rebuild command:
  ```bash
  python execution/create_financial_model.py \
    --config .tmp/<project>_config.json \
    --output-id "EXISTING_SHEET_ID"
  ```
- [ ] Verify all sheets regenerated
- [ ] Inform user: "All formulas automatically regenerated"

### If Using **Local-First Workflow**:

- [ ] Explain the 4-step process to user
- [ ] **Step 1 - Download:**
  ```bash
  python execution/edit_financial_model.py --sheet-id "ID" --prepare
  ```
- [ ] **Step 2 - Edit:** (user or agent edits CSV files)
  - [ ] Edit `*_formulas.csv` files (NOT `*.csv`)
  - [ ] Make precise changes
- [ ] **Step 3 - Validate:**
  ```bash
  python execution/edit_financial_model.py --sheet-id "ID" --validate
  ```

  - [ ] Check validation output
  - [ ] Fix any errors before proceeding
- [ ] **Step 4 - Apply:**
  ```bash
  python execution/edit_financial_model.py --sheet-id "ID" --preview  # Optional
  python execution/edit_financial_model.py --sheet-id "ID" --apply
  ```

  - [ ] Confirm changes applied
  - [ ] Verify in Google Sheets

---

## Red Flag Keywords

**If you see these in user request → USE CONFIG REBUILD:**

- ❌ "add revenue stream"
- ❌ "new business line"
- ❌ "remove [revenue stream name]"
- ❌ "split [stream] into two"
- ❌ "restructure TAM"
- ❌ "change methodology"
- ❌ "add to 10 years"
- ❌ "extend timeline"
- ❌ "add cost category"
- ❌ "new geographic region"
- ❌ "add industry vertical"

**If you see these → USE LOCAL-FIRST:**

- ✅ "update funding"
- ✅ "change to $X"
- ✅ "increase growth rate"
- ✅ "fix pricing"
- ✅ "correct formula"
- ✅ "update all values"
- ✅ "change percentage"

---

## Common Mistakes to Avoid

### ❌ DON'T:

1. Use Local-First to add/remove revenue streams
2. Use Local-First when rows will shift
3. Edit Google Sheets directly via API calls
4. Skip validation before applying
5. Edit `*.csv` files (edit `*_formulas.csv` instead)
6. Use Config Rebuild for simple value updates

### ✅ DO:

1. Always consult decision tree for structural changes
2. Use Config Rebuild when adding/removing rows
3. Validate before applying changes
4. Explain approach to user
5. Preserve formulas (never hardcode)
6. Document changes in commit messages

---

## Example Scenarios

### Scenario A: "Change Seed Round from $500K to $1.6M"

**Decision:**

- Q1: Add/remove revenue streams? **NO**
- Q2: Add/remove rows? **NO**
- Q7: Update values? **YES**
- **→ LOCAL-FIRST WORKFLOW ✅**

**Execution:**

```bash
python execution/edit_financial_model.py --sheet-id "ID" --prepare
# Edit Cash_Flow_formulas.csv: Row 12, Col C: 500000 → 1600000
python execution/edit_financial_model.py --sheet-id "ID" --validate
python execution/edit_financial_model.py --sheet-id "ID" --apply
```

---

### Scenario B: "Add Training Services as 6th revenue stream"

**Decision:**

- Q1: Add/remove revenue streams? **YES**
- **→ CONFIG-BASED REBUILD ✅**

**Execution:**

```bash
# Edit .tmp/rapidtools_config.json - add to revenue_streams
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json \
  --output-id "1-Ss62..."
```

---

### Scenario C: "Restructure TAM to be vertical-based instead of geographic"

**Decision:**

- Q1: Add/remove revenue streams? **NO**
- Q2: Add/remove rows? **YES** (TAM rows will change)
- **→ CONFIG-BASED REBUILD ✅**

---

### Scenario D: "Update all Year 1 growth rates to 50%"

**Decision:**

- Q1-Q6: **NO**
- Q9: Bulk value update? **YES**
- **→ LOCAL-FIRST WORKFLOW ✅**

---

## Quick Reference

**Two Tools:**

1. **Config-Based Rebuild** = Structural changes (add/remove streams, restructure)
2. **Local-First Workflow** = Value updates (pricing, growth, funding)

**One Rule:**

- **Adds/removes rows? → Config Rebuild**
- **Just changing values? → Local-First**

**Full Documentation:**

- Decision tree: `directives/DECISION_TREE.md`
- Editing guide: `directives/EDITING_WORKFLOW.md`
- Implementation: `directives/LOCAL_FIRST_IMPLEMENTATION.md`

---

## Self-Check Before Proceeding

Before executing ANY edit to a financial model:

- [ ] I have identified the change type (structural vs value)
- [ ] I have consulted the decision tree
- [ ] I know which tool to use (Config Rebuild or Local-First)
- [ ] I can explain to the user why this approach is correct
- [ ] I understand the downstream impact on formulas

**If any checkbox is unchecked → STOP and consult `directives/DECISION_TREE.md`**
