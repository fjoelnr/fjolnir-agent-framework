# Fjölnir Resolved Agent Task

Build: `sha256:b2eb6ec333f4faa354170dc55c65b8ce3f9e17d770db61c25122375ad0f33ce5`

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
