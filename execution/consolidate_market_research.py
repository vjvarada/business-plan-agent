#!/usr/bin/env python3
"""
Consolidate Research - Comprehensive categorized research management

Aggregates ALL research files into categorized sources of truth:

RESEARCH CATEGORIES:
1. Market Research - TAM/SAM/SOM, market size, industry trends
2. Headcount/Hiring - Team composition, salaries, roles, hiring benchmarks
3. Geographic/Location - Regional data, market entry, expansion
4. Business Model - Revenue models, pricing, unit economics
5. Competitors - Competitive landscape, positioning
6. Financial Benchmarks - CAC, LTV, margins, ratios

Each category gets its own consolidated file with deduplication and metadata.
"""
import argparse
import glob
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def categorize_research_file(filename):
    """Determine research category from filename"""
    name_lower = filename.lower()

    # Category mapping
    if any(
        kw in name_lower
        for kw in ["headcount", "hiring", "salary", "team", "roles", "staffing"]
    ):
        return "headcount"
    elif any(
        kw in name_lower
        for kw in ["market_research", "tam", "sam", "industry", "market_size"]
    ):
        return "market"
    elif any(
        kw in name_lower
        for kw in ["location", "geographic", "regional", "country", "india", "asia"]
    ):
        return "geographic"
    elif any(
        kw in name_lower
        for kw in ["business_model", "revenue_model", "pricing", "unit_economics"]
    ):
        return "business_model"
    elif any(kw in name_lower for kw in ["competitor", "competitive", "landscape"]):
        return "competitors"
    elif any(
        kw in name_lower
        for kw in ["benchmark", "cac", "ltv", "margin", "ratio", "financial"]
    ):
        return "benchmarks"
    else:
        return "general"


def extract_market_sizes(text):
    """Extract market size mentions from text"""
    sizes = []
    # Match patterns like "$5.2B", "$150M", "$3.5 billion", "USD 2.1 million"
    patterns = [
        r"\$\s*([0-9,.]+)\s*(B|M|billion|million|trillion)",
        r"USD\s*([0-9,.]+)\s*(B|M|billion|million|trillion)",
        r"([0-9,.]+)\s*(billion|million|trillion)\s*USD",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.I)
        for size, unit in matches:
            # Normalize
            size = size.replace(",", "")
            unit = unit.lower()
            if unit in ["b", "billion"]:
                unit = "billion"
            elif unit in ["m", "million"]:
                unit = "million"
            sizes.append({"value": float(size), "unit": unit})
    return sizes


def categorize_source(filename, title, snippet):
    """Categorize a source based on content"""
    categories = []

    # Geographic
    if any(
        kw in filename.lower() or kw in title.lower() or kw in snippet.lower()
        for kw in ["asia", "india", "apac", "southeast asia"]
    ):
        categories.append("geographic_asia")

    # Use cases
    use_case_keywords = {
        "jigs": ["jig", "fixture", "tooling"],
        "drilling_guides": ["drilling guide", "drill guide"],
        "assembly_guides": ["assembly guide", "assembly fixture"],
        "shadow_boxes": ["shadow box", "foam organizer"],
        "soft_jaws": ["soft jaw", "custom jaw"],
        "reverse_engineering": ["reverse engineer", "3d scan"],
        "sand_casting": ["sand casting", "foundry pattern"],
        "vacuum_casting": ["vacuum cast", "urethane cast"],
        "generative_design": ["generative design", "topology optimization"],
    }

    for category, keywords in use_case_keywords.items():
        if any(
            kw in filename.lower() or kw in title.lower() or kw in snippet.lower()
            for kw in keywords
        ):
            categories.append(f"use_case_{category}")

    # Market data
    if any(
        kw in title.lower() or kw in snippet.lower()
        for kw in ["market size", "market value", "cagr", "forecast", "analysis"]
    ):
        categories.append("market_data")

    # Competitors
    if any(
        kw in title.lower() or kw in snippet.lower()
        for kw in ["competitor", "companies", "vendors", "players"]
    ):
        categories.append("competitors")

    # Trends
    if any(
        kw in title.lower() or kw in snippet.lower()
        for kw in ["trend", "future", "growth", "adoption", "demand"]
    ):
        categories.append("trends")

    return categories if categories else ["general"]


