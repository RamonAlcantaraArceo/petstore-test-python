"""API tests - pet CRUD operations.

Covers the core Petstore pet endpoints using fluent assertions.
"""

from __future__ import annotations

import pytest
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.models.pet_status import PetStatus

from framework.assertions import assert_that


@pytest.mark.usefixtures("new_pet")
@pytest.mark.asyncio
# @allure.title("All pets returned for 'available' have status 'available'")
async def test_all_returned_pets_match_requested_status(
    gen_pet_api_client: PetApi,
) -> None:
    """Every pet returned for 'available' should have status == 'available'."""

    pets = await gen_pet_api_client.find_pets_by_status(status=PetStatus.AVAILABLE)
    assert_that(pets).is_not_empty()
    for pet in pets:
        assert_that(pet.status).equals(PetStatus.AVAILABLE)
