#!/usr/bin/env python3
"""
Edit Financial Model - Local-First Workflow Helper
===================================================
Orchestrates the complete local-first editing workflow for Google Sheets financial models.

⚠️ WHEN TO USE THIS SCRIPT:
   ✅ Updating values (funding amounts, growth rates, pricing)
   ✅ Fixing formulas (convert hardcoded to formula, fix #REF!)
   ✅ Bulk edits (same structure, different values)

⚠️ DO NOT USE FOR:
   ❌ Adding/removing revenue streams → Use create_financial_model.py with updated config
   ❌ Changing TAM/SAM structure → Use create_financial_model.py with updated config
   ❌ Adding/removing rows → Use create_financial_model.py with updated config
   ❌ Major business model changes → Use create_financial_model.py with updated config

📖 Full decision tree: directives/DECISION_TREE.md

This script automates the 5-step workflow:
1. Download snapshot
2. (User edits CSV files)
3. Validate changes
4. Preview changes (dry run)
5. Apply changes to Google Sheets

Usage:
    # Step 1: Download current model
    python edit_financial_model.py --sheet-id "1-Ss62..." --download

    # Step 2: Edit CSV files in .tmp/snapshot/sheets/
    #         - Edit *_formulas.csv to change formulas
    #         - Edit *.csv to change values

    # Step 3: Validate your changes
    python edit_financial_model.py --sheet-id "1-Ss62..." --validate

    # Step 4: Preview what will change
    python edit_financial_model.py --sheet-id "1-Ss62..." --preview

    # Step 5: Apply changes
    python edit_financial_model.py --sheet-id "1-Ss62..." --apply

    # All-in-one (download + validate + preview)
    python edit_financial_model.py --sheet-id "1-Ss62..." --prepare

    # Backup before editing
    python edit_financial_model.py --sheet-id "1-Ss62..." --backup

Examples:
    # Standard workflow
    python edit_financial_model.py --sheet-id "1-Ss62..." --download
    # ... edit CSV files ...
    python edit_financial_model.py --sheet-id "1-Ss62..." --validate
    python edit_financial_model.py --sheet-id "1-Ss62..." --preview
    python edit_financial_model.py --sheet-id "1-Ss62..." --apply

    # Quick prepare for editing
    python edit_financial_model.py --sheet-id "1-Ss62..." --prepare
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}\n")
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed")
        return False

    print(f"\n✅ {description} completed")
    return True


def download_snapshot(sheet_id, output_dir=".tmp/snapshot"):
    """Download snapshot from Google Sheets."""
    cmd = [
        sys.executable,
        "execution/download_model_snapshot.py",
        "--sheet-id",
        sheet_id,
        "--output",
        output_dir,
    ]
    return run_command(cmd, "STEP 1: Download Snapshot")


def validate_snapshot(snapshot_dir=".tmp/snapshot"):
    """Validate snapshot."""
    cmd = [
        sys.executable,
        "execution/validate_model_snapshot.py",
        "--snapshot",
        snapshot_dir,
    ]
    return run_command(cmd, "STEP 3: Validate Changes")


def preview_changes(sheet_id, snapshot_dir=".tmp/snapshot"):
    """Preview changes (dry run)."""
    cmd = [
        sys.executable,
        "execution/sync_snapshot_to_sheets.py",
        "--snapshot",
        snapshot_dir,
        "--sheet-id",
        sheet_id,
        "--dry-run",
    ]
    return run_command(cmd, "STEP 4: Preview Changes (Dry Run)")


def apply_changes(sheet_id, snapshot_dir=".tmp/snapshot"):
    """Apply changes to Google Sheets."""
    cmd = [
        sys.executable,
        "execution/sync_snapshot_to_sheets.py",
        "--snapshot",
        snapshot_dir,
        "--sheet-id",
        sheet_id,
        "--apply",
    ]
    return run_command(cmd, "STEP 5: Apply Changes")


def backup_snapshot(sheet_id):
    """Create timestamped backup."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f".tmp/snapshot_backup_{timestamp}"

    cmd = [
        sys.executable,
        "execution/download_model_snapshot.py",
        "--sheet-id",
        sheet_id,
        "--output",
        backup_dir,
    ]

    if run_command(cmd, "Creating Backup"):
        print(f"\n📦 Backup saved to: {backup_dir}")
        return True
    return False


def prepare_for_editing(sheet_id):
    """Download snapshot and prepare for editing."""
    print("\n" + "=" * 80)
    print("PREPARING FOR EDITING")
    print("=" * 80)

    # Download
    if not download_snapshot(sheet_id):
        return False

    # Show instructions
    print("\n" + "=" * 80)
    print("READY TO EDIT")
    print("=" * 80)
    print("\n📝 Next Steps:")
    print("   1. Open .tmp/snapshot/sheets/ folder")
    print("   2. Edit CSV files:")
    print("      - *_formulas.csv = Edit formulas")
    print("      - *.csv = View calculated values")
    print("   3. When done, run:")
    print(f'      python edit_financial_model.py --sheet-id "{sheet_id}" --validate')
    print(f'      python edit_financial_model.py --sheet-id "{sheet_id}" --preview')
    print(f'      python edit_financial_model.py --sheet-id "{sheet_id}" --apply')

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Local-First Financial Model Editing Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard workflow
  python edit_financial_model.py --sheet-id "1-Ss62..." --download
  # ... edit CSV files in .tmp/snapshot/sheets/ ...
  python edit_financial_model.py --sheet-id "1-Ss62..." --validate
  python edit_financial_model.py --sheet-id "1-Ss62..." --preview
  python edit_financial_model.py --sheet-id "1-Ss62..." --apply
  
  # Quick prepare
  python edit_financial_model.py --sheet-id "1-Ss62..." --prepare
  
  # Backup first
  python edit_financial_model.py --sheet-id "1-Ss62..." --backup
        """,
    )

    parser.add_argument("--sheet-id", required=True, help="Google Sheets ID")
    parser.add_argument(
        "--snapshot",
        default=".tmp/snapshot",
        help="Snapshot directory (default: .tmp/snapshot)",
    )

    # Actions
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--download", action="store_true", help="Download snapshot (Step 1)"
    )
    action_group.add_argument(
        "--validate", action="store_true", help="Validate snapshot (Step 3)"
    )
    action_group.add_argument(
        "--preview", action="store_true", help="Preview changes (Step 4)"
    )
    action_group.add_argument(
        "--apply", action="store_true", help="Apply changes (Step 5)"
    )
    action_group.add_argument(
        "--prepare", action="store_true", help="Download + show editing instructions"
    )
    action_group.add_argument(
        "--backup", action="store_true", help="Create timestamped backup"
    )

    args = parser.parse_args()

    # Execute action
    success = False

    if args.download:
        success = download_snapshot(args.sheet_id, args.snapshot)

    elif args.validate:
        success = validate_snapshot(args.snapshot)

    elif args.preview:
        success = preview_changes(args.sheet_id, args.snapshot)

    elif args.apply:
        # Confirm before applying
        print("\n⚠️  WARNING: This will overwrite data in Google Sheets!")
        response = input("Are you sure you want to apply changes? (yes/no): ")
        if response.lower() == "yes":
            success = apply_changes(args.sheet_id, args.snapshot)
        else:
            print("❌ Cancelled")
            return 1

    elif args.prepare:
        success = prepare_for_editing(args.sheet_id)

    elif args.backup:
        success = backup_snapshot(args.sheet_id)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
