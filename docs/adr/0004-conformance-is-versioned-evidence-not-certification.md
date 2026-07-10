# ADR 0004: Conformance is versioned evidence, not certification

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

FAF now has executable schemas, semantic rules, a resolver, a compiler, and
Execution Records. Automated test success could be misunderstood as validation
of an agent's fitness, safety, compliance, or operational maturity.

## Decision

1. FAF conformance means that an implementation passes a declared version of
   the structural and semantic compatibility suite.
2. A conformance claim identifies the FAF specification versions, suite commit,
   implementation version, supported artifact kinds, and supported backends.
3. Positive fixtures demonstrate accepted behavior. Negative fixtures declare
   their complete expected stable error-code set in an external manifest.
4. Each negative fixture should isolate one rule wherever possible, and the
   suite must fail when a negative fixture lacks a manifest entry.
5. CI conformance evidence is necessary for compatibility claims but does not
   establish assurance, compliance, safety, production readiness, or lifecycle
   status.
6. Lifecycle claims such as `validated` or `operational` require separate,
   scope-specific criteria, evidence, review, and approval.

## Consequences

- Compatibility regressions become visible and reproducible.
- Test evidence remains properly bounded and cannot silently become an approval
  claim.
- Other implementations can use the same fixtures and error-code expectations.
- Formal lifecycle validation remains future governance work.

## Compatibility impact

No source or IR format changes. Future implementations making conformance claims
must publish the declared evidence fields.

## Alternatives considered

- Treat a green CI suite as agent validation: rejected because implementation
  compatibility is not evidence of fitness for a concrete operational context.
- Test only positive fixtures: rejected because authority and failure semantics
  are central FAF behavior.

## Affected artifacts

- `docs/CONFORMANCE.md`
- `fixtures/v1/invalid/expectations.json`
- `tests/test_reference_implementation.py`
- `.github/workflows/ci.yml`
