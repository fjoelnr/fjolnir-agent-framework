# FAF v1 Schemas

These JSON Schema Draft 2020-12 documents are the normative structural schemas
for FAF v1 machine-readable artifacts.

Schema validation establishes document shape only. Implementations must also
apply the resolution, authority, conflict, provenance, and compatibility rules
in `docs/META_MODEL.md`.

The canonical media type is `application/json` encoded as UTF-8. Schemas reject
unknown properties. Schema `$id` values are stable identifiers; they do not
require network access and should be registered in a validator's local schema
registry.

The schemas intentionally do not fetch remote references. Register every file
in this directory by its `$id` before validation.

See `docs/META_MODEL.md` for semantic rules and `fixtures/v1/` for positive and
negative examples.

`execution-record.schema.json` validates post-execution gate results and review
state. Execution observations are runtime input rather than governed definition
artifacts.
