from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Iterable

from .catalog import Artifact, Catalog, canonical_json, identity, ref, ref_identity
from .errors import Finding, ValidationFailure
from .policy import evaluate_policies
from .schema import SchemaValidator

KIND_BY_SELECTION = {
    "policies": "Policy",
    "domains": "Domain",
    "reasoningPacks": "ReasoningPack",
    "capabilities": "Capability",
    "tools": "Tool",
    "qualityGates": "QualityGate",
}

ALLOW_FIELD = {
    "policies": "allowedPolicies",
    "domains": "allowedDomains",
    "reasoningPacks": "allowedReasoningPacks",
    "capabilities": "allowedCapabilities",
    "tools": "allowedTools",
}


def _keys(values: Iterable[Artifact]) -> set[tuple[str, str]]:
    return {ref_identity(value) for value in values}


def _sorted_refs(values: Iterable[Artifact]) -> list[Artifact]:
    return sorted((ref(value) for value in values), key=lambda item: (item["id"], item["version"]))


class Resolver:
    def __init__(self, catalog: Catalog, schema_validator: SchemaValidator):
        self.catalog = catalog
        self.schemas = schema_validator

    @classmethod
    def from_paths(cls, catalog_dir: Path, schema_dir: Path) -> "Resolver":
        return cls(Catalog.load(catalog_dir), SchemaValidator(schema_dir))

    def resolve(self, genome_document: Artifact, task_document: Artifact) -> Artifact:
        self.schemas.validate(genome_document)
        self.schemas.validate(task_document)
        genome = genome_document
        task = task_document
        constitution = self.catalog.resolve(genome["spec"]["constitution"], "Constitution", "/spec/constitution")
        contract = self.catalog.resolve(genome["spec"]["agentContract"], "AgentContract", "/spec/agentContract")
        role = self.catalog.resolve(genome["spec"]["role"], "Role", "/spec/role")
        self.schemas.validate(constitution)
        self.schemas.validate(contract)
        self.schemas.validate(role)

        findings: list[Finding] = []
        if ref_identity(task["spec"]["agentContract"]) != identity(contract):
            findings.append(Finding("FAF-AUTH-CONTRACT-MISMATCH", "Task and Genome select different Agent Contracts.", "/spec/agentContract"))
        if ref_identity(contract["spec"]["role"]) != identity(role):
            findings.append(Finding("FAF-AUTH-ROLE-NOT-ALLOWED", "Genome role differs from the Agent Contract role.", "/spec/role"))
        if task["spec"]["taskType"] not in contract["spec"]["allowedTaskTypes"]:
            findings.append(Finding("FAF-AUTH-TASK-TYPE-NOT-ALLOWED", "Task type is not allowed by the Agent Contract.", "/spec/taskType"))

        selected: dict[str, list[Artifact]] = {}
        for field, expected_kind in KIND_BY_SELECTION.items():
            selected[field] = []
            for index, reference in enumerate(genome["spec"][field]):
                artifact = self.catalog.resolve(reference, expected_kind, f"/spec/{field}/{index}")
                self.schemas.validate(artifact)
                selected[field].append(artifact)
            allowed_field = ALLOW_FIELD.get(field)
            if allowed_field:
                allowed = _keys(contract["spec"].get(allowed_field, []))
                for artifact in selected[field]:
                    if identity(artifact) not in allowed:
                        findings.append(Finding(
                            f"FAF-AUTH-{expected_kind.upper()}-NOT-ALLOWED",
                            f"Selected {expected_kind} is not allowed by the Agent Contract.",
                            f"/spec/{field}",
                        ))

        required_gates = _keys(contract["spec"]["requiredQualityGates"])
        genome_gates = {identity(value) for value in selected["qualityGates"]}
        if not required_gates <= genome_gates:
            findings.append(Finding("FAF-GATE-REQUIRED-MISSING", "Genome omits a required Agent Contract gate.", "/spec/qualityGates"))

        allowed_caps = _keys(contract["spec"]["allowedCapabilities"])
        for item in task["spec"]["requestedCapabilities"]:
            if ref_identity(item) not in allowed_caps:
                findings.append(Finding("FAF-AUTH-CAPABILITY-NOT-ALLOWED", "Task requests a capability not allowed by the Agent Contract.", "/spec/requestedCapabilities"))
        allowed_tools = _keys(contract["spec"]["allowedTools"])
        for item in task["spec"]["requestedTools"]:
            if ref_identity(item) not in allowed_tools:
                findings.append(Finding("FAF-AUTH-TOOL-NOT-ALLOWED", "Task requests a tool not allowed by the Agent Contract.", "/spec/requestedTools"))
        task_gates = _keys(task["spec"]["qualityGates"])
        if not required_gates <= task_gates:
            findings.append(Finding("FAF-GATE-REQUIRED-MISSING", "Task omits a required Agent Contract gate.", "/spec/qualityGates"))
        if findings:
            raise ValidationFailure(findings)

        task_capabilities = [self.catalog.resolve_any(value, "/spec/requestedCapabilities") for value in task["spec"]["requestedCapabilities"]]
        task_tools = [self.catalog.resolve_any(value, "/spec/requestedTools") for value in task["spec"]["requestedTools"]]
        policy_decisions = evaluate_policies(
            selected["policies"],
            task_type=task["spec"]["taskType"],
            risk_level=task["spec"]["riskLevel"],
            capabilities=task_capabilities,
            tools=task_tools,
        )
        denied = [decision for decision in policy_decisions if decision.matched and decision.effect == "deny"]
        if denied:
            raise ValidationFailure([
                Finding(
                    "FAF-POLICY-DENIED",
                    f"{decision.source['id']} rule {decision.rule_id}: {decision.message}",
                    "/spec",
                )
                for decision in denied
            ])
        review_requirements = list(contract["spec"]["reviewRequirements"])
        review_requirements.extend(
            decision.message
            for decision in policy_decisions
            if decision.matched and decision.effect == "require-human-review"
        )
        review_requirements = list(dict.fromkeys(review_requirements))
        all_gate_refs = {ref_identity(value): value for value in contract["spec"]["requiredQualityGates"] + task["spec"]["qualityGates"]}
        gates = [self.catalog.resolve(value, "QualityGate", "/spec/qualityGates") for _, value in sorted(all_gate_refs.items())]

        policies = [statement for artifact in selected["policies"] for statement in artifact["spec"]["statements"]]
        reasoning = [step for artifact in selected["reasoningPacks"] for step in artifact["spec"].get("steps", [])]
        instructions = role["spec"]["statements"] + [statement for artifact in selected["domains"] for statement in artifact["spec"]["statements"]]
        prohibited = set(contract["spec"]["prohibitedActions"] + role["spec"].get("prohibitedActions", []))
        for artifact in selected["domains"] + selected["policies"]:
            prohibited.update(artifact["spec"].get("prohibitedActions", []))

        source_artifacts = [constitution, genome, contract, task, role]
        for values in selected.values():
            source_artifacts.extend(values)
        source_artifacts.extend(task_capabilities + task_tools + gates)
        unique_sources = {identity(value): value for value in source_artifacts}

        ir: Artifact = {
            "irVersion": "1.0",
            "kind": "ResolvedAgentTask",
            "buildId": "pending",
            "sources": _sorted_refs(unique_sources.values()),
            "agent": {
                "genome": ref(genome), "contract": ref(contract), "role": ref(role),
                "domains": _sorted_refs(selected["domains"]),
                "lifecycle": genome["metadata"]["lifecycle"],
            },
            "task": {
                "contract": ref(task), "taskType": task["spec"]["taskType"],
                "objective": task["spec"]["objective"], "inputs": task["spec"]["inputs"],
                "constraints": task["spec"]["constraints"],
                "acceptanceCriteria": task["spec"]["acceptanceCriteria"],
                "riskLevel": task["spec"]["riskLevel"],
                "requiredOutput": task["spec"]["requiredOutput"],
                "escalationConditions": task["spec"]["escalationConditions"],
            },
            "behavior": {
                "policies": sorted(set(policies)), "reasoning": reasoning,
                "instructions": list(dict.fromkeys(instructions)),
                "policyDecisions": [decision.as_dict() for decision in policy_decisions],
            },
            "authority": {
                "capabilities": _sorted_refs(task_capabilities), "tools": _sorted_refs(task_tools),
                "prohibitedActions": sorted(prohibited),
                "reviewRequirements": review_requirements,
            },
            "qualityGates": [{
                "source": ref(gate), "phase": gate["spec"]["gate"]["phase"],
                "passCriteria": gate["spec"]["gate"]["passCriteria"],
                "failureAction": gate["spec"]["gate"]["failureAction"],
                **({"evaluator": gate["spec"]["gate"]["evaluator"]} if "evaluator" in gate["spec"]["gate"] else {}),
            } for gate in sorted(gates, key=identity)],
            "provenance": [
                {"target": "/authority", "sources": [ref(contract), ref(task)]},
                {"target": "/behavior/instructions", "sources": _sorted_refs([role] + selected["domains"])},
                {"target": "/behavior/policyDecisions", "sources": _sorted_refs(selected["policies"])},
            ],
        }
        semantic = dict(ir)
        semantic.pop("buildId")
        ir["buildId"] = "sha256:" + hashlib.sha256(canonical_json(semantic).encode("utf-8")).hexdigest()
        self.schemas.validate(ir)
        return ir
