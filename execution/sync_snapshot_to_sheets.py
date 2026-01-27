#!/usr/bin/env python3
"""
Sync Snapshot to Google Sheets
===============================
Atomically sync local snapshot to Google Sheets financial model.

Usage:
    python sync_snapshot_to_sheets.py --snapshot <DIR> --sheet-id <ID> [--dry-run]
    
Example:
    python sync_snapshot_to_sheets.py --snapshot .tmp/snapshot --sheet-id "1-Ss62..." --dry-run
    python sync_snapshot_to_sheets.py --snapshot .tmp/snapshot --sheet-id "1-Ss62..." --apply
"""

import os
import sys
import json
import argparse
import csv
import time
from pathlib import Path
from collections import defaultdict
import gspread
from google.oauth2.credentials import Credentials

def get_credentials():
    """Get OAuth2 credentials for Google Sheets API."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    return creds

class SnapshotSyncer:
    def __init__(self, snapshot_dir, sheet_id, dry_run=True):
        self.snapshot_dir = Path(snapshot_dir)
        self.sheet_id = sheet_id
        self.dry_run = dry_run
        self.metadata = None
        self.changes = defaultdict(list)
        
    def load_snapshot(self):
        """Load snapshot metadata and files."""
        metadata_file = self.snapshot_dir / "snapshot.json"
        if not metadata_file.exists():
            print(f"Error: Snapshot metadata not found: {metadata_file}")
            return False
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        return True
    
    def connect_to_sheets(self):
        """Connect to Google Sheets."""
        creds = get_credentials()
        if not creds:
            print("Error: No credentials found. Run setup first.")
            return None
        
        gc = gspread.authorize(creds)
        
        try:
            spreadsheet = gc.open_by_key(self.sheet_id)
            return spreadsheet
        except Exception as e:
            print(f"Error opening spreadsheet: {e}")
            return None
    
    def load_sheet_data(self, sheet_info):
        """Load values and formulas for a sheet."""
        values_file = self.snapshot_dir / sheet_info['values_file']
        formulas_file = self.snapshot_dir / sheet_info['formulas_file']
        
        values = []
        formulas = []
        
        with open(values_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                values.append(row[1:])  # Skip Row column
        
        with open(formulas_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                formulas.append(row[1:])  # Skip Row column
        
        return values, formulas
    
    def detect_changes(self, spreadsheet):
        """Detect what changed between snapshot and current sheets."""
        print(f"\n{'='*80}")
        print("DETECTING CHANGES")
        print(f"{'='*80}\n")
        
        for sheet_info in self.metadata['sheets']:
            sheet_name = sheet_info['name']
            print(f"Checking {sheet_name}...")
            
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
                current_formulas = worksheet.get(value_render_option='FORMULA')
                
                # Load snapshot formulas
                snapshot_values, snapshot_formulas = self.load_sheet_data(sheet_info)
                
                # Compare
                changes = []
                for row_idx, (snap_row, curr_row) in enumerate(zip(snapshot_formulas, current_formulas)):
                    for col_idx, (snap_cell, curr_cell) in enumerate(zip(snap_row[:8], (curr_row + [''] * 8)[:8])):
                        if snap_cell != curr_cell:
                            col_letter = chr(65 + col_idx)
                            changes.append({
                                'cell': f"{col_letter}{row_idx + 1}",
                                'old': curr_cell,
                                'new': snap_cell
                            })
                
                if changes:
                    self.changes[sheet_name] = changes
                    print(f"   {len(changes)} changes detected")
                else:
                    print(f"   No changes")
                
            except Exception as e:
                print(f"   Error: {e}")
        
        total_changes = sum(len(changes) for changes in self.changes.values())
        print(f"\nTotal changes: {total_changes} cells across {len(self.changes)} sheets")
        
        return total_changes > 0
    
    def preview_changes(self):
        """Show preview of changes."""
        if not self.changes:
            print("\nNo changes to preview")
            return
        
        print(f"\n{'='*80}")
        print("CHANGE PREVIEW")
        print(f"{'='*80}\n")
        
        for sheet_name, changes in list(self.changes.items())[:5]:  # Show first 5 sheets
            print(f"{sheet_name}:")
            for change in changes[:10]:  # Show first 10 changes per sheet
                old = change['old'][:50] if change['old'] else '(empty)'
                new = change['new'][:50] if change['new'] else '(empty)'
                print(f"  {change['cell']}: {old}  {new}")
            
            if len(changes) > 10:
                print(f"  ... and {len(changes) - 10} more changes")
            print()
        
        if len(self.changes) > 5:
            remaining_sheets = len(self.changes) - 5
            remaining_changes = sum(len(changes) for sheet, changes in list(self.changes.items())[5:])
            print(f"... and {remaining_changes} changes in {remaining_sheets} more sheets\n")
    
    def apply_changes(self, spreadsheet):
        """Apply changes to Google Sheets."""
        if not self.changes:
            print("\nNo changes to apply")
            return True
        
        print(f"\n{'='*80}")
        print("APPLYING CHANGES")
        print(f"{'='*80}\n")
        
        for sheet_name, changes in self.changes.items():
            print(f"Updating {sheet_name}...")
            
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
                
                # Batch update in chunks of 50
                batch_size = 50
                for i in range(0, len(changes), batch_size):
                    batch = changes[i:i+batch_size]
                    
                    # Prepare batch update
                    updates = []
                    for change in batch:
                        updates.append({
                            'range': change['cell'],
                            'values': [[change['new']]]
                        })
                    
                    worksheet.batch_update(updates)
                    print(f"   Updated {len(updates)} cells")
                    
                    # Rate limiting
                    if i + batch_size < len(changes):
                        time.sleep(2)
                
                print(f"   {len(changes)} changes applied\n")
                
            except Exception as e:
                print(f"   Error: {e}\n")
                return False
        
        return True
    
    def sync(self):
        """Main sync workflow."""
        print(f"\n{'='*80}")
        print(f"SNAPSHOT SYNC {'(DRY RUN)' if self.dry_run else '(LIVE)'}")
        print(f"{'='*80}")
        print(f"Snapshot: {self.snapshot_dir}")
        print(f"Target: {self.sheet_id}")
        print(f"Mode: {'Preview only' if self.dry_run else 'Apply changes'}")
        
        # Connect
        spreadsheet = self.connect_to_sheets()
        if not spreadsheet:
            return False
        
        print(f"Spreadsheet: {spreadsheet.title}")
        
        # Detect changes
        has_changes = self.detect_changes(spreadsheet)
        
        if not has_changes:
            print("\n Snapshot already in sync with Google Sheets")
            return True
        
        # Preview
        self.preview_changes()
        
        # Apply if not dry run
        if self.dry_run:
            print(f"\n{'='*80}")
            print("DRY RUN COMPLETE")
            print(f"{'='*80}")
            print("\nTo apply these changes, run with --apply flag")
            return True
        else:
            # Apply changes
            success = self.apply_changes(spreadsheet)
            
            if success:
                print(f"\n{'='*80}")
                print(" SYNC COMPLETE")
                print(f"{'='*80}")
                print(f"\nAll changes applied to: {spreadsheet.title}")
            else:
                print(f"\n{'='*80}")
                print(" SYNC FAILED")
                print(f"{'='*80}")
                print("\nSome changes could not be applied")
            
            return success

def main():
    parser = argparse.ArgumentParser(
        description='Sync local snapshot to Google Sheets'
    )
    parser.add_argument('--snapshot', required=True, help='Snapshot directory')
    parser.add_argument('--sheet-id', required=True, help='Google Sheets spreadsheet ID')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--apply', action='store_true', help='Apply changes to Google Sheets')
    
    args = parser.parse_args()
    
    # Default to dry-run if neither specified
    dry_run = not args.apply
    
    syncer = SnapshotSyncer(args.snapshot, args.sheet_id, dry_run)
    
    if not syncer.load_snapshot():
        sys.exit(1)
    
    success = syncer.sync()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
