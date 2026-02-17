#!/usr/bin/env python3
"""
Setup Project Structure - Ensure proper .tmp folder organization

Creates standardized folder structure for business plan projects:
- consolidated_research/ - Growing research database (6 categories)
- research_archive/ - Raw research files preservation
- <project_name>/ - Project-specific folder
  ├── business_plan/ - Business plan documents
  ├── pitch_deck/ - Pitch deck content
  ├── config/ - Financial model configs
  └── notes/ - Work notes and updates
- templates/ - Reusable templates
- scripts_archive/ - One-time analysis scripts

Usage:
  python execution/setup_project_structure.py --project my_startup
  python execution/setup_project_structure.py --project ai_tutoring --init-only
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


class ProjectStructureManager:
    """Manages .tmp folder organization for business plan projects"""

    def __init__(self, base_dir=".tmp"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def ensure_core_folders(self):
        """Create core shared folders if they don't exist"""

        core_folders = {
            "consolidated_research": "Categorized research database (6 categories)",
            "research_archive": "Raw SERP API research files",
            "templates": "Reusable templates for new projects",
            "scripts_archive": "One-time analysis scripts",
        }

        created = []
        for folder, description in core_folders.items():
            folder_path = self.base_dir / folder
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                created.append(folder)

                # Create .gitkeep to preserve empty folders
                gitkeep = folder_path / ".gitkeep"
                gitkeep.write_text(f"# {description}\n")

        # Ensure research database files exist
        research_dir = self.base_dir / "consolidated_research"
        self._ensure_research_files(research_dir)

        return created

    def _ensure_research_files(self, research_dir):
        """Ensure research category files exist"""

        categories = {
            "market_research.json": {
                "category": "Market Research",
                "description": "TAM/SAM/SOM, market size, industry trends",
                "sources": [],
            },
            "headcount_research.json": {
                "category": "Headcount & Hiring",
                "description": "Team composition, salaries, roles, hiring benchmarks",
                "sources": [],
            },
            "geographic_research.json": {
                "category": "Geographic & Location",
                "description": "Regional data, market entry, expansion strategies",
                "sources": [],
            },
            "business_model_research.json": {
                "category": "Business Model",
                "description": "Revenue models, pricing, unit economics",
                "sources": [],
            },
            "competitors_research.json": {
                "category": "Competitors",
                "description": "Competitive landscape, positioning",
                "sources": [],
            },
            "benchmarks_research.json": {
                "category": "Financial Benchmarks",
                "description": "CAC, LTV, margins, financial ratios",
                "sources": [],
            },
        }

        for filename, template in categories.items():
            filepath = research_dir / filename
            if not filepath.exists():
                with open(filepath, "w") as f:
                    json.dump(template, f, indent=2)

        # Create metadata file
        metadata_file = research_dir / "_metadata.json"
        if not metadata_file.exists():
            metadata = {
                "created_at": datetime.now().isoformat(),
                "total_sources": 0,
                "categories": list(categories.keys()),
            }
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

    def create_project(self, project_name):
        """Create project-specific folder structure"""

        project_dir = self.base_dir / project_name

        if project_dir.exists():
            print(f"⚠️  Project '{project_name}' already exists")
            return False

        # Create project subfolder structure
        subfolders = {
            "business_plan": "Business plan documents and analysis",
            "pitch_deck": "Pitch deck content and versions",
            "config": "Financial model configuration and data",
            "notes": "Work notes, fix logs, and updates",
        }

        for folder, description in subfolders.items():
            folder_path = project_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)

            # Create README in each subfolder
            readme = folder_path / "README.md"
            readme.write_text(
                f'# {folder.replace("_", " ").title()}\n\n{description}\n'
            )

        # Create project README
        project_readme = project_dir / "README.md"
        readme_content = f"""# {project_name.replace("_", " ").title()} - Business Plan Project

Created: {datetime.now().strftime("%Y-%m-%d")}

## Folder Structure

- **business_plan/** - Business plan documents and market analysis
- **pitch_deck/** - Pitch deck content and presentations
- **config/** - Financial model configuration files
- **notes/** - Work notes, updates, and fix logs

## Workflow

1. Conduct research -> Add to `.tmp/consolidated_research/`
2. Create config -> Save in `config/`
3. Generate business plan -> Output to `business_plan/`
4. Create pitch deck -> Output to `pitch_deck/`
5. Notes and updates -> Save in `notes/`

## Google Sheets Links

- Financial Model: [Add link here]
- Sources & References: [Add link here]

## Google Docs Links

- Business Plan: [Add link here]
- Pitch Deck: [Add link here]
"""
        with open(project_readme, "w", encoding="utf-8") as f:
            f.write(readme_content)

        return True

    def get_structure_summary(self):
        """Get current .tmp folder structure summary"""

        summary = {"core_folders": {}, "projects": {}, "total_files": 0}

        # Count files in core folders
        for folder in [
            "consolidated_research",
            "research_archive",
            "templates",
            "scripts_archive",
        ]:
            folder_path = self.base_dir / folder
            if folder_path.exists():
                file_count = len(list(folder_path.rglob("*"))) - len(
                    list(folder_path.rglob("*/"))
                )
                summary["core_folders"][folder] = file_count
                summary["total_files"] += file_count

        # Find project folders (exclude core folders)
        core_folders = {
            "consolidated_research",
            "research_archive",
            "templates",
            "scripts_archive",
            "snapshot",
            "snapshot_test",
            "_archive",
        }

        for item in self.base_dir.iterdir():
            if (
                item.is_dir()
                and item.name not in core_folders
                and not item.name.startswith(".")
            ):
                # Check if it's a project folder (has business_plan, pitch_deck, etc.)
                if (item / "business_plan").exists() or (item / "config").exists():
                    file_count = len(list(item.rglob("*"))) - len(
                        list(item.rglob("*/"))
                    )
                    summary["projects"][item.name] = file_count
                    summary["total_files"] += file_count

        return summary


