# Architecture Decision Records

Architecture Decision Records (ADRs) capture material decisions that affect the
FAF meta-model, compatibility, governance, or runtime architecture.

## Status lifecycle

An ADR has one of these states:

- Proposed: open for review and not yet authoritative.
- Accepted: part of the architecture baseline.
- Superseded: replaced by a later ADR.
- Rejected: considered but not adopted.
- Deprecated: retained for traceability but no longer recommended.

Accepted ADRs are immutable decision records. A material change requires a new
ADR that supersedes the earlier record. Editorial corrections may be made when
they do not alter the decision.

## Numbering and filenames

Use a four-digit sequence and a short title:

`NNNN-short-kebab-case-title.md`

Numbers are never reused. ADRs are ordered by number, not by acceptance date.

## When an ADR is required

Create an ADR for changes to:

- Constitutional interpretation or layer precedence.
- Canonical architectural concepts or dependency rules.
- Agent Genome, contract, or intermediate-representation compatibility.
- Authority, capability, tool-permission, or quality-gate semantics.
- Compiler, policy-engine, validation, or execution boundaries.
- Lifecycle, versioning, migration, or revalidation rules.

Routine editorial changes, examples, and compatible additions do not require an
ADR unless they establish new normative behavior.

## Review requirements

An ADR must state its context, decision, consequences, compatibility impact,
and affected artifacts. Review rigor is proportional to risk. Decisions that
affect human oversight, safety boundaries, or constitutional requirements need
explicit governance review before acceptance.

Use [0000-template.md](0000-template.md) for new records.

## Index

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-freeze-core-architecture-meta-model.md) | Freeze the core architecture meta-model | Accepted |
| [0002](0002-use-json-schema-and-a-resolved-ir.md) | Use JSON Schema source artifacts and a resolved IR | Accepted |
| [0003](0003-reference-implementation-and-build-identity.md) | Reference implementation and build identity | Accepted |
