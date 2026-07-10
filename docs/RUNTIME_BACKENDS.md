# FAF Runtime Backends

## Boundary

A Runtime Backend converts a validated resolved IR into a provider-specific
request representation. It does not resolve artifacts, evaluate policy, grant
authority, invoke a provider API, or interpret provider output.

The resolver remains the only component that establishes effective authority.
The Execution Record remains the component that captures post-execution review
and Quality Gate results.

## Generic backend

`compile_generic_text` produces a deterministic Markdown representation for
inspection and fixtures.

## OpenAI Responses request renderer

`compile_openai_responses_request` produces a JSON object for the OpenAI
Responses API. It requires an explicit model identifier and renders:

- `instructions`: agent rules, constraints, prohibitions, policy evidence,
  review requirements, Quality Gates, and informational FAF Tool references.
- `input`: task objective, supplied input descriptions, acceptance criteria,
  output requirement, and escalation conditions.

The renderer deliberately does **not** add an OpenAI `tools` field. An FAF Tool
reference is a governed description, not an automatically executable provider
tool. Any future execution adapter must map provider tools through explicit FAF
capability, contract, and policy checks.

## Use

```text
faf compile-openai \
  --ir resolved-ir.json \
  --model "your-explicit-model-id" \
  --output openai-request.json
```

This command writes a request artifact only. It does not read credentials or
make a network call.

## Provider evidence

The request shape follows the OpenAI Responses API documentation: the API
accepts a model with `instructions` and `input`, and instructions take priority
over input for the request. See [OpenAI text generation guide](https://developers.openai.com/api/docs/guides/text).
