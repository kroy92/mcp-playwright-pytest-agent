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



@function_tool()
def get_totp() -> str:
    """Generate a MFA code for Login."""
    mfa_key = getattr(get_settings(), "mfa_key", None)  # Not required by default
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()


runner = BaseFlowRunner()

@pytest.mark.asyncio
@pytest.mark.PGSQL
async def test_create_lead_with_mcp_ado():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "MCP Started -1"
    FIRST_NAME = "MCP Started"
    LAST_NAME = "MCP Started"
    user_step = f"""
    
    Execute the following tests  and Report results as PASS/FAIL with details.
    
    ** Last time you stopped and didnt complete the test. Please complete it now unless there is a Failure. **

    NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS> Please try till 30 seconds for each step before failing.
    NOTE: If any unexpected popups appear, close them and continue.
    ** TRY SELF HEALING IF ELEMENTS NOT FOUND **
    1. Go to Dynamics URL {url} → Page should load
2. Type "{username}" into Username → Password field should appear
3. Type "{password}" into Password → Main page or MFA prompt should load
4. If MFA appears, enter code → Next page should load
5. If "Stay signed in?" prompt appears, click "No" → Main page should load
6. Wait until logged in → Main page should show - This may take up to 60 seconds
7. Click "Sales Hub" Applications → Sales Hub should open
8. Wait until sitemap-entity-Lead is visible - may take upto 60 seconds
9. Click "Leads - sitemap-entity" in sitemap → Leads grid should appear
10. Close any popups, then click "Read Only Grid" → Read-only grid should activate
11. If Copilot tab is open, close it → Copilot tab should disappear
12. Click "New Lead" → Lead form should open
13. Enter "{lead_name} - Another Again" in Topic → Field should accept
14. Enter "{FIRST_NAME}" in First Name → Field should accept
15. Click Accept Suggestion if it appears → Suggestion should be accepted (if appeared)
16. Enter "{LAST_NAME} Again" in Last Name → Field should accept 
17. Save Lead → Lead should be saved. There should be no error notifications/warnings/messages. **FAIL** if any appear. **FAIL** if lead is not Saved
18. Capture Lead Name from header → It should match "{FIRST_NAME} {LAST_NAME}"
19. Click "Qualify Command"  → Qualify dialog box should appear (fail if Duplicate dialog appears)
    - Last Time You clicked Qualify Button on Business Process Flow. Dont do that. Click on Command Bar Button. check role=menuitem title=Qualify
20. In dialog, click "Qualify" → Finish button should appear
21. Click "Finish" → Opportunity page should load
22. Close Browser → No browser left running


* Bug Creation Logic for Test Failures if the test Failed **
- Only create one consolidated work item of type bug in Project learn for all failures in this test run.
- Create Bug **only if a similar bug does not already exist**. Check for existing bugs using similar titles or descriptions to avoid duplication.
- If a new bug is created:
  - Provide **clear and detailed steps to reproduce** in the bug description.
  - **Attach screenshots** or relevant artifacts if available.
- Use your **best judgment** and  assign appropriate **severity and priority**.
- Return the **Bug ID** in the **exception message** for traceability.

"""

    class CustomAssertions(RunResult):
        # check if duplicate Account or Contact dialog appeared in step 17
        is_duplicate_dialog_appeared: bool = Field(..., description="Success conditions : Whether Duplicate Account or Contact dialog appeared in step 17")

        is_opportunity_page_created_and_loaded: bool = Field(...,description="Success conditions : Whether the New Opportunity was created and Opportunity Page loaded successfully")
        is_step_21_successful: bool = Field(..., description="Success conditions : Whether Step 21 was successful")
        opp_id_created: str = Field(..., description="The Opportunity ID , NOT LEAD ID created if Test is Passed, else set value to 'TEST FAILED'")
        is_lead_converted_to_opportunity: bool = Field(...,description="Success conditions: Whether the Lead was converted to Opportunity successfully. FAIL IF NOT CONVERTED")

    async with MCPServerStdio(params=ado_mcp_params, client_session_timeout_seconds=30) as ado_tools:
        result = await runner._run_agent_flow(
            user_step,
            CustomAssertions,
            tools=[get_totp],
            mcp_servers=[ado_tools]
        )

    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_21_successful, "Step 21 was not successful"



