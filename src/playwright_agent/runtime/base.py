from __future__ import annotations
import asyncio
import logging
from pathlib import Path
from typing import Any, TypeVar

from playwright_agent.settings import get_settings, Settings, ConfigurationError
from playwright_agent.integrations.mcp_servers import MCPServerManager, MCPServerError
from playwright_agent.runtime.runner import AgentRunner, AgentExecutionError, MCPToolError

logger = logging.getLogger("playwright_agent.base")

T = TypeVar("T")


class FlowExecutionError(Exception):
    """Raised when a flow execution fails."""
    
    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause


def _load_instructions(path: Path | None) -> str:
    """Load agent instructions from file."""
    if path is None:
        path = Path(__file__).with_suffix("").parent / "prompts" / "generic_instructions.md"
    
    if not path.exists():
        raise FileNotFoundError(f"Instructions file not found: {path}")
    
    return path.read_text(encoding="utf-8")


class BaseFlowRunner:
    """Pytest-facing base class to run human-readable web flows through MCP Playwright Agent."""

    def __init__(self, instructions_path: Path | None = None):
        """
        Initialize the flow runner.
        
        Args:
            instructions_path: Optional path to custom instructions file
            
        Raises:
            ConfigurationError: If required settings are missing
            FileNotFoundError: If instructions file doesn't exist
        """
        try:
            self.settings: Settings = get_settings()
            self.server_manager = MCPServerManager(self.settings)
            self.instructions = _load_instructions(instructions_path)
            logger.info("BaseFlowRunner initialized successfully")
        except ConfigurationError:
            raise
        except Exception as e:
            logger.error(f"Failed to initialize BaseFlowRunner: {e}")
            raise

    async def _run_agent_flow(
        self, 
        user_steps: str, 
        output_schema, 
        tools: list | None = None, 
        mcp_servers: list | None = None,
        trace_name: str = "web_flow",
    ) -> Any:
        """
        Execute an agent flow with the given steps.
        
        Args:
            user_steps: Natural language test steps
            output_schema: Pydantic model for structured output
            tools: Optional list of additional tools
            mcp_servers: Optional list of additional MCP servers
            trace_name: Optional trace name for observability (defaults to caller's function name)
            
        Returns:
            Typed result matching output_schema
            
        Raises:
            FlowExecutionError: If the flow execution fails
            MCPServerError: If MCP server fails to start
            MCPToolError: If an MCP tool call fails
        """
        logger.info("Starting agent flow execution")
        browser = None
        
        try:
            browser = await self.server_manager.get_browser_server()
            async with browser as browser_ctx:
                default_mcp_servers = [browser_ctx]
                default_tools: list = []

                consolidate_mcps = (mcp_servers or []) + default_mcp_servers
                consolidate_tools = (tools or []) + default_tools
                
                logger.debug(f"Using {len(consolidate_mcps)} MCP servers and {len(consolidate_tools)} tools")
                
                runner = AgentRunner(
                    instructions=self.instructions,
                    output_type=output_schema,
                    mcp_servers=consolidate_mcps,
                    settings=self.settings,
                    tools=consolidate_tools,
                    trace_name=trace_name,
                )
                return await runner.run(user_steps)
                
        except MCPServerError as e:
            logger.error(f"MCP server error: {e}")
            raise FlowExecutionError(f"Failed to start MCP server: {e}", cause=e) from e
            
        except (AgentExecutionError, MCPToolError) as e:
            logger.error(f"Agent execution error: {e}")
            raise FlowExecutionError(str(e), cause=e) from e
            
        except asyncio.CancelledError:
            logger.warning("Flow execution was cancelled")
            raise FlowExecutionError("Flow execution was cancelled")
            
        except Exception as e:
            logger.error(f"Unexpected error in flow execution: {e}", exc_info=True)
            raise FlowExecutionError(
                f"Unexpected error: {type(e).__name__}: {e}",
                cause=e
            ) from e

    def run_flow(
        self, 
        user_steps: str, 
        output_schema, 
        tools: list | None = None, 
        mcp_servers: list | None = None,
        trace_name: str | None = None,
    ) -> Any:
        """
        Run a flow from a string of steps (pytest/CLI-friendly synchronous wrapper).
        
        Args:
            user_steps: Natural language test steps
            output_schema: Pydantic model for structured output
            tools: Optional list of additional tools
            mcp_servers: Optional list of additional MCP servers
            
        Returns:
            Typed result matching output_schema
        """
        return asyncio.run(self._run_agent_flow(user_steps, output_schema, tools, mcp_servers, trace_name or "web_flow"))

    def run_flow_from_file(
        self, 
        file_path: str, 
        output_schema, 
        tools: list | None = None, 
        mcp_servers: list | None = None
    ) -> Any:
        """
        Run a flow from a file path.
        
        Args:
            file_path: Path to file containing test steps
            output_schema: Pydantic model for structured output
            tools: Optional list of additional tools
            mcp_servers: Optional list of additional MCP servers
            
        Returns:
            Typed result matching output_schema
            
        Raises:
            FileNotFoundError: If steps file doesn't exist
        """
        steps_path = Path(file_path)
        if not steps_path.exists():
            raise FileNotFoundError(f"Steps file not found: {file_path}")
            
        steps = steps_path.read_text(encoding="utf-8")
        return self.run_flow(steps, output_schema, tools, mcp_servers)