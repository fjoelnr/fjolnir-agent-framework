# Invalid v1 Fixtures

Invalid fixtures exercise either structural or semantic rejection. Expected
error codes are declared in `expectations.json`, and the test suite requires the
manifest to cover every negative JSON input.

`unauthorized-tool.task-contract.json` is structurally valid. Its requested tool
is not allowed by the reference Agent Contract and must produce
`FAF-AUTH-TOOL-NOT-ALLOWED`. Expected results are kept outside normative
artifacts in `expectations.json`.

Each fixture is designed to isolate one rule. `duplicate-identity/` is a catalog
fixture rather than a Genome or Task input.
