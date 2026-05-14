"""Generated-client fixtures for integration tests."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from petstore_openapi_client import ApiClient, Configuration
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.api.user_api import UserApi


@pytest.fixture
def api_key() -> str:
    """Provide the API key for authentication, defaulting to dev-api-key."""
    return os.getenv("PETSTORE_API_KEY", "dev-api-key")


@pytest.fixture
def configuration(api_key: str) -> Configuration:
    """Provide generated client configuration for integration tests."""
    return Configuration(api_key={"APIKeyHeader": api_key})


@pytest_asyncio.fixture
async def openapi_api_client(
    configuration: Configuration,
) -> AsyncGenerator[ApiClient, None]:
    """Provide an async generated API client instance."""
    async with ApiClient(configuration=configuration) as client:
        yield client


@pytest_asyncio.fixture
async def pet_api_client(openapi_api_client: ApiClient) -> AsyncGenerator[PetApi, None]:
    """Provide PetApi backed by the generated API client."""
    yield PetApi(api_client=openapi_api_client)


@pytest_asyncio.fixture
async def user_api_client(
    openapi_api_client: ApiClient,
) -> AsyncGenerator[UserApi, None]:
    """Provide UserApi backed by the generated API client."""
    yield UserApi(api_client=openapi_api_client)
