from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .errors import Finding, ValidationFailure

SCHEMA_BY_KIND = {
    "Constitution": "constitution.schema.json",
    "Policy": "definition-artifact.schema.json",
    "ReasoningPack": "definition-artifact.schema.json",
    "Capability": "definition-artifact.schema.json",
    "Role": "definition-artifact.schema.json",
    "Domain": "definition-artifact.schema.json",
    "Tool": "definition-artifact.schema.json",
    "QualityGate": "definition-artifact.schema.json",
    "AgentContract": "agent-contract.schema.json",
    "TaskContract": "task-contract.schema.json",
    "AgentGenome": "agent-genome.schema.json",
    "ResolvedAgentTask": "resolved-ir.schema.json",
    "ExecutionRecord": "execution-record.schema.json",
}


class SchemaValidator:
    def __init__(self, schema_dir: Path):
        schemas: dict[str, dict[str, Any]] = {}
        registry = Registry()
        for path in sorted(schema_dir.glob("*.schema.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        self._schemas = schemas
        self._registry = registry

    def validate(self, artifact: dict[str, Any], source: str = "") -> None:
        kind = artifact.get("kind")
        schema_name = SCHEMA_BY_KIND.get(kind)
        if schema_name is None:
            raise ValidationFailure([Finding(
                "FAF-KIND-UNKNOWN", f"Unsupported artifact kind: {kind!r}.", source
            )])
        validator = Draft202012Validator(self._schemas[schema_name], registry=self._registry)
        findings = []
        for error in sorted(validator.iter_errors(artifact), key=lambda item: list(item.path)):
            pointer = "".join(f"/{part}" for part in error.absolute_path)
            findings.append(Finding("FAF-SCHEMA-INVALID", error.message, pointer or source))
        if findings:
            raise ValidationFailure(findings)
