# Operating Costs Fix - RapidTools Financial Model

> Last Updated: January 21, 2026
> Status: **COMPLETED**

## Summary

Fixed the Operating Costs double counting issue and increased S&M spend to industry-appropriate levels.

## Changes Made

### 1. Removed Duplicate Rows

| Sheet | Row | Action |
|-------|-----|--------|
| Operating Costs | 27 | Cleared (was duplicate Marketing Budget) |
| Operating Costs | 28 | Restored as "TOTAL" header |
| Operating Costs | 29 | Updated formula to =C10+C23+C26 |
| Assumptions | 61 | Cleared (was Marketing Budget %) |

### 2. Updated Marketing & Content (Assumptions Row 50)

| Year | Old Value | New Value |
|------|-----------|-----------|
| Y0 | $18K | $18K |
| Y1 | $39K | $54K |
| Y2 | $62K | $282K |
| Y3 | $93K | $729K |
| Y4 | $130K | $946K |
| Y5 | $185K | $1,655K |

### 3. Fixed P&L Row 21

Updated to reference Operating Costs row 26 (CAC only) with USER_ENTERED value input.

## Final S&M Structure

| Component | Location | Y0 | Y1 | Y2 | Y3 | Y4 | Y5 |
|-----------|----------|-----|-----|-----|-----|-----|-----|
| Marketing & Content | Fixed Costs (row 22) | $18K | $54K | $282K | $729K | $946K | $1,655K |
| Travel & Trade Shows | Fixed Costs (row 21) | $11K | $22K | $41K | $46K | $65K | $92K |
| CAC (per new customer) | S&M (row 26) | $20K | $137K | $234K | $342K | $549K | $673K |
| **Total S&M** | | **$49K** | **$213K** | **$557K** | **$1,117K** | **$1,560K** | **$2,420K** |
| **% of Revenue** | | **25.3%** | **18.0%** | **16.0%** | **14.0%** | **12.0%** | **10.0%** |

## Verification

-  No double counting
-  All formulas working
-  P&L calculating correctly
-  S&M % ranges from 25% (Y0) to 10% (Y5) - industry appropriate
