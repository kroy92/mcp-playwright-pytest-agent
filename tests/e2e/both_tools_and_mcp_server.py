from __future__ import annotations
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner
from pydantic import Field
from agents.tool import function_tool
from playwright_agent.settings import get_settings
import pyotp
from agents.mcp.server import MCPServerStdio,MCPServerStdioParams
import asyncio




ado_mcp_params=MCPServerStdioParams(
    command="npx",
    args=["-y", "@azure-devops/mcp", "krishnaroy"],
 
)

@pytest.fixture
def flow_runner():
    return BaseFlowRunner()


@pytest.mark.asyncio
async def test_using_mcp_ado(flow_runner, trace_name):
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)
    url = os.environ.get("D365_FO_URL")
    username = os.environ.get("D365_FO_USERNAME")
    password = os.environ.get("D365_FO_PASSWORD")

    if not username or not password or not url:
        pytest.skip("Environment variables D365_FO_USERNAME or D365_FO_PASSWORD or D365_FO_URL not set")

    user_step = f"""
Fetch the Test Case from Azure DevOps with ID "219" for project 'learn'.
Execute each step in the test case and capture the results.

**Login Details (for execution only):**
    URL: {url}
    Username: {username}
    Password: {password}

**IMPORTANT SECURITY NOTE:**
- Do NOT include actual credentials (username, password, MFA codes) in any bug description, logs, screenshots, or comments.
- Use placeholders like {{username}}, {{password}} in all documentation.

If any step fails:
    - Create a new Work Item of type "Bug" in Azure DevOps.
    - Populate the "Microsoft.VSTS.TCM.ReproSteps" field with detailed reproduction steps in beautiful markdown format in tabular form
     -**When using a table, insert  line breaks after each row to ensure proper formatting**.
    - Link the bug to the original test case.
    - Assign the bug to the original test case owner.
    - Set the bug's severity and priority as per your judgment.
    - Ensure NO sensitive information (credentials, tokens, URLs with secrets) is included in the bug.
    - ** Verify the Reproduction Steps field renders correctly in Azure DevOps before saving the bug. **

Additional Guidelines:
- Apply reasonable retries for transient issues (e.g., network delays, UI load).
- Think like a smart manual tester: validate UI states, handle unexpected popups, and confirm expected results.
- Capture clear evidence (screenshots, logs) without exposing sensitive data.

Close Bugs:
- If test case passes and a related bugs exists, close the bug with a comment referencing the successful test run.

"""


    class CustomRunResult(RunResult):
        journal_number: str | None = Field(description="The created journal number in step 5, if not created and error occurred, this will be None")

    async with MCPServerStdio(params=ado_mcp_params, client_session_timeout_seconds=30) as ado_tools:
        result = await flow_runner._run_agent_flow(
            user_step,
            CustomRunResult,
            mcp_servers=[ado_tools],
            trace_name=trace_name,
        )

    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    for step in result.steps:
        print(step, '\n')  # Print each step result if -s flag is enabled
        assert step.status == "PASS", f"Step {step.step_id} failed: {step.exception}. Expected: {step.expected_result}, Actual: {step.actual_result}"



