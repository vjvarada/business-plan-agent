#!/usr/bin/env python3
"""
Industry Benchmark Analyzer
===========================
Researches and analyzes industry benchmarks for financial model validation.
Uses SerpAPI to gather real-world data on comparable companies.

Usage:
    python analyze_benchmarks.py --mode sm --industry "3D printing software"
    python analyze_benchmarks.py --mode cac --industry "B2B SaaS manufacturing"
    python analyze_benchmarks.py --mode valuation --industry "AI automation"
    python analyze_benchmarks.py --mode comprehensive --industry "design automation AI"

Modes:
    sm          - Sales & Marketing benchmarks (S&M % of revenue)
    cac         - Customer Acquisition Cost benchmarks
    valuation   - Revenue multiples and valuation benchmarks
    margins     - Gross margin and EBITDA margin benchmarks
    comprehensive - All of the above
"""

import argparse
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    from serpapi import GoogleSearch
except ImportError:
    print("Installing serpapi...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-search-results"])
    from serpapi import GoogleSearch


def search_benchmarks(query: str, num_results: int = 10) -> dict:
    """Search for benchmark data using SerpAPI"""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set")
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
        "hl": "en"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    organic_results = []
    for result in results.get("organic_results", []):
        organic_results.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet"),
        })
    
    related = []
    for q in results.get("related_questions", []):
        related.append({
            "question": q.get("question"),
            "snippet": q.get("snippet")
        })
    
    return {
        "query": query,
        "results": organic_results,
        "related_questions": related,
        "timestamp": datetime.now().isoformat()
    }


def analyze_sm_benchmarks(industry: str) -> dict:
    """Analyze Sales & Marketing spend benchmarks"""
    queries = [
        f"{industry} sales marketing expense percentage revenue",
        f"{industry} SG&A selling general administrative expenses annual report",
        "B2B SaaS sales marketing spend benchmark 2024 2025",
        "Gartner manufacturing marketing budget benchmark"
    ]
    
    results = []
    for q in queries:
        results.append(search_benchmarks(q))
    
    # Standard benchmarks
    benchmarks = {
        "industry": industry,
        "mode": "sales_marketing",
        "research_results": results,
        "standard_benchmarks": {
            "pre_revenue_y0": {"range": "40-60%", "notes": "Heavy investment in GTM"},
            "early_y1_y2": {"range": "35-50%", "notes": "Building sales team, brand"},
            "growth_y3_y4": {"range": "25-40%", "notes": "Scaling efficiently"},
            "scale_y5_plus": {"range": "15-25%", "notes": "Mature, word-of-mouth"},
        },
        "company_benchmarks": {
            "materialise": {"sm_pct": "23%", "gross_margin": "56.5%", "revenue": "$289M"},
            "stratasys": {"sm_pct": "25%", "gross_margin": "45%", "revenue": "$573M"},
            "3d_systems": {"sm_pct": "28%", "gross_margin": "37-40%", "revenue": "$450M"},
        }
    }
    
    return benchmarks


def analyze_cac_benchmarks(industry: str) -> dict:
    """Analyze Customer Acquisition Cost benchmarks"""
    queries = [
        f"{industry} CAC customer acquisition cost benchmark",
        "enterprise B2B software CAC benchmark 2024 2025",
        "B2B SaaS customer acquisition cost industry average",
        "LTV CAC ratio benchmark SaaS"
    ]
    
    results = []
    for q in queries:
        results.append(search_benchmarks(q))
    
    benchmarks = {
        "industry": industry,
        "mode": "customer_acquisition",
        "research_results": results,
        "standard_benchmarks": {
            "b2b_general": {"cac": "$536", "source": "First Page Sage"},
            "b2b_saas": {"cac": "$700-1,200", "source": "Phoenix Strategy"},
            "enterprise_saas": {"cac": "$10,000-50,000", "source": "Industry avg"},
            "manufacturing_software": {"cac": "$15,000-40,000", "source": "Technical sales"},
        },
        "ratios": {
            "ltv_cac_good": ">3x",
            "ltv_cac_excellent": ">5x",
            "cac_payback_good": "<18 months",
            "cac_payback_excellent": "<12 months",
        }
    }
    
    return benchmarks


