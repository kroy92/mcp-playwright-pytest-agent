from __future__ import annotations
import pathlib
import pytest
import asyncio
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner
from pydantic import Field

# Initialize the runner (assuming it's synchronous to create)
runner = BaseFlowRunner()

# Use pytest-asyncio marker
pytestmark = pytest.mark.asyncio

@pytest.mark.e2e
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/google_search.md",
    "tests/data/flows/demo_login.md",
])
async def test_generic_web_flows(steps_path: str):
    steps = pathlib.Path(steps_path).read_text(encoding="utf-8")
    result = await runner.run_flow(steps, RunResult)  # Await the async call
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    assert result.proof_of_pass, "Missing proof_of_pass (screenshot path)"

@pytest.mark.BVT
async def test_create_lead_with_mcp():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "Detailed Lead using Framework"
    FIRST_NAME = "DETAILED Framework"
    LAST_NAME = "LAST"
    user_step = f"""Do the following in the Dynamics 365 UI:

    NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS> Please try till 30 seconds for each step before failing.
    NOTE: If any unexpected popups appear, close them and continue.
    ** TRY SELF HEALING IF ELEMENTS NOT FOUND **
    1) STEP: Launch URL: {url} , WAIT FOR: Page to load , ASSERT: Page loaded successfully
    2) STEP: Enter username: {username} and click "Next" , WAIT FOR: Password field to appear , ASSERT: Username accepted
    3) STEP: Enter password: {password} and click "Sign in" , WAIT FOR: MFA prompt or Stay signed in prompt or main page , ASSERT: Password accepted
    4) STEP: If prompted for MFA, enter the current code, WAIT FOR: Next page prompt , ASSERT: MFA successful
    5) STEP: If prompted 'Stay signed in?', click 'No' , WAIT FOR: Main page to load , ASSERT: User is not stuck on login prompts
    6) STEP: Wait to be fully logged in , WAIT FOR: Main page to load , ASSERT: Logged in successfully
    7) STEP: Click Sales HUB Application , WAIT FOR: Sales Hub to load , ASSERT: Sales Hub visible
    8) STEP: In the sitemap, click 'Leads' , WAIT FOR: Leads view to load , ASSERT: Leads grid visible
    9) STEP: Close any Pop up, Wait for "Read Only Grid" button and then Click It , WAIT FOR: Read Only Grid to be activated , ASSERT: Grid switched to read-only mode
    10) STEP: From Right Side Pane, Click On Copilot Icon to close Copilot Tab if it appears , WAIT FOR: Copilot tab to close , ASSERT: Copilot tab closed if it was open
    11) STEP: Click 'New Lead' button on the command bar , WAIT FOR: New Lead form to load , ASSERT: Lead creation form displayed
    12) STEP: Enter TOPIC name as "{lead_name} - Another" in the primary name field , WAIT FOR: Field input accepted , ASSERT: Lead name entered
    13) STEP: Fill First Name (NOT LAST NAME) as '{FIRST_NAME}' , WAIT FOR: Field input accepted , ASSERT: First name entered
    14) STEP : Fill Last Name as '{LAST_NAME}' , WAIT FOR: Field input accepted , ASSERT: Last name entered
    15) STEP: Click 'Save this Lead' on the command bar , WAIT FOR: Lead to be created , ASSERT: Lead saved successfully
    16) STEP: Capture Leads Name from header , WAIT FOR: Header to update , ASSERT: Lead name matches "{FIRST_NAME} {LAST_NAME}"
    17) STEP: Click On ' role = menuitem title = Qualify' Button WAIT FOR: Till a Duplicate Account or Contact dialog appears or Qualify dialog appears , ASSERT: Duplicate Account or Contact dialog does NOT appear. If Appears, Assert Failure
    18) STEP: Click Qualify button on the dialog , WAIT FOR: Finish button to appear , ASSERT: Qualify process continued
    19) STEP: Click on Finish button on the dialog , WAIT FOR: Opportunity Page to load , ASSERT: Opportunity page displayed
    20) STEP: CLOSE THE BROWSER , WAIT FOR: Browser session to end , ASSERT: No browser instance left running"""


    class CustomAssertions(RunResult):
        is_opportunity_page_created_and_loaded: bool = Field(...,
                                                             description="Whether the New Opportunity was created and Opportunity Page loaded successfully")
        is_step_18_successful: bool = Field(..., description="Whether Step 18 was successful")

    result = await runner.run_flow(user_step, CustomAssertions)
    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_18_successful, "Step 19 was not successful"

