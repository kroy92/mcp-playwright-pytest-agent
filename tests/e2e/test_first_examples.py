from __future__ import annotations
from playwright_agent.runtime.base import BaseFlowRunner
from playwright_agent.schemas.results import RunResult

runner = BaseFlowRunner()

def test_google_search_inline():
    steps = """
    Open https://www.google.com
    Type "Playwright MCP Agent" into the search input and press Enter
    Wait for the results page to load
    Click the first result link
    Take a final full-page screenshot
    """
    result = runner.run_flow(steps, RunResult)
    print (result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
