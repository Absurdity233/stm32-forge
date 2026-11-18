from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ForgeConfig:
    cubemx_home: Path | None = None
    firmware_repository: Path | None = None
    cubemx_executable: Path | None = None

    @classmethod
    def load(cls, path: Path | None = None) -> "ForgeConfig":
        path = path or Path(os.environ.get("STM32_FORGE_CONFIG", Path.home() / ".stm32-forge" / "config.json"))
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        detected_executable = _detect_cube_executable()
        executable = _path(data.get("cubemx_executable")) or detected_executable
        home = _path(data.get("cubemx_home")) or (executable.parent if executable else None)
        repository = _path(data.get("firmware_repository") or data.get("repository"))
        if repository is None:
            default_repository = Path.home() / "STM32Cube" / "Repository"
            repository = default_repository if default_repository.is_dir() else None
        return cls(cubemx_home=home, firmware_repository=repository, cubemx_executable=executable)

    def to_dict(self) -> dict[str, str | None]:
        return {"cubemx_home": _str(self.cubemx_home), "firmware_repository": _str(self.firmware_repository), "cubemx_executable": _str(self.cubemx_executable)}


def _detect_cube_executable() -> Path | None:
    candidates = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "STMicroelectronics" / "STM32CubeMX" / "STM32CubeMX.exe",
        Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "Programs" / "STM32CubeMX" / "STM32CubeMX.exe",
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "STMicroelectronics" / "STM32CubeMX" / "STM32CubeMX",
    ]
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def _path(value: str | None) -> Path | None:
    return Path(value).expanduser() if value else None


def _str(value: Path | None) -> str | None:
    return str(value) if value else None
