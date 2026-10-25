#!/usr/bin/env python3
"""Weighted-pipeline summary from a prospect tracker CSV.

Usage: python execution/pipeline_summary.py --file .tmp/<project>/pipeline/prospect_tracker.csv
Counts prospects by type and stage, and sums probability-weighted ACV (INR lakh) and expected signings.
"""
import argparse
import csv
import sys
from collections import Counter


def num(v):
    try:
        return float(str(v).strip())
    except ValueError:
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.file, encoding="utf-8-sig")))
    filled = [r for r in rows if r.get("company", "").strip()]
    print(f"Prospects with a company named: {len(filled)} of {len(rows)} slots")
    for t in ("pilot", "direct"):
        sub = [r for r in filled if r["type"] == t]
        exp = sum(num(r["probability_pct"]) / 100 for r in sub)
        acv = sum(num(r["probability_pct"]) / 100 * num(r["acv_inr_lakh"]) for r in sub)
        print(f"{t}: {len(sub)} named, {exp:.1f} expected signings, weighted ACV Rs {acv:.1f} lakh")
        for st, n in sorted(Counter(r["stage"] or "(unset)" for r in sub).items()):
            print(f"   {st}: {n}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
