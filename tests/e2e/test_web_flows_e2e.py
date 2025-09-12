from __future__ import annotations
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner
from pydantic import Field
from agents.tool import function_tool
from playwright_agent.settings import get_settings
import pyotp
  # type: ignore[import-not-found]


@function_tool()
def get_totp() -> str:
    """Generate a MFA code for Login."""
    mfa_key = getattr(get_settings(), "mfa_key", None)  # Not required by default
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()


runner = BaseFlowRunner()


@pytest.mark.e2e
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/google_search.md",
    "tests/data/flows/demo_login.md",
])
def test_generic_web_flows(steps_path: str):
    steps = pathlib.Path(steps_path).read_text(encoding="utf-8")
    result = runner.run_flow(steps, RunResult)
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    assert result.proof_of_pass, "Missing proof_of_pass (screenshot path)"


#@pytest.mark.BVT
def test_create_lead_with_mcp():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "Detailed Lead using Framework"
    FIRST_NAME = "DETAILED Framework"
    LAST_NAME = "LAST"
    user_step = f"""
    Do the following in the Dynamics 365 UI:

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
        opp_id_created: str = Field(...,
                                    description="The Opportunity ID created if Test is Passed, else set value to 'TEST FAILED'")

    result = runner.run_flow(user_step, CustomAssertions)

    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_18_successful, "Step 19 was not successful"


@pytest.mark.BVT
def test_create_lead_with_mcp():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "Detailed Lead using Framework"
    FIRST_NAME = "DETAILED Framework"
    LAST_NAME = "LAST"
    user_step = f"""
    Do the following in the Dynamics 365 UI:

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
        opp_id_created: str = Field(...,
                                    description="The Opportunity ID created if Test is Passed, else set value to 'TEST FAILED'")

    result = runner.run_flow(user_step, CustomAssertions)

    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_18_successful, "Step 19 was not successful"


@pytest.mark.BVT
def test_create_lead_with_mcp1():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "VD Started"
    FIRST_NAME = "VD Started"
    LAST_NAME = "VD Started"
    user_step = f"""
    Do the following in the Dynamics 365 UI:

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
"""

    class CustomAssertions(RunResult):
        # check if duplicate Account or Contact dialog appeared in step 17
        is_duplicate_dialog_appeared: bool = Field(...,
                                                   description="Success conditions : Whether Duplicate Account or Contact dialog appeared in step 17")

        is_opportunity_page_created_and_loaded: bool = Field(...,
                                                             description="Success conditions : Whether the New Opportunity was created and Opportunity Page loaded successfully")
        is_step_21_successful: bool = Field(..., description="Success conditions : Whether Step 21 was successful")
        opp_id_created: str = Field(...,
                                    description="The Opportunity ID , NOT LEAD ID created if Test is Passed, else set value to 'TEST FAILED'")
        is_lead_converted_to_opportunity: bool = Field(...,
                                                       description="Success conditions: Whether the Lead was converted to Opportunity successfully. FAIL IF NOT CONVERTED")

    result = runner.run_flow(user_step, CustomAssertions, tools =[get_totp])

    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_21_successful, "Step 21 was not successful"


