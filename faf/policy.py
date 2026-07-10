from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .catalog import Artifact, ref
from .errors import Finding, ValidationFailure

RISK_ORDER = {"low": 0, "moderate": 1, "high": 2, "critical": 3}


@dataclass(frozen=True)
class PolicyDecision:
    source: dict[str, str]
    rule_id: str
    effect: str
    subject: str
    value: str
    matched: bool
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "ruleId": self.rule_id,
            "effect": self.effect,
            "subject": self.subject,
            "value": self.value,
            "matched": self.matched,
            "message": self.message,
        }


def _matches(rule: dict[str, Any], facts: dict[str, set[str]]) -> bool:
    subject = rule["subject"]
    value = rule["value"]
    if subject == "risk-level":
        actual = next(iter(facts[subject]))
        return RISK_ORDER[actual] >= RISK_ORDER[value]
    return value in facts[subject]


def evaluate_policies(
    policies: Iterable[Artifact],
    *,
    task_type: str,
    risk_level: str,
    capabilities: Iterable[Artifact],
    tools: Iterable[Artifact],
) -> list[PolicyDecision]:
    facts = {
        "task-type": {task_type},
        "risk-level": {risk_level},
        "capability": {item["id"] for item in capabilities},
        "tool": {item["id"] for item in tools},
    }
    decisions = []
    for policy in sorted(policies, key=lambda item: (item["id"], item["version"])):
        seen_rule_ids: set[str] = set()
        for rule in policy["spec"]["rules"]:
            if rule["id"] in seen_rule_ids:
                raise ValidationFailure([Finding(
                    "FAF-POLICY-DUPLICATE-RULE",
                    f"Policy {policy['id']}@{policy['version']} repeats rule id {rule['id']!r}.",
                    "/spec/rules",
                )])
            seen_rule_ids.add(rule["id"])
            decisions.append(PolicyDecision(
                source=ref(policy),
                rule_id=rule["id"],
                effect=rule["effect"],
                subject=rule["subject"],
                value=rule["value"],
                matched=_matches(rule, facts),
                message=rule["message"],
            ))
    return decisions
