from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compiler import compile_generic_text
from .errors import ValidationFailure
from .execution import create_execution_record
from .resolver import Resolver


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="faf")
    parser.add_argument("--schemas", type=Path, default=Path("schemas/v1"))
    sub = parser.add_subparsers(dest="command", required=True)
    resolve = sub.add_parser("resolve")
    resolve.add_argument("--catalog", type=Path, required=True)
    resolve.add_argument("--genome", type=Path, required=True)
    resolve.add_argument("--task", type=Path, required=True)
    resolve.add_argument("--output", type=Path)
    compile_cmd = sub.add_parser("compile")
    compile_cmd.add_argument("--ir", type=Path, required=True)
    compile_cmd.add_argument("--output", type=Path)
    record = sub.add_parser("record")
    record.add_argument("--ir", type=Path, required=True)
    record.add_argument("--observations", type=Path, required=True)
    record.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "resolve":
            resolver = Resolver.from_paths(args.catalog, args.schemas)
            result = resolver.resolve(_load(args.genome), _load(args.task))
            rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        elif args.command == "compile":
            result = _load(args.ir)
            from .schema import SchemaValidator
            SchemaValidator(args.schemas).validate(result)
            rendered = compile_generic_text(result)
        else:
            from .schema import SchemaValidator
            validator = SchemaValidator(args.schemas)
            ir = _load(args.ir)
            validator.validate(ir)
            result = create_execution_record(ir, _load(args.observations))
            validator.validate(result)
            rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        else:
            sys.stdout.write(rendered)
        return 0
    except (ValidationFailure, json.JSONDecodeError, OSError) as error:
        if isinstance(error, ValidationFailure):
            payload = {"valid": False, "findings": [item.as_dict() for item in error.findings]}
        else:
            payload = {"valid": False, "findings": [{"code": "FAF-INPUT-ERROR", "severity": "error", "pointer": "", "message": str(error)}]}
        sys.stderr.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 2
