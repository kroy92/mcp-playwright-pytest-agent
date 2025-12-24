from __future__ import annotations
import platform
import asyncio
import pytest
from playwright_agent.runtime.base import BaseFlowRunner
import sys
print(sys.path)

# Windows asyncio policy (optional)
if platform.system() == "Windows":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore[attr-defined]
    except Exception:
        pass

@pytest.fixture(scope="session")
def flow_runner() -> BaseFlowRunner:
    """Session-scoped runner."""
    return BaseFlowRunner()

@pytest.fixture
def trace_name(request) -> str:
    """Returns the current test name for tracing."""
    return request.node.name