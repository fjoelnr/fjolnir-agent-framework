from __future__ import annotations

import json
import unittest
from pathlib import Path

from faf.compiler import compile_generic_text
from faf.errors import ValidationFailure
from faf.execution import create_execution_record
from faf.resolver import Resolver

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

    def test_unauthorized_tool_is_rejected(self) -> None:
        bad_task = load(ROOT / "fixtures" / "v1" / "invalid" / "unauthorized-tool.task-contract.json")
        with self.assertRaises(ValidationFailure) as raised:
            self.resolver.resolve(self.genome, bad_task)
        self.assertIn("FAF-AUTH-TOOL-NOT-ALLOWED", {item.code for item in raised.exception.findings})

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

    def test_duplicate_gate_result_is_rejected(self) -> None:
        ir = self.resolver.resolve(self.genome, self.task)
        observations = load(REFERENCE / "execution-observations.json")
        observations["gateResults"].append(dict(observations["gateResults"][0]))
        with self.assertRaises(ValidationFailure) as raised:
            create_execution_record(ir, observations)
        self.assertIn("FAF-GATE-RESULT-DUPLICATE", {item.code for item in raised.exception.findings})


if __name__ == "__main__":
    unittest.main()