def analyze_valuation_benchmarks(industry: str) -> dict:
    """Analyze valuation multiples benchmarks"""
    queries = [
        f"{industry} revenue multiple valuation 2024",
        "AI SaaS company valuation multiple seed series A",
        f"{industry} comparable company valuation",
        "B2B SaaS revenue multiple by growth rate"
    ]
    
    results = []
    for q in queries:
        results.append(search_benchmarks(q))
    
    benchmarks = {
        "industry": industry,
        "mode": "valuation",
        "research_results": results,
        "standard_benchmarks": {
            "traditional_saas": {
                "seed": "8-15x revenue",
                "series_a": "6-12x revenue",
                "series_b": "5-10x revenue"
            },
            "ai_native": {
                "seed": "12-30x revenue",
                "series_a": "10-20x revenue",
                "series_b": "8-15x revenue"
            }
        },
        "comparables": {
            "materialise": {"multiple": "~3x", "notes": "Mature, lower growth"},
            "figma": {"multiple": "50x", "notes": "High growth design"},
            "canva": {"multiple": "25-30x", "notes": "AI-enhanced"},
        }
    }
    
    return benchmarks


def analyze_margin_benchmarks(industry: str) -> dict:
    """Analyze margin benchmarks"""
    queries = [
        f"{industry} gross margin EBITDA margin",
        "B2B SaaS gross margin benchmark",
        f"{industry} operating margin profit margin",
        "manufacturing software gross margin industry"
    ]
    
    results = []
    for q in queries:
        results.append(search_benchmarks(q))
    
    benchmarks = {
        "industry": industry,
        "mode": "margins",
        "research_results": results,
        "standard_benchmarks": {
            "gross_margin": {
                "saas_pure": "70-85%",
                "saas_hardware": "50-70%",
                "manufacturing_sw": "40-60%"
            },
            "ebitda_margin": {
                "startup": "-20% to 0%",
                "growth": "0-15%",
                "mature": "15-30%"
            }
        }
    }
    
    return benchmarks


def print_analysis(benchmarks: dict):
    """Print formatted analysis"""
    print("=" * 80)
    print(f"BENCHMARK ANALYSIS: {benchmarks['industry'].upper()}")
    print(f"Mode: {benchmarks['mode']}")
    print("=" * 80)
    
    if "standard_benchmarks" in benchmarks:
        print("\nSTANDARD BENCHMARKS:")
        print("-" * 40)
        for key, value in benchmarks["standard_benchmarks"].items():
            if isinstance(value, dict):
                print(f"\n  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
    
    if "company_benchmarks" in benchmarks:
        print("\nCOMPARABLE COMPANIES:")
        print("-" * 40)
        for company, data in benchmarks["company_benchmarks"].items():
            print(f"\n  {company}:")
            for k, v in data.items():
                print(f"    {k}: {v}")
    
    if "ratios" in benchmarks:
        print("\nKEY RATIOS:")
        print("-" * 40)
        for k, v in benchmarks["ratios"].items():
            print(f"  {k}: {v}")
    
    print("\n" + "=" * 80)
    print("RESEARCH SOURCES:")
    print("-" * 40)
    for research in benchmarks.get("research_results", []):
        print(f"\nQuery: {research['query']}")
        for i, r in enumerate(research.get("results", [])[:3], 1):
            print(f"  {i}. {r['title']}")
            print(f"     {r['link']}")


def main():
    parser = argparse.ArgumentParser(description="Analyze industry benchmarks")
    parser.add_argument("--mode", required=True, 
                       choices=["sm", "cac", "valuation", "margins", "comprehensive"],
                       help="Analysis mode")
    parser.add_argument("--industry", required=True, help="Industry to analyze")
    parser.add_argument("--output", help="Output file (JSON)")
    
    args = parser.parse_args()
    
    all_benchmarks = {}
    
    if args.mode == "sm" or args.mode == "comprehensive":
        all_benchmarks["sales_marketing"] = analyze_sm_benchmarks(args.industry)
        print_analysis(all_benchmarks["sales_marketing"])
    
    if args.mode == "cac" or args.mode == "comprehensive":
        all_benchmarks["cac"] = analyze_cac_benchmarks(args.industry)
        print_analysis(all_benchmarks["cac"])
    
    if args.mode == "valuation" or args.mode == "comprehensive":
        all_benchmarks["valuation"] = analyze_valuation_benchmarks(args.industry)
        print_analysis(all_benchmarks["valuation"])
    
    if args.mode == "margins" or args.mode == "comprehensive":
        all_benchmarks["margins"] = analyze_margin_benchmarks(args.industry)
        print_analysis(all_benchmarks["margins"])
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(all_benchmarks, f, indent=2)
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
