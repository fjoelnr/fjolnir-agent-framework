# ADR 0010: Separate personal identity, delegation and privileged approval

- Status: Proposed
- Date: 2026-10-15
- Decision owners: Project maintainers and GNOMI application owner
- Supersedes: None
- Superseded by: None
- Scope: GNOMI application proposal

## Context

[Issue #2](https://github.com/fjoelnr/fjolnir-agent-framework/issues/2) combines
private primary assistants, shared specialists and Gnomi as administrative contact.
This must not imply that Gnomi can read every user's memory or approve its own
privileged changes. FAF contracts narrow capabilities/tools; the v1 policy engine
has no authenticated tenant, object ACL, credential lease or revocation mechanism.
Directories and instructions alone cannot enforce data isolation.

## Decision

Propose independent authenticated human principals, tenant IDs, agent IDs and
temporary runtime/run IDs. Share specialist definitions, never mutable live
sessions. All tool/memory operations pass a trusted broker and resource service
that enforce current object ACLs and task-scoped grants server-side.

Effective rights intersect human rights, agent/task contracts, parent delegation,
resource policy and supported runtime controls. Denials prevail, absent authority
denies, and delegation cannot widen scope. Grants bind recipient, purpose, resource,
action, audience/run, expiry and policy revision. Recheck before dispatch and
returning results; revocation stops future access and invalidates controlled caches.

Private memory belongs to its human principal. Family/project sharing requires
explicit consent and ACL changes. Gnomi's administrative role conveys no blanket
private-memory read permission. Infrastructure access is separately governed.

Gnomi prepares proposals; an independent service authenticates human approval;
a separate executor verifies a payload-hash/revision/expiry-bound receipt and
current policy. Gnomi and specialists cannot self-approve. Define two distinct
human approvers for selected high-impact operations before enabling those classes.
Emergency revoke must work independently of Gnomi and the runtime.

## Consequences

Benefits: explicit ownership, bounded delegation, auditable changes and no
authority expansion through runtime migration or shared specialists.
Costs: identity lifecycle, grant storage, object labels, consent UX, cache eviction
and recovery processes. Already disclosed data cannot be recalled after revocation.
Issuer/broker compromise remains a significant risk; separate service boundaries
and least-privilege credentials need deployment review and tests.

## Compatibility impact

No mutation of accepted FAF policies/ADRs or schemas. Resource authorization is a
GNOMI application responsibility alongside FAF's contract validation. Existing
Execution Records remain unchanged and are linked from private application audit
envelopes. `accepted` record status never substitutes for privileged approval.

## Alternatives considered

- One family-wide assistant/session and token: rejected for cross-user leakage
  and lack of attributable delegated authority.
- Folder-based memory partitioning: usable organization, rejected as sole ACL.
- Gnomi as privileged approver/executor: convenient, rejected for self-approval
  and concentration of proposal and execution authority.
- Encode ACLs in current FAF policy prose: rejected as unenforced; a future
  core policy extension requires its own schema/ADR/conformance review.

## Affected artifacts

- GNOMI identity directory, future grants/approval schema and tool/memory gateways.
- [Architecture flows and threat model](../GNOMI_COLLECTIVE_ARCHITECTURE.md).
- [MUNIN integration plan](../GNOMI_MUNIN_INTEGRATION_PLAN.md).

## Review and acceptance conditions

Decide identity issuer, credential custody, storage isolation, privileged operation
classes, approvers, retention/deletion and recovery. Later synthetic tests must
deny cross-tenant delegation, forged/replayed approvals and stale/revoked grants,
and prove shared-specialist context isolation. No such operational enforcement
has been tested in this documentation phase. Proposed; no implementation approval.
