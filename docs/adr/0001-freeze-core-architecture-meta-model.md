# ADR 0001: Freeze the core architecture meta-model

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

FAF's foundation documents agree on constitution-first, modular agent design,
but use overlapping terms and sometimes present the architecture as a single
linear pipeline. In particular, `Operating Mode` overlaps with `Domain`, and
`Capability Profile` overlaps with `Agent Genome`. Quality Gates also appear
both as definition-time inputs and as runtime checks without an explicit
distinction.

Implementing schemas or a compiler before resolving these differences would
make accidental terminology and ordering choices part of the public format.

## Decision

FAF adopts the following canonical meta-model:

1. The Constitution is the highest-precedence normative artifact. Lower layers
   may strengthen but never weaken it.
2. Global Policies, Reasoning Packs, Capability definitions, Roles, Domains,
   Tool definitions, and Quality Gate definitions are independently versioned,
   reusable definition artifacts.
3. `Domain` is the canonical architectural concept. An `Operating Mode` is a
   compatibility and presentation term for a selectable Domain Profile. New
   architecture specifications use `Domain` or `Domain Profile`.
4. An Agent Contract is the durable authority boundary for one concrete agent.
   It selects permitted definition artifacts and declares purpose, allowed and
   prohibited actions, tool permissions, outputs, review requirements, and
   lifecycle state.
5. A Task Contract is an assignment scoped by an Agent Contract. It cannot add
   authority, capabilities, or tool permissions absent from that contract.
6. An Agent Genome is the complete, versioned, resolvable specification used to
   reproduce and evaluate an agent. `Capability Profile` is retained only as a
   legacy term for an incomplete or earlier genome-shaped composition.
7. Quality Gate definitions are selected into an Agent Genome or Task Contract.
   Their evaluations occur during validation or execution and produce explicit
   results. A gate definition and a gate result are different artifacts.
8. Definition dependencies are not a single execution order. The build path is
   `source artifacts -> resolved Agent Genome -> IR -> runtime-specific
   representation`. Runtime applies an Agent Contract to a Task Contract,
   records evidence and gate results, and emits feedback.
9. Precedence is Constitution, Global Policies, Agent Contract, then Task
   Contract. More specific artifacts may narrow behavior but never grant
   authority prohibited or not granted above them. Unresolvable conflicts are
   validation errors, not compiler interpretation choices.
10. All stable artifacts require explicit identity and version metadata. Exact
    schema and compatibility rules are deferred to the schema and IR milestone.

## Consequences

- The architecture can be represented as a dependency graph and deterministic
  build process rather than an ambiguous layer pipeline.
- Existing mode documents remain usable as Domain Profiles; they do not require
  immediate filename changes.
- Existing Capability Profile references need migration to Agent Genome.
- Schema work can now define concrete identifiers, resolution, conflict, and
  compatibility rules without reopening the core vocabulary.
- This ADR freezes conceptual boundaries, not data formats or implementation
  technology.

## Compatibility impact

The decision is conceptually compatible with existing examples and templates.
Documents using `Operating Mode` should identify it as a Domain Profile when
materially revised. `Capability Profile` is deprecated in favor of `Agent
Genome`. No runtime migration is required because no compiler or machine-readable
genome format exists yet.

## Alternatives considered

- Keep both Mode and Domain as separate first-class layers. Rejected because the
  current documents give them the same responsibility without a stable boundary.
- Use Capability Profile as the canonical composition. Rejected because Agent
  Genome is broader, includes governance and lifecycle metadata, and is already
  central to the intended compiler architecture.
- Treat the published arrow chain as strict dependency order. Rejected because
  several reusable layers constrain one another without forming a safe linear
  inheritance chain.

## Affected artifacts

- `docs/ARCHITECTURE.md`
- `docs/FJOLNIR_CONSTITUTION.md`
- `docs/FOUNDING_PRINCIPLES.md`
- `README.md`
- Future Agent Genome, contract, IR, compiler, and validation specifications
