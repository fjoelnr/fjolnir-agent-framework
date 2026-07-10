# FAF Agent Builder and Artifact Registry

## Scope

The first Builder milestone helps authors create reusable Definition Artifacts
and catalog them safely. It does not compose a complete agent or infer contract
authority.

## Scaffold a reusable definition

```text
faf scaffold-definition \
  --kind Policy \
  --id "urn:faf:policy:example" \
  --name "Example policy" \
  --output artifacts/example-policy.json
```

Supported kinds are `Policy`, `ReasoningPack`, `Capability`, `Role`, `Domain`,
`Tool`, and `QualityGate`. The output is schema-valid and starts in lifecycle
`draft`. It must still be given meaningful statements, rules, procedures, or
gate criteria before operational use.

The command refuses to overwrite an existing output path. Use `--force` only
when replacement is intentional.

## Build a local Registry

```text
faf registry-build \
  --catalog artifacts \
  --output artifacts/faf-registry.json
```

The Registry is a deterministic index containing exact artifact identities,
source paths, metadata, and content digests. It is a review and integrity aid;
it is not a runtime authority source and cannot select an implicit latest
version.

## Verify a Registry

```text
faf registry-verify \
  --catalog artifacts \
  --registry artifacts/faf-registry.json
```

Verification fails when catalog content changes, an indexed artifact is missing,
or the Registry does not match the catalog's canonical index.

## Boundary

Agent Contracts, Task Contracts, and Agent Genomes remain deliberately manual
in this milestone. They require explicit references, authority choices,
prohibited actions, gates, and lifecycle decisions. A later composition Builder
will guide those decisions rather than inventing defaults.
