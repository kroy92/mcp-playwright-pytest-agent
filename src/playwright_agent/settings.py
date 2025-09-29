from __future__ import annotations
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = "2025-04-01-preview"

    # D365 MFA Key
    mfa_key: str  = os.getenv("D365_MFA_KEY")  # Optional, for TOTP generation

    # MCP / Playwright
    mcp_isolated_dir: Path = Path(".isolated")
    mcp_output_dir: Path = Path(".mcp-output")
    viewport: str = os.getenv("VIEWPORT", "1600,900")
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "5000"))

    # Agent behavior
    default_step_timeout_seconds: int = int(os.getenv("DEFAULT_STEP_TIMEOUT_SECONDS", "30"))
    max_turns: int = int(os.getenv("MAX_TURNS", "1000"))

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

def get_settings() -> Settings:
    s = Settings()
    s.mcp_isolated_dir.mkdir(parents=True, exist_ok=True)
    s.mcp_output_dir.mkdir(parents=True, exist_ok=True)
    return s