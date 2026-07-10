# FAF Architecture Roadmap

## Status

FAF has completed its Foundation, Meta Model, Reference Architecture,
Conformance, and first Policy Engine milestones. It remains experimental and is
not yet an operational assurance or governance system.

## Milestone 1: Architecture baseline

Status: Complete

- Establish the canonical architectural vocabulary.
- Distinguish definition artifacts from runtime results.
- Define authority precedence and conflict behavior.
- Introduce Architecture Decision Records.
- Align the Constitution, Architecture, and repository overview.

Exit criterion: the core concepts can be used to design schemas without making
unrecorded architectural choices.

## Milestone 2: Agent Genome and IR specification

Status: Complete

- Define versioned schemas for Agent Genomes, Agent Contracts, Task Contracts,
  policies, capabilities, tools, reasoning packs, and quality gates.
- Define identity, references, composition, resolution, and conflict semantics.
- Define a model-independent Intermediate Representation.
- Define compatibility, migration, provenance, and validation-error rules.
- Provide valid and invalid reference fixtures.

Exit criterion: a genome and task can be deterministically resolved and
validated into a documented IR without selecting an LLM runtime.

## Milestone 3: End-to-end reference architecture

Status: Complete

- Implement schema and policy validation.
- Resolve one reference Agent Genome and Task Contract into the IR.
- Implement one deterministic runtime compiler backend.
- Produce an execution record with provenance and Quality Gate results.
- Add reproducibility, authority-boundary, and invalid-input tests.

Exit criterion: one existing example passes through the complete architecture
and produces reproducible, traceable artifacts without gaining hidden authority.

Reference implementation: `faf/` and `docs/REFERENCE_IMPLEMENTATION.md`.

## Milestone 4: Conformance and CI hardening

Status: Complete

- Maintain manifest-driven positive and negative conformance fixtures.
- Isolate structural, identity, kind, authority, and gate failures.
- Test supported Python versions on every push and pull request.
- Build an installable distribution in CI.
- Ensure installed CLI operation does not depend on repository-relative schemas.
- Establish explicit compatibility-claim requirements.

Exit criterion: the reference implementation, packaged CLI, schemas, fixtures,
and documentation are checked reproducibly by local tests and CI.

## Milestone 5: Explainable Policy Engine

Status: Complete

- Define a bounded, declarative v1 policy rule language.
- Ensure policies narrow authority but never grant it.
- Preserve matched and unmatched decisions with rule provenance.
- Enforce denial and human-review effects during resolution.
- Add policy-specific positive and negative conformance fixtures.

Exit criterion: policy evaluation is deterministic, explainable in the IR, and
cannot expand Agent Contract or Task Contract authority.

## Later milestones

- Additional compiler backends.
- Agent Builder authoring workflow.
- Operational validation, monitoring, feedback, and revalidation workflows.

## Milestone 6: Deterministic Quality Gate Evaluation

Status: In progress

- Define a bounded automated evaluator model.
- Preserve manual Gate behavior where no evaluator is declared.
- Apply evaluator results before Execution Record disposition.
- Prove automated evidence presence does not remove human review.
- Add evaluator-specific conformance checks and documentation.

Exit criterion: an automated Gate is deterministic, traceable, bounded to its
declared check, and cannot be interpreted as approval authority.
