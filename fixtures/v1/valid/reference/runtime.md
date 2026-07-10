# Fjölnir Resolved Agent Task

Build: `sha256:83916b91fc85104673ab114a4bb5befd542cfd2dab3f198ada91c7dcf20b97ea`

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
