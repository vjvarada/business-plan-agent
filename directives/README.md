# Directives - Agent Operating Instructions

This folder contains the Standard Operating Procedures (SOPs) for the business planning agent.

## 📖 Reading Order for Agents

### **START HERE** - Core Decision Logic

1. **[DECISION_TREE.md](DECISION_TREE.md)** ⚠️ **READ FIRST BEFORE ANY SHEET EDIT**
   - Chooses between Local-First vs Config-Based Rebuild
   - CRITICAL: Prevents breaking 1,418+ formulas
   - **Always consult before editing financial models**

### Main Workflows

2. **[business_planning.md](business_planning.md)** - Complete business planning SOP
   - 14-step workflow from idea to finished plan
   - Step-gated financial model creation workflow (mandatory)
   - Dependency-gated data collection + user confirmation protocol
   - Consulting-grade controls (source tiering, assumption register, sign-off cards)
   - Sheet structure (14 sheets)
   - Formula linkage principles
   - Integration with execution scripts

3. **[EDITING_WORKFLOW.md](EDITING_WORKFLOW.md)** - Local-First editing guide
   - 5-step workflow: Download → Edit → Validate → Preview → Apply
   - Real-world examples
   - Troubleshooting guide
   - Best practices

4. **[LOCAL_FIRST_IMPLEMENTATION.md](LOCAL_FIRST_IMPLEMENTATION.md)** - Technical details
   - How snapshot download works
   - CSV format structure
   - Validation logic
   - Sync mechanism

### Reference Material

5. **[FINANCIAL_MODEL_TEMPLATE.md](FINANCIAL_MODEL_TEMPLATE.md)** - RapidTools template
   - Complete sheet structure
   - Formula patterns
   - Formatting standards
   - Row-by-row layouts

6. **[REUSABLE_PATTERNS.md](REUSABLE_PATTERNS.md)** - Code patterns
   - Sheet linkage analysis
   - Formula verification
   - Restructuring patterns
   - Credibility audits

## ⚠️ Critical Rules

### Before Editing ANY Financial Model:

```
Q: Does the edit add/remove revenue streams?
   YES → Use create_financial_model.py with updated config
   NO ↓

Q: Does the edit add/remove rows anywhere?
   YES → Use create_financial_model.py with updated config
   NO ↓

Q: Does the edit change business model structure?
   YES → Use create_financial_model.py with updated config
   NO ↓

Q: Is it updating values or fixing formulas?
   YES → Use edit_financial_model.py (Local-First)
```

**Full decision tree:** [DECISION_TREE.md](DECISION_TREE.md)

## Common Scenarios

| User Request                                  | Use This                             | Why                              |
| --------------------------------------------- | ------------------------------------ | -------------------------------- |
| "Add Training Services as 6th revenue stream" | `create_financial_model.py --config` | Adds rows → all formulas shift   |
| "Change Seed Round from $500K to $1.6M"       | `edit_financial_model.py`            | Value change only                |
| "Restructure TAM to be vertical-based"        | `create_financial_model.py --config` | Changes sheet structure          |
| "Update all growth rates to 50%"              | `edit_financial_model.py`            | Bulk value update                |
| "Remove Job Work Services"                    | `create_financial_model.py --config` | Removes rows → formulas break    |
| "Fix hard-coded TAM value to formula"         | `edit_financial_model.py`            | Formula fix, no structure change |

## Tools Available

### Execution Scripts

| Script                       | Purpose                    | When to Use                    |
| ---------------------------- | -------------------------- | ------------------------------ |
| `run_stepwise_workflow.py`   | Stage-gated orchestration across business + financial model | Primary step-by-step execution |
| `validate_script_registry.py`| Validate that all execution scripts are mapped to stages | Governance / CI sanity check |
| `create_financial_model.py`  | Create/rebuild full 14-sheet model | New model creation (preferred), structural changes |
| `create_financial_model_local.py` | Create reduced local Excel draft | Offline prototyping only (not production baseline) |
| `validate_excel_model.py`    | Validate local Excel formulas | Before uploading new model |
| `sync_to_cloud.py`           | Upload local .xlsx to Google Sheets | After validation passes |
| `edit_financial_model.py`    | Local-First editing helper | Value updates, formula fixes   |
| `download_model_snapshot.py` | Download to CSV            | Part of Local-First workflow   |
| `sync_snapshot_to_sheets.py` | Sync CSV back to Sheets    | Part of Local-First workflow   |
| `validate_model_snapshot.py` | Pre-flight validation      | Part of Local-First workflow   |
| `format_sheets.py`           | Apply formatting           | After any edit                 |
| `audit_financial_model.py`   | Comprehensive validation   | Verify model integrity         |
| `repair_financial_model.py`  | Fix common issues          | When formulas break            |

