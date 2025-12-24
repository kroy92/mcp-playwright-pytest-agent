"""
Azure OpenAI Client Factory
===========================

This module provides a factory function for creating Azure OpenAI clients
configured with the application settings.

The client is used by the AgentRunner to communicate with Azure OpenAI
for AI-powered test execution.

Usage
-----
    from playwright_agent.integrations.azure_openai import make_async_client
    from playwright_agent.settings import get_settings
    
    settings = get_settings()
    async with make_async_client(settings) as client:
        # Use client for OpenAI API calls
        response = await client.chat.completions.create(...)

Configuration
-------------
The client requires these settings (from .env file):
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI service endpoint
- AZURE_OPENAI_API_KEY: Your API key
- AZURE_OPENAI_API_VERSION: API version (default: 2025-04-01-preview)

"""

from __future__ import annotations
from openai import AsyncAzureOpenAI
from playwright_agent.settings import Settings


def make_async_client(settings: Settings) -> AsyncAzureOpenAI:
    """
    Create an async Azure OpenAI client from settings.
    
    Args:
        settings: Application settings with Azure OpenAI configuration
        
    Returns:
        AsyncAzureOpenAI client configured for the specified endpoint
        
    Example:
        async with make_async_client(settings) as client:
            agent = Agent(model=OpenAIResponsesModel(openai_client=client, ...))
    """
    return AsyncAzureOpenAI(
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,

