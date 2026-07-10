# ADR 0005: Policies only narrow authority

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

FAF policies have so far been descriptive statements. An executable Policy
Engine needs deterministic matching, precedence, and explainable results without
allowing policy syntax to become a hidden authority-grant mechanism.

## Decision

1. FAF v1 policy rules evaluate explicit facts in four subject classes:
   `task-type`, `risk-level`, `capability`, and `tool`.
2. Rules have one of two effects: `deny` or `require-human-review`.
3. Policies cannot grant authority. Capabilities, tools, and task types remain
   bounded by the Agent Contract and Task Contract even when no policy denies
   them.
4. `task-type`, `capability`, and `tool` values match exactly. A `risk-level`
   rule matches when the task risk is equal to or higher than the configured
   threshold in the order low, moderate, high, critical.
5. Every evaluated rule emits a Policy Decision containing source policy,
   stable rule identifier, effect, subject, value, match result, and message.
6. Any matched `deny` rule blocks resolution with `FAF-POLICY-DENIED`. A matched
   `require-human-review` rule adds a review requirement to the resolved IR.
7. Policy Decisions are preserved in the IR even when a rule does not match, so
   reviewers can reconstruct which rules were considered.

## Consequences

- Policy behavior is deterministic and explainable.
- The initial language is deliberately small and cannot express arbitrary code.
- More complex conditions, obligations, and organization-specific facts require
  a later compatible language extension or schema version.
- Policy evaluation supplements rather than replaces contract authority checks.

## Compatibility impact

Policy artifacts gain structured `rules`. Existing descriptive Policy artifacts
must add a rules array when migrated to executable v1 policies. The resolved IR
may include `policyDecisions`; existing IR without decisions remains structurally
valid for compatibility.

## Alternatives considered

- Permit `allow` rules: rejected because they could be mistaken for authority
  grants and complicate deny-by-contract semantics.
- Embed a general expression language: rejected because it would add execution,
  security, determinism, and portability risks before requirements justify it.
- Emit only matched rules: rejected because reviewers need evidence of the
  complete evaluated rule set.

## Affected artifacts

- `schemas/v1/definition-artifact.schema.json`
- `schemas/v1/resolved-ir.schema.json`
- `faf/policy.py`
- `faf/resolver.py`
- Policy fixtures and conformance tests
