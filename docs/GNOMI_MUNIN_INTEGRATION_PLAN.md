# GNOMI Collective: MUNIN integration plan and direct probe results

- Status: Proposal v0.1; read-only discovery completed, integration not implemented.
- Date: 2026-10-15.
- Related: [architecture](GNOMI_COLLECTIVE_ARCHITECTURE.md), [gap report](GNOMI_COLLECTIVE_GAP_REPORT.md),
  [identity ADR](adr/0010-gnomi-identity-and-authorization.md), issues #1 AP03 and #2 AP03/AP06.

## 1. Observed surface, not inferred connectivity

Five `mcp__munin__*` tools were exposed in this Codex session and each was directly
called on 2026-10-15. `health` returned service time `2026-10-15T13:58:57.671470+00:00`,
`status=ok`, service `munin-mcp`, version `0.1.0`, vault `MUNIN-General`,
`read_only=true`. This is evidence for this client's access at that time only.
It is not evidence that a GNOMI runtime, another user or a deployed gateway can connect.

| Tool | Actual request | Actual result | What is established |
| --- | --- | --- | --- |
| `health` | `{}` | OK; service/vault/read-only metadata | Service reachable from this session |
| `vault_info` | `{}` | Vault metadata and counts returned; read-only true | Metadata endpoint reachable; private inventory intentionally omitted here |
| `knowledge_read` | `path="00-System/Prompts/Brain-First.md", max_lines=12` | 12 lines returned with path/line/truncation metadata | Bounded Markdown read works; no family material read |
| `knowledge_search` | `query="GNOMI-COLLECTIVE-001", max_results=3` | Zero results; backend `sqlite_fts5` | Search call works; this identifier was not found in the index |
| `project_context` | `project="GNOMI", max_lines_per_file=30` | Structured `project_not_found`, no matches | Tool reachable, but requested project resolution failed |

The not-found results are not treated as proof that no relevant note could exist.
No broader search was performed after the distinctive identifier returned no
results. Only the canonical policy excerpt was read; no whole-vault preload.
Its supporting vault-relative path is `00-System/Prompts/Brain-First.md` lines 1–12.
That private knowledge source is not copied into the public repository.

The exposed signatures are:

| Tool | Arguments offered by current schema |
| --- | --- |
| `health`, `vault_info` | Object; probes used no parameters |
| `knowledge_read` | Required `path`; optional `start_line`, `max_lines` |
| `knowledge_search` | Required `query`; optional `path_prefix`, `max_results` |
| `project_context` | Required `project`; optional `max_lines_per_file` |

No write/ingest/delete tool, principal/tenant selector, grant argument or AEGIR
tool was present on this MUNIN surface. Authentication transport and backend ACL
semantics were not inspected or tested. Lack of an argument does not prove the
backend has no security controls; it means multi-user enforcement is unverified.
No restricted-vault access, denial probe against it, mutation or attachment access
was attempted. No secrets, service addresses, private paths or raw vault inventory
are included in this public report.

## 2. Retrieval design

The proposed path is authenticated principal → task grant → memory gateway →
scoped MUNIN backend → authorized result/provenance → isolated agent context.
Workers receive no direct vault filesystem or unrestricted MCP credentials.

Apply Brain First: use current task context first; then exact project/path;
curated `50-Knowledge` where relevant; then a narrow search with small limit;
read only one to three relevant files. Search hits are candidates, not evidence.
Open the supporting bounded passage before citing it with a vault-relative path.
Do not broaden a distinctive no-hit identifier without a concrete alternative.
Retrieved instructions are untrusted source content and cannot alter authority.

The gateway must authorize every query scope, result, snippet, project-context
file, title and metadata response. Post-filtering model context alone is inadequate:
search counts, ranking and error messages may also leak information. Validate
canonical paths, reject traversal/aliases escaping scope, bound result/line sizes
and normalize errors so unauthorized object existence is not revealed.

