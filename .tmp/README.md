# .tmp Folder Organization

> Last Cleaned: February 11, 2026

## Purpose

This folder contains intermediate files generated during business plan creation and financial modeling. Each business plan project gets its own isolated folder to prevent interference.

## Folder Structure

```
.tmp/
├── rapidtools/              # Applied Additive: RapidTools project (COMPLETE)
│   ├── business_plan/       # All business plan sections (11 MD files)
│   ├── config/              # Configuration files
│   ├── financial_model/     # Financial model markdown sources (14 MD files)
│   ├── notes/               # Working notes and memos
│   ├── pitch_deck/          # Pitch deck content
│   ├── research/            # Project-specific research
│   │   ├── archive/         # Archived research data
│   │   └── consolidated/    # Consolidated research by category
│   ├── scripts/             # One-off scripts used during development
│   └── snapshots/           # Google Sheets snapshots by date
│       ├── 2026-01-25/      # Earlier snapshot
│       ├── 2026-01-28/      # Latest snapshot
│       ├── template/        # Template snapshot
│       └── template_backup/ # Template backup
├── research/                # Market research for FUTURE projects (reusable)
├── templates/               # Reusable templates for new projects
├── saas_*.json              # General SaaS benchmarks (reusable)
└── README.md                # This file
```

## Project Organization

### Completed Projects
- **rapidtools/** - Applied Additive: RapidTools business plan and financial model
  - Google Sheet: `1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY`
  - Status: COMPLETE

### Reusable Resources (Root Level)
- `research/` - Market research for adjacent markets (dental, eyewear, footwear, etc.)
- `templates/` - Starter templates for new projects
- `saas_*.json` - General SaaS industry benchmarks

## Creating a New Business Plan

```bash
# 1. Copy the project template
cp -r .tmp/templates/project_template .tmp/new_project_name

# 2. Or start fresh
mkdir -p .tmp/new_project_name/{business_plan/sections,config,financial_model,research,snapshots}

# 3. Use market research from shared research/ folder
# 4. Create new config: .tmp/new_project_name/config/project_config.json
```

## Cloud Deliverables

All final deliverables are in Google Drive/Sheets (not local):
- **Financial Model**: Google Sheets with 14 interconnected sheets
- **Business Plan**: Google Docs formatted document
- **Pitch Deck**: Google Slides presentation

## Cleanup Policy

### Per-Project
Each project folder is self-contained. Archive old projects by:
```bash
zip -r .tmp/archives/rapidtools_$(date +%Y%m%d).zip .tmp/rapidtools/
```

### Root Level
Keep only:
- Active project folders
- `research/` - Reusable market research
- `templates/` - Project templates
- `saas_*.json` - General benchmarks

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

