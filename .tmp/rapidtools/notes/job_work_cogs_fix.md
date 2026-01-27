# Job Work Services COGS Fix

> Last Updated: January 21, 2026

## Problem

Row 38 (Job Work Services: COGS %) shows dollar values instead of percentages:
- Current: \\\ (incorrect)
- Should be: \55%\ (percentage like other COGS rows)

## Comparison with Other COGS %

| Revenue Stream | COGS % |
|----------------|--------|
| Software Subscription | 15% |
| 3D Printer Sales | 60% |
| Consumables Materials | 60% |
| AMC Spares | 35% |
| Managed Services | 50% |
| Job Work Services | **55%** (recommended) |

## Rationale for 55%

Job Work Services includes:
- Material costs (~25%)
- Machine time/depreciation (~15%)
- Labor (~10%)
- Overhead (~5%)
- Total: ~55%

## Fix

Update Assumptions row 38, columns C-H from \\\ to \55%\ (or 0.55 as decimal)
