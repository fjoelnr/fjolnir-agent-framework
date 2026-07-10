# FAF v1 Agent Genome and IR Specification

## 1. Scope

This document specifies the first machine-readable FAF source model and the
model-independent resolved Intermediate Representation (IR). It refines the
concepts in `ARCHITECTURE.md` and ADRs 0001 and 0002.

The schemas define structural validity. This document also defines semantic
rules that cannot be expressed reliably in JSON Schema alone.

## 2. Artifact classes

FAF v1 defines seven schema boundaries:

- Constitution Artifact: a versioned machine-readable identity and normative
  principle index for the controlling Constitution document.
- Definition Artifact: a Policy, Reasoning Pack, Capability, Role, Domain, Tool,
  or Quality Gate.
- Agent Contract: the durable authority boundary of a concrete agent.
- Task Contract: one assignment within an Agent Contract.
- Agent Genome: the versioned composition and resolution root.
- Resolved IR: normalized compiler input with provenance and no unresolved
  component references.
- Execution Record: post-execution Quality Gate results, disposition, and human
  review state tied to one resolved IR build.

Human-facing templates and prompts are derived or authoring artifacts. They are
not normative machine-readable inputs unless converted into these formats.

## 3. Identity and versioning

Every artifact has:

- `specVersion`: the schema family, currently `1.0`.
- `kind`: the artifact class or definition kind.
- `id`: a globally stable URN beginning with `urn:faf:`.
- `version`: an exact Semantic Versioning 2.0.0 version.
- `name`: a human-readable label.
- Optional descriptive and lifecycle metadata.

Identity is the tuple `(id, version)`. Two documents with that tuple but
different content are a repository integrity error. Renaming does not change
identity; a material semantic change requires a new artifact version.

## 4. References and resolution

An Artifact Reference contains exactly `id` and `version`. A resolver MUST:

1. Load the Agent Genome and selected Task Contract.
2. Resolve every reference by exact identity.
3. Reject missing identities and duplicate identities with different content.
4. Confirm that the resolved artifact kind matches the reference location.
5. Resolve the Agent Contract's allowed definitions and the Genome's selections.
6. Confirm that every selected definition is allowed by the Agent Contract.
7. Apply the authority and conflict rules below.
8. Emit one deterministic resolved IR or a list of validation errors.

Resolution MUST NOT use network discovery implicitly. Registries or catalogs
may supply artifacts, but their use must be explicit execution configuration.

## 5. Authority and conflict rules

The effective authority is an intersection, never a union, of higher- and
lower-precedence permissions:

```text
Constitution and Global Policies
             ∩
        Agent Contract
             ∩
         Task Contract
```

The following are semantic errors:

- A Task Contract requests a capability or tool not allowed by its Agent
  Contract.
- A selected genome component is absent from the Agent Contract's allowed
  component set.
- An action is both allowed and prohibited at the same or a higher precedence.
- A lower layer attempts to weaken a required review, escalation, or quality
  gate.
- A referenced kind does not match its selection slot.
- A required quality gate cannot be resolved or evaluated for its declared
  phase.
- A selected executable Policy denies a task type, capability, or tool fact.

Prohibitions take precedence over permissions. Lower layers may add
prohibitions, constraints, gates, or review requirements.

Executable Policy rules may deny explicit facts or require human review. They
cannot grant authority. Every rule evaluation is retained as a Policy Decision
in the IR with its source and match result; see ADR 0005.

## 6. Composition rules

An Agent Genome selects exactly one Constitution reference, one Agent Contract,
one Role, and one or more Domains. Policies, Reasoning Packs, Capabilities,
Tools, and Quality Gates are selectable collections.

The Agent Contract declares the maximum selectable set. The Genome chooses an
operational subset. A Task Contract may choose a further subset and may add
task-specific constraints and gates, but it cannot expand authority.

Order is meaningful for instructional sequences in Reasoning Packs and for gate
evaluation phases. Lists of references otherwise have set semantics and are
canonicalized by `id`, then `version`.

## 7. Resolved IR

The IR is a derived, immutable compilation input. It contains:

- The IR format version and deterministic build identifier.
- The exact source artifact identities.
- Resolved role, domains, policies, and reasoning procedures.
- Effective capabilities and tool permissions.
- Effective prohibitions and constraints.
- The task objective, inputs, acceptance criteria, and required output.
- Applicable Quality Gate definitions grouped by evaluation phase.
- Lifecycle and human-review requirements.
- Provenance entries mapping resolved sections to source artifacts.

The IR MUST contain no unresolved Definition Artifact, Agent Contract, or Task
Contract references. External task inputs may remain locators when the contract
explicitly treats them as runtime inputs.

Compilers MUST treat the IR as read-only and MUST NOT add authority. Runtime
specific optimization may change representation, not semantics.

Execution Records are derived after runtime work. Every configured gate needs
exactly one result. A passed automated gate does not satisfy an independent
human-review requirement; in that case the record remains `pending-review`.

Quality Gate definitions may declare a deterministic evaluator. v1 supports the
`evidence-set` evaluator, which checks only that configured evidence statements
were supplied. It does not establish their truth or substitute for human
approval; see ADR 0006 and `QUALITY_GATES.md`.

## 8. Determinism and canonicalization

Given identical source artifacts and resolver configuration, resolution MUST
produce semantically identical IR. A canonical implementation:

- Encodes JSON as UTF-8.
- Sorts object keys for hashing.
- Canonicalizes set-like reference arrays by identity.
- Preserves explicitly ordered procedural steps.
- Excludes timestamps from semantic hashes.
- Records the resolver name and version separately from the semantic content.

The v1 `buildId` is an opaque string. A later implementation ADR will define the
mandatory canonical JSON and digest algorithm before build IDs become portable
conformance claims.

## 9. Compatibility

Artifact content versions and schema versions are independent:

- Patch artifact version: editorial or non-semantic clarification.
- Minor artifact version: backward-compatible addition or strengthening.
- Major artifact version: incompatible behavior, authority, required input, or
  output change.
- `specVersion` change: serialization or schema-family change.

Consumers MUST reject unsupported major `specVersion` values. Because v1 uses
exact artifact references, any dependency upgrade is deliberate and reviewable.
Changes to authority, tools, gates, or human oversight require revalidation even
when represented as a compatible artifact-version change.

## 10. Validation errors

Semantic validators emit errors with:

- Stable error code.
- Severity (`error` or `warning`).
- JSON Pointer to the source location where possible.
- Human-readable message.
- Related artifact identities.

Initial error code families are:

- `FAF-REF-*`: resolution and identity failures.
- `FAF-KIND-*`: artifact-kind mismatch.
- `FAF-AUTH-*`: authority expansion or prohibition conflict.
- `FAF-GATE-*`: quality-gate selection or evaluation failure.
- `FAF-COMPAT-*`: unsupported or incompatible versions.
- `FAF-IR-*`: normalization or provenance failure.

## 11. Schema inventory

Normative v1 schemas are under `schemas/v1/`:

- `common.schema.json`
- `constitution.schema.json`
- `definition-artifact.schema.json`
- `agent-contract.schema.json`
- `task-contract.schema.json`
- `agent-genome.schema.json`
- `resolved-ir.schema.json`
- `execution-record.schema.json`

Reference fixtures under `fixtures/v1/` demonstrate structural validity and
semantic failures. Fixtures are informative until a conformance runner is
implemented in Milestone 3.
