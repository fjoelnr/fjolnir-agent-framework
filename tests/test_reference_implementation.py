from __future__ import annotations

import json
from copy import deepcopy
from contextlib import redirect_stderr
from io import StringIO
from shutil import copytree
from tempfile import TemporaryDirectory
import unittest
from pathlib import Path

from faf.compiler import compile_generic_text
from faf.backends import compile_openai_responses_request
from faf.catalog import Catalog
from faf.errors import ValidationFailure
from faf.execution import create_execution_record
from faf.policy import evaluate_policies
from faf.resolver import Resolver
from faf.registry import build_registry, scaffold_definition, verify_registry
from faf.schema import SchemaValidator
from faf.cli import main as cli_main

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "fixtures" / "v1" / "valid" / "reference"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ReferenceImplementationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resolver = Resolver.from_paths(REFERENCE, ROOT / "schemas" / "v1")
        cls.genome = load(REFERENCE / "agent-genome.json")
        cls.task = load(REFERENCE / "task-contract.json")

    def test_resolution_is_deterministic(self) -> None:
        first = self.resolver.resolve(self.genome, self.task)
        second = self.resolver.resolve(self.genome, self.task)
        self.assertEqual(first, second)
        self.assertRegex(first["buildId"], r"^sha256:[0-9a-f]{64}$")

    def test_reference_ir_matches_generated_ir(self) -> None:
        self.assertEqual(self.resolver.resolve(self.genome, self.task), load(REFERENCE / "resolved-ir.json"))

    def test_compiler_is_deterministic_and_preserves_build_id(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        first = compile_generic_text(ir)
        self.assertEqual(first, compile_generic_text(ir))
        self.assertIn(ir["buildId"], first)
        self.assertIn("Perform destructive repository operations", first)

    def test_openai_backend_is_deterministic_and_has_no_provider_tools(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        request = compile_openai_responses_request(ir, "test-model")
        self.assertEqual(request, compile_openai_responses_request(ir, "test-model"))
        self.assertEqual(request, load(REFERENCE / "openai-responses-request.json"))
        self.assertNotIn("tools", request)
        self.assertIn("workspace-editor", request["instructions"])
        self.assertIn(ir["task"]["objective"], request["input"])

    def test_openai_backend_requires_explicit_model(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        with self.assertRaises(ValueError):
            compile_openai_responses_request(ir, "  ")

    def test_unauthorized_tool_is_rejected(self) -> None:
        bad_task = load(ROOT / "fixtures" / "v1" / "invalid" / "unauthorized-tool.task-contract.json")
        with self.assertRaises(ValidationFailure) as raised:
            self.resolver.resolve(self.genome, bad_task)
        self.assertIn("FAF-AUTH-TOOL-NOT-ALLOWED", {item.code for item in raised.exception.findings})

    def test_policy_decisions_are_preserved_in_ir(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        decisions = ir["behavior"]["policyDecisions"]
        self.assertEqual(["deny-production-task", "review-moderate-risk"], [item["ruleId"] for item in decisions])
        self.assertFalse(any(item["matched"] for item in decisions))

    def test_policy_requires_review_at_moderate_risk(self) -> None:
        policy = load(REFERENCE / "policy.json")
        decisions = evaluate_policies(
            [policy],
            task_type="documentation-change",
            risk_level="moderate",
            capabilities=[],
            tools=[],
        )
        matched = [item for item in decisions if item.matched]
        self.assertEqual(["review-moderate-risk"], [item.rule_id for item in matched])
        elevated_task = deepcopy(self.task)
        elevated_task["spec"]["riskLevel"] = "moderate"
        ir = self.resolver.resolve(self.genome, elevated_task)
        self.assertIn("Moderate or higher risk requires human review.", ir["authority"]["reviewRequirements"])

    def test_duplicate_policy_rule_id_is_rejected(self) -> None:
        policy = load(REFERENCE / "policy.json")
        policy["spec"]["rules"].append(dict(policy["spec"]["rules"][0]))
        with self.assertRaises(ValidationFailure) as raised:
            evaluate_policies(
                [policy], task_type="documentation-change", risk_level="low",
                capabilities=[], tools=[]
            )
        self.assertIn("FAF-POLICY-DUPLICATE-RULE", {item.code for item in raised.exception.findings})

    def test_execution_record_requires_human_review(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        observations = load(REFERENCE / "execution-observations.json")
        record = create_execution_record(ir, observations)
        self.assertEqual(record, load(REFERENCE / "execution-record.json"))
        self.assertEqual("pending-review", record["status"])
        self.assertTrue(record["humanReviewRequired"])

    def test_missing_gate_result_is_rejected(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        with self.assertRaises(ValidationFailure) as raised:
            create_execution_record(ir, {"outputSummary": "Missing result", "gateResults": []})
        self.assertIn("FAF-GATE-RESULT-MISSING", {item.code for item in raised.exception.findings})

    def test_evidence_set_gate_overrides_unsubstantiated_pass(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        observations = load(REFERENCE / "execution-observations.json")
        observations["gateResults"][0]["status"] = "passed"
        observations["gateResults"][0]["evidence"] = ["Automated validation passed"]
        record = create_execution_record(ir, observations)
        self.assertEqual("failed", record["gateResults"][0]["status"])
        self.assertEqual("blocked", record["status"])

    def test_duplicate_gate_result_is_rejected(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        observations = load(REFERENCE / "execution-observations.json")
        observations["gateResults"].append(dict(observations["gateResults"][0]))
        with self.assertRaises(ValidationFailure) as raised:
            create_execution_record(ir, observations)
        self.assertIn("FAF-GATE-RESULT-DUPLICATE", {item.code for item in raised.exception.findings})


class ConformanceFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.invalid = ROOT / "fixtures" / "v1" / "invalid"
        cls.reference = REFERENCE
        cls.resolver = Resolver.from_paths(REFERENCE, ROOT / "schemas" / "v1")
        cls.genome = load(REFERENCE / "agent-genome.json")
        cls.task = load(REFERENCE / "task-contract.json")
        cls.expectations = load(cls.invalid / "expectations.json")

    def test_declared_invalid_fixtures_produce_exact_error_codes(self) -> None:
        for relative, expectation in self.expectations.items():
            with self.subTest(fixture=relative):
                expected = set(expectation["semanticErrors"])
                with self.assertRaises(ValidationFailure) as raised:
                    if relative.endswith("/"):
                        Catalog.load(self.invalid / relative)
                    elif relative.endswith(".agent-genome.json"):
                        self.resolver.resolve(load(self.invalid / relative), self.task)
                    else:
                        self.resolver.resolve(self.genome, load(self.invalid / relative))
                actual = {finding.code for finding in raised.exception.findings}
                self.assertEqual(expected, actual)

    def test_expectation_manifest_covers_all_negative_inputs(self) -> None:
        declared = set(self.expectations)
        actual = {
            path.relative_to(self.invalid).as_posix()
            for path in self.invalid.glob("*.json")
            if path.name != "expectations.json"
        }
        actual.add("duplicate-identity/")
        self.assertEqual(declared, actual)


class ArtifactRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = ROOT / "schemas" / "v1"

    def test_reference_registry_is_deterministic_and_valid(self) -> None:
        registry = build_registry(REFERENCE, self.schemas)
        self.assertEqual(registry, load(REFERENCE / "faf-registry.json"))
        SchemaValidator(self.schemas).validate(registry)
        self.assertRegex(registry["catalogBuildId"], r"^sha256:[0-9a-f]{64}$")

    def test_registry_detects_drift(self) -> None:
        with TemporaryDirectory() as temporary:
            catalog = Path(temporary) / "catalog"
            copytree(REFERENCE, catalog)
            registry_path = catalog / "faf-registry.json"
            registry_path.write_text(json.dumps(build_registry(catalog, self.schemas)), encoding="utf-8")
            policy = load(catalog / "policy.json")
            policy["metadata"]["name"] = "Changed policy"
            (catalog / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
            with self.assertRaises(ValidationFailure) as raised:
                verify_registry(catalog, registry_path, self.schemas)
            self.assertIn("FAF-REGISTRY-STALE", {item.code for item in raised.exception.findings})

    def test_registry_rejects_duplicate_identity_catalog(self) -> None:
        with self.assertRaises(ValidationFailure) as raised:
            build_registry(ROOT / "fixtures" / "v1" / "invalid" / "duplicate-identity", self.schemas)
        self.assertIn("FAF-REF-DUPLICATE-IDENTITY", {item.code for item in raised.exception.findings})

    def test_scaffolds_are_schema_valid_for_every_definition_kind(self) -> None:
        validator = SchemaValidator(self.schemas)
        for kind in ("Policy", "ReasoningPack", "Capability", "Role", "Domain", "Tool", "QualityGate"):
            with self.subTest(kind=kind):
                artifact = scaffold_definition(kind, f"urn:faf:test:{kind.lower()}", f"{kind} scaffold")
                validator.validate(artifact)
                self.assertEqual("draft", artifact["metadata"]["lifecycle"])

    def test_scaffold_refuses_overwrite_without_force(self) -> None:
        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "policy.json"
            output.write_text("original", encoding="utf-8")
            with redirect_stderr(StringIO()):
                result = cli_main([
                    "scaffold-definition", "--kind", "Policy", "--id", "urn:faf:test:policy",
                    "--name", "Test policy", "--output", str(output),
                ])
            self.assertEqual(2, result)
            self.assertEqual("original", output.read_text(encoding="utf-8"))
            with redirect_stderr(StringIO()):
                result = cli_main([
                    "scaffold-definition", "--kind", "Policy", "--id", "urn:faf:test:policy",
                    "--name", "Test policy", "--output", str(output), "--force",
                ])
            self.assertEqual(0, result)
            SchemaValidator(self.schemas).validate(load(output))


if __name__ == "__main__":
    unittest.main()
