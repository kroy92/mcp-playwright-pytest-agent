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
    "tests/data/flows/verify_only_digits_allowed.md",
])
async def test_generic_phone_number(flow_runner, steps_path: str):
    username = os.environ.get("CRM_USERNAME")
    password = os.environ.get("CRM_PASSWORD")

    if not username or not password:
        pytest.skip("Environment variables CRM_USERNAME or CRM_PASSWORD not set")

    # Read markdown and inject credentials using f-string formatting
    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(username=username, password=password)

    # Define a custom RunResult class to include additional validation results
    # Add boolean flags for key business rules (e.g., phone_validation_passed)
    class CustomRunResult(RunResult):
        phone_validation_passed: bool = Field(description="True if phone validation message appeared, else False")

    # Run the flow and get results in the custom result class
    result = await flow_runner.run(steps, CustomRunResult)

    print(result) # Print result, if -s flag is enabled
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    assert result.phone_validation_passed, "Phone field accepted non-digit characters, validation failed."