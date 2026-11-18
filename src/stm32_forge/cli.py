from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ForgeConfig
from .cube import generate_project
from .ioc import import_ioc, write_ioc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stm32-forge")
    sub = parser.add_subparsers(dest="command", required=True)

    config = sub.add_parser("config")
    config.add_argument("--file", type=Path)
    config.add_argument("--json", action="store_true")

    create = sub.add_parser("ioc-create")
    create.add_argument("--input", required=True, type=Path, help="target JSON")
    create.add_argument("--output", required=True, type=Path, help="IOC output")

    imp = sub.add_parser("ioc-import")
    imp.add_argument("path", type=Path)
    imp.add_argument("--output", type=Path)

    gen = sub.add_parser("generate")
    gen.add_argument("ioc", type=Path)
    gen.add_argument("output", type=Path)
    gen.add_argument("--config", type=Path)
    gen.add_argument("--timeout", type=int, default=300)

    args = parser.parse_args(argv)
    if args.command == "config":
        data = ForgeConfig.load(args.file).to_dict()
        print(json.dumps(data, indent=2))
        return 0
    if args.command == "ioc-create":
        write_ioc(args.output, json.loads(args.input.read_text(encoding="utf-8")))
        print(args.output)
        return 0
    if args.command == "ioc-import":
        data = import_ioc(args.path)
        text = json.dumps(data, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0
    if args.command == "generate":
        result = generate_project(args.ioc, args.output, ForgeConfig.load(args.config), args.timeout)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(result.get("returncode", 1))
    return 2
