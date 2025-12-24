"""
Custom Tools for AI Agent
=========================

This module provides custom tools (functions) that the AI agent can call
during test execution. Tools extend the agent's capabilities beyond
browser automation.

Built-in Tools
--------------
- `get_totp`: Generate TOTP MFA codes for multi-factor authentication

Creating Custom Tools
---------------------
Tools are Python functions decorated with `@function_tool`. The docstring
becomes the tool description that the AI uses to decide when to call it.

    from agents import function_tool
    
    @function_tool
    def get_test_data(user_type: str) -> dict:
        '''Get test user credentials for the specified user type.
        
        Args:
            user_type: Type of user ("admin", "standard", "guest")
            
        Returns:
            Dictionary with username and password
        '''
        users = {
            "admin": {"username": "admin@test.com", "password": "Admin123"},
            "standard": {"username": "user@test.com", "password": "User123"},
        }
        return users.get(user_type, {})

Using Tools in Tests
--------------------
Pass tools to `run()` to make them available to the agent:

    result = await runner.run(
        steps,
        RunResult,
        tools=[get_totp, get_test_data]  # Agent can call these
    )

"""

from __future__ import annotations
import pyotp
from playwright_agent.settings import get_settings

# OpenAI Agents SDK decorator for creating tools
from agents import function_tool  # type: ignore[import-not-found]


@function_tool
def get_totp() -> str:
    """
    Generate a TOTP (Time-based One-Time Password) MFA code.
    
    This tool is used during login flows that require multi-factor
    authentication. It generates a 6-digit code from the configured
    MFA secret key.
    
    Returns:
        A 6-digit TOTP code valid for 30 seconds
        
    Raises:
        ValueError: If D365_MFA_KEY is not configured in settings
        
    Configuration:
        Set D365_MFA_KEY in your .env file with the TOTP secret
    """
    mfa_key = getattr(get_settings(), "mfa_key", None)
    if not mfa_key:
        raise ValueError("MFA key is not configured. Set D365_MFA_KEY in .env file.")
    return pyotp.TOTP(mfa_key).now()
