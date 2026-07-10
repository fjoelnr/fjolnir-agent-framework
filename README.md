# Fjölnir Agent Framework (FAF)

**Fjölnir Agent Framework (FAF) – A Modular Constitution Framework for Trustworthy AI Agents**

## Vision

FAF defines a structured foundation for professional AI agents that must operate under explicit rules, traceable decisions, and reviewable outputs. The framework treats agent behavior as an engineering and governance concern, not as an informal prompt-writing exercise.

The long-term vision is a reusable constitution framework for agents used in technical, regulated, safety-relevant, or assurance-heavy environments.

## Goals

- Define stable operating principles for professional agents.
- Separate constitution, role, operating mode, task briefing, and review criteria.
- Support traceability from task input to output and follow-up decision.
- Provide reusable templates for repeatable agent configuration.
- Make uncertainty, assumptions, risks, and evidence visible.
- Establish a basis for engineering review and governance review.

## Architecture

The current repository exposes four practical groups:

- Constitution: baseline behavioral rules for all agents.
- Domain Profiles (currently named Modes): domain-specific operating rules for contexts such as aerospace, AI assurance, software engineering, and research.
- Templates: reusable structures for system prompts, roles, task briefings, and reviews.
- Checks: lightweight review artifacts for prompt quality and consistency.

These groups are the current documentation surface, not the complete architectural meta-model. The normative model also defines policies, reasoning packs, capabilities, roles, tools, Agent and Task Contracts, Agent Genomes, execution, quality gates, and feedback. See `docs/ARCHITECTURE.md` and accepted records under `docs/adr/`.

The repository currently mirrors the practical groups:

```text
docs/       Constitution, operating modes, writing rules, decision logic, and prompt patterns
templates/  Reusable prompt, role, task, and review skeletons
examples/   Example agent configurations
tests/      Checklist-based quality and consistency reviews
schemas/    Normative JSON Schemas for machine-readable FAF artifacts
fixtures/   Positive and negative conformance examples
faf/        Executable reference resolver, validator, and compiler
```

## Reference Implementation

FAF includes an experimental Python reference implementation for resolving an
Agent Genome and Task Contract into a deterministic IR, compiling a generic
runtime representation, and recording Quality Gate results. See
`docs/REFERENCE_IMPLEMENTATION.md` for installation, commands, and boundaries.
Conformance requirements and the negative-fixture matrix are documented in
`docs/CONFORMANCE.md`.
The bounded executable rule language is documented in `docs/POLICY_ENGINE.md`.
Quality-Gate semantics and automated evaluator boundaries are documented in
`docs/QUALITY_GATES.md`.

## Design Principles

- Explicit scope before autonomous action.
- Evidence and assumptions separated from recommendations.
- Traceable outputs instead of opaque conclusions.
- Conservative wording for compliance, safety, and assurance claims.
- Modular documents that can be reviewed and versioned independently.
- Clear escalation when authority, evidence, or risk boundaries are exceeded.

## Planned Modules

- Core constitution for baseline agent behavior.
- Writing guide for clear and reviewable agent output.
- Aerospace mode for safety- and compliance-sensitive engineering work.
- AI assurance mode for trustworthy AI evaluation and governance.
- Software engineering mode for repository-based implementation and review.
- Research mode for evidence-based technical research.
- Decision framework for structured option evaluation.
- Prompt patterns for reusable agent configuration.

## Roadmap

### Phase 1: Foundation

- Establish repository structure.
- Define initial constitution and operating modes.
- Provide first templates and examples.
- Add basic quality and consistency checklists.

### Phase 1.5: Architecture Baseline

- Freeze the core vocabulary, dependencies, and precedence rules.
- Record material architecture decisions through ADRs.
- Align foundation documents with the Agent Genome model.

### Phase 2: Reviewability

- Add criteria for severity, confidence, and escalation.
- Expand examples with realistic task briefings.
- Introduce versioning rules for agent constitutions and modes.

### Phase 3: Assurance Use

- Map framework artifacts to assurance evidence.
- Add governance workflows for approval and revalidation.
- Define practical review gates for high-impact agent use.

## Status

Reference Implementation stage. The architecture baseline, machine-readable schemas, deterministic resolver, semantic validator, bounded Policy Engine, generic compiler backend, and Execution Record flow are implemented as an experimental vertical slice. Additional backends, automated gate evaluators, operational validation, and governance workflows remain future work. The framework is not yet a complete assurance method or compliance standard.
