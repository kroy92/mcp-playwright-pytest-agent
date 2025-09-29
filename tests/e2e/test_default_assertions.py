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



@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/verify_company_name.md",
])
def test_generic_phone_number(flow_runner, steps_path: str):
    username = os.environ.get("CRM_USERNAME")
    password = os.environ.get("CRM_PASSWORD")

    if not username or not password:
        pytest.skip("Environment variables CRM_USERNAME or CRM_PASSWORD not set")

    # Read markdown and inject credentials using f-string formatting
    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(username=username, password=password)

    result = flow_runner.run_flow(steps, RunResult)
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    for step in result.steps:
        print(step, '\n')  # Print each step result if -s flag is enabled
        assert step.status == "PASS", f"Step {step.step_id} failed: {step.exception}. Expected: {step.expected_result}, Actual: {step.actual_result}"