def load_existing_research(output_dir):
    """Load existing consolidated research files to merge with new data"""
    existing = {}

    if not os.path.exists(output_dir):
        return existing

    # Load each category file if it exists
    category_files = [
        "market_research.json",
        "headcount_research.json",
        "geographic_research.json",
        "business_model_research.json",
        "competitors_research.json",
        "benchmarks_research.json",
        "general_research.json",
    ]

    for filename in category_files:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    category_id = filename.replace("_research.json", "")
                    existing[category_id] = {
                        "sources": data.get("sources", []),
                        "market_sizes": data.get("market_sizes", []),
                        "data_points": data.get("data_points", []),
                    }
            except:
                pass

    return existing


def merge_research(existing_research, new_data, category):
    """Merge new research with existing, deduplicating by URL"""

    # Get existing sources for this category
    existing_sources = existing_research.get(category, {}).get("sources", [])
    existing_urls = {s.get("url", "") for s in existing_sources if s.get("url")}

    # Track what's new
    added_count = 0
    duplicate_count = 0

    # Merge sources
    merged_sources = list(existing_sources)  # Start with existing
    for new_source in new_data.get("sources", []):
        url = new_source.get("url", "")
        if url and url not in existing_urls:
            merged_sources.append(new_source)
            existing_urls.add(url)
            added_count += 1
        elif url:
            duplicate_count += 1

    # Merge market sizes (for market research category)
    merged_market_sizes = existing_research.get(category, {}).get("market_sizes", [])
    if "market_sizes" in new_data:
        merged_market_sizes.extend(new_data["market_sizes"])

    # Merge data points (for other categories)
    merged_data_points = existing_research.get(category, {}).get("data_points", [])
    if "data_points" in new_data:
        merged_data_points.extend(new_data["data_points"])

    return {
        "sources": merged_sources,
        "market_sizes": merged_market_sizes,
        "data_points": merged_data_points,
        "stats": {
            "added": added_count,
            "duplicates": duplicate_count,
            "total": len(merged_sources),
        },
    }


