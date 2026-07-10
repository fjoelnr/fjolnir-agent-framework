from __future__ import annotations

from typing import Any


def _section(title: str, values: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(f"- {value}" for value in values)
    if not values:
        lines.append("- None")
    lines.append("")
    return lines


def compile_generic_text(ir: dict[str, Any]) -> str:
    """Render deterministic, runtime-neutral text without adding authority."""
    lines = [
        "# Fjölnir Resolved Agent Task", "",
        f"Build: `{ir['buildId']}`", "",
        "## Objective", "", ir["task"]["objective"], "",
        "## Required output", "", ir["task"]["requiredOutput"], "",
    ]
    lines += _section("Instructions", ir["behavior"]["instructions"])
    lines += _section("Policies", ir["behavior"]["policies"])
    matched_policy_decisions = [
        decision["message"]
        for decision in ir["behavior"].get("policyDecisions", [])
        if decision["matched"]
    ]
    lines += _section("Matched policy decisions", matched_policy_decisions)
    lines += _section("Reasoning procedure", ir["behavior"]["reasoning"])
    lines += _section("Constraints", ir["task"]["constraints"])
    lines += _section("Prohibited actions", ir["authority"]["prohibitedActions"])
    lines += _section("Acceptance criteria", ir["task"]["acceptanceCriteria"])
    lines += _section("Escalation conditions", ir["task"]["escalationConditions"])
    lines += ["## Granted tools", ""]
    lines += [f"- `{item['id']}@{item['version']}`" for item in ir["authority"]["tools"]] or ["- None"]
    lines += ["", "## Quality gates", ""]
    for gate in ir["qualityGates"]:
        lines.append(f"- `{gate['source']['id']}@{gate['source']['version']}` ({gate['phase']}, failure: {gate['failureAction']})")
    if not ir["qualityGates"]:
        lines.append("- None")
    return "\n".join(lines).rstrip() + "\n"
