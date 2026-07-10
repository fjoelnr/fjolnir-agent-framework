# ADR 0006: Automated gates verify evidence, not approval

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

FAF Quality Gates currently record caller-supplied results. The framework needs
repeatable checks for objective conditions while preserving the Constitution's
human-accountability boundary.

## Decision

1. FAF v1 introduces the deterministic `evidence-set` Quality Gate evaluator.
2. An `evidence-set` evaluator passes only when every configured required
   evidence statement is present in the observation for that gate.
3. Automated evaluator results override a caller-supplied pass or fail status
   for that evaluator, but preserve the supplied evidence as review input.
4. Gates without an evaluator remain manual: their supplied status and evidence
   are recorded unchanged.
5. Evaluators emit only `passed` or `failed`; disposition still follows the
   Gate's configured failure action and applicable human-review requirements.
6. Automated gate success is evidence of the declared check only. It never
   creates approval, certification, compliance, safety, or operational status.

## Consequences

- The first automated evaluator is simple, portable, and testable.
- Organizations can require specific validation evidence without trusting a
  self-reported pass flag.
- The evaluator does not establish that an evidence statement is true; it only
  verifies its presence. Human or domain review remains necessary where truth
  or adequacy is material.
- Richer evaluators need separate ADRs and conformance cases.

## Compatibility impact

The `evaluator` field is optional on Quality Gate definitions. Existing manual
gates remain valid and preserve their execution behavior.

## Alternatives considered

- Infer evaluators from prose pass criteria: rejected because natural-language
  inference would be non-deterministic and hidden.
- Treat an automated pass as release approval: rejected by constitutional human
  accountability and bounded-autonomy principles.

## Affected artifacts

- Quality Gate schema and resolved IR schema.
- `faf/gates.py` and Execution Record generation.
- Reference gate fixture, conformance tests, and gate documentation.
