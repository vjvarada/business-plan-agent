#!/usr/bin/env python3
"""
Validate execution/script_stage_registry.json coverage.

Ensures every Python script in execution/ is mapped to at least one
stage/group.

Usage:
  python execution/validate_script_registry.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    execution_dir = Path("execution")
    registry_file = execution_dir / "script_stage_registry.json"

    if not registry_file.exists():
        print("❌ Registry file missing: execution/script_stage_registry.json")
        return 1

    with open(registry_file, "r", encoding="utf-8") as handle:
        registry = json.load(handle)

    mapped = set()
    for scripts in registry.get("stages", {}).values():
        mapped.update(scripts)

    discovered = {
        path.name
        for path in execution_dir.glob("*.py")
        if path.name != "validate_script_registry.py"
    }

    missing = sorted(discovered - mapped)
    unknown = sorted(mapped - discovered)

    if missing:
        print("❌ Unmapped scripts:")
        for script in missing:
            print(f"  - {script}")
    else:
        print("✅ All execution scripts are mapped in stage registry")

    if unknown:
        print("\n⚠️ Registry entries not found as scripts:")
        for script in unknown:
            print(f"  - {script}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
