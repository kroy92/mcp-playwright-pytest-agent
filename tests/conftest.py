"""
Pytest Configuration and Fixtures
==================================

This module provides pytest fixtures and configuration for the test suite.

Fixtures
--------
- `flow_runner`: Session-scoped BaseFlowRunner instance (reused across tests)
- `trace_name`: Current test function name for OpenAI tracing

Usage
-----
Fixtures are automatically available in test functions:

    def test_login(flow_runner, trace_name):
        result = flow_runner.run_flow(
            steps,
            RunResult,
            trace_name=trace_name  # "test_login" in OpenAI dashboard
        )
        assert result.status == "PASS"

Windows Compatibility
---------------------
This module sets the Windows-compatible asyncio event loop policy to
avoid issues with subprocess-based MCP servers on Windows.

"""

from __future__ import annotations
import platform
import asyncio
import pytest
from playwright_agent.runtime.base import BaseFlowRunner

# Set Windows-compatible asyncio policy for subprocess support
# Required for MCP servers that run as subprocesses via npx
if platform.system() == "Windows":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore[attr-defined]
    except Exception:
        pass  # Ignore if policy already set or not available


@pytest.fixture(scope="session")
def flow_runner() -> BaseFlowRunner:
    """
    Session-scoped BaseFlowRunner instance.
    
    This fixture creates a single BaseFlowRunner that is reused across
    all tests in the session. This improves performance by avoiding
    repeated initialization of settings and instructions.
    
    Returns:
        BaseFlowRunner instance ready for running web automation flows
        
    Example:
        def test_search(flow_runner):
            result = flow_runner.run_flow(
                "Open google.com and search for Playwright",
                RunResult
            )
    """
    return BaseFlowRunner()


@pytest.fixture
def trace_name(request) -> str:
    """
    Get the current test function name for OpenAI tracing.
    
    This fixture provides the test function name to use as the trace
    identifier in the OpenAI trace dashboard. This makes it easy to
    find and debug specific test runs.
    
    Args:
        request: Pytest request fixture (injected automatically)
        
    Returns:
        The name of the current test function (e.g., "test_login")
        
    Example:
        def test_checkout(flow_runner, trace_name):
            result = flow_runner.run_flow(
                steps,
                RunResult,
                trace_name=trace_name  # "test_checkout" in dashboard
            )
    """
    return request.node.name