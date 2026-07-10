# Fjölnir Agent Framework (FAF)
## Founding Principles

Version: 0.1

---

# Purpose

This document preserves the original vision, architectural philosophy, design principles, and long-term goals of the Fjölnir Agent Framework (FAF).

It is intended to preserve project intent across contributors, AI agents, and future maintainers.

The current project mandate is maintained in `PROJECT_CHARTER.md`. The Constitution remains the highest-precedence normative document.

---

# Why FAF Exists

Most current AI systems are controlled through monolithic prompts.

Those prompts mix

- behavior
- reasoning
- role
- domain knowledge
- task
- output format
- safety rules

into a single artifact.

This creates several problems:

- poor maintainability
- difficult reviews
- weak traceability
- limited reuse
- inconsistent behavior
- weak governance

FAF addresses this problem by treating AI agents as engineered systems rather than prompt collections.

---

# Vision

FAF shall become a modular engineering framework for defining, governing, reviewing and evolving professional AI agents.

The framework should be independent of any particular LLM.

Supported runtimes may include

- GPT
- Claude
- Gemini
- Codex
- local LLMs

without changing the conceptual architecture.

---

# Core Philosophy

The project follows one central assumption:

Agent behaviour is an engineering problem.

Therefore agent behaviour should be

- specified
- versioned
- reviewed
- validated
- governed
- continuously improved

using established engineering practices.

---

# Design Principles

The following principles are considered foundational.

## Constitution First

Every agent inherits the Constitution.

Lower layers may extend but never weaken it.

---

## Layered Architecture

Agent behaviour emerges through explicit layers rather than one prompt.

---

## Separation of Concerns

Reasoning

Role

Domain

Capabilities

Policies

Contracts

Quality Gates

must remain independently reviewable.

---

## Human Accountability

Agents assist humans.

Agents do not replace accountable decision makers.

---

## Explainability

Every important decision should be reconstructable.

---

## Traceability

Outputs should be traceable back to

- evidence
- assumptions
- reasoning
- contracts

---

# Conceptual Architecture

The current architecture consists of:

Constitution

↓

Global Policies

↓

Reasoning Packs

↓

Capability Layer

↓

Roles

↓

Domains

↓

Tools

↓

Agent Contract

↓

Task Contract

↓

Agent Genome

↓

Execution

↓

Quality Gates

↓

Feedback

This sequence is a conceptual inventory, not a strict dependency or execution
order. Roles, Domains, Reasoning Packs, Capabilities, Tools, and Quality Gates
are reusable definition artifacts selected by contracts. The canonical
dependency, precedence, and build model is defined in `ARCHITECTURE.md` and ADR
0001.

---

# Important Discovery

During project discussions an important insight emerged.

FAF is NOT primarily a prompt framework.

FAF is an architecture for professional AI agents.

Prompts are merely one possible runtime representation.

---

# Future Architecture

The project is expected to evolve toward:

Agent Genome

↓

Intermediate Representation (IR)

↓

Prompt Compiler

↓

Runtime Prompt

↓

Execution

The IR is expected to become model-independent.

Compiler backends may generate prompts optimized for

- GPT

- Claude

- Gemini

- Codex

or future runtimes.

---

# Long-Term Goal

FAF should eventually provide:

- Constitution Framework
- Policy Engine
- Agent Genome
- Prompt Compiler
- Runtime Validation
- Quality Gates
- Agent Builder
- Governance Framework

forming a complete ecosystem for governed AI agents.

---

# Development Methodology

The project follows an architecture-first approach.

Architecture precedes implementation.

The expected order is:

Foundation

↓

Meta Model

↓

Reference Models

↓

Reference Implementations

↓

Production Use

---

# Architecture Governance

Architecture changes require Architecture Decision Records (ADRs).

Constitution changes require exceptional care.

All major architectural decisions should remain traceable.

---

# Working Style

Contributors should think like software architects rather than prompt engineers.

The preferred mindset is:

- systems thinking

- engineering discipline

- explicit assumptions

- modularity

- reviewability

- maintainability

- proportional rigor

---

# Immediate Next Goals

1. Freeze architecture. (Completed by ADR 0001.)

2. Introduce ADRs. (Completed.)

3. Define the Agent Genome.

4. Define the Intermediate Representation.

5. Define Reasoning Packs.

6. Define Agent Contracts.

7. Build the Prompt Compiler.

---

# Success Criteria

The project succeeds if a professional AI agent can be completely specified, reviewed, versioned, reproduced and evolved without relying on opaque monolithic prompts.

---

End of Charter.
