# FAF v1 Conformance

## Purpose

The conformance suite verifies that implementations preserve FAF's structural,
identity, authority, gate, determinism, and provenance rules. Passing the suite
demonstrates compatibility with the tested FAF specification version; it is not
an assurance, compliance, safety, or production-readiness certification.

## Conformance areas

| Area | Required behavior | Current evidence |
| --- | --- | --- |
| Structural validity | Validate source and derived artifacts against Draft 2020-12 schemas | Positive reference package and schema-invalid fixture |
| Exact identity | Resolve `(id, version)` and reject conflicting duplicates | Reference resolution and duplicate-identity fixture |
| Kind safety | Reject an artifact used in the wrong selection slot | Wrong-kind Genome fixture |
| Authority narrowing | Reject tools, capabilities, and task types outside the Agent Contract | Isolated negative Task Contracts |
| Required controls | Reject omission of required Quality Gates | Missing-gate Task Contract |
| Determinism | Produce identical IR and build identifiers from identical inputs | Repeated resolver test and golden IR |
| Compiler boundary | Preserve prohibitions and build identity in runtime output | Generic-backend golden test |
| Execution accountability | Require one result per gate and preserve human review | Execution Record tests |

## Fixture rules

Positive fixtures under `fixtures/v1/valid/` must pass structural and semantic
validation. Negative fixtures under `fixtures/v1/invalid/` must isolate the
error codes declared in `expectations.json`.

Each negative fixture should violate one architectural rule. If one input
necessarily produces multiple findings, the manifest must list the complete
stable error-code set. Test annotations remain outside normative artifacts.

## Running the suite

```text
python -m pip install -e .
python -m unittest discover -s tests -p "test_*.py" -v
```

CI runs the suite on every push and pull request across all Python versions
declared by the project workflow.

## Compatibility claims

A conforming implementation must declare:

- Supported FAF `specVersion` and `irVersion` values.
- Supported artifact kinds and compiler backends.
- Conformance-suite revision or commit.
- Any unsupported optional behavior.
- Resolver and compiler implementation versions.

Claims must not use `validated` or `operational` lifecycle terminology unless
the applicable lifecycle criteria and human approval record also exist.
