#!/usr/bin/env python3
"""
Stage-Gated Workflow Orchestrator

Runs business-model and financial-model workflow in strict stages:
0. Scope Lock / Project Init
1. TAM-SAM-SOM Research Foundation
2. Revenue Driver Configuration
3. Cost Driver Validation
4. Financial Model Creation + Audits
5. Final Validation + Sign-off Artifacts

This script orchestrates existing deterministic scripts in execution/ and
stores stage status in .tmp/<project>/notes/stage_state.json.

Usage examples:
  python execution/run_stepwise_workflow.py --project myproject --stage status
    python execution/run_stepwise_workflow.py --project myproject --stage 0 \
        --company "My Company" --execute
    python execution/run_stepwise_workflow.py --project myproject --stage 1 \
        --research-dir .tmp/myproject/research --execute
    python execution/run_stepwise_workflow.py --project myproject --stage 2 \
        --sections-dir .tmp/myproject/business_plan/sections --execute
    python execution/run_stepwise_workflow.py --project myproject --stage 4 \
        --company "My Company" \
        --config .tmp/myproject/config/myproject_config.json --execute
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

STAGES = ["0", "1", "2", "3", "4", "5"]

LOCAL_SHEET_SEQUENCE = [
    "Sources & References",
    "Assumptions",
    "Headcount Plan",
    "Revenue",
    "Operating Costs",
    "P&L",
    "Cash Flow",
    "Balance Sheet",
    "Summary",
    "Sensitivity Analysis",
    "Valuation",
    "Break-even Analysis",
    "Funding Cap Table",
    "Charts Data",
]


@dataclass
class CommandStep:
    name: str
    cmd: List[str]


def run_command(step: CommandStep, execute: bool) -> int:
    command_str = " ".join(step.cmd)
    print(f"\n[{step.name}] {command_str}")
    if not execute:
        print("  ↳ Dry-run (not executed)")
        return 0

    result = subprocess.run(step.cmd, check=False)
    return result.returncode


def project_paths(project: str) -> Dict[str, Path]:
    base = Path(".tmp") / project
    return {
        "base": base,
        "business_plan": base / "business_plan",
        "sections": base / "business_plan" / "sections",
        "config": base / "config",
        "notes": base / "notes",
        "financial_model": base / "financial_model",
        "research": base / "research",
        "state": base / "notes" / "stage_state.json",
        "gate_state": base / "notes" / "local_sheet_gates.json",
    }


def load_gate_state(gate_file: Path) -> Dict:
    if gate_file.exists():
        with open(gate_file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return {
        "required_sheets": LOCAL_SHEET_SEQUENCE,
        "approved_sheets": {},
        "last_updated": datetime.now().isoformat(),
    }


def save_gate_state(gate_file: Path, state: Dict) -> None:
    gate_file.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().isoformat()
    with open(gate_file, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


def load_state(state_file: Path) -> Dict:
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as handle:
            return json.load(handle)

    return {
        "created_at": datetime.now().isoformat(),
        "completed_stages": [],
        "stage_history": [],
        "artifacts": {},
        "last_updated": datetime.now().isoformat(),
    }


def save_state(state_file: Path, state: Dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().isoformat()
    with open(state_file, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


def require_previous_stage(stage: str, state: Dict) -> Optional[str]:
    if stage == "0":
        return None

    prev_stage = str(int(stage) - 1)
    if prev_stage not in state.get("completed_stages", []):
        return (
            f"Stage {stage} is blocked. Complete Stage {prev_stage} first. "
            f"Completed: {state.get('completed_stages', [])}"
        )
    return None


def mark_stage_complete(state: Dict, stage: str, artifacts: Dict) -> None:
    if stage not in state["completed_stages"]:
        state["completed_stages"].append(stage)

    state["stage_history"].append(
        {
            "stage": stage,
            "completed_at": datetime.now().isoformat(),
            "artifacts": artifacts,
        }
    )
    state["artifacts"].update(artifacts)


def stage_0_init(
    args: argparse.Namespace, paths: Dict[str, Path], execute: bool
) -> Dict:
    commands = [
        CommandStep(
            "Initialize project structure",
            [
                sys.executable,
                "execution/setup_project_structure.py",
                "--project",
                args.project,
            ],
        )
    ]

    if args.config and Path(args.config).exists():
        commands.append(
            CommandStep(
                "Validate config",
                [
                    sys.executable,
                    "execution/validate_config.py",
                    "--config",
                    args.config,
                ],
            )
        )

    for step in commands:
        code = run_command(step, execute)
        if code != 0:
            raise RuntimeError(f"Step failed: {step.name}")

    if execute:
        paths["sections"].mkdir(parents=True, exist_ok=True)

    return {
        "project": args.project,
        "company": args.company,
        "config": args.config,
        "sections_dir": str(paths["sections"]),
    }


def stage_1_research(args: argparse.Namespace, execute: bool) -> Dict:
    if not args.research_dir:
        raise RuntimeError("Stage 1 requires --research-dir")

    output_dir = args.output_research_dir or ".tmp/consolidated_research"
    commands = [
        CommandStep(
            "Consolidate research",
            [
                sys.executable,
                "execution/consolidate_market_research.py",
                "--research-dir",
                args.research_dir,
                "--output-dir",
                output_dir,
            ],
        )
    ]

    for step in commands:
        code = run_command(step, execute)
        if code != 0:
            raise RuntimeError(f"Step failed: {step.name}")

    return {
        "research_dir": args.research_dir,
        "consolidated_research_dir": output_dir,
    }


def stage_2_revenue_config(
    args: argparse.Namespace, paths: Dict[str, Path], execute: bool
) -> Dict:
    if not args.sections_dir:
        raise RuntimeError("Stage 2 requires --sections-dir")

    output_config = args.config or str(paths["config"] / f"{args.project}_config.json")

    commands = [
        CommandStep(
            "Extract config from business plan sections",
            [
                sys.executable,
                "execution/extract_config_from_plan.py",
                "--sections-dir",
                args.sections_dir,
                "--output",
                output_config,
            ],
        ),
        CommandStep(
            "Validate extracted config",
            [
                sys.executable,
                "execution/validate_config.py",
                "--config",
                output_config,
            ],
        ),
    ]

    for step in commands:
        code = run_command(step, execute)
        if code != 0:
            raise RuntimeError(f"Step failed: {step.name}")

    return {
        "sections_dir": args.sections_dir,
        "config": output_config,
    }


def stage_3_cost_validation(args: argparse.Namespace, execute: bool) -> Dict:
    if not args.config:
        raise RuntimeError("Stage 3 requires --config")

    commands = [
        CommandStep(
            "Re-validate config (cost assumptions gate)",
            [
                sys.executable,
                "execution/validate_config.py",
                "--config",
                args.config,
            ],
        )
    ]

    for step in commands:
        code = run_command(step, execute)
        if code != 0:
            raise RuntimeError(f"Step failed: {step.name}")

    return {"config": args.config}


def stage_4_build_model(
    args: argparse.Namespace, paths: Dict[str, Path], execute: bool
) -> Dict:
    if not args.company:
        raise RuntimeError("Stage 4 requires --company")
    if not args.config:
        raise RuntimeError("Stage 4 requires --config")

    if args.local_first:
        local_model_path = args.local_model_path or str(
            paths["financial_model"] / f"{args.project}_financial_model.xlsx"
        )
        local_model = Path(local_model_path)
        if execute:
            local_model.parent.mkdir(parents=True, exist_ok=True)

        commands = [
            CommandStep(
                "Build local 14-sheet model",
                [
                    sys.executable,
                    "execution/build_financial_model.py",
                    "--config",
                    args.config,
                    "--output",
                    str(local_model),
                    "--validate",
                ],
            )
        ]

        for step in commands:
            code = run_command(step, execute)
            if code != 0:
                raise RuntimeError(f"Step failed: {step.name}")

        return {
            "config": args.config,
            "model_mode": "local_first",
            "local_model_path": str(local_model),
        }

    result_file = paths["notes"] / "stage4_create_result.json"
    commands = [
        CommandStep(
            "Create model from template",
            [
                sys.executable,
                "execution/create_financial_model.py",
                "--company",
                args.company,
                "--config",
                args.config,
                "--from-template",
                "--output",
                str(result_file),
            ],
        )
    ]

    for step in commands:
        code = run_command(step, execute)
        if code != 0:
            raise RuntimeError(f"Step failed: {step.name}")

    artifacts: Dict[str, str] = {
        "config": args.config,
        "create_result_file": str(result_file),
    }

    if execute and result_file.exists():
        with open(result_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("sheet_id"):
            artifacts["sheet_id"] = data["sheet_id"]
        if data.get("url"):
            artifacts["sheet_url"] = data["url"]

    return artifacts


def stage_5_signoff(
    args: argparse.Namespace,
    paths: Dict[str, Path],
    state: Dict,
    execute: bool,
) -> Dict:
    commands: List[CommandStep] = []

    if args.local_first:
        local_model_path = args.local_model_path or state.get("artifacts", {}).get(
            "local_model_path"
        )
        if not local_model_path:
            raise RuntimeError(
                "Stage 5 local-first requires --local-model-path or Stage 4 local model artifact"
            )

        commands.append(
            CommandStep(
                "Validate local Excel model",
                [
                    sys.executable,
                    "execution/validate_excel_model.py",
                    "--file",
                    local_model_path,
                    "--check-balance",
                ],
            )
        )

        for step in commands:
            code = run_command(step, execute)
            if code != 0:
                raise RuntimeError(f"Step failed: {step.name}")

        gate_state = load_gate_state(paths["gate_state"])
        gate_state["required_sheets"] = LOCAL_SHEET_SEQUENCE

        for sheet_name in args.approve_sheet or []:
            if sheet_name not in LOCAL_SHEET_SEQUENCE:
                raise RuntimeError(
                    f"Unknown sheet for approval: '{sheet_name}'. Use exact sheet names."
                )
            gate_state["approved_sheets"][sheet_name] = {
                "approved_at": datetime.now().isoformat()
            }

        if execute:
            save_gate_state(paths["gate_state"], gate_state)

        approved_names = set(gate_state.get("approved_sheets", {}).keys())
        pending = [name for name in LOCAL_SHEET_SEQUENCE if name not in approved_names]
        if pending:
            raise RuntimeError(
                "Local sheet gates pending. Approve one or more with "
                '--approve-sheet "<Sheet Name>". Pending: ' + ", ".join(pending)
            )

        if args.sync_to_cloud:
            sync_step = CommandStep(
                "Sync approved local model to Google Drive",
                [
                    sys.executable,
                    "execution/sync_to_cloud.py",
                    "--file",
                    local_model_path,
                ],
            )
            code = run_command(sync_step, execute)
            if code != 0:
                raise RuntimeError(f"Step failed: {sync_step.name}")

        return {
            "model_mode": "local_first",
            "local_model_path": local_model_path,
            "local_sheet_gates": "approved",
            "signoff_ready": True,
        }

    sheet_id = args.sheet_id or state.get("artifacts", {}).get("sheet_id")
    if sheet_id:
        commands.extend(
            [
                CommandStep(
                    "Export model summary",
                    [
                        sys.executable,
                        "execution/export_model_summary.py",
                        "--sheet-id",
                        sheet_id,
                        "--format",
                        "markdown",
                    ],
                ),
                CommandStep(
                    "Final comprehensive model audit",
                    [
                        sys.executable,
                        "execution/audit_financial_model.py",
                        "--sheet-id",
                        sheet_id,
                        "--mode",
                        "comprehensive",
                    ],
                ),
                CommandStep(
                    "Final sheet integrity check",
                    [
                        sys.executable,
                        "execution/verify_sheet_integrity.py",
                        "--sheet-id",
                        sheet_id,
                        "--sheet",
                        "Balance Sheet",
                    ],
                ),
            ]
        )

    if args.sections_dir:
        commands.append(
            CommandStep(
                "Audit business plan sections",
                [
                    sys.executable,
                    "execution/audit_business_plan.py",
                    "--sections-dir",
                    args.sections_dir,
                ],
            )
        )

    for step in commands:
        code = run_command(step, execute)
        if code != 0:
            raise RuntimeError(f"Step failed: {step.name}")

    return {
        "sheet_id": sheet_id,
        "sections_dir": args.sections_dir,
        "signoff_ready": True,
    }


def print_status(state: Dict) -> None:
    completed = state.get("completed_stages", [])
    print("\nStage Status")
    print("------------")
    for stage in STAGES:
        marker = "✅" if stage in completed else "⬜"
        print(f"{marker} Stage {stage}")

    if state.get("artifacts"):
        print("\nArtifacts")
        print("---------")
        for key, value in state["artifacts"].items():
            print(f"- {key}: {value}")

    gate_file = None
    model_path = state.get("artifacts", {}).get("local_model_path")
    if model_path:
        gate_file = Path(model_path).parent.parent / "notes" / "local_sheet_gates.json"
    if gate_file and gate_file.exists():
        gate_state = load_gate_state(gate_file)
        required = gate_state.get("required_sheets", LOCAL_SHEET_SEQUENCE)
        approved = set(gate_state.get("approved_sheets", {}).keys())
        pending = [name for name in required if name not in approved]
        print("\nLocal Sheet Gates")
        print("-----------------")
        print(f"- approved: {len(approved)}/{len(required)}")
        if pending:
            print(f"- pending: {', '.join(pending)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run stage-gated business/financial model workflow"
    )
    parser.add_argument("--project", required=True, help="Project name under .tmp/")
    parser.add_argument("--stage", required=True, help="0|1|2|3|4|5|status")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute commands (default is dry-run)",
    )

    parser.add_argument("--company", help="Company name (required for stage 4)")
    parser.add_argument("--config", help="Config JSON path")
    parser.add_argument(
        "--research-dir",
        help="Research input directory for consolidation",
    )
    parser.add_argument(
        "--output-research-dir",
        help="Consolidated research output directory",
    )
    parser.add_argument("--sections-dir", help="Business plan sections directory")
    parser.add_argument("--sheet-id", help="Existing Google Sheet ID (used in stage 5)")
    parser.add_argument(
        "--local-first",
        action="store_true",
        help="Use local Excel-first model creation and validation flow",
    )
    parser.add_argument(
        "--local-model-path",
        help="Path to local Excel model (.xlsx) for local-first stages",
    )
    parser.add_argument(
        "--approve-sheet",
        action="append",
        help="Approve a local sheet gate (repeat per sheet) during Stage 5",
    )
    parser.add_argument(
        "--sync-to-cloud",
        action="store_true",
        help="In local-first Stage 5, sync approved local model to Google Drive",
    )

    args = parser.parse_args()

    paths = project_paths(args.project)
    state = load_state(paths["state"])

    if args.stage == "status":
        print_status(state)
        return 0

    if args.stage not in STAGES:
        print(f"Invalid stage: {args.stage}")
        return 1

    blocked = require_previous_stage(args.stage, state)
    if blocked:
        print(blocked)
        return 1

    try:
        if args.stage == "0":
            artifacts = stage_0_init(args, paths, args.execute)
        elif args.stage == "1":
            artifacts = stage_1_research(args, args.execute)
        elif args.stage == "2":
            artifacts = stage_2_revenue_config(args, paths, args.execute)
        elif args.stage == "3":
            artifacts = stage_3_cost_validation(args, args.execute)
        elif args.stage == "4":
            artifacts = stage_4_build_model(args, paths, args.execute)
        else:
            artifacts = stage_5_signoff(args, paths, state, args.execute)

        if args.execute:
            mark_stage_complete(state, args.stage, artifacts)
            save_state(paths["state"], state)
            print(f"\n✅ Stage {args.stage} completed and recorded")
        else:
            print(f"\nℹ️ Dry-run complete for Stage {args.stage}")

        return 0
    except RuntimeError as error:
        print(f"\n❌ {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
