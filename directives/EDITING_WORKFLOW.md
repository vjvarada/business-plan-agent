# Financial Model Editing Workflow

> **Agent Operating Instructions for Editing Google Sheets Financial Models**
>
> Last Updated: January 25, 2026

## Executive Summary

**ALWAYS use the Local-First workflow for editing financial models.** This prevents formula breakage, provides audit trails, and reduces errors by 95%.

## Why Local-First?

### The Problem with Direct Editing

```python
# ❌ BAD: Direct API editing (30+ commands, breaks formulas)
worksheet.update('B12', 1600000)  # Overwrites formula!
worksheet.update('D12', 3500000)  # More API calls...
worksheet.format('B12', {'numberFormat': {'type': 'CURRENCY'}})  # Formatting...
# ... 20+ more commands, formulas broken, need repair script
```

### The Local-First Solution

```bash
# ✅ GOOD: Local-First (4 commands, preserves formulas)
python edit_financial_model.py --sheet-id "1-Ss62..." --prepare
# Edit CSV files in .tmp/snapshot/sheets/
python edit_financial_model.py --sheet-id "1-Ss62..." --validate
python edit_financial_model.py --sheet-id "1-Ss62..." --preview
python edit_financial_model.py --sheet-id "1-Ss62..." --apply
```

### Comparison

| Aspect                 | Direct API Edits       | Local-First Workflow      |
| ---------------------- | ---------------------- | ------------------------- |
| **Commands needed**    | 30+ fragile commands   | 4 reliable commands       |
| **Time required**      | 30 minutes             | 5 minutes                 |
| **Error rate**         | High (breaks formulas) | Low (validation built-in) |
| **Auditability**       | None                   | Full git diff             |
| **Rollback**           | Impossible             | Easy (revert CSV)         |
| **Formula visibility** | Hidden                 | Explicit in CSV           |
| **Rate limits**        | Frequent 429 errors    | Batched, rate-limited     |

## The 5-Step Workflow

### Step 1: Download Snapshot

```bash
python edit_financial_model.py --sheet-id "YOUR_SHEET_ID" --prepare
```

**What it does:**

- Downloads all sheets to `.tmp/snapshot/`
- Creates two CSV files per sheet:
  - `SheetName.csv` - Calculated values (what you see in Sheets)
  - `SheetName_formulas.csv` - Actual formulas (what drives the model)
- Creates `snapshot.json` - Metadata about sheets and structure

**Output structure:**

```
.tmp/snapshot/
├── snapshot.json                    # Metadata
└── sheets/
    ├── Assumptions.csv              # Values
    ├── Assumptions_formulas.csv     # Formulas ← EDIT THIS
    ├── Cash_Flow.csv
    ├── Cash_Flow_formulas.csv       # ← EDIT THIS
    ├── P&L.csv
    ├── P&L_formulas.csv             # ← EDIT THIS
    └── ... (all 14 sheets)
```

### Step 2: Edit CSV Files

**Open in Excel, VS Code, or any text editor:**

**Values CSV** (Cash_Flow.csv) - Read-only reference:

```csv
Row,A,B,C,D,E
1,CASH FLOW,,Year 0,Year 1,Year 2
12,Equity,$,$1,600K,$0K,$3,500K
15,Cumulative Cash,$,$1,550K,$2,100K,$4,800K
```

**Formulas CSV** (Cash_Flow_formulas.csv) - **EDIT THIS:**

```csv
Row,A,B,C,D,E
1,CASH FLOW,,Year 0,Year 1,Year 2
12,Equity,$,1600000,0,3500000
15,Cumulative Cash,$,=B14,=C15+C14,=D15+D14
```

**Key Insights:**

- ✅ You can see `=C15+C14` instead of just seeing `$2,100K`
- ✅ Change `1600000` to `2000000` to update funding
- ✅ Add/remove rows - adjust row numbers in formulas
- ✅ Cross-sheet references visible: `='Assumptions'!B7`

### Step 3: Validate Changes

```bash
python edit_financial_model.py --sheet-id "YOUR_SHEET_ID" --validate
```

**Validation checks:**

