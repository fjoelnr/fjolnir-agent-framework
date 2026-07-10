from __future__ import annotations

from typing import Any


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- None"


def compile_openai_responses_request(ir: dict[str, Any], model: str) -> dict[str, Any]:
    """Render a pure OpenAI Responses request without provider tool bindings."""
    if not model.strip():
        raise ValueError("An explicit OpenAI model identifier is required.")
    policy_decisions = [
        f"{item['source']['id']}::{item['ruleId']} matched={str(item['matched']).lower()}: {item['message']}"
        for item in ir["behavior"].get("policyDecisions", [])
    ]
    gates = [
        f"{item['source']['id']}@{item['source']['version']} ({item['phase']}; failure: {item['failureAction']})"
        for item in ir["qualityGates"]
    ]
    tools = [f"{item['id']}@{item['version']}" for item in ir["authority"]["tools"]]
    instructions = "\n".join([
        "# FAF Resolved Agent Instructions",
        f"Build ID: {ir['buildId']}",
        "",
        "## Instructions", _bullets(ir["behavior"]["instructions"]),
        "",
        "## Policies", _bullets(ir["behavior"]["policies"]),
        "",
        "## Policy decisions", _bullets(policy_decisions),
        "",
        "## Constraints", _bullets(ir["task"]["constraints"]),
        "",
        "## Prohibited actions", _bullets(ir["authority"]["prohibitedActions"]),
        "",
        "## Required human review", _bullets(ir["authority"]["reviewRequirements"]),
        "",
        "## Quality gates", _bullets(gates),
        "",
        "## Authorized FAF tool references (informational only)", _bullets(tools),
    ])
    input_text = "\n".join([
        "# Task", "",
        f"Objective: {ir['task']['objective']}",
        "", "## Inputs", _bullets(ir["task"]["inputs"]),
        "", "## Acceptance criteria", _bullets(ir["task"]["acceptanceCriteria"]),
        "", "## Required output", ir["task"]["requiredOutput"],
        "", "## Escalation conditions", _bullets(ir["task"]["escalationConditions"]),
    ])
    return {"model": model, "instructions": instructions, "input": input_text}
