# RapidTools Business Plan Project

> **Company**: Applied Additive / RapidTools
> **Status**: COMPLETE
> **Last Updated**: February 11, 2026

## Project Overview

RapidTools is an integrated platform for automated tooling design (software), additive manufacturing (hardware), and Design-as-a-Service (DaaS). This folder contains all business plan artifacts.

## Cloud Deliverables

| Asset | Type | Link |
|-------|------|------|
| Financial Model | Google Sheets | [1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY](https://docs.google.com/spreadsheets/d/1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY/edit) |

## Folder Structure

```
rapidtools/
 business_plan/sections/   # Business plan markdown sections (11 files)
    00_Executive_Summary.md
    01_Market_Drivers.md
    02_TAM_SAM_SOM_Calculation.md
    ... (9 more sections)
 config/                   # Project configuration files
    rapidtools_config.json
    model_config.json
    ... (other configs)
 financial_model/          # Financial model markdown sources (14 sheets)
    01_Sources_References.md
    02_Assumptions.md
    ... (12 more sheets)
 notes/                    # Working notes, memos, fixes
 pitch_deck/               # Pitch deck content JSONs
 research/                 # Project-specific research
    archive/              # Archived raw research data
    consolidated/         # Consolidated research by category
 scripts/                  # Development scripts (for reference)
 snapshots/                # Google Sheets snapshots
    2026-01-25/           # Earlier snapshot
    2026-01-28/           # Latest snapshot
    template*/            # Template snapshots
 RapidTools_Financial_Model.xlsx  # Local Excel export
```

## Key Metrics (Year 8)

| Metric | Value |
|--------|-------|
| Revenue | $105.2M |
| EBITDA Margin | 25%+ |
| Total Funding | $38M |
| Valuation (Exit) | ~$400M |

## Revenue Streams

1. **Software** (SaaS) - Automated tooling design platform
2. **Hardware** - 3D printers and equipment
3. **Consumables** - Materials and parts
4. **Services** (DaaS) - Design-as-a-Service, job work

## Project Complete

This project is complete. All files are archived here for reference.
For any updates, download fresh snapshot from Google Sheets:

```bash
python execution/download_model_snapshot.py \
  --sheet-id "1-Ss62JDYgrD9W3vwAcmvdikdmoy-Ud--8wpBFRzkaXY" \
  --output .tmp/rapidtools/snapshots/$(Get-Date -Format "yyyy-MM-dd")
```
