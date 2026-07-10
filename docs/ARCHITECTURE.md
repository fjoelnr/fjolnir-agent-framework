# FAF Architecture

## 1. Purpose

This document defines the architectural meta-model of the Fjölnir Agent Framework (FAF).

FAF is a layered architecture for specifying, composing, reviewing, and operating professional AI agents. It is not a collection of prompts. Prompts are generated or assembled artifacts derived from a governed set of architectural elements.

The architecture provides a reference model for how agent behavior, policies, capabilities, domains, tools, contracts, execution rules, and quality gates relate to each other.

This document and accepted Architecture Decision Records define the current architecture baseline. The Constitution remains the higher-precedence normative artifact.

## 2. Design Goals

The architecture is designed to support:

- Traceable agent configuration.
- Separation of stable rules from task-specific instructions.
- Reuse of roles, domains, policies, and quality gates.
- Independent review of agent-defining elements.
- Controlled extension without rewriting the Constitution.
- Compatibility between human governance and runtime validation.
- Clear distinction between agent specification, prompt assembly, and execution.

## 3. Architectural Principles

FAF uses the following architectural principles:

- Constitution first: baseline behavior is defined by the Constitution and cannot be weakened by lower layers.
- Layered composition: agent behavior is composed from explicit layers with defined responsibilities.
- Local specificity: task-specific instructions belong in contracts, not in global constitutional text.
- Minimal coupling: reusable layers should avoid dependencies on concrete tasks or tools unless required.
- Reviewability: each layer should be inspectable as an independent artifact.
- Versionability: each stable layer should support change tracking and compatibility review.
- Runtime accountability: execution behavior should be tied back to the Agent Contract and Task Contract.

## 4. Layer Model

FAF defines the following layers.

### Constitution

The Constitution defines the non-negotiable baseline for FAF agents. It specifies core principles, evidence handling, communication rules, safety boundaries, human oversight, lifecycle expectations, and governance requirements.

The Constitution MUST remain independent of specific tools, tasks, models, and domains.

### Global Policies

Global Policies define framework-wide constraints that apply across agents and domains. They may include security policy, data handling policy, escalation policy, logging expectations, or organizational constraints.

Global Policies may refine the Constitution for an organization or deployment context, but they MUST NOT weaken constitutional requirements.

### Reasoning Packs

Reasoning Packs define reusable reasoning procedures for recurring classes of work. Examples include decision analysis, root-cause analysis, evidence review, risk assessment, research synthesis, or code review.

Reasoning Packs SHOULD specify inputs, reasoning structure, output expectations, and review checks. They MUST NOT hide unsupported assumptions or create authority beyond the Agent Contract.

### Capability Layer

The Capability Layer defines what an agent is allowed to do. Capabilities may include reading documents, editing files, invoking tools, running tests, producing reviews, drafting reports, or preparing decision records.

Capabilities MUST be explicit. The absence of a prohibited action is not sufficient authorization.

### Roles

Roles define the standing responsibility of an agent. A role describes purpose, expected behavior, scope boundaries, and accountability assumptions.

Examples include Research Agent, Aerospace Review Agent, Software Engineering Agent, and Assurance Review Agent.

Roles SHOULD be reusable across tasks and SHOULD avoid embedding task-specific instructions.

### Domains

Domains define subject-matter constraints and review expectations. A domain may correspond to aerospace, AI assurance, software engineering, research, governance, safety analysis, or another controlled context.

Domain rules MAY add stricter terminology, evidence requirements, review criteria, and escalation conditions.

Domain is the canonical architectural term. Existing Operating Modes are Domain Profiles: selectable domain-specific packages that may combine terminology, reasoning guidance, review criteria, escalation triggers, output formats, and quality gates. They are not a separate authority layer.

### Tools

Tools define external capabilities available to an agent at execution time. A tool may read files, query a repository, run tests, create documents, inspect web sources, or interact with an external system.

Tool access MUST be governed by explicit permissions, expected use, and safety constraints. Tool results should be treated as evidence, not as unquestioned truth.

### Agent Contracts

An Agent Contract binds together the long-lived definition of a concrete agent. It describes purpose, role, domain, capabilities, allowed tools, prohibited actions, output formats, review requirements, and lifecycle state.

The Agent Contract is the primary governance artifact for deciding whether an agent is fit for a class of work.

### Task Contracts

A Task Contract defines a specific assignment for an agent. It describes objective, context, inputs, constraints, acceptance criteria, risk level, required output, and escalation conditions.

Task Contracts MUST remain within the authority granted by the Agent Contract.

### Quality Gates

Quality Gates define checks that must be considered before an output is accepted or forwarded. They may include evidence separation, logical consistency, scope compliance, assumption visibility, risk visibility, output completeness, or required human review.

Quality Gates may be manual, checklist-based, tool-assisted, or automated.

A Quality Gate definition is a versioned rule selected by an Agent Genome or Task Contract. A Quality Gate result is runtime or validation evidence recording applicability, status, findings, and required follow-up. Definitions and results MUST remain distinguishable.

### Execution

Execution is the runtime application of an Agent Contract to a Task Contract under the active policies, tools, domains, reasoning packs, and quality gates.

Execution outputs should preserve traceability to the relevant contract, inputs, assumptions, tool results, and review status.

### Feedback & Continuous Improvement

Feedback & Continuous Improvement captures review findings, incidents, user corrections, validation results, and operational lessons.

Feedback may lead to changes in policies, roles, domains, reasoning packs, quality gates, task templates, or agent contracts. Changes to the Constitution require governance review.

## 5. Agent Genome

An Agent Genome is the modular composition of all elements that define an agent.

A genome may include:

