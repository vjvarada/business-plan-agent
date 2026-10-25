#!/usr/bin/env python3
"""Renumber a business plan section's references so they run 1, 2, 3… in list order.

- Merges category headings that repeat (e.g. "### Internal Data" and
  "### Internal Data (continued)") into one group, keeping first-appearance order
- Renumbers anchors, list numbers and every inline citation [[X]](#ref-X)
- Reports missing anchors and unreferenced sources

Usage:
  python execution/renumber_references.py --file .tmp/<project>/business_plan/sections/07_Revenue_Model.md
  python execution/renumber_references.py --file <section.md> --check   # report only, no write
"""
import argparse
import re
import sys
from pathlib import Path

HEADING = "## References & Sources"
BLOCK = re.compile(
    r'<a name="ref-(\d+)"></a>\s*\n\s*\n(\d+\.\s.*?)(?=\n\s*\n(?:<a name|###)|\Z)', re.S
)
CITE = re.compile(r"\[\[(\d+)\]\]\(#ref-(\d+)\)")


def parse_references(refs):
    """Return [(category, [(old_number, block_text), ...]), ...] merged by category name."""
    groups = {}
    order = []
    for part in re.split(r"^### ", refs, flags=re.M)[1:]:
        title, _, body = part.partition("\n")
        name = re.sub(r"\s*\(continued\)\s*$", "", title.strip(), flags=re.I)
        if name not in groups:
            groups[name] = []
            order.append(name)
        for m in BLOCK.finditer(body):
            groups[name].append((int(m.group(1)), m.group(2).strip()))
    return [(name, groups[name]) for name in order]


def renumber(text):
    if HEADING not in text:
        raise ValueError(f"no '{HEADING}' heading found")
    body, refs = text.split(HEADING, 1)
    grouped = parse_references(refs)
    remap = {}
    out = HEADING + "\n"
    n = 0
    for name, blocks in grouped:
        out += f"\n### {name}\n"
        for old, block in blocks:
            n += 1
            remap[old] = n
            block = re.sub(r"^\d+\.\s", f"{n}. ", block)
            out += f'\n<a name="ref-{n}"></a>\n\n{block}\n'
    cited = {int(m.group(1)) for m in CITE.finditer(body)}
    missing = sorted(cited - set(remap))
    unused = sorted(set(remap) - cited)
    body = CITE.sub(lambda m: "[[{0}]](#ref-{0})".format(remap.get(int(m.group(1)), m.group(1))), body)
    return body + out, remap, missing, unused


def main():
    parser = argparse.ArgumentParser(description="Renumber section references sequentially")
    parser.add_argument("--file", required=True)
    parser.add_argument("--check", action="store_true", help="Report only; do not write")
    args = parser.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")
    new_text, remap, missing, unused = renumber(text)
    changed = {o: n for o, n in remap.items() if o != n}

    print(f"{path.name}: {len(remap)} references")
    if changed:
        print("  renumbered: " + ", ".join(f"{o}→{n}" for o, n in sorted(changed.items())))
    if missing:
        print(f"  MISSING ANCHORS for citations: {missing}")
    if unused:
        print(f"  UNREFERENCED sources: {unused}")
    if not args.check and new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print("  ✓ written")
    return 1 if missing else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
