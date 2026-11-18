from __future__ import annotations

import json
from pathlib import Path


def read_ioc(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def write_ioc(path: Path, values: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# STM32 Forge generated IOC", "# Edit the target JSON and regenerate this file."]
    for key in sorted(values):
        value = values[key]
        if isinstance(value, bool):
            encoded = "true" if value else "false"
        elif isinstance(value, (dict, list)):
            encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        else:
            encoded = str(value)
        lines.append(f"{key}={encoded}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def import_ioc(path: Path) -> dict[str, object]:
    values = read_ioc(path)
    device = values.get("mcu.Mcu", values.get("Mcu.CPN", ""))
    return {"device": device, "settings": values, "source": str(path)}
