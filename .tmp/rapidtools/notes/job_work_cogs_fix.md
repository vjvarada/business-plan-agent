# Job Work Services COGS Fix

> Last Updated: January 21, 2026

## Problem

Row 38 (Job Work Services: COGS %) shows dollar values instead of percentages:

- Current: \\\ (incorrect)
- Should be: \55%\ (percentage like other COGS rows)

## Comparison with Other COGS %

| Revenue Stream        | COGS %  | Gross Margin | Notes                                 |
| --------------------- | ------- | ------------ | ------------------------------------- |
| Software Subscription | 20%     | 80%          | SaaS benchmark                        |
| 3D Printer Sales      | 76%     | 24%          | Blended (Fracktal 28%, Partners 17%)  |
| Consumables Materials | 67%     | 33%          | Materials + logistics                 |
| AMC Spares            | 60%     | 40%          | **OEM/VAR share 34% + service costs** |
| Managed Services      | 72%     | 28%          | Dedicated staff + equipment           |
| Job Work Services     | **75%** | **25%**      | Third-party fulfillment model         |

## Rationale for 55%

Job Work Services includes:

- Material costs (~25%)
- Machine time/depreciation (~15%)
- Labor (~10%)
- Overhead (~5%)
- Total: ~55%

## Fix

Update Assumptions row 38, columns C-H from \\\ to \55%\ (or 0.55 as decimal)