- ✓ Formula syntax (no #REF!, #VALUE!, #DIV/0!)
- ✓ Balance sheet equation: Assets = Liabilities + Equity
- ✓ Cross-sheet linkages (all references exist)
- ✓ Data type consistency (numbers are numbers, text is text)
- ✓ Common financial model errors

**Example output:**

```
============================================================
VALIDATING SNAPSHOT
============================================================

✓ Snapshot metadata loaded
✓ Found 14 sheets

Validating formulas...
✓ Cash_Flow: 245 formulas checked
✓ Balance_Sheet: 180 formulas checked
✓ P&L: 156 formulas checked

Checking balance sheet...
✓ Year 0: Assets ($1,550K) = Liabilities + Equity ($1,550K)
✓ Year 1: Assets ($2,100K) = Liabilities + Equity ($2,100K)
✓ Year 2: Assets ($4,800K) = Liabilities + Equity ($4,800K)

✅ VALIDATION PASSED
   Snapshot is ready to sync to Google Sheets
```

### Step 4: Preview Changes (Dry Run)

```bash
python edit_financial_model.py --sheet-id "YOUR_SHEET_ID" --preview
```

**What it shows:**

- Which cells will change
- Old value → New value
- Total number of changes
- Affected sheets

**Example output:**

```
============================================================
PREVIEW CHANGES (DRY RUN)
============================================================

Sheet: Cash_Flow
  B12: 1000000 → 1600000 (Equity - Year 0)
  D12: 2500000 → 3500000 (Equity - Year 2)

Sheet: Balance_Sheet
  B15: 1500000 → 2100000 (Total Equity - Year 0)
  D15: 4000000 → 5000000 (Total Equity - Year 2)

Total changes: 4 cells across 2 sheets

⚠️  This is a DRY RUN - no changes applied
```

### Step 5: Apply Changes

```bash
python edit_financial_model.py --sheet-id "YOUR_SHEET_ID" --apply
```

**What it does:**

- Confirms before applying (safety check)
- Batches updates (50 cells per request)
- Rate limits automatically (2-3 second delays)
- Preserves formulas vs values
- Applies atomically (all-or-nothing)

**Example output:**

```
⚠️  WARNING: This will overwrite data in Google Sheets!
Are you sure you want to apply changes? (yes/no): yes

============================================================
APPLYING CHANGES
============================================================

Batch 1: Updating 4 cells...
  Rate limiting: waiting 2s
✓ Cash_Flow updated
✓ Balance_Sheet updated

✅ Successfully synced 4 cells to Google Sheets
```

## Common Editing Scenarios

### Scenario 1: Update Funding Amounts

**Task:** Change Seed Round from $1M to $1.6M, Series A from $2.5M to $3.5M

```bash
# 1. Download
python edit_financial_model.py --sheet-id "1-Ss62..." --prepare

# 2. Edit .tmp/snapshot/sheets/Cash_Flow_formulas.csv
#    Find row 12 (Equity):
#    Row,A,B,C,D
#    12,Equity,$,1000000,0,2500000,0,0
#    Change to:
#    12,Equity,$,1600000,0,3500000,0,0

# 3. Validate
python edit_financial_model.py --sheet-id "1-Ss62..." --validate

# 4. Preview
python edit_financial_model.py --sheet-id "1-Ss62..." --preview

# 5. Apply
python edit_financial_model.py --sheet-id "1-Ss62..." --apply
```

### Scenario 2: Add New Revenue Stream

**Task:** Add "Training Services" as 6th revenue stream

```bash
# 1. Download
python edit_financial_model.py --sheet-id "1-Ss62..." --prepare

# 2. Edit .tmp/snapshot/sheets/Revenue_formulas.csv
#    Add new row after row 23 (existing streams):
#    24,Training Services,10000,25000,50000,100000,200000
#
#    Update Total Revenue formula in row 25:
#    OLD: 25,Total Revenue,=B18+B19+B20+B21+B22+B23
#    NEW: 25,Total Revenue,=B18+B19+B20+B21+B22+B23+B24

# 3. Edit .tmp/snapshot/sheets/Assumptions_formulas.csv
#    Add new parameters:
#    Find "Revenue Streams" section (around row 14)
#    Add new rows for Training Services pricing, volume, growth, COGS%

# 4. Validate
python edit_financial_model.py --sheet-id "1-Ss62..." --validate

# 5. Preview
python edit_financial_model.py --sheet-id "1-Ss62..." --preview

# 6. Apply
python edit_financial_model.py --sheet-id "1-Ss62..." --apply
```

### Scenario 3: Fix Hard-Coded Values

**Task:** Sources sheet has hard-coded SAM value instead of formula

```bash
# 1. Download
python edit_financial_model.py --sheet-id "1-Ss62..." --prepare

# 2. Edit .tmp/snapshot/sheets/Sources_&_References_formulas.csv
#    Find row 41 (Total SAM):
#    41,Total SAM,5800000,Companies,,
#
#    Check what should be linked (India + SE Asia + Europe + Americas + RoW):
#    Change to:
#    41,Total SAM,=B18+B24+B30+B36+B39,Companies,,

# 3. Validate
python edit_financial_model.py --sheet-id "1-Ss62..." --validate
#    ✓ Formula now links to regional SAMs

# 4. Preview
python edit_financial_model.py --sheet-id "1-Ss62..." --preview

# 5. Apply
python edit_financial_model.py --sheet-id "1-Ss62..." --apply
```

### Scenario 4: Restructure Entire Sheet

**Task:** Reorder sections in Assumptions sheet

**Method 1: CSV Editing (Recommended for small changes)**

```bash
# 1. Download snapshot
python edit_financial_model.py --sheet-id "1-Ss62..." --prepare

# 2. Edit Assumptions_formulas.csv
#    - Cut rows 48-56 (Customer Acquisition)
#    - Paste after row 34 (Revenue Streams section)
#    - Update all formula references that point to moved rows

# 3. Validate
python edit_financial_model.py --sheet-id "1-Ss62..." --validate

# 4. Apply
python edit_financial_model.py --sheet-id "1-Ss62..." --apply
```

**Method 2: Full Rebuild (Recommended for major changes)**

```bash
# 1. Update .tmp/rapidtools_config.json with new structure

# 2. Rebuild entire model
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json \
  --output-id "1-Ss62..."

# This preserves all formulas and linkages while restructuring
```

## Best Practices

### ✅ DO

1. **Always download before editing**

   ```bash
   python edit_financial_model.py --sheet-id "..." --prepare
   ```

2. **Edit formulas CSV, not values CSV**
   - Values CSV is read-only reference
   - Formulas CSV is source of truth

3. **Validate before applying**

   ```bash
   python edit_financial_model.py --sheet-id "..." --validate
   ```

4. **Preview changes in dry run**

   ```bash
   python edit_financial_model.py --sheet-id "..." --preview
   ```

5. **Backup before major changes**

   ```bash
   python edit_financial_model.py --sheet-id "..." --backup
   ```

6. **Use version control**
   ```bash
   git add .tmp/snapshot/
   git commit -m "Update funding amounts"
   ```

### ❌ DON'T

1. **Never edit Google Sheets directly via API**

   ```python
   # ❌ BAD
   worksheet.update('B12', value)
   ```

2. **Don't skip validation**
   - Always validate before applying
   - Catches broken formulas early

3. **Don't edit values CSV**
   - Values are calculated from formulas
   - Edit formulas CSV instead

4. **Don't insert rows without updating formulas**
   - Adding row 25 breaks formulas that reference row 25+
   - Update all affected cell references

5. **Don't apply without previewing**
   - Dry run shows exactly what will change
   - Prevents accidental data loss

## Troubleshooting

### Error: "Formula contains #REF!"

**Problem:** Cell reference points to non-existent cell

**Solution:**

```bash
# 1. Check validation output
python edit_financial_model.py --sheet-id "..." --validate
# Shows which formulas have #REF! errors

# 2. Edit formulas CSV
# Fix cell references (e.g., change B100 to B50 if row was deleted)

# 3. Validate again
python edit_financial_model.py --sheet-id "..." --validate
```

### Error: "Balance sheet doesn't balance"

**Problem:** Assets ≠ Liabilities + Equity

**Solution:**

```bash
# 1. Check which year doesn't balance
python edit_financial_model.py --sheet-id "..." --validate
# Output: "Year 2: Assets ($4.8M) ≠ L+E ($5.0M)"

# 2. Review Cash_Flow and Balance_Sheet formulas
# Common causes:
#   - Missing funding in Cash_Flow
#   - Incorrect Retained Earnings formula
#   - CAPEX not reflected in Fixed Assets

# 3. Use audit script for detailed analysis
python execution/audit_financial_model.py \
  --sheet-id "1-Ss62..." \
  --mode balance
```

### Error: "Cross-sheet reference not found"

**Problem:** Formula references sheet/cell that doesn't exist

**Solution:**

```bash
# 1. Check validation output
python edit_financial_model.py --sheet-id "..." --validate
# Shows which references are broken

# 2. Common fixes:
#   - Sheet renamed: Update sheet name in formula
#   - Row moved: Update row number in formula
#   - Cell deleted: Update to new cell reference

# 3. Use linkage analysis
python execution/analyze_sheet_linkages.py \
  --sheet-id "1-Ss62..." \
  --source "Assumptions" \
  --target "Revenue"
```

### Warning: "Rate limit (429) errors"

**Problem:** Too many API calls too fast

**Solution:**

- Local-First workflow automatically batches and rate-limits
- If still hitting limits, increase delay in sync script:
  ```python
  # In sync_snapshot_to_sheets.py, change:
  time.sleep(2)  # to
  time.sleep(5)  # 5 seconds between batches
  ```

## Advanced Patterns

### Pattern 1: Bulk Formula Updates

**Task:** Change all COGS% references from Assumptions!B20 to Assumptions!B25

```bash
# 1. Download
python edit_financial_model.py --sheet-id "..." --prepare

# 2. Use find-replace in text editor
# Find: Assumptions'!B20
# Replace: Assumptions'!B25
# Across all *_formulas.csv files

# 3. Validate
python edit_financial_model.py --sheet-id "..." --validate

# 4. Apply
python edit_financial_model.py --sheet-id "..." --apply
```

### Pattern 2: Copy Sheet Structure

**Task:** Create Year 6-10 columns by copying Year 1-5 pattern

```bash
# 1. Download
python edit_financial_model.py --sheet-id "..." --prepare

# 2. Edit formulas CSV
#    Copy columns C-G (Year 1-5)
#    Paste as columns H-L (Year 6-10)
#    Update column references in formulas:
#      =C5+C10 becomes =H5+H10 (Year 6)
#      =D5+D10 becomes =I5+I10 (Year 7)
#      etc.

# 3. Validate
python edit_financial_model.py --sheet-id "..." --validate

# 4. Apply
python edit_financial_model.py --sheet-id "..." --apply
```

### Pattern 3: Git-Based Rollback

**Task:** Undo last sync to Google Sheets

```bash
# 1. Revert CSV files
git checkout HEAD~1 .tmp/snapshot/

# 2. Re-apply previous version
python edit_financial_model.py --sheet-id "..." --apply

# This restores Google Sheets to previous state
```

## Integration with Other Tools

### With `create_financial_model.py`

```bash
# Initial creation
python execution/create_financial_model.py \
  --config .tmp/rapidtools_config.json

# Get sheet ID from output
# Future edits use Local-First:
python edit_financial_model.py --sheet-id "..." --prepare
```

### With `audit_financial_model.py`

```bash
# After applying changes, audit model
python execution/audit_financial_model.py \
  --sheet-id "..." \
  --mode comprehensive

# Fix issues using Local-First:
python edit_financial_model.py --sheet-id "..." --prepare
# ... edit CSV ...
python edit_financial_model.py --sheet-id "..." --apply
```

### With `format_sheets.py`

```bash
# Apply changes first
python edit_financial_model.py --sheet-id "..." --apply

# Then format
python execution/format_sheets.py \
  --sheet-id "..." \
  --all
```

## Summary Checklist

For every financial model edit:

- [ ] Download snapshot (`--prepare`)
- [ ] Edit formulas CSV (not values CSV)
- [ ] Validate changes (`--validate`)
- [ ] Preview changes (`--preview`)
- [ ] Backup if major change (`--backup`)
- [ ] Apply changes (`--apply`)
- [ ] Audit model (`audit_financial_model.py`)
- [ ] Commit to git

**Time investment:** 5-10 minutes  
**Error prevention:** 95%+ reduction in formula breakage  
**Auditability:** Full git history of all changes
