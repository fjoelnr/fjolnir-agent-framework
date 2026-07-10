# ADR 0002: Use JSON Schema source artifacts and a resolved IR

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

ADR 0001 defines the core concepts but deliberately leaves serialization,
identity, resolution, compatibility, and IR rules open. FAF needs a portable
format that can be validated without depending on a language, LLM, or prompt
syntax. Human-facing Markdown templates should remain usable, but their current
headings are not a sufficiently precise interchange format.

## Decision

1. FAF v1 machine-readable source artifacts use JSON and JSON Schema Draft
   2020-12.
2. Every stable artifact has a canonical URN identifier, a semantic version,
   an artifact kind, and a specification version.
3. References use an identifier plus an exact version. Version ranges and
   implicit latest-version selection are excluded from v1.
4. Reusable definition artifacts share one envelope and have kind-specific
   payloads. Agent Contracts, Task Contracts, and Agent Genomes have dedicated
   schemas because they define authority and composition boundaries.
5. JSON Schema validates document shape. Cross-artifact reference resolution,
   precedence, authority narrowing, and conflict detection are semantic
   validation steps defined separately.
6. A resolved IR contains no unresolved artifact references. It records all
   source identities and versions, normalized effective authority, selected
   behavior, quality gates, and provenance.
7. Arrays are ordered only where the specification states that order is
   meaningful. Resolvers otherwise canonicalize set-like arrays by identifier
   before hashing or compilation.
8. Unknown properties are rejected in v1 source and IR schemas. Additive format
   evolution therefore requires a new compatible schema version or explicit
   extension mechanism.

## Consequences

- Source artifacts are portable and supported by mature validation tooling.
- Exact references favor reproducibility over dependency-selection convenience.
- Schema validation alone cannot establish that a task is authorized; a FAF
  semantic validator remains necessary.
- YAML may be offered later as an authoring representation only if it maps
  deterministically to the normative JSON data model.
- The resolved IR is suitable input for multiple runtime compiler backends.

## Compatibility impact

No runtime artifacts exist, so no data migration is required. Existing Markdown
templates and examples remain documentation and authoring aids; they are not
implicitly machine-readable FAF v1 artifacts.

## Alternatives considered

- YAML as the normative format: rejected for v1 because parser behavior and
  implicit scalar typing make deterministic interchange harder.
- Markdown with front matter: rejected because prose structure is unsuitable as
  the sole validation and compilation boundary.
- Protocol Buffers: deferred because a binary/code-generation format would add
  implementation coupling before the model is operationally proven.

## Affected artifacts

- `docs/META_MODEL.md`
- `schemas/v1/`
- `fixtures/v1/`
- Future resolvers, validators, compilers, and migration tools
