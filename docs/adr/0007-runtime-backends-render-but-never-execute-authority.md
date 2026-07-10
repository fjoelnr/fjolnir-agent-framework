# ADR 0007: Runtime backends render but never execute authority

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

FAF's generic compiler proves that a resolved IR can be rendered, but does not
demonstrate a concrete provider request shape. A provider backend must preserve
FAF semantics without translating declared tool references into executable
provider tools or silently applying provider-specific authority.

## Decision

1. Runtime backends are pure renderers from a validated resolved IR to a
   provider request representation. They do not call a provider API.
2. The first provider renderer targets the OpenAI Responses API request shape
   and requires an explicit model identifier.
3. The renderer places stable behavior, constraints, prohibitions, policy
   decisions, review requirements, and Quality Gates in `instructions`.
4. The task objective, inputs, acceptance criteria, output requirement, and
   escalation conditions are placed in `input`.
5. FAF tool references are represented only as informational authority context.
   The renderer MUST NOT emit an OpenAI `tools` field or convert an FAF Tool
   definition into a provider tool declaration.
6. Request execution, credentials, retries, model selection defaults, and
   provider response handling remain outside this milestone.

## Consequences

- The provider boundary is testable without credentials or network execution.
- The backend preserves the model-independent resolver as the authority source.
- Applications may add an execution adapter later, but it must explicitly bind
  provider tools to FAF capability and contract checks.
- The first backend does not claim compatibility with every OpenAI model option.

## Compatibility impact

No changes to source artifacts or IR semantics. The backend output is a derived
representation with its own fixture and tests.

## Alternatives considered

- Send FAF Tool references as provider tools automatically: rejected because it
  would turn descriptive authority into executable access without a binding
  contract.
- Embed provider-specific request fields in the IR: rejected because it would
  compromise model independence.

## Affected artifacts

- `faf/backends.py`
- CLI compiler commands
- OpenAI Responses request fixture and backend tests
- `docs/RUNTIME_BACKENDS.md`