### Quick Commands

```bash
# Canonical New Model Creation (step-gated)
python execution/create_financial_model.py --company "<CompanyName>" --config .tmp/<project>/config/<project>_config.json --from-template
python execution/verify_template_copy.py --sheet-id "<SHEET_ID>"
python execution/audit_financial_model.py --sheet-id "<SHEET_ID>" --mode comprehensive
python execution/verify_sheet_integrity.py --sheet-id "<SHEET_ID>"

# Full stage-gated orchestration (recommended)
python execution/run_stepwise_workflow.py --project <project> --stage 0 --company "<CompanyName>" --config .tmp/<project>/config/<project>_config.json --execute
python execution/run_stepwise_workflow.py --project <project> --stage 1 --research-dir .tmp/<project>/research --execute
python execution/run_stepwise_workflow.py --project <project> --stage 2 --sections-dir .tmp/<project>/business_plan/sections --execute
python execution/run_stepwise_workflow.py --project <project> --stage 3 --config .tmp/<project>/config/<project>_config.json --execute
python execution/run_stepwise_workflow.py --project <project> --stage 4 --company "<CompanyName>" --config .tmp/<project>/config/<project>_config.json --execute
python execution/run_stepwise_workflow.py --project <project> --stage 5 --sections-dir .tmp/<project>/business_plan/sections --execute

# Registry coverage check
python execution/validate_script_registry.py

# Config-Based Rebuild (for structural changes)
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json \
  --output-id "EXISTING_SHEET_ID"

# Local-First Workflow (for value updates)
python execution/edit_financial_model.py --sheet-id "ID" --prepare
# Edit CSV files
python execution/edit_financial_model.py --sheet-id "ID" --validate
python execution/edit_financial_model.py --sheet-id "ID" --apply
```

## Agent Memory Aids

### Red Flags for Config Rebuild

If you see ANY of these keywords in user request:

- ❌ "add revenue stream"
- ❌ "remove revenue stream"
- ❌ "new business line"
- ❌ "restructure TAM"
- ❌ "change methodology"
- ❌ "extend to 10 years"
- ❌ "add cost category"

→ **Use Config-Based Rebuild, NOT Local-First**

### Green Lights for Local-First

If you see these keywords:

- ✅ "update funding"
- ✅ "change growth rate"
- ✅ "fix pricing"
- ✅ "correct formula"
- ✅ "update value"

→ **Use Local-First workflow**

## Error Prevention

### What Breaks Formulas

```python
# ❌ BAD: Adding row via Local-First
# Before:
# Row 25: Total Revenue = SUM(rows 20-24)
# Row 30: Reference to Total Revenue (=Revenue!C25)

# After adding new revenue stream at row 24:
# Row 26: Total Revenue = SUM(rows 20-25)  ← Moved down!
# Row 31: Reference (=Revenue!C25)  ← NOW BROKEN! Points to wrong row

# ✅ GOOD: Using Config Rebuild
# All formulas automatically regenerated with correct row numbers
```

### Formula Preservation Stats

From RapidTools model:

- **1,418 total formulas** across 14 sheets
- **774 cross-sheet references** (e.g., `='P&L'!C36`)
- **131 cross-sheet refs** in Assumptions alone

**One row shift = hundreds of broken formulas**

## File Organization

```
directives/
├── README.md (this file)
├── DECISION_TREE.md ⚠️ READ FIRST
├── business_planning.md
├── EDITING_WORKFLOW.md
├── LOCAL_FIRST_IMPLEMENTATION.md
├── FINANCIAL_MODEL_TEMPLATE.md
└── REUSABLE_PATTERNS.md
```

## Quick Reference

**For agents:**

1. **Always read** `DECISION_TREE.md` before sheet edits
2. **Use config rebuild** for structural changes
3. **Use local-first** for value updates
4. **Never** edit sheets directly via API

**For humans:**

- Full workflow: `EDITING_WORKFLOW.md`
- Quick start: `QUICK_REFERENCE.md` (in root)
- Decision logic: `DECISION_TREE.md`

## Summary

This agent has **two powerful tools**:

1. **Config-Based Rebuild** - Safely handles structural changes
2. **Local-First Workflow** - Efficiently handles value updates

**The key is choosing the right tool for the job.**

**Always consult `DECISION_TREE.md` when in doubt.**
