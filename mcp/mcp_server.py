"""Compatibility wrapper for the packaged STM32CubeMX MCP server."""

from cubemx1.mcp_server import *  # noqa: F401,F403
from cubemx1.mcp_server import main


if __name__ == "__main__":
    raise SystemExit(main())
