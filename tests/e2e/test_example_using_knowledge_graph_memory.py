from __future__ import annotations
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner
from pydantic import Field
from agents.tool import function_tool
import os
from dotenv import load_dotenv
load_dotenv(override=True)
import pyotp


# Define a tool to generate TOTP codes for MFA
@function_tool()
def get_totp() -> str:
    """Generate a MFA code for Login."""
    mfa_key = os.getenv("D365_MFA_KEY")  # Not required by default
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()

@pytest.fixture
def flow_runner():
    return BaseFlowRunner()


@pytest.mark.asyncio
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/d365_lead_opportunity.md",
])
async def test_create_lead_and_qualify_opportunity(flow_runner, steps_path: str):
 
    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "Lessons Tracker"
    FIRST_NAME = "Prank"
    LAST_NAME = "Tiwari"

    if not url or not username or not password:
        pytest.skip("Environment variables DYNAMICS_CRM_URL, D365_USERNAME or D365_PASSWORD not set")

    # Read markdown and inject credentials using f-string formatting
    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(url=url, username=username, password=password, lead_name=lead_name, FIRST_NAME=FIRST_NAME, LAST_NAME=LAST_NAME)

    knowledge_graph_steps_path = pathlib.Path("tests/data/prompts/knowledge_graph_instruction.md")
    knowledge_graph_instructions = knowledge_graph_steps_path.read_text(encoding="utf-8")
    steps = knowledge_graph_instructions + "\n" + steps

    class CustomRunResult(RunResult):
        login_successful: bool = Field(description="True if user reached Dynamics main page after login")
        lead_saved: bool = Field(description="True if lead was actually saved in CRM")
        duplicate_dialog_shown: bool = Field(description="True if duplicate account/contact dialog appeared")
        opportunity_page_loaded: bool = Field(description="True if opportunity page was displayed after qualify")

    async with await flow_runner.server_manager.get_knowledge_graph_based_memory(kg_path='Leads_opportunities.json') as kg_server:
        result = await flow_runner._run_agent_flow(steps, CustomRunResult, tools=[get_totp], mcp_servers=[kg_server])

    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    assert result.login_successful, "Login to Dynamics CRM was not successful"
    assert result.lead_saved, "Lead was not saved in Dynamics CRM"
    assert result.opportunity_page_loaded, "Opportunity page did not load after qualifying the lead"
    assert not result.duplicate_dialog_shown, "Duplicate dialog appeared during lead creation"
    for step in result.steps:
        print(step, '\n')  # Print each step result if -s flag is enabled
        assert (
            step.status == "PASS"
        ), f"Step {step.step_id} failed: {step.exception}. Expected: {step.expected_result}, Actual: {step.actual_result}"



    
