# FAF v1 Policy Engine

## Purpose

The Policy Engine evaluates bounded declarative rules during Agent Genome and
Task Contract resolution. It supplements contract authority checks and cannot
grant capabilities, tools, task types, or approval authority.

## Rule model

Every Policy definition contains ordered rules with:

- `id`: stable within the Policy version.
- `effect`: `deny` or `require-human-review`.
- `subject`: `task-type`, `risk-level`, `capability`, or `tool`.
- `value`: the exact target or risk threshold.
- `message`: the reviewable rationale returned by evaluation.

Duplicate rule identifiers within one Policy are semantic errors.

## Matching

Task type, capability, and tool rules use exact string matching. Risk rules use
this fixed order:

```text
low < moderate < high < critical
```

A risk rule matches its configured level and every higher level. Schemas reject
unknown risk values before policy evaluation.

## Effects

A matched `deny` stops resolution with `FAF-POLICY-DENIED`. Contract permission
does not override a Policy denial.

A matched `require-human-review` adds its message to the effective IR review
requirements. It cannot be removed by the Task Contract or compiler.

An unmatched rule has no behavioral effect, but its Policy Decision is retained
for traceability.

## Decision evidence

Every evaluated rule produces an IR entry containing:

- Source Policy identity and version.
- Rule identifier.
- Effect, subject, and configured value.
- Match result.
- Human-readable message.

This allows a reviewer to distinguish an absent rule, an evaluated but unmatched
rule, and a matched rule.

## Security and portability boundary

Policy files contain data, not executable expressions. The v1 engine performs
no dynamic evaluation, network lookup, user-defined code execution, regex
matching, or implicit fact discovery. New subjects or effects require governed
schema and semantic evolution.
