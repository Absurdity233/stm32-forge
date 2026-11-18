import json
import subprocess
import sys


def test_mcp_initialize():
    proc = subprocess.run([sys.executable, "-m", "stm32_forge.mcp"], input=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n", text=True, capture_output=True)
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["result"]["serverInfo"]["name"] == "stm32-forge"
