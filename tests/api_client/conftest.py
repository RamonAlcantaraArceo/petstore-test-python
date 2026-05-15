"""API-specific fixtures for the tests/api suite."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest_asyncio
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.models.pet import Pet
from petstore_openapi_client.models.pet_create import PetCreate

from framework.factories import PetFactory


@pytest_asyncio.fixture()
async def new_pet(gen_pet_api_client: PetApi) -> AsyncGenerator[Pet, None]:
    """Create a pet via the API and yield it; delete it after the test."""
    data = PetFactory.build(status="available")
    created: Pet = await gen_pet_api_client.add_pet(
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
        await gen_pet_api_client.delete_pet(pet_id=created.id)
    except Exception:
        pass
