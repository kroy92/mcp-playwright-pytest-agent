from __future__ import annotations
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner


# Define a fixture that creates and returns a runner instance
@pytest.fixture
def flow_runner():
    return BaseFlowRunner()


@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/failed_login.md",
    "tests/data/flows/demo_login.md",
])
async def test_generic_web_flows(flow_runner, steps_path: str):
    steps = pathlib.Path(steps_path).read_text(encoding="utf-8")
    result = await flow_runner.run(steps, RunResult)
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"