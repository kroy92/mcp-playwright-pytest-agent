"""
mcp-playwright-pytest-agent
============================

An AI-powered web automation testing framework that combines:
- **Playwright MCP** for browser automation via Model Context Protocol
- **OpenAI Agents SDK** for intelligent test execution
- **Pytest** for structured test organization

Quick Start
-----------
1. Set up your .env file with Azure OpenAI credentials:
   - AZURE_OPENAI_DEPLOYMENT
   - AZURE_OPENAI_ENDPOINT  
   - AZURE_OPENAI_API_KEY

2. Write a test:
    ```python
    import pytest
    from playwright_agent import BaseFlowRunner, RunResult
    
    @pytest.mark.asyncio
    async def test_login():
        runner = BaseFlowRunner()
        steps = '''
        Open https://example.com/login
        Type "user@email.com" in the Email field
        Type "password123" in the Password field
        Click the Login button
        Verify the Dashboard page loads
        '''
        result = await runner.run(steps, RunResult)
        assert result.status == "PASS"
    ```

3. Run with pytest:
    ```bash
    uv run pytest tests/e2e/your_test.py -v
    ```

Key Classes
-----------
- `BaseFlowRunner`: Main entry point for running web automation flows
- `RunResult`: Pydantic model for test results with step-by-step details
- `StepResult`: Individual step result with pass/fail status

Exceptions
----------
- `ConfigurationError`: Missing or invalid configuration (e.g., Azure credentials)
- `FlowExecutionError`: Flow execution failed (wraps underlying errors)
- `AgentExecutionError`: AI agent execution failed
- `MCPToolError`: MCP tool call failed (timeout, connection, etc.)
- `MCPServerError`: MCP server failed to start

For more details, see the README.md or individual module docstrings.
"""

from playwright_agent.settings import ConfigurationError
from playwright_agent.runtime.base import BaseFlowRunner, FlowExecutionError
from playwright_agent.runtime.runner import AgentExecutionError, MCPToolError
from playwright_agent.integrations.mcp_servers import MCPServerError
from playwright_agent.schemas.results import RunResult, StepResult

__all__ = [
    "__version__",
    # Core classes
    "BaseFlowRunner",
    "RunResult",
    "StepResult",
    # Exceptions
    "ConfigurationError",
    "FlowExecutionError",
    "AgentExecutionError",
    "MCPToolError",
    "MCPServerError",
]

__version__ = "0.1.0"