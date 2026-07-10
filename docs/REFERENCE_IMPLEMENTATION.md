# FAF Reference Implementation

## Scope

The Python package under `faf/` is the first executable reference for the FAF
v1 source model. It demonstrates the architecture; it does not make Python or
the generic text backend normative for other implementations.

The implementation provides:

- Draft 2020-12 structural validation.
- Exact local artifact resolution.
- Kind, contract, task type, capability, tool, and quality-gate checks.
- Deterministic resolved IR and portable SHA-256 build identity.
- A generic Markdown runtime backend.
- Post-execution gate evaluation and Execution Records.
- Explainable Policy evaluation that can deny facts or require human review.
- Deterministic `evidence-set` Quality Gate evaluation.

## Install

Use Python 3.11 or newer:

```text
python -m pip install -e .
```

The distribution includes the v1 schemas. `--schemas PATH` may override them for
development or conformance testing.

## Resolve a reference task

```text
faf resolve \
  --catalog fixtures/v1/valid/reference \
  --genome fixtures/v1/valid/reference/agent-genome.json \
  --task fixtures/v1/valid/reference/task-contract.json \
  --output resolved-ir.json
```

## Compile a runtime representation

```text
faf compile --ir resolved-ir.json --output runtime.md
```

## Create an Execution Record

```text
faf record \
  --ir resolved-ir.json \
  --observations fixtures/v1/valid/reference/execution-observations.json \
  --output execution-record.json
```

Passing automated gates does not override a human-review requirement. The
reference record therefore remains `pending-review` even though its automated
gate passed.

## Test

```text
python -m unittest discover -s tests -p "test_*.py" -v
```

## Current boundaries

- Catalog discovery is local and filesystem-based.
- The generic backend is intentionally vendor-neutral.
- Execution observations are supplied by the caller; FAF does not execute an
  LLM or external tool itself.
- Policy semantics beyond explicit selection, prohibitions, and authority sets
  remain future work.
- This implementation is experimental and not an assurance or compliance
  certification mechanism.
