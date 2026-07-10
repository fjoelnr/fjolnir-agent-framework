# ADR 0008: Derived registry and safe definition scaffolds

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

FAF artifacts are currently authored as individual JSON files. Teams need a
deterministic inventory for review and a safe way to begin new reusable
definitions without hand-copying schema envelopes.

## Decision

1. The FAF v1 Artifact Registry is a derived, local JSON index over a catalog
   directory. It is not a source of authority and is never used to select an
   implicit latest artifact version.
2. A registry entry records exact identity, kind, lifecycle, human name, source
   path, and SHA-256 digest of each source artifact.
3. The registry build identifier is a SHA-256 digest of its canonical entry
   collection. Registry verification rebuilds the expected index and rejects a
   stale or modified registry.
4. Registry construction validates every indexed source artifact and rejects
   duplicate identities with differing content.
5. The first Builder command scaffolds valid reusable Definition Artifacts:
   Policy, Reasoning Pack, Capability, Role, Domain, Tool, and Quality Gate.
6. Builder output requires an explicit destination and refuses to overwrite an
   existing file unless `--force` is explicitly supplied.
7. Agent Contracts, Task Contracts, and Agent Genomes are not scaffolded in v1
   because their mandatory references and authority decisions require more
   context than safe defaults can provide.

## Consequences

- Catalogs become inspectable and integrity-checkable without a server.
- Teams can create valid reusable definitions with less schema boilerplate.
- A Registry cannot silently change resolution: resolvers continue to use exact
  source references.
- A later full Agent Builder must guide contract composition and make authority
  choices explicit.

## Compatibility impact

No existing artifact changes are required. Registry documents are derived and
may be regenerated. Definition scaffolds follow existing v1 schemas.

## Alternatives considered

- A mutable central registry as the resolution authority: rejected because it
  would introduce hidden dependency selection and operational coupling.
- Scaffold complete Agents with placeholder authority: rejected because invalid
  or overly permissive defaults would undermine contract review.

## Affected artifacts

- `faf/registry.py`
- Builder and registry CLI commands
- Artifact Registry schema and reference fixture
- `docs/AGENT_BUILDER.md`
