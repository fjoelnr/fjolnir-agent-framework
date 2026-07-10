from __future__ import annotations

from typing import Any


def evaluate_gate_results(ir: dict[str, Any], observations: dict[str, Any]) -> dict[str, Any]:
    """Apply deterministic evaluator semantics to supplied gate observations."""
    configured = {
        (gate["source"]["id"], gate["source"]["version"]): gate
        for gate in ir["qualityGates"]
    }
    results = []
    for result in observations.get("gateResults", []):
        key = (result["source"]["id"], result["source"]["version"])
        gate = configured.get(key)
        if gate is None or "evaluator" not in gate:
            results.append(result)
            continue
        evaluator = gate["evaluator"]
        if evaluator["kind"] != "evidence-set":
            raise ValueError(f"Unsupported Quality Gate evaluator: {evaluator['kind']!r}")
        supplied = set(result["evidence"])
        status = "passed" if set(evaluator["requiredEvidence"]) <= supplied else "failed"
        results.append({**result, "status": status})
    return {**observations, "gateResults": results}
