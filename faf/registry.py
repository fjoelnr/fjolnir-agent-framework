from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .catalog import canonical_json
from .errors import Finding, ValidationFailure
from .schema import SchemaValidator

DEFINITION_KINDS = {
    "Policy", "ReasoningPack", "Capability", "Role", "Domain", "Tool", "QualityGate"
}


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def build_registry(catalog_dir: Path, schema_dir: Path) -> dict[str, Any]:
    validator = SchemaValidator(schema_dir)
    entries: list[dict[str, str]] = []
    identities: dict[tuple[str, str], str] = {}
    findings: list[Finding] = []
    for path in sorted(catalog_dir.rglob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or not {"id", "version", "kind", "metadata"} <= value.keys():
            continue
        validator.validate(value, path.as_posix())
        key = (value["id"], value["version"])
        digest = _digest(value)
        existing = identities.get(key)
        if existing is not None and existing != digest:
            findings.append(Finding(
                "FAF-REF-DUPLICATE-IDENTITY",
                f"Identity {key[0]}@{key[1]} has conflicting definitions.",
                path.as_posix(),
            ))
            continue
        identities[key] = digest
        entries.append({
            "id": value["id"], "version": value["version"], "kind": value["kind"],
            "name": value["metadata"]["name"], "lifecycle": value["metadata"]["lifecycle"],
            "source": path.relative_to(catalog_dir).as_posix(), "digest": digest,
        })
    if findings:
        raise ValidationFailure(findings)
    entries.sort(key=lambda entry: (entry["id"], entry["version"], entry["source"]))
    return {
        "registryVersion": "1.0",
        "kind": "ArtifactRegistry",
        "catalogBuildId": _digest(entries),
        "artifacts": entries,
    }


def verify_registry(catalog_dir: Path, registry_path: Path, schema_dir: Path) -> None:
    expected = build_registry(catalog_dir, schema_dir)
    actual = json.loads(registry_path.read_text(encoding="utf-8"))
    SchemaValidator(schema_dir).validate(actual, registry_path.as_posix())
    if canonical_json(actual) != canonical_json(expected):
        raise ValidationFailure([Finding(
            "FAF-REGISTRY-STALE",
            "Registry does not match the current validated catalog.",
            registry_path.as_posix(),
        )])


def scaffold_definition(kind: str, artifact_id: str, name: str) -> dict[str, Any]:
    if kind not in DEFINITION_KINDS:
        raise ValueError(f"Unsupported definition kind: {kind!r}.")
    spec: dict[str, Any] = {"statements": []}
    if kind == "Policy":
        spec["rules"] = []
    elif kind == "ReasoningPack":
        spec["steps"] = []
    elif kind == "QualityGate":
        spec["gate"] = {
            "phase": "pre-execution", "passCriteria": [], "failureAction": "disclose"
        }
    return {
        "specVersion": "1.0", "kind": kind, "id": artifact_id, "version": "0.1.0",
        "metadata": {"name": name, "lifecycle": "draft"}, "spec": spec,
    }
