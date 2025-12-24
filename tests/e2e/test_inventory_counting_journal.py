from __future__ import annotations
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner
from pydantic import  Field
import os
from dotenv import load_dotenv
load_dotenv(override=True)


# Define a fixture that creates and returns a runner instance
@pytest.fixture
def flow_runner():
    return BaseFlowRunner()



@pytest.mark.asyncio
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/ICJ.md",
])
async def test_ICJ(flow_runner, steps_path: str):
    url = os.environ.get("D365_FO_URL")
    username = os.environ.get("D365_FO_USERNAME")
    password = os.environ.get("D365_FO_PASSWORD")

    if not username or not password or not url:
        pytest.skip("Environment variables D365_FO_USERNAME or D365_FO_PASSWORD or D365_FO_URL not set")

    # Read markdown and inject credentials using f-string formatting
    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(username=username, password=password, url=url)

    class CustomRunResult(RunResult):
        journal_number: str | None = Field(description="The created journal number in step 5, if not created and error occurred, this will be None")

    result = await flow_runner.run(steps, CustomRunResult)
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    for step in result.steps:
        print(step, '\n')  # Print each step result if -s flag is enabled
        assert step.status == "PASS", f"Step {step.step_id} failed: {step.exception}. Expected: {step.expected_result}, Actual: {step.actual_result}"
    assert result.journal_number is not None, "Journal number was not captured in the result"