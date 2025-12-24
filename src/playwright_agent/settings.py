from __future__ import annotations
import logging
import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

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
    """Raised when required configuration is missing or invalid."""
    pass


class Settings(BaseSettings):
    # Azure OpenAI
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