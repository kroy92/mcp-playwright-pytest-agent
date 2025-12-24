"""
Runtime Module - Execution Engine
==================================

This module provides the execution engine for running web automation flows.

Classes
-------
- `BaseFlowRunner`: Main entry point for pytest tests
- `AgentRunner`: Internal execution engine (typically not used directly)

Exceptions
----------
- `FlowExecutionError`: Raised when flow execution fails
- `AgentExecutionError`: Raised when agent execution fails
- `MCPToolError`: Raised when an MCP tool call fails

Typical usage is via BaseFlowRunner:

    import pytest
    from playwright_agent.runtime import BaseFlowRunner
    from playwright_agent import RunResult
    
    @pytest.mark.asyncio
    async def test_example():
        runner = BaseFlowRunner()
        result = await runner.run(steps, RunResult)

"""

from playwright_agent.runtime.base import BaseFlowRunner, FlowExecutionError
from playwright_agent.runtime.runner import AgentRunner, AgentExecutionError, MCPToolError

__all__ = [
    "BaseFlowRunner",
    "FlowExecutionError",
    "AgentRunner",
    "AgentExecutionError",
    "MCPToolError",
]