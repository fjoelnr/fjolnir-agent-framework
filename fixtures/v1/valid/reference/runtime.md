# Fjölnir Resolved Agent Task

Build: `sha256:8be51b3b56eac9da1d820c29630fd5f74e57de30ffbe06b0c1673064a5980c5d`

## Objective

Update architecture documentation consistently.

## Required output

markdown-report

## Instructions

- Inspect relevant context before changing files
- Report validation evidence
- Preserve unrelated user changes
- Validate changes proportionally to risk

## Policies

- Moderate or higher risk requires human review
- Production deployment is denied

## Matched policy decisions

- None

## Reasoning procedure

- None

## Constraints

- Do not modify implementation files

## Prohibited actions

- Claim approval authority
- Claim final approval authority
- Perform destructive repository operations

## Acceptance criteria

- Local Markdown links resolve
- Documents use canonical terminology

## Escalation conditions

- Requested work exceeds documentation scope

## Granted tools

- `urn:faf:tool:workspace-editor@1.0.0`

## Quality gates

- `urn:faf:gate:scope-and-evidence@1.0.0` (post-execution, failure: block)
