from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

from .config import ForgeConfig


def run_cube(command: list[str], cwd: Path | None = None, timeout: int = 300) -> dict[str, object]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=os.environ.copy())
    return {"command": command, "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}


def generate_project(ioc: Path, output: Path, cfg: ForgeConfig, timeout: int = 300) -> dict[str, object]:
    executable = cfg.cubemx_executable
    if executable is None and cfg.cubemx_home:
        candidates = [cfg.cubemx_home / "STM32CubeMX.exe", cfg.cubemx_home / "STM32CubeMX"]
        executable = next((candidate for candidate in candidates if candidate.exists()), candidates[0])
    if executable is None:
        return {"returncode": 2, "error": "CubeMX executable is not configured", "hint": "set cubemx_executable in ~/.stm32-forge/config.json"}
    output.mkdir(parents=True, exist_ok=True)
    # CubeMX CLI syntax differs between releases; keep the command explicit and inspectable.
    command = [str(executable), "-q", str(ioc), "-o", str(output)]
    return run_cube(command, cwd=output, timeout=timeout)


def split_command(value: str) -> list[str]:
    return shlex.split(value, posix=False)
