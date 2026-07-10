# FAF v1 Reference Package

This directory is a minimal, internally consistent source package and its
illustrative resolved IR. It models a bounded software-engineering agent
performing a documentation task.

All source references resolve by exact `(id, version)`. The selected capability,
tool, domain, task type, and quality gate are allowed by the Agent Contract.
`resolved-ir.json` is illustrative output; Milestone 3 will generate it through
the reference resolver rather than maintaining it manually. `runtime.md` is the
generic compiler output. The observations and Execution Record demonstrate that
passing an automated gate still leaves the result pending when human review is
required by the Agent Contract.
