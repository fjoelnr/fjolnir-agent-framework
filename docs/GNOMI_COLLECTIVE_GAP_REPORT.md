# GNOMI Collective: architecture gap report

- Status: Proposal v0.1; documentation only, no implementation approval.
- Date: 2026-10-15.
- Baseline: `0738ae1f4af6fd43d273198a6c63c056b61d4ec4` (`main`).
- Requirements: [FAF-WORKFLOW-001 / #1](https://github.com/fjoelnr/fjolnir-agent-framework/issues/1), [GNOMI-COLLECTIVE-001 / #2](https://github.com/fjoelnr/fjolnir-agent-framework/issues/2).
- Reading scope: README, Constitution, architecture/meta-model, reference implementation,
  conformance, policies, gates, backends, ADRs 0001–0008, `faf/`, v1 contract/IR/record
  schemas, reference/negative fixtures and `tests/test_reference_implementation.py`.

## Findings and safe extension points

The repository is an experimental governance vertical slice, not a running
multi-user agent platform. GNOMI should consume it as an application dependency.
The following are source-inspection findings, not claims of operational assurance.

| Area | Existing evidence | Gap | Proposed owner / extension |
| --- | --- | --- | --- |
| Authority | [Architecture §6](ARCHITECTURE.md), [ADR 0001](adr/0001-freeze-core-architecture-meta-model.md); Constitution > policies > Agent Contract > Task Contract | No authenticated human/tenant principal | GNOMI identity and authorization service; retain precedence |
| Resolution | `faf/resolver.py:Resolver.resolve`, `faf/catalog.py`, `faf/schema.py`; exact versions, schema/kind checks, task/tool/capability narrowing, required gates | No delegated-task lineage or resource ACL checks | Reuse resolver per node; GNOMI binds verified principal and scoped delegation outside v1 artifacts |
| Build identity | Resolver canonical JSON SHA-256, [ADR 0003](adr/0003-reference-implementation-and-build-identity.md), resolved IR fixture | Build ID does not authenticate caller, runtime, approvals or actual tool execution | Separate GNOMI run envelope with FAF build ID, policy revision, payload/evidence hashes and audit references |
| Policy | `faf/policy.py:evaluate_policies`, [Policy Engine](POLICY_ENGINE.md), [ADR 0005](adr/0005-policies-only-narrow-authority.md) | Four fact subjects, deny/review effects only; no tenant/resource/expiry/revocation decisions | Independent GNOMI resource policy enforcement; do not pretend v1 evaluates ACLs |
| Compilation | `faf/compiler.py`, `faf/backends.py:compile_openai_responses_request`, [ADR 0007](adr/0007-runtime-backends-render-but-never-execute-authority.md) | Pure renderers; no model/tool execution, credentials or sandbox | External GNOMI runtime adapters and tool broker with explicit binding; compiler remains pure |
| Workflow | `faf/cli.py` resolves/compiles/records individual tasks; no workflow schema in `schemas/v1/` | DAG scheduling, budgets, cancellation, retry, resume and isolated workers absent | Reusable workflow layer researched under #1; GNOMI contributes use cases, no duplicate scheduler |
| Gates | `faf/gates.py:evaluate_gate_results`, [Quality Gates](QUALITY_GATES.md), [ADR 0006](adr/0006-automated-gates-verify-evidence-not-approval.md) | `evidence-set` checks statement presence, not truth; manual results supplied by caller | Independent Assurance execution plus separate human approval; no self-certification |
| Records | `faf/execution.py:create_execution_record`, `schemas/v1/execution-record.schema.json` | Record lacks authenticated event chain, tenant, runtime, approval receipts, workflow lineage | GNOMI sidecar envelope references unmodified v1 Execution Record; status `accepted` is not a tool-execution permit |
| Registry | `faf/registry.py`, [ADR 0008](adr/0008-derived-registry-and-safe-definition-scaffolds.md) | Derived local index, not identity directory, runtime discovery or secret store | Keep artifact registry; separate agent directory and runtime capability registry |
| Memory | No memory service or MCP client in `faf/`; [MUNIN plan](GNOMI_MUNIN_INTEGRATION_PLAN.md) records direct checks | Retrieval, tenant isolation, provenance, consent and ingest missing | GNOMI memory gateway; current MUNIN remains read-only |
| AEGIR / tools | FAF Tool definitions are descriptive | No verified AEGIR interface or resource permissions in this baseline | Tool broker adapter proposal only; AEGIR unavailable/unverified in this work |
| Conformance | [Conformance](CONFORMANCE.md), negative fixture manifest, reference implementation tests | Covers deterministic artifact semantics, not cross-tenant leakage or runtime containment | Preserve suite; add synthetic application security tests only after implementation approval |

## Boundary with FAF-WORKFLOW-001

Reuse one provider-neutral workflow design: nodes bind exact Agent/Task Contracts,
resolve separately and produce individual records. #1 owns reusable DAG semantics,
worker isolation, concurrency, budgets, retries, recovery and benchmark machinery.
#2 owns personal assistants, tenant identity, consent, memory separation, runtime
portability and administration UX. The tool broker is the shared enforcement seam;
neither issue authorizes making it part of normative FAF v1 without a later ADR.

Issue #1 AP01 and the architecture/ADR portion of #2 are addressed by this proposal.
#1 AP02–AP05 remain research/pilot work: no full workflow schema, benchmark result,
or vendor orchestration validation is claimed. Anthropic Dynamic Workflows,
`ultracode` and JEV have not been verified here and are not architecture dependencies.

## Documentation consistency observations

- README's final status paragraph still describes additional backends and automated
  gate evaluators as future work, while `REFERENCE_IMPLEMENTATION.md`, code and
  accepted ADRs 0006/0007 describe the implemented evidence-set evaluator and
  OpenAI request renderer. This report uses the explicit code/ADRs for those facts;
  maintainers should reconcile the status prose separately.
- `docs/adr/README.md` indexes 0001–0006, while accepted files 0007/0008 also exist.
  They were read and remain part of the baseline. This proposal does not edit
  accepted decisions or silently change that index.

## Priority and decisions needed

| Priority | Decision / missing evidence | Review outcome required |
| --- | --- | --- |
| P0 | Identity issuer, resource policy engine, credential custody and enforcement location | Name a trusted service boundary before any pilot execution |
| P0 | Multi-user memory security | Choose isolated stores/credentials or a service enforcing object ACLs before enabling a second user |
| P0 | Administrative approvals | Decide privileged operation classes, approvers, two-person rules and emergency recovery owner |
| P1 | Shared #1 workflow contract | Agree envelope/event version, global budgets and recovery semantics |
| P1 | Runtime candidates | Pin exact OpenClaw/Hermes/Codex versions and test adapter controls; no winner established |
| P1 | Retention, export, deletion and sharing consent | Approve policies before importing personal memory |
| P2 | AEGIR interface | Supply a scoped sandbox interface and independent authorization tests |

## Review package and exit gate

Read [architecture](GNOMI_COLLECTIVE_ARCHITECTURE.md),
[runtime ADR](adr/0009-gnomi-runtime-independence.md),
[identity ADR](adr/0010-gnomi-identity-and-authorization.md) and
[MUNIN plan](GNOMI_MUNIN_INTEGRATION_PLAN.md).
All decisions remain Proposed. Review must explicitly authorize a later synthetic,
local pilot; merging documentation alone does not authorize implementation,
production access, secrets provisioning or personal-data ingestion.

## Verification performed in this phase

- Existing reference/conformance suite: **20 tests passed** on Python 3.11.15.
  The first attempt had 18 passes and two temporary-directory permission errors
  in the local sandbox. Re-running with TEMP/TMP directed to a writable scratch
  directory passed all 20, without changing source or tests.
- Local Markdown file targets: all checked targets in the five new documents
  resolve. Source inspection and public-content review found only synthetic user
  examples and sanitized MUNIN probe outcomes; no personal memory was copied.
- MUNIN: three successful metadata/read calls, one successful search with no hits,
  and one reachable project-context call returning `project_not_found`; details
  and limits are in the integration plan. No deployed integration tested.
- Runtime adapters, multi-user ACL enforcement, approval services, AEGIR and
  benchmarks: **not implemented or executed**. Proposed tests are future gates.
