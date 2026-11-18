from __future__ import annotations

import json
import sys
from pathlib import Path

from .config import ForgeConfig
from .cube import generate_project
from .ioc import import_ioc, write_ioc

TOOLS = [
    {"name": "ioc_create", "description": "Create an IOC file from target configuration JSON", "inputSchema": {"type": "object", "properties": {"input": {"type": "string"}, "output": {"type": "string"}}, "required": ["input", "output"]}},
    {"name": "ioc_import", "description": "Read an IOC file into structured JSON", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "cube_generate", "description": "Run STM32CubeMX in command-line mode", "inputSchema": {"type": "object", "properties": {"ioc": {"type": "string"}, "output": {"type": "string"}, "config": {"type": "string"}}, "required": ["ioc", "output"]}},
]


def reply(request_id, result=None, error=None):
    message = {"jsonrpc": "2.0", "id": request_id}
    message["error" if error else "result"] = error or result
    sys.stdout.write(json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def handle(request: dict) -> None:
    method = request.get("method")
    rid = request.get("id")
    if method == "initialize":
        reply(rid, {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "stm32-forge", "version": "0.1.0"}})
    elif method == "notifications/initialized":
        return
    elif method == "tools/list":
        reply(rid, {"tools": TOOLS})
    elif method == "tools/call":
        args = request.get("params", {}).get("arguments", {})
        name = request.get("params", {}).get("name")
        if name == "ioc_create":
            write_ioc(Path(args["output"]), json.loads(Path(args["input"]).read_text(encoding="utf-8")))
            value = {"output": args["output"]}
        elif name == "ioc_import":
            value = import_ioc(Path(args["path"]))
        elif name == "cube_generate":
            value = generate_project(Path(args["ioc"]), Path(args["output"]), ForgeConfig.load(Path(args["config"]) if args.get("config") else None))
        else:
            reply(rid, error={"code": -32601, "message": f"Unknown tool: {name}"})
            return
        reply(rid, {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, indent=2)}]})
    else:
        reply(rid, error={"code": -32601, "message": f"Unknown method: {method}"})


def main() -> int:
    for line in sys.stdin:
        if line.strip():
            try:
                handle(json.loads(line))
            except Exception as exc:
                reply(None, error={"code": -32000, "message": str(exc)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
