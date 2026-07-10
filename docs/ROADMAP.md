# FAF Architecture Roadmap

## Status

FAF is transitioning from the Foundation stage to the Meta Model stage. ADR
0001 freezes the core conceptual vocabulary and dependency model. No
machine-readable genome format, IR, compiler, or runtime validator exists yet.

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

## Later milestones

- Additional compiler backends.
- Policy engine and automated quality gates.
- Agent Builder authoring workflow.
- Operational validation, monitoring, feedback, and revalidation workflows.
