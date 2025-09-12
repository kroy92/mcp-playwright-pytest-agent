from __future__ import annotations
from typing import Any
from playwright_agent.settings import Settings

# Provided by your MCP/agents SDK
from agents.mcp import MCPServerStdio  # type: ignore[import-not-found]

class MCPServerManager:
    """Factory for browser and filesystem MCP servers."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_browser_server(self) -> MCPServerStdio:
        params: dict[str, Any] = {
            "command": "npx",
            "args": [
                "@playwright/mcp@latest",
                "--isolated",
                f"--viewport-size={self.settings.viewport}",
                f"--output-dir={str(self.settings.mcp_isolated_dir)}",
                "--caps=vision,verify",
            ],
        }
        return MCPServerStdio(params=params, client_session_timeout_seconds=120)

    async def get_file_server(self) -> MCPServerStdio:
        params: dict[str, Any] = {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                str(self.settings.mcp_isolated_dir),
                str(self.settings.mcp_output_dir),
            ],
        }
        return MCPServerStdio(params=params)