def consolidate(research_dir, output_dir=None, incremental=True):
    """Consolidate all research files with categorization and incremental merging"""

    # Load existing research if incremental mode
    existing_research = {}
    if incremental and output_dir:
        existing_research = load_existing_research(output_dir)
        if existing_research:
            print(f"\n📚 Loading existing research database...")
            for cat_id, cat_data in existing_research.items():
                print(
                    f"   {cat_id}: {len(cat_data.get('sources', []))} existing sources"
                )

    # Track unique URLs to avoid duplicates
    seen_urls = set()

    # Pre-populate seen_urls with existing URLs
    for cat_id, cat_data in existing_research.items():
        for source in cat_data.get("sources", []):
            url = source.get("url", "")
            if url:
                seen_urls.add(url)

    # Organized by research category
    categories = {
        "market": {
            "name": "Market Research",
            "description": "TAM/SAM/SOM, market size, industry trends",
            "sources": [],
            "market_sizes": [],
            "files": [],
        },
        "headcount": {
            "name": "Headcount & Hiring",
            "description": "Team composition, salaries, roles, hiring benchmarks",
            "sources": [],
            "data_points": [],
            "files": [],
        },
        "geographic": {
            "name": "Geographic & Location",
            "description": "Regional data, market entry, expansion strategies",
            "sources": [],
            "regional_data": [],
            "files": [],
        },
        "business_model": {
            "name": "Business Model",
            "description": "Revenue models, pricing, unit economics",
            "sources": [],
            "data_points": [],
            "files": [],
        },
        "competitors": {
            "name": "Competitors",
            "description": "Competitive landscape, positioning",
            "sources": [],
            "companies": [],
            "files": [],
        },
        "benchmarks": {
            "name": "Financial Benchmarks",
            "description": "CAC, LTV, margins, financial ratios",
            "sources": [],
            "metrics": [],
            "files": [],
        },
        "general": {
            "name": "General Research",
            "description": "Uncategorized research data",
            "sources": [],
            "files": [],
        },
    }

    metadata = {
        "consolidated_at": datetime.now().isoformat(),
        "total_files": 0,
        "total_sources": 0,
        "unique_sources": 0,
        "duplicates_removed": 0,
        "new_sources": 0,  # Track what's new in this run
        "mode": "incremental" if incremental else "full",
    }

    # Find all research files
    json_files = glob.glob(os.path.join(research_dir, "*.json"))
    research_files = [
        f
        for f in json_files
        if not any(
            skip in os.path.basename(f)
            for skip in [
                "consolidated",
                "config",
                "template",
                "output",
                "content",
                "structure",
                "result",
                "input",
            ]
        )
    ]

    for filepath in research_files:
        filename = os.path.basename(filepath)
        category = categorize_research_file(filename)

        metadata["total_files"] += 1
        categories[category]["files"].append(filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                research = json.load(f)
        except:
            continue

        # Process based on category
        if category == "market":
            # Process market research (SERP results)
            for result in research.get("organic_results", []):
                url = result.get("link", "")
                title = result.get("title", "")
                snippet = result.get("snippet", "")

                metadata["total_sources"] += 1

                if url and url in seen_urls:
                    metadata["duplicates_removed"] += 1
                    continue

                if url:
                    seen_urls.add(url)
                    metadata["unique_sources"] += 1

                # Extract market sizes
                market_sizes = extract_market_sizes(snippet)
                for size in market_sizes:
                    categories[category]["market_sizes"].append(
                        {
                            "value": size["value"],
                            "unit": size["unit"],
                            "source_title": title,
                            "source_url": url,
                            "file_source": filename.replace(
                                "market_research_", ""
                            ).replace(".json", ""),
                        }
                    )

                categories[category]["sources"].append(
                    {
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "file_source": filename,
                    }
                )

        elif category == "headcount":
            # Process headcount research
            for result in research.get("organic_results", []):
                url = result.get("link", "")
                title = result.get("title", "")
                snippet = result.get("snippet", "")

                metadata["total_sources"] += 1

                if url and url in seen_urls:
                    metadata["duplicates_removed"] += 1
                    continue

                if url:
                    seen_urls.add(url)
                    metadata["unique_sources"] += 1

                # Extract salary/headcount data
                salary_patterns = [
                    r"₹\s*([0-9,.]+)\s*(L|lakh|lakhs|cr|crore)",
                    r"\$\s*([0-9,.]+)k?\s*(per year|annually|salary)",
                    r"([0-9,.]+)\s*(employees|headcount|team size)",
                ]

                data_points = []
                for pattern in salary_patterns:
                    matches = re.findall(pattern, snippet, re.I)
                    for value, unit in matches:
                        data_points.append(
                            {"value": value, "unit": unit, "context": snippet[:100]}
                        )

                categories[category]["sources"].append(
                    {
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "data_points": data_points,
                        "file_source": filename,
                    }
                )

        elif category in ["geographic", "business_model", "competitors", "benchmarks"]:
            # Process other research types
            for result in research.get("organic_results", []):
                url = result.get("link", "")
                title = result.get("title", "")
                snippet = result.get("snippet", "")

                metadata["total_sources"] += 1

                if url and url in seen_urls:
                    metadata["duplicates_removed"] += 1
                    continue

                if url:
                    seen_urls.add(url)
                    metadata["unique_sources"] += 1
                    metadata["new_sources"] += 1  # Track new sources in this run

                categories[category]["sources"].append(
                    {
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "file_source": filename,
                    }
                )

        else:  # general
            # Store as-is for uncategorized
            if isinstance(research, dict) and "organic_results" in research:
                for result in research.get("organic_results", []):
                    url = result.get("link", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        metadata["unique_sources"] += 1
                        metadata["new_sources"] += 1
                        categories[category]["sources"].append(result)

    # Merge with existing research if incremental mode
    if incremental and existing_research:
        print(f"\n🔄 Merging with existing research...")
        merge_stats = {}

        for cat_id in categories.keys():
            merged = merge_research(
                existing_research,
                {
                    "sources": categories[cat_id]["sources"],
                    "market_sizes": categories[cat_id].get("market_sizes", []),
                    "data_points": categories[cat_id].get("data_points", []),
                },
                cat_id,
            )

            # Replace category data with merged data
            categories[cat_id]["sources"] = merged["sources"]
            if "market_sizes" in categories[cat_id]:
                categories[cat_id]["market_sizes"] = merged["market_sizes"]
            if "data_points" in categories[cat_id]:
                categories[cat_id]["data_points"] = merged["data_points"]

            merge_stats[cat_id] = merged["stats"]

        # Update metadata with merge stats
        total_added = sum(s["added"] for s in merge_stats.values())
        total_existing = sum(s["total"] for s in merge_stats.values()) - total_added

        metadata["merge_stats"] = {
            "new_sources_added": total_added,
            "existing_sources_preserved": total_existing,
            "by_category": merge_stats,
        }

    return {"metadata": metadata, "categories": categories}


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Consolidate all research files into categorized sources of truth"
    )
    p.add_argument(
        "--research-dir",
        default=".tmp",
        help="Directory containing research JSON files",
    )
    p.add_argument(
        "--output-dir",
        default=".tmp/consolidated_research",
        help="Output directory for categorized research files",
    )
    p.add_argument(
        "--single-file",
        help="Output single consolidated file instead of category files",
    )
    p.add_argument(
        "--full-rebuild",
        action="store_true",
        help="Rebuild from scratch instead of incremental merge (default: incremental)",
    )
    p.add_argument("--verbose", action="store_true", help="Print detailed statistics")
    args = p.parse_args()

    # Incremental mode by default, unless --full-rebuild is specified
    incremental = not args.full_rebuild

    data = consolidate(args.research_dir, args.output_dir, incremental=incremental)

    # Print summary
    mode_label = "Incremental Update" if incremental else "Full Rebuild"
    print(f"\n✓ Consolidated Research ({mode_label})")
    print(f"  Total files processed: {data['metadata']['total_files']}")
    print(f"  Total sources in input: {data['metadata']['total_sources']}")
    print(f"  New unique sources: {data['metadata']['new_sources']}")
    print(f"  Duplicates skipped: {data['metadata']['duplicates_removed']}")

    # Show merge stats if incremental
    if incremental and "merge_stats" in data["metadata"]:
        stats = data["metadata"]["merge_stats"]
        print(f"\n  Merge Results:")
        print(f"    Added to database: {stats['new_sources_added']} sources")
        print(f"    Already in database: {stats['existing_sources_preserved']} sources")

    print(f"\n  Research Categories:")
    for cat_id, cat_data in data["categories"].items():
        if cat_data["sources"] or cat_data["files"]:
            total = len(cat_data["sources"])
            new_count = 0
            if incremental and "merge_stats" in data["metadata"]:
                new_count = (
                    data["metadata"]["merge_stats"]["by_category"]
                    .get(cat_id, {})
                    .get("added", 0)
                )

            if new_count > 0:
                print(f"    {cat_data['name']}: {total} sources (+{new_count} new)")
            else:
                print(f"    {cat_data['name']}: {total} sources")

    # Save consolidated data
    if args.single_file:
        # Single file output
        with open(args.single_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Saved to {args.single_file}\n")
    else:
        # Category-based files
        os.makedirs(args.output_dir, exist_ok=True)

        for cat_id, cat_data in data["categories"].items():
            if cat_data["sources"] or cat_data["files"]:
                output_file = os.path.join(args.output_dir, f"{cat_id}_research.json")
                category_output = {
                    "category": cat_data["name"],
                    "description": cat_data["description"],
                    "consolidated_at": data["metadata"]["consolidated_at"],
                    "source_files": cat_data["files"],
                    "sources": cat_data["sources"],
                }

                # Add category-specific data
                if "market_sizes" in cat_data and cat_data["market_sizes"]:
                    category_output["market_sizes"] = cat_data["market_sizes"]
                if "data_points" in cat_data and cat_data["data_points"]:
                    category_output["data_points"] = cat_data["data_points"]

                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(category_output, f, indent=2)

                if args.verbose:
                    print(
                        f"    Saved {cat_id}_research.json ({len(cat_data['sources'])} sources)"
                    )

        # Also save complete metadata
        metadata_file = os.path.join(args.output_dir, "_metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(data["metadata"], f, indent=2)

        print(f"\n✓ Saved categorized research to {args.output_dir}/\n")
