from __future__ import annotations
import logging
from typing import Any, TypeVar

# Provided by your agents SDK
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel, OpenAIResponsesModel  # type: ignore[import-not-found]
from agents.model_settings import ModelSettings  # type: ignore[import-not-found]
from agents.exceptions import AgentsException  # type: ignore[import-not-found]
from playwright_agent.integrations.azure_openai import make_async_client
from playwright_agent.settings import Settings
from openai.types.shared import Reasoning

logger = logging.getLogger("playwright_agent.runner")

T = TypeVar("T")


class AgentExecutionError(Exception):
    """Raised when agent execution fails."""
    
    def __init__(self, message: str, cause: Exception | None = None, partial_result: Any = None):
        super().__init__(message)
        self.cause = cause
        self.partial_result = partial_result


class MCPToolError(AgentExecutionError):
    """Raised when an MCP tool call fails."""
    
    def __init__(self, tool_name: str, message: str, cause: Exception | None = None):
        super().__init__(f"MCP tool '{tool_name}' failed: {message}", cause)
        self.tool_name = tool_name


class AgentRunner:
    """Executes a flow via MCP Playwright and returns typed results for pytest assertions."""

    def __init__(self, instructions: str, output_type, mcp_servers: list, settings: Settings, tools: list, trace_name: str):
        self.settings = settings
        self.instructions = instructions
        self.output_type = output_type
        self.mcp_servers = mcp_servers
        self.tools = tools
        self.trace_name = trace_name

    async def run(self, prompt: str) -> T:
        """
        Execute the agent flow with the given prompt.
        
        Args:
            prompt: The user prompt/steps to execute
            
        Returns:
            The typed result from the agent
            
        Raises:
            AgentExecutionError: If the agent execution fails
            MCPToolError: If an MCP tool call fails
        """
        logger.info("Starting agent execution")
        logger.debug(f"Prompt: {prompt[:200]}...")
        
        try:
            async with make_async_client(self.settings) as client:
                agent = Agent(
                    name="mcp_playwright_test_agent",
                    instructions=self.instructions,
                    model=OpenAIResponsesModel(
                        openai_client=client,
                        model=self.settings.azure_openai_deployment,
                    ),
                    tools=self.tools,
                    mcp_servers=self.mcp_servers,
                    output_type=self.output_type,
                    model_settings=ModelSettings(
                        parallel_tool_calls=True, 
                        reasoning=Reasoning(effort="medium")
                    )
                )
                
                with trace(self.trace_name):
                    result = await Runner.run(
                        agent, 
                        input=prompt.strip(), 
                        max_turns=self.settings.max_turns
                    )

                logger.info("Agent execution completed successfully")
                return result.final_output
                
        except AgentsException as e:
            error_msg = str(e)
            logger.error(f"Agent execution failed: {error_msg}")
            
            # Check for MCP tool errors (timeout, connection issues)
            if "MCP tool" in error_msg:
                tool_name = self._extract_tool_name(error_msg)
                if "Timed out" in error_msg:
                    raise MCPToolError(
                        tool_name,
                        f"Tool timed out after {self.settings.mcp_client_timeout_seconds}s. "
                        "Consider increasing MCP_CLIENT_TIMEOUT_SECONDS.",
                        cause=e
                    ) from e
                raise MCPToolError(tool_name, error_msg, cause=e) from e
            
            raise AgentExecutionError(f"Agent execution failed: {error_msg}", cause=e) from e
            
        except TimeoutError as e:
            logger.error(f"Agent execution timed out: {e}")
            raise AgentExecutionError(
                "Agent execution timed out. Consider increasing timeout settings.",
                cause=e
            ) from e
            
        except Exception as e:
            logger.error(f"Unexpected error during agent execution: {e}", exc_info=True)
            raise AgentExecutionError(
                f"Unexpected error during agent execution: {type(e).__name__}: {e}",
                cause=e
            ) from e

    @staticmethod
    def _extract_tool_name(error_msg: str) -> str:
        """Extract tool name from error message."""
        # Pattern: "Error invoking MCP tool <tool_name>:"
        if "MCP tool" in error_msg:
            parts = error_msg.split("MCP tool")
            if len(parts) > 1:
                tool_part = parts[1].strip()
                # Get the tool name (first word after "MCP tool")
                tool_name = tool_part.split(":")[0].strip()
                return tool_name
        return "unknown"