@pytest.mark.BVT
def test_create_lead_with_mcp_handhold():
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    lead_name = "AI CDP"
    FIRST_NAME = "AI CDP Framework Parallel Tools"
    LAST_NAME = "DETAILED Framework Parallel Tools"
    user_step = f"""
    Do the following in the Dynamics 365 UI:

    NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS> Please try till 30 seconds for each step before failing.
    NOTE: If any unexpected popups appear, close them and continue.
    ** TRY SELF HEALING IF ELEMENTS NOT FOUND **browser_navigate("Go to Dynamics URL {url}")
    IMPORTANT: ADD APPROPRIATE WAIT AND VERIFY STEPS AFTER EACH ACTION STEP
browser_verify_element_visible("Sign-in page is loaded and visible")

browser_type("Type {username} into the Username field")
browser_wait_for("Password field to appear")
browser_verify_element_visible("Password field is now visible")

browser_type("Type {password} into the Password field and submit")
browser_wait_for("Either the main page is visible or an MFA prompt appears")
browser_verify_element_visible("Either the main page is visible or an MFA prompt appears")

browser_fill_form("If an MFA prompt appears, enter the MFA code  and submit")
browser_wait_for("Main page to be visible or 'Stay signed in?' prompt to appear")
browser_verify_element_visible("Main page is visible after MFA or MFA prompt is dismissed")

browser_click("If a 'Stay signed in?' prompt appears, click No")
browser_wait_for("'Stay signed in?' prompt to be dismissed or not present")
browser_verify_text_visible("'Stay signed in?' prompt is dismissed or not present")

browser_wait_for("Main Dynamics home page to load completely")
browser_wait_for("Dynamics home shell and global navigation to be visible . This may take some time like 60 seconds")
browser_verify_element_visible("Dynamics home shell and global navigation are visible")

browser_click("Open the 'Sales Hub' application")
browser_verify_element_visible("'Sales Hub' application landing area is visible")

browser_wait_for("'sitemap-entity-Lead' entry to be visible in the sitemap")
browser_verify_element_visible("'sitemap-entity-Lead' entry is visible in the sitemap")

browser_click("Click 'Leads - sitemap-entity' in the sitemap")
browser_verify_element_visible("Leads grid is visible")

browser_click("Close any visible popups, callouts, teaching bubbles, or banners")
browser_verify_text_visible("No popups, callouts, or banners are visible")

browser_click("Activate 'Read Only Grid'")
browser_verify_text_visible("Read-only grid is active")

browser_click("If the Copilot tab or pane is open, close it")
browser_verify_text_visible("Copilot tab or pane is closed or not present")

browser_click("Click 'New Lead' to open the Lead form")
browser_verify_element_visible("Lead form header and fields are visible")

browser_type("Enter {lead_name} - Another Again in the Topic field")
browser_verify_value("Topic field value equals {lead_name} - Another Again")

browser_type("Enter {FIRST_NAME} in the First Name field")
browser_verify_value("First Name field value equals {FIRST_NAME}")

browser_click("If an inline suggestion appears for First Name, click Accept")
browser_verify_text_visible("Suggestion accepted or no suggestion shown")

browser_type("Enter {LAST_NAME} Again in the Last Name field")
browser_verify_value("Last Name field value equals {LAST_NAME} Again")

browser_click("Click Save on the lead form")
browser_verify_text_visible("Save completed; no error notifications, warnings, or validation messages are present")

browser_verify_value("Header lead name equals {FIRST_NAME} {LAST_NAME}")

browser_click("From the Command Bar, click Qualify (role=menuitem, title=Qualify). Do NOT click the BPF Qualify")
browser_verify_text_visible("Qualify lead dialog is displayed and Duplicate detection dialog is NOT present")

browser_click("In the Qualify dialog, click Qualify")
browser_verify_element_visible("Finish button is visible")

browser_click("Click Finish to complete qualification")
browser_verify_element_visible("Opportunity page is loaded and visible")

browser_close("Close the browser")
browser_verify_text_visible("No browser instances remain running")
"""

    class CustomAssertions(RunResult):
        # check if duplicate Account or Contact dialog appeared in step 17
        is_duplicate_dialog_appeared: bool = Field(...,
                                                   description="Success conditions : Whether Duplicate Account or Contact dialog appeared in step 17")
        is_opportunity_page_created_and_loaded: bool = Field(...,
                                                             description="Success conditions : Whether the New Opportunity was created and Opportunity Page loaded successfully")
        is_step_21_successful: bool = Field(...,
                                            description="""Success conditions : Whether Step browser_verify_element_visible("Opportunity page is loaded and visible") was successful""")
        opp_id_created: str = Field(...,
                                    description="The Opportunity ID , NOT LEAD ID created if Test is Passed, else set value to 'TEST FAILED'")
        is_lead_converted_to_opportunity: bool = Field(...,
                                                       description="Success conditions: Whether the Lead was converted to Opportunity successfully. FAIL IF NOT CONVERTED")

    result = runner.run_flow(user_step, CustomAssertions, tools= [get_totp])

    print(result)
    assert result.status == "PASS", f"Test failed with exception: {result.exception} at step {result.failed_step_id}"
    assert result.is_opportunity_page_created_and_loaded, "Opportunity page was not created and loaded successfully"
    assert result.is_step_21_successful, "Step 21 was not successful"
