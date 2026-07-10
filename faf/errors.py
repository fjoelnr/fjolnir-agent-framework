from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    pointer: str = ""
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "severity": self.severity,
            "pointer": self.pointer,
            "message": self.message,
        }


class ValidationFailure(Exception):
    def __init__(self, findings: list[Finding]):
        super().__init__("FAF validation failed")
        self.findings = findings
