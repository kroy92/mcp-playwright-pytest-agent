"""
Configuration Management for MCP Playwright Agent
==================================================

This module handles all configuration settings for the framework, including:
- Azure OpenAI credentials and API settings
- MCP server timeouts and directories
- Agent behavior settings (max turns, step timeouts)
- Logging configuration

Configuration Sources
---------------------
Settings are loaded from environment variables or a `.env` file.
Required variables:
- AZURE_OPENAI_DEPLOYMENT: Your Azure OpenAI deployment name
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL
- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key

Optional variables:
- D365_MFA_KEY: TOTP secret for MFA (if using MFA tool)
- VIEWPORT: Browser viewport size (default: "1600,900")
- TIMEOUT_SECONDS: Action timeout in ms (default: 5000)
- MAX_TURNS: Maximum agent conversation turns (default: 1000)
- MCP_CLIENT_TIMEOUT_SECONDS: MCP tool timeout (default: 120)

Usage
-----
    from playwright_agent.settings import get_settings, ConfigurationError
    
    try:
        settings = get_settings()
        print(f"Using deployment: {settings.azure_openai_deployment}")
    except ConfigurationError as e:
        print(f"Configuration error: {e}")

"""

from __future__ import annotations
import logging
import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file (override existing)
load_dotenv(override=True)

# Configure logging - reduce noise from external libraries
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("playwright_agent")

# Silence noisy loggers
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("anyio").setLevel(logging.WARNING)
logging.getLogger("mcp").setLevel(logging.WARNING)


class ConfigurationError(Exception):
    """
    Raised when required configuration is missing or invalid.
    
    This exception is raised during settings initialization if:
    - Required Azure OpenAI credentials are missing
    - Environment variables have invalid values
    - Configuration file cannot be read
    
    Example:
        try:
            settings = get_settings()
        except ConfigurationError as e:
            print(f"Please check your .env file: {e}")
    """
    pass


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class uses Pydantic's BaseSettings for automatic environment
    variable loading and validation. All settings can be overridden
    via environment variables or a .env file.
    
    Attributes:
        azure_openai_deployment: Name of the Azure OpenAI deployment
        azure_openai_endpoint: Azure OpenAI service endpoint URL
        azure_openai_api_key: API key for Azure OpenAI authentication
        azure_openai_api_version: API version (default: 2025-04-01-preview)
        mfa_key: Optional TOTP secret for MFA code generation
        mcp_isolated_dir: Directory for isolated browser data
        mcp_output_dir: Directory for MCP server outputs
        viewport: Browser viewport dimensions as "width,height"
        timeout_seconds: Default action timeout in milliseconds
        default_step_timeout_seconds: Step-level timeout for retries
        max_turns: Maximum conversation turns for the AI agent
        mcp_client_timeout_seconds: Timeout for MCP tool calls
    """
    
    # Azure OpenAI Configuration
    azure_openai_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_openai_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = "2025-04-01-preview"

    # D365 MFA Key
    mfa_key: str | None = os.getenv("D365_MFA_KEY")  # Optional, for TOTP generation

    # MCP / Playwright
    mcp_isolated_dir: Path = Path(".isolated")
    mcp_output_dir: Path = Path(".mcp-output")
    viewport: str = os.getenv("VIEWPORT", "1600,900")
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "5000"))

    # Agent behavior
    default_step_timeout_seconds: int = int(os.getenv("DEFAULT_STEP_TIMEOUT_SECONDS", "30"))
    max_turns: int = int(os.getenv("MAX_TURNS", "1000"))
    
    # MCP timeout settings
    mcp_client_timeout_seconds: int = int(os.getenv("MCP_CLIENT_TIMEOUT_SECONDS", "120"))

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    @field_validator("azure_openai_deployment", "azure_openai_endpoint", "azure_openai_api_key")
    @classmethod
    def validate_required_azure_fields(cls, v: str | None, info) -> str:
        if not v:
            raise ConfigurationError(
                f"{info.field_name.upper()} is required. Please set it in your .env file."
            )
        return v

    def validate_all(self) -> None:
        """Validate all required settings are present."""
        missing = []
        if not self.azure_openai_deployment:
            missing.append("AZURE_OPENAI_DEPLOYMENT")
        if not self.azure_openai_endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not self.azure_openai_api_key:
            missing.append("AZURE_OPENAI_API_KEY")
        
        if missing:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Please set them in your .env file."
            )


def get_settings() -> Settings:
    """Get validated settings instance."""
    try:
        s = Settings()
        s.validate_all()
        s.mcp_isolated_dir.mkdir(parents=True, exist_ok=True)
        s.mcp_output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Settings loaded successfully")
        return s
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        raise ConfigurationError(f"Failed to initialize settings: {e}") from e