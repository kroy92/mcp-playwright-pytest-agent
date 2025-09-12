from __future__ import annotations
# Provided by your agents SDK
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel  # type: ignore[import-not-found]
from agents.model_settings import ModelSettings  # type: ignore[import-not-found]
from playwright_agent.integrations.azure_openai import make_async_client
from playwright_agent.settings import Settings

class AgentRunner:
    """Executes a flow via MCP Playwright and returns typed results for pytest assertions."""

    def __init__(self, instructions: str, output_type, mcp_servers: list, settings: Settings, tools: list):
        self.settings = settings
        self.instructions = instructions
        self.output_type = output_type
        self.mcp_servers = mcp_servers
        self.tools = tools

    async def run(self, prompt: str):
        async with make_async_client(self.settings) as client:
            agent = Agent(
                name="mcp_playwright_test_agent",
                instructions=self.instructions,
                model=OpenAIChatCompletionsModel(
                    openai_client=client,
                    model=self.settings.azure_openai_deployment,
                ),
                tools=self.tools,              # extend with more tools if needed
                mcp_servers=self.mcp_servers,  # [Playwright MCP, Filesystem MCP]
                output_type=self.output_type,  # pydantic model type (e.g., RunResult)
                model_settings=ModelSettings(parallel_tool_calls=True)
            )
            with trace("pytest_web_flow"):
                result = await Runner.run(agent, input=prompt.strip(), max_turns=self.settings.max_turns)

            return result.final_output