def main():
    parser = argparse.ArgumentParser(
        description="Setup and manage .tmp folder structure for business plan projects"
    )
    parser.add_argument(
        "--project", help="Project name to create (e.g., my_startup, ai_tutoring)"
    )
    parser.add_argument(
        "--init-only",
        action="store_true",
        help="Only initialize core folders, don't create project",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Display current folder structure summary",
    )
    parser.add_argument(
        "--base-dir", default=".tmp", help="Base directory (default: .tmp)"
    )

    args = parser.parse_args()

    manager = ProjectStructureManager(args.base_dir)

    # Always ensure core folders exist
    created_core = manager.ensure_core_folders()

    if created_core:
        print(f"\n✓ Initialized core folders:")
        for folder in created_core:
            print(f"  • {folder}/")

    # Create project if requested
    if args.project and not args.init_only:
        print(f"\n📁 Creating project structure for '{args.project}'...")

        if manager.create_project(args.project):
            print(f"\n✓ Project '{args.project}' created successfully!")
            print(f"\nFolder structure:")
            print(f"  .tmp/{args.project}/")
            print(f"    ├── business_plan/")
            print(f"    ├── pitch_deck/")
            print(f"    ├── config/")
            print(f"    ├── notes/")
            print(f"    └── README.md")
            print(f"\nNext steps:")
            print(f"  1. Conduct research for {args.project}")
            print(
                f"  2. Create config: .tmp/{args.project}/config/{args.project}_config.json"
            )
            print(f"  3. Generate business plan")
        else:
            print(f"  Project already exists. Use existing structure.")

    # Display summary if requested
    if args.summary or (not args.project and not args.init_only):
        summary = manager.get_structure_summary()

        print(f"\n📊 .tmp Folder Structure Summary")
        print(f"─────────────────────────────────")

        print(f"\nCore Folders:")
        for folder, count in summary["core_folders"].items():
            print(f"  {folder:30} {count:3} files")

        if summary["projects"]:
            print(f"\nProjects:")
            for project, count in summary["projects"].items():
                print(f"  {project:30} {count:3} files")

        print(f"\nTotal files: {summary['total_files']}")

    print()


if __name__ == "__main__":
    main()
