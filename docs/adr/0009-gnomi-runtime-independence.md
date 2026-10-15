# ADR 0009: GNOMI identity and governance remain independent of runtime

- Status: Proposed
- Date: 2026-10-15
- Decision owners: Project maintainers and GNOMI application owner
- Supersedes: None
- Superseded by: None
- Scope: GNOMI application proposal, not a new normative FAF core requirement

## Context

[Issue #2](https://github.com/fjoelnr/fjolnir-agent-framework/issues/2) requires
Gnomi and other personal assistants to survive a change of execution host.
FAF already separates exact source artifacts, resolved IR and pure runtime
renderers ([ADR 0003](0003-reference-implementation-and-build-identity.md),
[ADR 0007](0007-runtime-backends-render-but-never-execute-authority.md)).
The reference implementation does not execute models, bind tool credentials or
enforce runtime resource isolation. Treating a vendor session as an agent would
couple identity and memory to that session's privileges and native storage.

## Decision

Propose an external GNOMI application layer with a stable agent directory,
versioned portable profiles, scoped memory gateway and runtime adapter contract.
Agent identity, owner, contracts, memory ownership and authorization remain
external to OpenClaw/Hermes/Codex/local-model hosts. Personality never grants rights.

Adapters discover controls, prepare isolated runs, execute broker-mediated calls,
emit audit/usage evidence, cancel, and export/restore only approved portable state.
Unsupported mandatory isolation, authorization or audit controls deny startup.
Tool execution is explicitly bound outside FAF compiler backends. No executable
provider tools are inferred from descriptive FAF Tool references.

A runtime change revokes old grants, freezes/checks exported state, reauthorizes
the destination and creates fresh run/grant IDs linked to the old run. Effective
rights can only stay equal or narrow. Do not replay unknown side effects or claim
hidden model reasoning is portable. See [adapter details](../GNOMI_COLLECTIVE_ARCHITECTURE.md).

## Consequences

Benefits: stable personal assistant identity, controlled runtime replacement,
provider-neutral governance and testable execution boundaries.
Costs: adapter maintenance, explicit capability negotiation, storage migration,
private audit retention and external enforcement infrastructure.
Risks: vendors may lack mandatory controls or portable memory; runtime feature
parity is not assured. No runtime winner or successful migration is claimed.

## Compatibility impact

No changes to FAF v1 source schemas, IR, compiler semantics, Constitution or
accepted ADRs. GNOMI profile/run envelopes live beside existing FAF artifacts and
reference exact versions/build IDs. A future FAF-core change needs separate
governance review. Runtime migration requires revalidation of controls and grants.

## Alternatives considered

- Runtime-native agent as identity: simpler setup, rejected for lock-in and
  implicit authority changes during migration.
- Add execution and vendor sessions to FAF core: rejected for premature coupling;
  conflicts with the current pure-renderer boundary.
- Prompt-only portability: inexpensive but cannot enforce credentials, isolation,
  cancellation or resource access; unsuitable as the security boundary.

## Affected artifacts

- GNOMI architecture, future portable profile/adapter specifications and tests.
- #1 workflow envelope/event design and #2 runtime comparison.
- FAF backends are consumed unchanged; no implementation in this ADR.

## Review and acceptance conditions

Choose pinned runtime candidates and the broker/sandbox boundary. Later tests
must show unchanged stable agent identity, fresh credentials, rejection of wider
destination permissions, cancellation/revocation and provenance-preserving export.
Status remains Proposed until explicit maintainer acceptance; implementation
requires separate authorization even if this document is merged.
