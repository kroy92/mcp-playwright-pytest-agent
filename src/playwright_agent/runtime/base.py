from __future__ import annotations
import asyncio
from pathlib import Path
from playwright_agent.settings import get_settings, Settings
from playwright_agent.integrations.mcp_servers import MCPServerManager
from playwright_agent.runtime.runner import AgentRunner


def _load_instructions(path: Path | None) -> str:
    if path is None:
        path = Path(__file__).with_suffix("").parent / "prompts" / "generic_instructions.md"
    return path.read_text(encoding="utf-8")


class BaseFlowRunner:
    """Pytest-facing base class to run human-readable web flows through MCP Playwright Agent."""

    def __init__(self, instructions_path: Path | None = None):
        self.settings: Settings = get_settings()
        self.server_manager = MCPServerManager(self.settings)
        self.instructions = _load_instructions(instructions_path)

    async def _run_agent_flow(self, user_steps: str, output_schema, tools:list =None , mcp_servers: list = None) -> dict:
        async with await self.server_manager.get_browser_server() as browser:
            #async with await self.server_manager.get_file_server() as files:
                default_mcp_servers = [browser] #, files]
                default_tools = []

                consolidate_mcps = (mcp_servers or []) + default_mcp_servers
                consolidate_tools = (tools or []) + default_tools
                runner = AgentRunner(
                    instructions=self.instructions,
                    output_type=output_schema,
                    mcp_servers=consolidate_mcps,
                    settings=self.settings,
                    tools=consolidate_tools,
                )
                return await runner.run(user_steps)

    def run_flow(self, user_steps: str, output_schema , tools:list =None , mcp_servers: list = None) -> dict:
        """Run a flow from a string of steps (pytest/CLI-friendly)."""
        return asyncio.run(self._run_agent_flow(user_steps, output_schema , tools, mcp_servers))
        #return await self._run_agent_flow(user_steps, output_schema)

    def run_flow_from_file(self, file_path: str, output_schema, tools:list =None , mcp_servers: list = None) -> dict:
        """Run a flow from a file path."""
        steps = Path(file_path).read_text(encoding="utf-8")
        return self.run_flow(steps, output_schema, tools, mcp_servers)
        #return await self.run_flow(steps, output_schema)