- Constitution version.
- Global Policies.
- Reasoning Packs.
- Capability definitions.
- Role.
- Domain.
- Tool permissions.
- Agent Contract.
- Supported Task Contract types.
- Output formats.
- Quality Gates.
- Lifecycle state.

The Agent Genome is the complete specification required to understand, review, reproduce, or evolve an agent.

Agent Genome is the canonical term for the complete composition. Capability Profile is a deprecated compatibility term for earlier or incomplete genome-shaped compositions and SHOULD NOT be used in new architecture artifacts.

Agent Genomes are preferable to monolithic prompts because they separate stable rules from variable task instructions. A monolithic prompt tends to mix constitution, policy, role, tool usage, task context, output format, and review criteria into a single artifact. That makes review, reuse, versioning, and controlled change difficult.

By contrast, a genome allows teams to update a role, add a quality gate, change a tool permission, or revise a task contract without rewriting the entire agent definition.

## 6. Layer Dependencies, Precedence, and Build Model

Layer dependencies define which elements may refer to or depend on other elements.

The Constitution MUST remain independent of all lower layers. It may define constraints on lower layers, but it must not depend on a specific role, domain, tool, or task.

Global Policies may depend on the Constitution and organizational context. They should not depend on individual Task Contracts.

Reasoning Packs may depend on the Constitution and Global Policies. They may be specialized by domain, but generic reasoning packs should remain tool-independent where possible.

Capabilities may depend on Global Policies and tool availability. They should not depend on a single task unless defined as task-specific capabilities.

Roles may depend on the Constitution, Global Policies, and Capability Layer. They should not depend on concrete Task Contracts.

Domains may depend on the Constitution and Global Policies. They may define constraints for Roles, Reasoning Packs, Quality Gates, and Task Contracts.

Tools may depend on the Capability Layer and Global Policies. Tools must not define constitutional behavior.

Agent Contracts may depend on all stable definition layers: Constitution, Global Policies, Reasoning Packs, Capabilities, Roles, Domains, Tools, and Quality Gates.

Task Contracts may depend on the Agent Contract and may select applicable reasoning packs, output formats, and quality gates within that contract.

Quality Gates may depend on the Constitution, Global Policies, Domains, Agent Contracts, and Task Contracts. They should be explicit about what they check.

Execution depends on all selected layers. It must not introduce hidden authority beyond the Agent Contract and Task Contract.

Feedback may affect any evolvable layer, subject to governance rules.

These dependencies form a graph, not a strict top-to-bottom execution sequence. Roles, Domains, Reasoning Packs, Capabilities, Tools, and Quality Gates are reusable definitions selected and constrained by contracts.

Normative precedence is:

1. Constitution.
2. Global Policies.
3. Agent Contract.
4. Task Contract.

A lower-precedence artifact MAY narrow behavior but MUST NOT weaken a higher-precedence requirement or grant authority that a higher layer prohibits or does not grant. A material unresolved conflict is a validation error.

The canonical build model is:

```text
Versioned source artifacts
        ↓ resolve and validate
Resolved Agent Genome + Task Contract
        ↓ normalize
Intermediate Representation (IR)
        ↓ compile for target runtime
Runtime representation
        ↓ execute and evaluate
Execution record + Quality Gate results + Feedback
```

The IR and runtime representation are derived artifacts. They MUST preserve provenance to their source versions and MUST NOT introduce authority absent from the resolved contracts.

## 7. Extensibility

FAF is designed for extension without modifying the Constitution.

New Roles may be added by defining purpose, scope, capabilities, prohibited actions, expected outputs, and review requirements.

New Domains may be added by defining domain-specific terminology, evidence requirements, risks, escalation triggers, and quality gates.

New Reasoning Packs may be added by defining a reusable reasoning structure, required inputs, expected outputs, and validation checks.

New Quality Gates may be added by defining the checked condition, applicability, pass criteria, failure handling, and evidence requirements.

Extensions MUST remain compatible with the Constitution. If an extension requires weaker safety boundaries, weaker evidence handling, or reduced human accountability, it is not a valid extension under FAF.

## 8. Governance

FAF architecture artifacts should be versioned. Versioning may apply to the Constitution, policies, roles, domains, reasoning packs, agent contracts, task contract templates, and quality gates.

Material architectural decisions SHOULD be recorded in Architecture Decision Records (ADRs) or an equivalent decision record format.

Accepted ADRs define the architecture baseline alongside this document. New decisions follow the process in `docs/adr/README.md`. If an ADR and this document diverge, the newer accepted decision governs until the architecture document is reconciled; neither may override the Constitution.

Backward compatibility should be evaluated when changes affect existing Agent Genomes, Agent Contracts, Task Contracts, output formats, tool permissions, or quality gates.

Review is required before production use of:

- New or materially changed Agent Contracts.
- New or materially changed Domains.
- New tool permissions with operational impact.
- Quality Gates used for assurance, compliance, safety, or release decisions.
- Changes that affect escalation, authority, or human oversight.

Revalidation is required when changes alter the behavior, evidence model, execution context, tool access, or review criteria of an operational agent.

## 9. Future Directions

Future FAF architecture work may include:

- Prompt Compiler: a component that assembles prompts from Agent Genomes, Task Contracts, and active policies.
- Agent Builder: an authoring workflow for creating roles, domains, contracts, and capability profiles.
- Policy Engine: a rule evaluation layer for enforcing global policies and safety boundaries.
- Runtime Validation: execution-time checks against the Agent Contract, Task Contract, and active Quality Gates.
- Automated Quality Gates: machine-checkable validation for consistency, required sections, evidence separation, escalation triggers, and output format compliance.

These components should preserve the layered model. They should make agent configuration more inspectable, not more opaque.
