#!/usr/bin/env python3
"""Check business plan sections against the category creation narrative standard.

Reference: directives/CATEGORY_CREATION_NARRATIVE.md

Errors (exit 1):
  - 00_Category_Design.md missing or missing a required heading
  - Banned cliches outside quotes and outside References sections

Warnings (exit 0):
  - Superlatives without an inline citation in the same sentence
  - Label-style H2 headlines (Ogilvy: headlines should be claims)
  - Category name not mentioned in a section
  - "leverage" used (banned as a verb; allowed as a finance noun)
"""
import argparse
import re
import sys
from pathlib import Path

CATEGORY_FILE = "00_Category_Design.md"

REQUIRED_HEADINGS = [
    "Executive Summary",
    "The Big Idea",
    "The Problem We Name",
    "The Enemy",
    "From → To",
    "Category Name",
    "Point of View",
    "The Psychological Job",
    "Who It Is For (and Not For)",
    "Proof Points",
    "Key Insights",
    "Investment Implications",
    "References & Sources",
]

STANDARD_H2 = {
    "executive summary",
    "key insights",
    "investment implications",
    "references & sources",
}

BANNED = [
    "revolutionary", "game-changing", "game changer", "game-changer",
    "cutting-edge", "cutting edge", "best-in-class", "world-class",
    "seamless", "seamlessly", "synergy", "synergies", "next-gen",
    "next-generation", "paradigm shift", "disruptive", "holistic",
    "robust solution", "state-of-the-art", "unlock value", "empower",
    "empowers", "empowering", "one-stop shop", "one-stop-shop",
]

SUPERLATIVE = re.compile(
    r"\b(the only|the first to|first-ever|the leading|largest|biggest|the best|best|#1|"
    r"number one|market leader|unmatched|unrivalled|unrivaled)\b",
    re.IGNORECASE,
)
CITATION = re.compile(r"\[\[\d+\]\]\(#ref-\d+\)")
QUOTED = re.compile(r"\"[^\"]*\"|“[^”]*”|\*\"[^\"]*\"\*")


def body_without_references(text):
    """Return text before the References section (sources may quote anything)."""
    match = re.search(r"^##\s+References", text, re.MULTILINE)
    return text[: match.start()] if match else text


def strip_quotes(line):
    return QUOTED.sub("", line)


def check_category_file(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    # AGENTS.md template puts Key Insights / Investment Implications at H3
    headings = [h.strip() for h in re.findall(r"^#{2,3}\s+(.+)$", text, re.MULTILINE)]
    for required in REQUIRED_HEADINGS:
        if not any(h.lower().startswith(required.lower()) for h in headings):
            errors.append(f"{path.name}: missing required heading '## {required}'")
    title = re.search(r"^#\s+Category Design:\s*(.+)$", text, re.MULTILINE)
    name = title.group(1).strip() if title else None
    if not name:
        errors.append(f"{path.name}: title must be '# Category Design: <Category Name>'")
    elif not 2 <= len(name.split()) <= 4:
        errors.append(f"{path.name}: category name '{name}' should be 2-4 words")
    return errors, name


def check_section(path, category_name):
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    body = body_without_references(text)

    for lineno, line in enumerate(body.splitlines(), 1):
        if line.lstrip().startswith(">"):
            continue
        clean = strip_quotes(line)
        lower = clean.lower()
        for word in BANNED:
            if re.search(rf"(?<![\w-]){re.escape(word)}(?![\w-])", lower):
                errors.append(f"{path.name}:{lineno}: banned cliche '{word}'")
        if re.search(r"\bleverag(e|es|ed|ing)\b", lower):
            warnings.append(f"{path.name}:{lineno}: 'leverage' — use a plain verb unless it is the finance noun")
        if line.startswith("#") and "ai-powered" in lower:
            errors.append(f"{path.name}:{lineno}: 'AI-powered' in a headline")
        for sentence in re.split(r"(?<=[.!?])\s+", clean):
            if SUPERLATIVE.search(sentence) and not CITATION.search(sentence):
                found = SUPERLATIVE.search(sentence).group(0)
                warnings.append(f"{path.name}:{lineno}: superlative '{found}' without a citation")

    if path.name != CATEGORY_FILE:
        for heading in re.findall(r"^##\s+(.+)$", body, re.MULTILINE):
            h = heading.strip()
            if h.lower() not in STANDARD_H2 and len(h.split()) < 4:
                warnings.append(f"{path.name}: H2 '{h}' reads as a label — make it a claim")
        if category_name and category_name.lower() not in text.lower():
            warnings.append(f"{path.name}: category name '{category_name}' not mentioned")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Check category creation narrative standard")
    parser.add_argument("--sections-dir", required=True, help="Business plan sections directory")
    args = parser.parse_args()

    sections_dir = Path(args.sections_dir)
    if not sections_dir.is_dir():
        print(f"ERROR: sections directory not found: {sections_dir}")
        return 1

    errors, warnings = [], []
    category_name = None
    category_path = sections_dir / CATEGORY_FILE
    if category_path.exists():
        file_errors, category_name = check_category_file(category_path)
        errors.extend(file_errors)
    else:
        errors.append(f"missing {CATEGORY_FILE} (write it first — see directives/CATEGORY_CREATION_NARRATIVE.md)")

    for path in sorted(sections_dir.glob("[0-9][0-9]_*.md")):
        file_errors, file_warnings = check_section(path, category_name)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\n✓ Category narrative check passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
