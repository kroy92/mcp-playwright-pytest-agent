"""End-to-end tests for business process flows using Dataverse MCP."""

import os
import pathlib
from datetime import date

import pyotp
import pytest
from agents.mcp.server import MCPServerStdio, MCPServerStdioParams
from agents.mcp import create_static_tool_filter
from agents.tool import function_tool
from dotenv import load_dotenv
from mcp import StdioServerParameters
from playwright_agent.runtime.base import BaseFlowRunner
from playwright_agent.schemas.results import RunResult


@function_tool()
def get_totp() -> str:
    """Generate a MFA code for Login."""
    mfa_key = os.getenv("D365_MFA_KEY")  # Not required by default
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()


@pytest.fixture
def flow_runner():
    """Fixture to provide a BaseFlowRunner instance."""
    return BaseFlowRunner()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "steps_path",
    [
        "tests/data/flows/business_process_flow.md",
    ],
)
async def test_business_process_opportunity(flow_runner, steps_path):
    """
    Tests a business process flow for creating an opportunity in Dynamics 365.

    This test uses a Dataverse MCP server to interact with the Dynamics environment.
    """
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    connection = os.getenv("DATAVERSE_CONNECTION_URL")
    tenant = os.getenv("DATAVERSE_TENANT_ID")

    if not all([url, username, password, connection, tenant]):
        pytest.skip(
            "Required environment variables for D365/Dataverse are not set."
        )

    opp_name = "OCR extraction of Polling Booth records for ECI India"
    today_str = str(date.today())

    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(
        url=url,
        username=username,
        password=password,
        OpportunityName=opp_name,
        today=today_str,
    )

    dataverse_mcp_param = StdioServerParameters(
        command="Microsoft.PowerPlatform.Dataverse.MCP",
        args=[
            f"--ConnectionUrl={connection}",
            "--MCPServerName=DataverseMCPServer",
            f"--TenantId={tenant}",
            "--EnableHttpLogging=true",
            "--EnableMsalLogging=false",
            "--Debug=false",
            "--BackendProtocol=HTTP",
        ],
    )

    async with MCPServerStdio(
        params=MCPServerStdioParams(dataverse_mcp_param),
        client_session_timeout_seconds=120,
        tool_filter=create_static_tool_filter(allowed_tool_names=["create_record"]) # Restrict to only the create_record tool
    ) as dataverse_mcp:
        result = await flow_runner._run_agent_flow(
            steps,
            RunResult,
            tools=[get_totp],
            mcp_servers=[
                dataverse_mcp
            ],  # Provide the MCP server instance - here we use  Dataverse MCP
        )

    assert result.status == "PASS", f"Flow failed: {result.exception} at {result.failed_step_id}"
    for step in result.steps:
        print(step, '\n')  # Print each step result if -s flag is enabled
        assert (
            step.status == "PASS"
        ), f"Step {step.step_id} failed: {step.exception}. Expected: {step.expected_result}, Actual: {step.actual_result}"



