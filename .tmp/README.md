# .tmp Folder Organization

> Last Cleaned: January 22, 2026

## Purpose

This folder contains intermediate files generated during business plan creation and financial modeling. It follows the **"intermediates are temporary, deliverables are cloud-based"** principle.

## Folder Structure

```
.tmp/
 _archive/                    # Old temporary scripts (91 files)
 snapshot_test/              # Latest financial model snapshot
 *.md                        # Important documentation
 *.txt                       # Analysis reports
 *.json                      # Data files and configurations
 README.md                   # This file
```

## What to Keep

### Documents (13 files)
- `funding_recommendation.txt` - Funding strategy analysis
- `model_update_summary.txt` - Financial model changes
- `local_first_*.txt` - Local-first workflow documentation
- `RapidTools_Business_Plan.md` - Business plan source
- `market_analysis.md` - Market research compilation
- `*.docx` - Word document exports

### Data Files (32 files)
- `pitch_content.json` - Pitch deck data
- `financial_model_data.json` - Model snapshots
- `market_research_*.json` - SerpAPI research results
- `*_config.json` - Configuration files

### Snapshots
- `snapshot_test/` - Financial model snapshot (29 files)
  - 14 value CSVs
  - 14 formula CSVs
  - 1 metadata JSON

## What's Archived

### Old Scripts (91 files in _archive/)
- `fix_*.py` - One-time fix scripts
- `update_*.py` - One-time update scripts
- `check_*.py` - Verification scripts
- `format_*.py` - Formatting utilities
- `sync_*.py` - One-time sync scripts

**These are kept for reference but not actively used.**

## Cleanup Policy

### Automatic (Run as Needed)
```bash
# Archive old scripts, keep important files
python -c "
import shutil
from pathlib import Path
tmp = Path('.tmp')
archive = tmp / '_archive'
archive.mkdir(exist_ok=True)
for f in tmp.glob('*.py'):
    if f.stem.startswith(('fix_', 'update_', 'check_', 'format_', 'sync_')):
        shutil.move(str(f), str(archive / f.name))
"
```

### Manual Review (Monthly)
1. Delete old market research JSON files (>30 days)
2. Keep only latest business plan .md/.docx
3. Archive old snapshot folders

## Important Files Summary

| Category | Count | Keep/Archive |
|----------|-------|--------------|
| Documents (.md, .txt, .docx) | 13 | KEEP - Source of truth |
| Data Files (.json) | 32 | KEEP - Research data |
| Snapshots (snapshot_test/) | 29 | KEEP - Latest model state |
| Old Scripts (_archive/) | 91 | ARCHIVE - Reference only |

## Usage

### Before Major Work
```bash
# Clean up old files
python -c "..." # Run cleanup script

# Download fresh snapshot
python execution/download_model_snapshot.py --sheet-id "1-Ss62..." --output .tmp/snapshot
```

### After Major Work
```bash
# Archive completed work
mv .tmp/snapshot .tmp/snapshot_$(date +%Y%m%d)

# Clean up temporary files
# (Documents and data files remain)
```

## Key Principle

**Deliverables live in the cloud (Google Docs, Sheets, Slides). The .tmp folder is for processing only.**

-  Keep: Documentation, data, latest snapshots
-  Delete: One-time scripts, old snapshots, temporary exports
-  Archive: Scripts that might be useful for reference

## Recovery

If you accidentally delete something important:
1. Check `_archive/` folder first
2. Check git history: `git log -- .tmp/`
3. Re-run the original generation script from `execution/`

