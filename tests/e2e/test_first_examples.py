from __future__ import annotations
from playwright_agent.runtime.base import BaseFlowRunner
from playwright_agent.schemas.results import RunResult
from dotenv import load_dotenv

load_dotenv(override=True)

runner = BaseFlowRunner()

def test_google_search_inline():
    steps = """
    Open https://the-internet.herokuapp.com/login
    Wait for the login form to appear
    Type "tomsmith" into the Username field
    Type "SuperSecretPassword!" into the Password field
    Click the Login button
    Wait for the message "You logged into a secure area!" to appear
    """
    result = runner.run_flow(steps, RunResult)
    print (result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"


