from __future__ import annotations
import pyotp
from playwright_agent.settings import get_settings

# Provided by your agents SDK
from agents import function_tool  # type: ignore[import-not-found]


@function_tool
def get_totp() -> str:
    """Generate a TOTP MFA code (optional)."""
    mfa_key = getattr(get_settings(), "mfa_key", None)  # Not required by default
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()
