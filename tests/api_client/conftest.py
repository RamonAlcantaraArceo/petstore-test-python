"""API-specific fixtures for the tests/api suite."""

from __future__ import annotations

from collections.abc import Generator, AsyncGenerator
import os

import pytest
import pytest_asyncio
from framework.factories import PetFactory
from petstore_openapi_client import Configuration, ApiClient
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.models.pet import Pet
from petstore_openapi_client.models.pet_create import PetCreate


@pytest.fixture
def api_key() -> str:
    """Provide the API key for authentication, defaulting to 'dev-api-key'."""
    return os.getenv("API_KEY", "dev-api-key")

@pytest.fixture
def configuration(api_key: str) -> Configuration:
    """Provide a configured API client for tests."""
    configuration = Configuration(
        # host=_get_default_host(),
        api_key={"APIKeyHeader": api_key}
    )

    return configuration

@pytest_asyncio.fixture()
async def api_client(configuration: Configuration) -> AsyncGenerator[ApiClient, None]:
    """Provide an API client instance for tests."""
    async with ApiClient(configuration = configuration) as client:
        yield client

@pytest_asyncio.fixture()
async def pet_api_client(api_client: ApiClient) -> AsyncGenerator[PetApi, None]:
    """Provide a PetApi instance for tests."""
    pet_api = PetApi(api_client)

    yield pet_api

@pytest_asyncio.fixture()
async def new_pet(pet_api_client: PetApi) -> AsyncGenerator[Pet, None]:
    """Create a pet via the API and yield it; delete it after the test."""
    data = PetFactory.build(status="available")
    created: Pet = await pet_api_client.add_pet(
        pet_create=PetCreate(
            name=data["name"],
            status=data["status"],
            photoUrls=data["photoUrls"],
        )
    )
    assert created.id is not None, "Created pet should have an ID"

    yield created
    # Cleanup – ignore 404 in case the test itself deleted the pet
    try:
        await pet_api_client.delete_pet(pet_id=created.id)
    except Exception:
        pass
