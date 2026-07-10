# Fjölnir Agent Framework Project Charter

Version: 0.1

## Mandate

The Fjölnir Agent Framework (FAF) develops a model-independent architecture for
specifying, governing, validating, executing, and evolving professional AI
agents. It treats agent behavior as a versioned engineering system rather than
an opaque prompt artifact.

The Constitution is the highest-precedence normative document. This Charter
defines project direction and delivery boundaries. Accepted ADRs govern material
architecture decisions within those boundaries.

## Intended outcomes

FAF aims to provide:

- A stable constitutional and policy foundation.
- Modular Agent Genomes and explicit Agent and Task Contracts.
- Model-independent resolution and validation.
- Traceable runtime representations and Execution Records.
- Proportional Quality Gates and human-review controls.
- Governance, migration, feedback, and revalidation workflows.

## Scope

The project includes architecture specifications, schemas, reference artifacts,
conformance tests, resolvers, policy evaluation, compiler backends, authoring
workflows, and governance guidance.

The project does not grant an agent regulatory, legal, medical, financial,
safety, certification, or organizational approval authority. FAF artifacts may
support such processes, but accountable approval remains external unless an
authorized governance process explicitly states otherwise.

## Delivery principles

- Architecture precedes implementation.
- The Constitution cannot be weakened by lower layers.
- Authority is explicit and narrows at lower precedence.
- Model-independent semantics remain separate from runtime-specific rendering.
- Material decisions are recorded through ADRs.
- Claims of validation are limited to a declared version, scope, and evidence.
- Operational maturity requires review, monitoring, and revalidation.

## Development stages

FAF evolves through:

1. Foundation.
2. Meta Model.
3. Reference Architecture.
4. Conformance and continuous integration.
5. Policy enforcement and runtime backends.
6. Authoring and governance workflows.
7. Validated operational profiles.

Progress and exit criteria are maintained in `ROADMAP.md`.

## Governance

Constitution changes require exceptional review. Material architecture changes
require an ADR. Schemas, contracts, policy behavior, compiler behavior, Quality
Gates, and lifecycle claims require compatibility assessment proportional to
their impact.

The maintainers may accept, revise, deprecate, or retire project artifacts. A
documented lifecycle state never substitutes for evidence that its validation
criteria were actually met.

## Current status

FAF is experimental. Its architecture, v1 schemas, and first reference vertical
slice exist, but the framework is not yet a complete assurance method,
compliance standard, or production governance system.
