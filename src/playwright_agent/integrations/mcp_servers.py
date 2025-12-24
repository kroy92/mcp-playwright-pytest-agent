"""
MCP Server Management
=====================

This module provides factory classes for creating Model Context Protocol (MCP)
servers used for browser automation and other capabilities.

Supported MCP Servers
---------------------
1. **Playwright Browser Server** (`@playwright/mcp`)
   - Browser automation (navigation, clicking, typing, screenshots)
   - Runs in isolated mode with configurable viewport
   - Blocks dangerous tools like `browser_run_code`

2. **Filesystem Server** (`@modelcontextprotocol/server-filesystem`)
   - Read/write files in isolated directories
   - Useful for downloading files during tests

3. **Knowledge Graph Memory** (`@modelcontextprotocol/server-memory`)
   - Persistent memory for locator hints and test data
   - Helps with self-healing tests

Usage
-----
Servers are created via `MCPServerManager` and used as async context managers:

    manager = MCPServerManager(settings)
    
    # Browser automation
    async with await manager.get_browser_server() as browser:
        # browser is now available as an MCP server
        result = await runner.run(steps, mcp_servers=[browser])

Configuration
-------------
Server behavior is controlled via Settings:
- `mcp_client_timeout_seconds`: Timeout for MCP tool calls
- `mcp_isolated_dir`: Directory for browser isolation
- `mcp_output_dir`: Directory for server outputs
- `viewport`: Browser viewport size ("width,height")
- `timeout_seconds`: Default action timeout

"""

from __future__ import annotations
import logging
from typing import Any

from playwright_agent.settings import Settings

# MCP SDK imports for server management
from agents.mcp import MCPServerStdio, create_static_tool_filter  # type: ignore[import-not-found]

logger = logging.getLogger("playwright_agent.mcp_servers")


class MCPServerError(Exception):
    """Raised when an MCP server fails to start or communicate."""
    
    def __init__(self, server_type: str, message: str, cause: Exception | None = None):
        super().__init__(f"MCP server '{server_type}' error: {message}")
        self.server_type = server_type
        self.cause = cause


class MCPServerManager:
    """
    Factory for creating and configuring MCP servers.
    
    This class creates properly configured MCP server instances for
    different purposes (browser automation, file operations, memory).
    Each server runs as a subprocess via npx.
    
    The manager uses settings to configure timeouts, directories, and
    other server-specific options.
    
    Attributes:
        settings: Application settings for server configuration
    
    Example:
        manager = MCPServerManager(get_settings())
        
        # Get a browser server
        browser = await manager.get_browser_server()
        async with browser as ctx:
            # Use browser for automation
            pass
        
        # Get a knowledge graph server
        kg = await manager.get_knowledge_graph_based_memory("memory.json")
        async with kg as ctx:
            # Use for persistent memory
            pass
    """

    def __init__(self, settings: Settings):
        """Initialize the server manager with application settings."""
        self.settings = settings

    async def get_browser_server(self) -> MCPServerStdio:
        """
        Create and return a Playwright MCP browser server.
        
        Returns:
            MCPServerStdio instance for browser automation
            
        Raises:
            MCPServerError: If server creation fails
        """
        try:
            params: dict[str, Any] = {
                "command": "npx",
                "args": [
                    "@playwright/mcp@v0.0.42",
                    "--isolated",
                    f"--viewport-size={self.settings.viewport}",
                    f"--output-dir={str(self.settings.mcp_isolated_dir)}",
                    f"--timeout-action={self.settings.timeout_seconds}",
                    "--caps=vision,testing",
                ],
            }
            logger.debug(f"Creating browser MCP server with params: {params}")
            return MCPServerStdio(
                params=params,
                client_session_timeout_seconds=self.settings.mcp_client_timeout_seconds,
                tool_filter=create_static_tool_filter(blocked_tool_names=["browser_run_code"]),
            )
        except Exception as e:
            logger.error(f"Failed to create browser MCP server: {e}")
            raise MCPServerError("browser", str(e), cause=e) from e

    async def get_file_server(self) -> MCPServerStdio:
        """
        Create and return a filesystem MCP server.
        
        Returns:
            MCPServerStdio instance for file operations
            
        Raises:
            MCPServerError: If server creation fails
        """
        try:
            params: dict[str, Any] = {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    str(self.settings.mcp_isolated_dir),
                    str(self.settings.mcp_output_dir),
                ],
            }
            logger.debug(f"Creating filesystem MCP server with params: {params}")
            return MCPServerStdio(
                params=params,
                client_session_timeout_seconds=self.settings.mcp_client_timeout_seconds,
            )
        except Exception as e:
            logger.error(f"Failed to create filesystem MCP server: {e}")
            raise MCPServerError("filesystem", str(e), cause=e) from e

    async def get_knowledge_graph_based_memory(self, kg_path: str) -> MCPServerStdio:
        """
        Create and return a knowledge graph memory MCP server.
        
        Args:
            kg_path: Path to the knowledge graph file
            
        Returns:
            MCPServerStdio instance for knowledge graph memory
            
        Raises:
            MCPServerError: If server creation fails
        """
        try:
            params: dict[str, Any] = {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-memory"],
                "env": {
                    "MEMORY_FILE_PATH": kg_path
                }
            }
            logger.debug(f"Creating knowledge graph MCP server with path: {kg_path}")
            return MCPServerStdio(
                params=params,
                client_session_timeout_seconds=self.settings.mcp_client_timeout_seconds,
            )
        except Exception as e:
            logger.error(f"Failed to create knowledge graph MCP server: {e}")
            raise MCPServerError("knowledge_graph", str(e), cause=e) from e
