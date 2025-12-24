"""
=============================================================================
TUTORIAL: Using trace_name for OpenAI Agent Tracing
=============================================================================

This file demonstrates three ways to set the trace name when running tests.
The trace name appears in OpenAI's trace dashboard, helping you identify
and debug specific test runs.

Trace names are useful for:
- Filtering test runs in the OpenAI trace viewer
- Correlating test results with specific test cases
- Debugging failed tests by finding their exact trace

=============================================================================
"""

from __future__ import annotations
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner


# -----------------------------------------------------------------------------
# EXAMPLE 1: Default Trace Name
# -----------------------------------------------------------------------------
# When you don't provide a trace_name, the framework uses "web_flow" as default.
# This is the simplest approach - just call run_flow() without trace_name.
#
# Use this when:
#   - You don't need to track individual test traces
#   - You're doing quick experiments or prototyping
#   - Trace identification is not important for your use case
# -----------------------------------------------------------------------------

def test_with_default_trace_name():
    """
    This test uses the default trace name "web_flow".
    
    In the OpenAI trace dashboard, this will appear as:
        Trace: web_flow
    """
    runner = BaseFlowRunner()
    
    steps = """
    Open https://the-internet.herokuapp.com/login
    Wait for the login form to appear
    Type "tomsmith" into the Username field
    Type "SuperSecretPassword!" into the Password field
    Click the Login button
    Wait for the message "You logged into a secure area!" to appear
    """
    
    # No trace_name parameter - uses default "web_flow"
    result = runner.run_flow(steps, RunResult)
    
    assert result.status == "PASS", f"Failed: {result.exception}"


# -----------------------------------------------------------------------------
# EXAMPLE 2: Explicit Trace Name
# -----------------------------------------------------------------------------
# You can pass a custom trace_name directly to run_flow().
# This gives you full control over the trace identifier.
#
# Use this when:
#   - You want to use a specific naming convention (e.g., Jira IDs, TC numbers)
#   - You need to correlate traces with external test management systems
#   - You want descriptive names that aren't tied to the test function name
# -----------------------------------------------------------------------------

def test_with_explicit_trace_name():
    """
    This test uses an explicitly provided trace name.
    
    In the OpenAI trace dashboard, this will appear as:
        Trace: TC_LOGIN_001_valid_credentials
    """
    runner = BaseFlowRunner()
    
    steps = """
    Open https://the-internet.herokuapp.com/login
    Wait for the login form to appear
    Type "tomsmith" into the Username field
    Type "SuperSecretPassword!" into the Password field
    Click the Login button
    Wait for the message "You logged into a secure area!" to appear
    """
    
    # Explicit trace_name - useful for test case IDs or custom identifiers
    result = runner.run_flow(
        steps, 
        RunResult, 
        trace_name="TC_LOGIN_001_valid_credentials"  # <-- Custom trace name
    )
    
    assert result.status == "PASS", f"Failed: {result.exception}"


# -----------------------------------------------------------------------------
# EXAMPLE 3: Using the trace_name Fixture (Recommended for Pytest)
# -----------------------------------------------------------------------------
# The trace_name fixture (defined in conftest.py) automatically provides
# the current test function name. This is the most "pytest-native" approach.
#
# Use this when:
#   - You want automatic trace naming based on test function names
#   - You prefer convention over configuration
#   - You want consistent naming without manual effort
#
# The fixture is defined in conftest.py as:
#
#     @pytest.fixture
#     def trace_name(request) -> str:
#         return request.node.name
#
# -----------------------------------------------------------------------------

def test_with_fixture_trace_name(flow_runner, trace_name):
    """
    This test uses the trace_name fixture from conftest.py.
    
    In the OpenAI trace dashboard, this will appear as:
        Trace: test_with_fixture_trace_name
    
    Note: We also use the flow_runner fixture here to avoid creating
    a new BaseFlowRunner instance in every test.
    """
    steps = """
    Open https://the-internet.herokuapp.com/login
    Wait for the login form to appear
    Type "tomsmith" into the Username field
    Type "SuperSecretPassword!" into the Password field
    Click the Login button
    Wait for the message "You logged into a secure area!" to appear
    """
    
    # Using fixtures: flow_runner and trace_name
    result = flow_runner.run_flow(
        steps, 
        RunResult, 
        trace_name=trace_name  # <-- Automatically set to "test_with_fixture_trace_name"
    )
    
    assert result.status == "PASS", f"Failed: {result.exception}"


# -----------------------------------------------------------------------------
# SUMMARY: Which approach to use?
# -----------------------------------------------------------------------------
#
# | Approach          | Trace Name                        | Best For                    |
# |-------------------|-----------------------------------|-----------------------------|
# | Default           | "web_flow"                        | Quick tests, prototyping    |
# | Explicit          | Your custom string                | Test case IDs, Jira links   |
# | Fixture           | Test function name (automatic)    | Production test suites      |
#
# For production test suites, we recommend using the fixture approach (Example 3)
# as it provides automatic, consistent naming without manual effort.
# -----------------------------------------------------------------------------
