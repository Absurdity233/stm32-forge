import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_server(*requests: dict) -> list[dict]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "mcp") + os.pathsep + env.get("PYTHONPATH", "")
    payload = "".join(json.dumps(item) + "\n" for item in requests)
    proc = subprocess.run(
        [sys.executable, "-m", "cubemx1.mcp_server"],
        cwd=ROOT,
        env=env,
        input=payload,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


def test_tools_resources_and_protocol_errors():
    responses = run_server(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "resources/list", "params": {}},
        {"jsonrpc": "2.0", "id": 4, "method": "resources/read", "params": {"uri": "cubemx1://protocol/mcp"}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "missing", "arguments": {}}},
    )
    assert responses[0]["result"]["serverInfo"]["name"] == "cubemx1"
    assert {tool["name"] for tool in responses[1]["result"]["tools"]} == {
        "cubemx1_ioc_build",
        "cubemx1_ioc_check",
        "cubemx1_ioc_generate",
        "cubemx1_ioc_import",
        "cubemx1_probe_describe",
        "cubemx1_status",
    }
    assert {item["uri"] for item in responses[2]["result"]["resources"]} == {
        "cubemx1://protocol/target",
        "cubemx1://protocol/mcp",
    }
    assert "stdio" in responses[3]["result"]["contents"][0]["text"]
    assert responses[4]["error"]["code"] == -32602


def test_notification_has_no_response():
    responses = run_server({"jsonrpc": "2.0", "method": "notifications/initialized"})
    assert responses == []
