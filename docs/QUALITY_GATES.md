# FAF v1 Quality Gates

## Purpose

Quality Gates make required checks, their evidence, failure handling, and
review state explicit. A gate definition is selected by a contract or genome;
its result belongs to a separate Execution Record.

## Evaluation modes

Gates without an `evaluator` are manual. The caller supplies their status and
evidence, and FAF records them without inferring correctness.

The v1 `evidence-set` evaluator is automated. It requires a configured set of
exact evidence statements. It passes only when the supplied evidence contains
all of them, otherwise it fails.

```json
{
  "evaluator": {
    "kind": "evidence-set",
    "requiredEvidence": ["Tests passed", "Scope was reviewed"]
  }
}
```

An evidence-set evaluator verifies that required statements were supplied. It
does not independently prove those statements true. Its pass result must never
be represented as approval, certification, compliance, safety assurance, or
operational authorization.

## Failure disposition

The Quality Gate's `failureAction` determines how a failed result affects the
Execution Record:

- `disclose`: pending review unless another condition is stricter.
- `block`: blocked.
- `escalate`: escalated.

Missing and duplicate results are validation errors. A passed automated gate
does not remove a separate human-review requirement.

## Extension boundary

New evaluator kinds need explicit schemas, deterministic semantics, tests,
security analysis, and an ADR. Evaluators may verify declared observable facts;
they must not grant authority or silently replace accountable review.
