from __future__ import annotations

from typing import Any

from .catalog import ref_identity
from .errors import Finding, ValidationFailure
from .gates import evaluate_gate_results


def create_execution_record(ir: dict[str, Any], observations: dict[str, Any]) -> dict[str, Any]:
    observations = evaluate_gate_results(ir, observations)
    configured = {ref_identity(gate["source"]): gate for gate in ir["qualityGates"]}
    findings: list[Finding] = []
    observed: dict[tuple[str, str], dict[str, Any]] = {}
    for result in observations.get("gateResults", []):
        key = ref_identity(result["source"])
        if key in observed:
            findings.append(Finding("FAF-GATE-RESULT-DUPLICATE", f"Multiple results were supplied for {key[0]}@{key[1]}.", "/gateResults"))
        observed[key] = result
    for key in sorted(configured):
        if key not in observed:
            findings.append(Finding("FAF-GATE-RESULT-MISSING", f"No result was supplied for {key[0]}@{key[1]}.", "/gateResults"))
    for key in sorted(observed):
        if key not in configured:
            findings.append(Finding("FAF-GATE-RESULT-UNKNOWN", f"Result supplied for unconfigured gate {key[0]}@{key[1]}.", "/gateResults"))
    if findings:
        raise ValidationFailure(findings)

    status = "accepted"
    for key, gate in configured.items():
        result_status = observed[key]["status"]
        if result_status == "not-evaluated":
            status = "pending-review"
        elif result_status == "failed" and gate["failureAction"] == "escalate":
            status = "escalated"
        elif result_status == "failed" and gate["failureAction"] == "block":
            status = "blocked"
        elif result_status == "failed" and status == "accepted":
            status = "pending-review"

    human_review = bool(ir["authority"]["reviewRequirements"]) or any(
        gate["phase"] == "human-review" for gate in ir["qualityGates"]
    )
    if human_review and status == "accepted":
        status = "pending-review"
    return {
        "recordVersion": "1.0",
        "kind": "ExecutionRecord",
        "irBuildId": ir["buildId"],
        "status": status,
        "outputSummary": observations["outputSummary"],
        "gateResults": [observed[key] for key in sorted(observed)],
        "humanReviewRequired": human_review,
    }