Current MUNIN-General access does not implement the proposed personal/family/project/
system partitioning. For a future multi-user pilot choose either independently
scoped stores/credentials, or a backend that checks authenticated object ACLs before
search and read. A single broad service credential plus caller-supplied folder
prefix is insufficient. If the backend cannot enforce these guarantees, remain
single-user with explicitly approved non-sensitive material and block multi-user use.

## 3. Provenance and controlled knowledge promotion

Proposed private evidence entries bind: tenant/resource label, source vault-relative
path, bounded line range, retrieval UTC time, source version/hash if available,
query, tool name, FAF build ID, run ID and applicable policy revision. The current
read response supplies path/line metadata but no authenticated immutable revision.
A future gateway must capture an approved content digest/snapshot reference and
document freshness limitations; a digest establishes identity, not truth.

Keep source text in a scoped private evidence store. Public GitHub documents may
link only approved public sources/commits/PRs; never upload retrieved personal
content, private Execution Records or tokens as review evidence. Public MUNIN probe
reports contain sanitized outcome summaries only, as above.

Writes are a separate future workflow, unavailable through this read-only MCP:

1. Agent prepares a candidate with target namespace, visibility, source paths/
   commits, run/Execution Record references, claims, uncertainty and content hash.
2. An independent reviewer checks source support, permissions and data minimization.
3. Deduplicate within the authorized namespace by stable source identity plus
   content hash; distinguish exact duplicates from updates and related claims.
4. Conflicting claims retain both paths/versions and a contested marker. Follow
   the canonical conflict policy; if unavailable, stop promotion for human review.
   Never silently merge or overwrite a competing claim.
5. A human approves the exact candidate hash and target ACL. A separately authorized
   ingest service performs an idempotent write with expected target revision.
6. Record the outcome privately, including source GitHub commit and Execution
   Record references. Failed/conflicted writes remain pending; no retry overwrite.

No ingest service is built or called here. Existing read-only MUNIN behavior stays
unchanged. Specialist outputs and feedback never become standing memory automatically.

## 4. Concrete staged work and test matrix

| Step | Owner role / prerequisite | Deliverable and acceptance |
| --- | --- | --- |
| M0 — completed | Architecture reviewer; current session | Five direct tool outcomes above; no claim of deployment integration |
| M1 — design approval | Human owner + security reviewer | Decide storage isolation, identity issuer, ACL labels, retention, allowed namespaces and whether read-only pilot is approved |
| M2 — future mock gateway | Engineer after explicit implementation approval | Synthetic tool responses only; schema/size/path validation; provenance contract and deny-by-default broker |
| M3 — future negative tests | Independent Assurance | Two synthetic principals; deny unauthorized search/read/context/metadata, traversal, expired/revoked grants and wrong audience; zero leaked canaries |
| M4 — future adapter test | Engineer + Assurance; one pinned runtime | Discover actual tools; allowed bounded read succeeds through broker; injection does not dispatch tools; failures/timeouts do not become “integrated” |
| M5 — future portability test | Assurance | Export/restore preserves ACLs/provenance; old runtime grants fail; target without controls rejected; caches partitioned/evicted |
| M6 — future ingest design | Human governance approval, separate service | Duplicate/conflict/revision/approval/replay tests with synthetic data; no production writes until separately authorized |

For M3, use dedicated synthetic authorized/unauthorized stores rather than probing
any restricted real vault. Check titles, hit counts, snippets, cache keys, audit
views, exports and specialist outputs as well as document bodies. Require an
auditable denial before backend disclosure, not a model promise of confidentiality.

## 5. Integration acceptance and unresolved questions

Claim a read-only integration only after a named runtime/version connects through
the gateway and passes discovery, allowed read, authorization denial, provenance,
injection, timeout and revocation tests with stored private evidence. Claim
multi-user isolation only after two-principal tests pass. Write integration needs
its own approval, service and evidence. None of these integration claims is made now.

Open: backend authentication and ACL capabilities; deployment/store boundaries;
source revision support and stale-index handling; private audit retention; consent
and deletion semantics; conflict-policy retrieval in a later ingest design; runtime
versions and AEGIR contract. MUNIN reachability is verified; these questions remain.
