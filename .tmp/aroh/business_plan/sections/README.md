# Aroh Business Plan Sections

## Overview

Business plan for **Aroh — Owner Intelligence** for owners of Indian businesses (it works like a chief of staff). Aroh is the customer-facing brand; DEWiN owns Aroh IP and contracts; Metorite (Hathi Labs) provides the product building blocks. Written as a category creation argument (`directives/CATEGORY_CREATION_NARRATIVE.md`). Horizon: pre-launch (Nov 2026–Mar 2027) + FY2027–28 to FY2029–30. Currency: ₹ (FX ₹95/US$).

## Section Index

| #   | Section                 | Status   | Key Insight |
| --- | ----------------------- | -------- | ----------- |
| 00  | Category Design         | ✅ Approved (renamed) | Category = Owner Intelligence; enemy = the owner's head as the integration layer; feeling = control that brings calm; $6T national stakes |
| 01  | Market Drivers          | ✅ Approved (draft) | Status quo squeezed by stakes ($6T by 2030), cost (−40×/yr), pressure, trust (India-hosted AI) and law (DPDP) |
| 02  | TAM/SAM/SOM             | ✅ Approved (updated) | 38,003 accounts → ₹6,841 Cr TAM; base SAM 8,361 → ₹1,505 Cr (LOW filters flagged); 500 customers = 6.0% (red flag, kept) |
| 03  | Technology Architecture | ✅ Approved (revised) | Building blocks live as Metorite; DeepSeek V4-class AI moves to Indian hosting before first paid contract |
| 04  | Competitive Analysis    | ✅ Approved (draft) | Seven categories serve someone other than the owner; closest threat = frontier labs' personal agents |
| 05  | Customer Validation     | 📝 Draft (updated) | No paying customers yet; 10 pilots by Dec 2026, 50 paid contracts by Mar 2027 is the test |
| 06  | Go-To-Market Strategy   | 📝 Draft (updated) | Sell the problem first; 133 / 236 / 329 pilots a year; one lightning strike a year |
| 07  | Revenue Model           | 📝 Draft (regenerated) | ₹1.5L/org/month + ₹6L setup (spread over year 1); 57 → 150 → 300 → 500; pre-launch revenue ₹0.8 Cr vs ₹13.7 Cr billed; FY30 revenue ₹95.8 Cr |
| 08  | Team & Fixed Costs      | 📝 Draft (regenerated) | 13 → 53 people; dev cloud ₹0.4–7 Cr; production infra costed; FY30 EBITDA margin 44% |
| 09  | Fundraising Strategy    | 📝 Draft (regenerated) | DEWiN ₹5 Cr bridge; seed after Mar 2027; downside needs ₹6.0 Cr (~₹5 Cr seed) |
| 10  | Financial Projections   | 📝 Draft (regenerated) | Pre-launch stub −₹2.7 Cr; EBITDA ₹9.9 / ₹20.4 / ₹41.7 Cr; deferred-revenue cash model |
| 11  | Risk Analysis           | 📝 Draft (updated) | 14 risks; decisive = 50 paid contracts by Mar 2027 and the March receipts' timing |

## Usage

### For Full Business Plan

Compile sections 00–11 in order.

### For Pitch Deck

Follow the category-creation arc in `directives/CATEGORY_CREATION_NARRATIVE.md` (Part 4): missing-ness → enemy → From → To → category → product as proof → why now → evidence → economic engine → category-king outcome → the ask.

### For Financial Model

Primary inputs from: 02 (TAM/SAM), 07 (Revenue), 08 (Costs), 09 (Funding). Assumptions live in `../../notes/assumption_register.md`.

### Validation

```bash
python execution/check_category_narrative.py --sections-dir .tmp/aroh/business_plan/sections
```
