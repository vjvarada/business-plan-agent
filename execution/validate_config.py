#!/usr/bin/env python3
"""
Configuration Validator for Financial Models
=============================================
Validates config.json before creating financial models to prevent errors.

Supports both canonical (structured) and legacy (flat) config formats.

Usage:
    python execution/validate_config.py --config config.json
    python execution/validate_config.py --config config.json --strict

Exit Codes:
    0 = Valid config (or warnings only in non-strict)
    1 = Warnings in strict mode
    2 = Errors found
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ValidationLevel(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    level: ValidationLevel
    field: str
    message: str
    suggestion: Optional[str] = None


class ConfigValidator:
    def __init__(self, config: Dict[str, Any], strict: bool = False):
        self.config = config
        self.strict = strict
        self.issues: List[ValidationIssue] = []

    def add_issue(
        self, level: ValidationLevel, field: str, message: str, suggestion: str = None
    ):
        self.issues.append(ValidationIssue(level, field, message, suggestion))

    def validate_all(self) -> bool:
        """Run all validations. Returns True if config is usable."""
        print("Validating configuration...\n")

        self.validate_required_fields()
        self.validate_general_params()
        self.validate_revenue_streams()
        self.validate_fixed_costs()
        self.validate_headcount()
        self.validate_funding()
        self.validate_market_data()
        self.validate_customer_acquisition()
        self.validate_consistency()

        return self.print_results()

    # ---- required fields ----

    def validate_required_fields(self):
        # Resolve company_name
        if "company_name" not in self.config:
            if isinstance(self.config.get("company"), str):
                self.config["company_name"] = self.config["company"]
            elif isinstance(self.config.get("company"), dict):
                self.config["company_name"] = self.config["company"].get("name", "")
        if not self.config.get("company_name"):
            self.add_issue(
                ValidationLevel.ERROR,
                "company_name",
                "Missing company name",
                "Add 'company' or 'company_name'",
            )

        # Resolve tax_rate
        if "tax_rate" not in self.config:
            gen = self.config.get("general", {})
            if isinstance(gen, dict) and isinstance(gen.get("tax_rate"), (int, float)):
                self.config["tax_rate"] = gen["tax_rate"]

        # Resolve starting_year
        if "starting_year" not in self.config:
            gen = self.config.get("general", {})
            if isinstance(gen, dict) and isinstance(gen.get("starting_year"), int):
                self.config["starting_year"] = gen["starting_year"]
            else:
                yr = datetime.now().year
                self.config["starting_year"] = yr
                self.add_issue(
                    ValidationLevel.WARNING,
                    "starting_year",
                    f"Missing; defaulting to {yr}",
                    "Set starting_year explicitly",
                )

        for field in ["company_name", "tax_rate", "starting_year"]:
            if field not in self.config:
                self.add_issue(
                    ValidationLevel.ERROR, field, f"Required field '{field}' is missing"
                )

    # ---- general ----

    def validate_general_params(self):
        tax = self.config.get("tax_rate")
        if tax is not None:
            if not isinstance(tax, (int, float)):
                self.add_issue(
                    ValidationLevel.ERROR,
                    "tax_rate",
                    f"Must be a number, got {type(tax).__name__}",
                )
            elif not (0 <= tax <= 1):
                self.add_issue(
                    ValidationLevel.ERROR,
                    "tax_rate",
                    f"Must be 0-1, got {tax}",
                    "Use 0.25 for 25%",
                )

        yr = self.config.get("starting_year")
        if yr is not None:
            if not isinstance(yr, int):
                self.add_issue(
                    ValidationLevel.ERROR,
                    "starting_year",
                    f"Must be int, got {type(yr).__name__}",
                )
            elif yr < 2020 or yr > 2035:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "starting_year",
                    f"{yr} seems unusual (expected 2020-2035)",
                )

        gen = self.config.get("general", {})
        if isinstance(gen, dict):
            for key, lo, hi, label in [
                ("capex_y0", 0, 50_000_000, "Initial CapEx"),
                ("capex_annual", 0, 10_000_000, "Annual CapEx"),
                ("depreciation_years", 1, 30, "Depreciation period"),
                ("debtor_days", 0, 365, "Debtor days"),
                ("creditor_days", 0, 365, "Creditor days"),
            ]:
                v = gen.get(key)
                if v is not None and isinstance(v, (int, float)):
                    if v < lo or v > hi:
                        self.add_issue(
                            ValidationLevel.WARNING,
                            f"general.{key}",
                            f"{label} = {v} outside typical range ({lo}-{hi})",
                        )

            for key in ["interest_rate", "cost_inflation"]:
                v = gen.get(key)
                if v is not None and isinstance(v, (int, float)):
                    if not (0 <= v <= 1):
                        self.add_issue(
                            ValidationLevel.ERROR,
                            f"general.{key}",
                            f"Must be 0-1, got {v}",
                            "Use 0.05 for 5%",
                        )

    # ---- revenue streams ----

    def validate_revenue_streams(self):
        streams = self.config.get("revenue_streams", [])
        if not isinstance(streams, list):
            self.add_issue(ValidationLevel.ERROR, "revenue_streams", "Must be a list")
            return
        if not streams:
            self.add_issue(
                ValidationLevel.ERROR, "revenue_streams", "No revenue streams defined"
            )
            return
        if len(streams) > 10:
            self.add_issue(
                ValidationLevel.WARNING,
                "revenue_streams",
                f"{len(streams)} streams (>10 may clutter the model)",
            )

        for i, s in enumerate(streams):
            pfx = f"revenue_streams[{i}]"
            if not isinstance(s, dict):
                self.add_issue(ValidationLevel.ERROR, pfx, "Must be an object")
                continue
            if not s.get("name"):
                self.add_issue(
                    ValidationLevel.ERROR, f"{pfx}.name", "Missing stream name"
                )

            # Check price (accept both 'price' and 'unit_price')
            price = s.get("price", s.get("unit_price"))
            if price is not None:
                if not isinstance(price, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"{pfx}.price",
                        f"Must be number, got {type(price).__name__}",
                    )
                elif price < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"{pfx}.price",
                        f"Cannot be negative: {price}",
                    )
                elif price == 0:
                    self.add_issue(
                        ValidationLevel.WARNING,
                        f"{pfx}.price",
                        "Price is 0 — intentional?",
                    )

            # Growth (accept 'growth' or 'growth_rate')
            growth = s.get("growth", s.get("growth_rate"))
            if growth is not None:
                if not isinstance(growth, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR, f"{pfx}.growth", f"Must be number"
                    )
                elif growth < -0.5 or growth > 10:
                    self.add_issue(
                        ValidationLevel.WARNING,
                        f"{pfx}.growth",
                        f"{growth*100:.0f}% seems extreme (-50% to 1000%)",
                    )

            # COGS (accept 'cogs_pct' or 'cogs_percentage')
            cogs = s.get("cogs_pct", s.get("cogs_percentage"))
            if cogs is not None:
                if not isinstance(cogs, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR, f"{pfx}.cogs_pct", f"Must be number"
                    )
                elif not (0 <= cogs <= 1):
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"{pfx}.cogs_pct",
                        f"Must be 0-1, got {cogs}",
                        "Use 0.20 for 20%",
                    )

            # Volume
            vol = s.get("volume", s.get("initial_volume"))
            if vol is not None and isinstance(vol, (int, float)) and vol < 0:
                self.add_issue(
                    ValidationLevel.ERROR, f"{pfx}.volume", f"Cannot be negative: {vol}"
                )

    # ---- fixed costs ----

    def validate_fixed_costs(self):
        fc = self.config.get("fixed_costs", [])
        if isinstance(fc, dict):
            fc = [{"name": k, "annual_cost": v} for k, v in fc.items()]
        if not isinstance(fc, list):
            self.add_issue(
                ValidationLevel.ERROR,
                "fixed_costs",
                f"Must be list or object, got {type(fc).__name__}",
            )
            return
        if len(fc) > 15:
            self.add_issue(
                ValidationLevel.WARNING,
                "fixed_costs",
                f"{len(fc)} categories — consider consolidating",
            )

        for i, c in enumerate(fc):
            pfx = f"fixed_costs[{i}]"
            if not isinstance(c, dict):
                self.add_issue(ValidationLevel.ERROR, pfx, "Must be an object")
                continue
            if not c.get("name") and not c.get("category"):
                self.add_issue(
                    ValidationLevel.ERROR, pfx, "Missing 'name' or 'category'"
                )
            amt = c.get("annual_cost", c.get("amount", c.get("value")))
            if amt is not None:
                if not isinstance(amt, (int, float)):
                    self.add_issue(
                        ValidationLevel.ERROR, f"{pfx}.annual_cost", f"Must be number"
                    )
                elif amt < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"{pfx}.annual_cost",
                        f"Cannot be negative: {amt}",
                    )

    # ---- headcount ----

    def validate_headcount(self):
        hc = self.config.get("headcount", {})
        if not isinstance(hc, dict):
            self.add_issue(ValidationLevel.ERROR, "headcount", "Must be an object")
            return

        # Canonical format: departments list
        depts = hc.get("departments")
        if isinstance(depts, list):
            if not depts:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "headcount.departments",
                    "Empty departments list",
                )
            for i, d in enumerate(depts):
                pfx = f"headcount.departments[{i}]"
                if not isinstance(d, dict):
                    self.add_issue(ValidationLevel.ERROR, pfx, "Must be an object")
                    continue
                if not d.get("name"):
                    self.add_issue(
                        ValidationLevel.ERROR, f"{pfx}.name", "Missing department name"
                    )
                sal = d.get("salary", 0)
                if isinstance(sal, (int, float)) and sal < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"{pfx}.salary",
                        f"Cannot be negative: {sal}",
                    )
                y0 = d.get("y0_count", 0)
                if isinstance(y0, (int, float)) and y0 < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"{pfx}.y0_count",
                        f"Cannot be negative: {y0}",
                    )
                gr = d.get("growth", 0)
                if isinstance(gr, (int, float)) and (gr < -0.5 or gr > 5):
                    self.add_issue(
                        ValidationLevel.WARNING,
                        f"{pfx}.growth",
                        f"{gr*100:.0f}% growth seems extreme",
                    )
            return

        # Legacy flat format: engineering_salary, engineering_y0, etc.
        found_any = False
        for prefix in [
            "engineering",
            "sales",
            "ops",
            "ga",
            "product",
            "data",
            "support",
        ]:
            sal_key = f"{prefix}_salary"
            y0_key = f"{prefix}_y0"
            if sal_key in hc or y0_key in hc:
                found_any = True
                sal = hc.get(sal_key)
                if sal is not None and isinstance(sal, (int, float)) and sal < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"headcount.{sal_key}",
                        f"Cannot be negative",
                    )
                y0 = hc.get(y0_key)
                if y0 is not None and isinstance(y0, (int, float)) and y0 < 0:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"headcount.{y0_key}",
                        f"Cannot be negative",
                    )

        if not found_any:
            self.add_issue(
                ValidationLevel.WARNING,
                "headcount",
                "No departments found (legacy or canonical format)",
                "Add headcount.departments list or legacy fields like engineering_salary",
            )

    # ---- funding ----

    def validate_funding(self):
        fund = self.config.get("funding", {})
        if not isinstance(fund, dict):
            self.add_issue(
                ValidationLevel.WARNING, "funding", "Missing or invalid funding block"
            )
            return

        # Canonical format: rounds list
        rounds = fund.get("rounds")
        if isinstance(rounds, list):
            for i, r in enumerate(rounds):
                pfx = f"funding.rounds[{i}]"
                if not isinstance(r, dict):
                    self.add_issue(ValidationLevel.ERROR, pfx, "Must be an object")
                    continue
                if not r.get("name"):
                    self.add_issue(
                        ValidationLevel.WARNING, f"{pfx}.name", "Missing round name"
                    )
                amt = r.get("amount")
                if amt is not None:
                    if not isinstance(amt, (int, float)):
                        self.add_issue(
                            ValidationLevel.ERROR, f"{pfx}.amount", f"Must be number"
                        )
                    elif amt < 0:
                        self.add_issue(
                            ValidationLevel.ERROR,
                            f"{pfx}.amount",
                            f"Cannot be negative",
                        )
                yr = r.get("year")
                if yr is not None and isinstance(yr, (int, float)):
                    if yr < 0 or yr > 15:
                        self.add_issue(
                            ValidationLevel.WARNING,
                            f"{pfx}.year",
                            f"Year {yr} outside 0-15 range",
                        )
            return

        # Legacy flat format: seed, series_a, etc.
        found_any = False
        for key in ["seed", "series_a", "series_b", "series_c"]:
            if key in fund:
                found_any = True
                amt = fund[key]
                if isinstance(amt, (int, float)) and amt < 0:
                    self.add_issue(
                        ValidationLevel.ERROR, f"funding.{key}", "Cannot be negative"
                    )

        # Also accept funding_rounds list (old format)
        old_rounds = self.config.get("funding_rounds", [])
        if isinstance(old_rounds, list) and old_rounds:
            found_any = True
            for i, r in enumerate(old_rounds):
                pfx = f"funding_rounds[{i}]"
                amt = r.get("amount") if isinstance(r, dict) else None
                if amt is not None and isinstance(amt, (int, float)) and amt < 0:
                    self.add_issue(
                        ValidationLevel.ERROR, f"{pfx}.amount", "Cannot be negative"
                    )

        if not found_any:
            self.add_issue(
                ValidationLevel.INFO,
                "funding",
                "No funding rounds defined (bootstrapped?)",
            )

    # ---- market data ----

    def validate_market_data(self):
        tam_raw = self.config.get("tam")
        sam_raw = self.config.get("sam")
        som_raw = self.config.get("som")

        def sum_market(val):
            """Extract total numeric value from market data in various formats."""
            if isinstance(val, (int, float)):
                return val
            if isinstance(val, dict):
                # Canonical: {streams: [{value_m: N}, ...]}
                streams = val.get("streams", [])
                if isinstance(streams, list) and streams:
                    return sum(
                        s.get("value_m", 0) for s in streams if isinstance(s, dict)
                    )
                # Canonical: {regions: [{value_m: N}, ...]}
                regions = val.get("regions", [])
                if isinstance(regions, list) and regions:
                    return sum(
                        r.get("value_m", 0) for r in regions if isinstance(r, dict)
                    )
                # Legacy flat: {software: 10000, hardware: 4000}
                nums = [v for v in val.values() if isinstance(v, (int, float))]
                if nums:
                    return sum(nums)
                # SOM: {year8_revenue: N} or {year8_revenue_m: N}
                for k in ["year8_revenue_m", "year8_revenue"]:
                    if isinstance(val.get(k), (int, float)):
                        return val[k]
            return None

        tam = sum_market(tam_raw)
        sam = sum_market(sam_raw)
        som = sum_market(som_raw)

        if tam is not None and tam < 0:
            self.add_issue(
                ValidationLevel.ERROR, "tam", f"TAM cannot be negative: {tam}"
            )
        if sam is not None and sam < 0:
            self.add_issue(
                ValidationLevel.ERROR, "sam", f"SAM cannot be negative: {sam}"
            )
        if som is not None and som < 0:
            self.add_issue(
                ValidationLevel.ERROR, "som", f"SOM cannot be negative: {som}"
            )

        # Logical hierarchy (only if all are in same units — skip if unclear)
        if all(v is not None for v in [tam, sam, som]):
            if sam > tam:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "market_data",
                    f"SAM ({sam}) > TAM ({tam}) — expected SAM <= TAM",
                )
            # SOM vs SAM: SOM might be in $M while SAM is total, so just warn gently
            if som > sam and som > 100:  # high SOM likely same units
                self.add_issue(
                    ValidationLevel.WARNING,
                    "market_data",
                    f"SOM ({som}) > SAM ({sam}) — check units match",
                )

    # ---- customer acquisition ----

    def validate_customer_acquisition(self):
        ca = self.config.get("customer_acquisition", {})
        if not isinstance(ca, dict):
            # Also check top-level fields (older format)
            ca = {}
            for k in ["cac_per_customer", "cac", "churn_rate"]:
                if k in self.config:
                    ca[k] = self.config[k]

        if not ca:
            return  # Optional block

        cac = ca.get("cac", ca.get("cac_per_customer"))
        if cac is not None:
            if not isinstance(cac, (int, float)):
                self.add_issue(
                    ValidationLevel.ERROR,
                    "customer_acquisition.cac",
                    "Must be a number",
                )
            elif cac < 0:
                self.add_issue(
                    ValidationLevel.ERROR,
                    "customer_acquisition.cac",
                    f"Cannot be negative: {cac}",
                )

        churn = ca.get("churn_rate", self.config.get("churn_rate"))
        if churn is not None:
            if not isinstance(churn, (int, float)):
                self.add_issue(ValidationLevel.ERROR, "churn_rate", "Must be a number")
            elif not (0 <= churn <= 1):
                self.add_issue(
                    ValidationLevel.ERROR,
                    "churn_rate",
                    f"Must be 0-1, got {churn}",
                    "Use 0.05 for 5%",
                )
            elif churn > 0.20:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "churn_rate",
                    f"{churn*100:.0f}% is very high (>20%)",
                    "B2B SaaS average is 5-15%",
                )

    # ---- cross-validation ----

    def validate_consistency(self):
        # Check opex coverage: can funding cover a few years of burn?
        streams = self.config.get("revenue_streams", [])
        fc = self.config.get("fixed_costs", [])

        y0_revenue = sum(
            s.get("price", 0) * s.get("volume", 0)
            for s in streams
            if isinstance(s, dict)
        )
        y0_fixed = 0
        for c in fc if isinstance(fc, list) else []:
            if isinstance(c, dict):
                y0_fixed += c.get("annual_cost", c.get("amount", 0))

        # Headcount costs
        hc = self.config.get("headcount", {})
        hc_cost = 0
        if isinstance(hc, dict):
            depts = hc.get("departments", [])
            if isinstance(depts, list):
                for d in depts:
                    if isinstance(d, dict):
                        hc_cost += d.get("salary", 0) * d.get("y0_count", 0)
            else:
                for pfx in ["engineering", "sales", "ops", "ga"]:
                    sal = hc.get(f"{pfx}_salary", 0) or 0
                    cnt = hc.get(f"{pfx}_y0", 0) or 0
                    hc_cost += sal * cnt

        total_y0_costs = y0_fixed + hc_cost
        if y0_revenue > 0 and total_y0_costs > 0:
            if total_y0_costs > y0_revenue * 5:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "consistency",
                    f"Year 0 costs (${total_y0_costs:,.0f}) are 5x+ revenue (${y0_revenue:,.0f})",
                    "Ensure funding covers the burn rate",
                )

        # Check total funding vs burn
        fund = self.config.get("funding", {})
        total_funding = 0
        rounds = fund.get("rounds", []) if isinstance(fund, dict) else []
        if isinstance(rounds, list):
            total_funding = sum(
                r.get("amount", 0) for r in rounds if isinstance(r, dict)
            )
        elif isinstance(fund, dict):
            for k in ["seed", "series_a", "series_b", "series_c"]:
                total_funding += fund.get(k, 0) or 0

        if total_funding > 0 and total_y0_costs > 0:
            runway_years = total_funding / total_y0_costs
            if runway_years < 1.5:
                self.add_issue(
                    ValidationLevel.WARNING,
                    "consistency",
                    f"Total funding ${total_funding:,.0f} only covers ~{runway_years:.1f} years at Year 0 burn",
                    "Consider larger funding or lower costs",
                )

    # ---- results ----

    def print_results(self) -> bool:
        errors = [i for i in self.issues if i.level == ValidationLevel.ERROR]
        warnings = [i for i in self.issues if i.level == ValidationLevel.WARNING]
        infos = [i for i in self.issues if i.level == ValidationLevel.INFO]

        if errors:
            print("\n ERRORS (must fix):")
            for issue in errors:
                print(f"  [{issue.field}] {issue.message}")
                if issue.suggestion:
                    print(f"     -> {issue.suggestion}")
        if warnings:
            print("\n  WARNINGS (review):")
            for issue in warnings:
                print(f"  [{issue.field}] {issue.message}")
                if issue.suggestion:
                    print(f"     -> {issue.suggestion}")
        if infos:
            print("\n  INFO:")
            for issue in infos:
                print(f"  [{issue.field}] {issue.message}")

        print("\n" + "=" * 60)
        if not errors and not warnings:
            print("  Configuration is VALID")
            print("=" * 60)
            return True
        elif not errors:
            print(
                f"  Configuration has {len(warnings)} WARNING(S) — review before proceeding"
            )
            print("=" * 60)
            return True
        else:
            print(f"  Configuration has {len(errors)} ERROR(S) — fix before building")
            print("=" * 60)
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate financial model configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )
    args = parser.parse_args()

    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Config not found: {args.config}")
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        sys.exit(2)

    validator = ConfigValidator(config, strict=args.strict)
    validator.validate_all()

    errors = [i for i in validator.issues if i.level == ValidationLevel.ERROR]
    warnings = [i for i in validator.issues if i.level == ValidationLevel.WARNING]

    if errors:
        sys.exit(2)
    elif warnings and args.strict:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
