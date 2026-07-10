# ADR 0003: Reference implementation and build identity

- Status: Accepted
- Date: 2026-07-10
- Decision owners: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

Milestone 3 requires an executable vertical slice without making the FAF model
dependent on one implementation language or LLM. ADR 0002 leaves the portable
build identifier algorithm open.

## Decision

1. The first reference resolver, semantic validator, and compiler are written in
   Python 3.11 or newer.
2. JSON Schema validation uses a Draft 2020-12 conforming validator and precedes
   semantic resolution.
3. The v1 build identifier is `sha256:` followed by the lowercase SHA-256 digest
   of the resolved IR with `buildId` omitted, serialized as UTF-8 JSON with
   lexicographically sorted object keys, no insignificant whitespace, and
   Unicode characters unescaped where JSON permits.
4. Set-like arrays are sorted during resolution. Procedural arrays retain source
   order. The resolver, not a compiler backend, owns normalization.
5. The first backend emits deterministic generic Markdown text. It is a runtime
   representation and makes no vendor-specific assumptions.
6. Compiler backends validate the IR and may only transform representation;
   they cannot add capabilities, tools, or remove prohibitions and gates.
7. Gate observations are evaluated after execution into a separate Execution
   Record. Passing automated gates does not imply approval when the Agent
   Contract still requires human review.

## Consequences

- The complete source-to-runtime path can be tested now.
- Other languages can implement the same specification without adopting Python.
- Portable build identity is defined for v1 reference outputs.
- Vendor-specific prompt optimization remains a later backend concern.

## Compatibility impact

The illustrative `buildId` in the Milestone 2 fixture is replaced by its
portable digest, and the fixture becomes generated reference output.

## Alternatives considered

- Hash source files directly: rejected because equivalent normalized genomes
  could differ due only to source formatting.
- Make Python objects the IR: rejected because it would violate the portable
  JSON boundary.
- Start with a vendor-specific prompt backend: rejected because it would blur
  the distinction between model-independent semantics and runtime rendering.

## Affected artifacts

- `faf/`
- `tests/test_reference_implementation.py`
- `fixtures/v1/valid/reference/resolved-ir.json`
- Future resolver and compiler conformance implementations
