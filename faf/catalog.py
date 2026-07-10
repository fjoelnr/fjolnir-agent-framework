from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import Finding, ValidationFailure

Artifact = dict[str, Any]
Identity = tuple[str, str]


def identity(value: Artifact) -> Identity:
    return value["id"], value["version"]


def ref_identity(value: Artifact) -> Identity:
    return value["id"], value["version"]


def ref(value: Artifact) -> Artifact:
    return {"id": value["id"], "version": value["version"]}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class Catalog:
    def __init__(self, artifacts: dict[Identity, Artifact]):
        self._artifacts = artifacts

    @classmethod
    def load(cls, root: Path) -> "Catalog":
        artifacts: dict[Identity, Artifact] = {}
        findings: list[Finding] = []
        for path in sorted(root.rglob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or not {"id", "version", "kind"} <= value.keys():
                continue
            key = identity(value)
            previous = artifacts.get(key)
            if previous is not None and canonical_json(previous) != canonical_json(value):
                findings.append(Finding(
                    "FAF-REF-DUPLICATE-IDENTITY",
                    f"Identity {key[0]}@{key[1]} has conflicting definitions.",
                    str(path),
                ))
            else:
                artifacts[key] = value
        if findings:
            raise ValidationFailure(findings)
        return cls(artifacts)

    def resolve(self, reference: Artifact, expected_kind: str, pointer: str) -> Artifact:
        key = ref_identity(reference)
        artifact = self._artifacts.get(key)
        if artifact is None:
            raise ValidationFailure([Finding(
                "FAF-REF-NOT-FOUND",
                f"Artifact {key[0]}@{key[1]} was not found.",
                pointer,
            )])
        if artifact["kind"] != expected_kind:
            raise ValidationFailure([Finding(
                "FAF-KIND-MISMATCH",
                f"Expected {expected_kind}, found {artifact['kind']} for {key[0]}@{key[1]}.",
                pointer,
            )])
        return artifact

    def resolve_any(self, reference: Artifact, pointer: str) -> Artifact:
        key = ref_identity(reference)
        artifact = self._artifacts.get(key)
        if artifact is None:
            raise ValidationFailure([Finding(
                "FAF-REF-NOT-FOUND",
                f"Artifact {key[0]}@{key[1]} was not found.",
                pointer,
            )])
        return artifact