@pytest.mark.BVT
async def test_create_lead_with_mcp1():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "Detailed Lead using Parallel Tools"
    FIRST_NAME = "DETAILED Framework Parallel Tools"
    LAST_NAME = "LAST"
    user_step = f"""
     Do the following in the Dynamics 365 UI:

    NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS> Please try till 30 seconds for each step before failing.
    NOTE: If any unexpected popups appear, close them and continue.
    ** TRY SELF HEALING IF ELEMENTS NOT FOUND **
    1) STEP: Launch URL: {url} , WAIT FOR: Page to load , ASSERT: Page loaded successfully
    2) STEP: page.get_by_placeholder("Email, phone, or Skype").fill("{username}") and page.get_by_role("button", name="Next").click(), WAIT FOR: Password field to appear , ASSERT: Username accepted
    3) STEP:page.get_by_placeholder("Password").fill("{password}") and page.get_by_role("button", name="Sign in").click() WAIT FOR: MFA prompt or Stay signed in prompt or main page , ASSERT: Password accepted
    4) STEP: If prompted for MFA, enter the current code, WAIT FOR: Next page prompt , ASSERT: MFA successful
    5) STEP: If prompted 'Stay signed in?', click 'No' , WAIT FOR: Main page to load , ASSERT: User is not stuck on login prompts
    6) STEP: Wait to be fully logged in , WAIT FOR: Main page to load , ASSERT: Logged in successfully
    7) STEP: Click Sales HUB Application , WAIT FOR: Sales Hub to load , ASSERT: Sales Hub visible
    8) STEP: page.get_by_text("Leads").click() , WAIT FOR: Leads view to load , ASSERT: Leads grid visible
    9) STEP: Close any Pop up, Wait for "Read Only Grid" button and then Click It , WAIT FOR: Read Only Grid to be activated , ASSERT: Grid switched to read-only mode
    10) STEP: From Right Side Pane, Click On Copilot Icon to close Copilot Tab if it appears , WAIT FOR: Copilot tab to close , ASSERT: Copilot tab closed if it was open
    11) STEP: page.get_by_role("menuitem", name="New", exact=True).click(timeout=60000) WAIT FOR: New Lead form to load , ASSERT: Lead creation form displayed
    12) STEP: Enter TOPIC name as "{lead_name} - Another" in the primary name field , WAIT FOR: Field input accepted , ASSERT: Lead name entered
    13) STEP: Fill First Name (NOT LAST NAME) as '{FIRST_NAME}' , WAIT FOR: Field input accepted , ASSERT: First name entered
    14) STEP : Fill Last Name as '{LAST_NAME}' , WAIT FOR: Field input accepted , ASSERT: Last name entered
    15) STEP: page.get_by_label("Save (CTRL+S)").click(), WAIT FOR: Lead to be created , ASSERT: Lead saved successfully
    16) STEP: Capture Leads Name from header , WAIT FOR: Header to update , ASSERT: Lead name matches "{FIRST_NAME} {LAST_NAME}"
    17) STEP: Click On "Create a new opportunity with an account or a contact using information from this lead. When the lead is converted, it is saved as qualified in the Closed Leads view." menuitem on the command bar
      - WAIT FOR: Till a Duplicate Account or Contact dialog appears or Qualify dialog appears , ASSERT: Duplicate Account or Contact dialog does NOT appear. If Appears, Assert Failure
    18) STEP: Click Qualify button on the dialog , WAIT FOR: Finish button to appear , ASSERT: Qualify process continued
    19) STEP: Click on Finish button on the dialog , WAIT FOR: Opportunity Page to load , ASSERT: Opportunity page displayed
    20) STEP: CLOSE THE BROWSER , WAIT FOR: Browser session to end , ASSERT: No browser instance left running
    """  # Your existing multi-line string

    class CustomAssertions(RunResult):
        is_duplicate_dialog_appeared: bool = Field(...,
                                                  description="Success conditions : Whether Duplicate Account or Contact dialog appeared in step 17")
        is_opportunity_page_created_and_loaded: bool = Field(...,
                                                             description="Success conditions : Whether the New Opportunity was created and Opportunity Page loaded successfully")
        is_step_18_successful: bool = Field(..., description="Success conditions : Whether Step 18 was successful")

    result = await runner.run_flow(user_step, CustomAssertions)
    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_18_successful, "Step 18 was not successful"