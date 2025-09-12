from __future__ import annotations
from openai import AsyncAzureOpenAI
from playwright_agent.settings import Settings

def make_async_client(settings: Settings) -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
    )
