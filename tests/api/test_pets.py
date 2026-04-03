"""API tests – pet CRUD operations.

Covers the core Petstore pet endpoints using fluent assertions.
"""

from __future__ import annotations

import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_response, assert_that
from framework.factories import PetFactory


@pytest.mark.api
class TestAddPet:
    """Tests for POST /pet."""

    def test_add_pet_returns_created_pet(self, api_client: PetstoreApiClient) -> None:
        """Adding a pet should return the created pet with an id."""
        pet_data = PetFactory.build(status="available")

        pet = api_client.add_pet(
            name=pet_data["name"],
            status=pet_data["status"],
            photoUrls=pet_data["photoUrls"],
        )

        try:
            assert_that(pet).has_keys("id", "name", "status")
            assert_that(pet["name"]).equals(pet_data["name"])
            assert_that(pet["status"]).equals("available")
            assert_that(pet["id"]).is_greater_than(0)
        finally:
            api_client.delete_pet(pet["id"])

    def test_add_pet_with_sold_status(self, api_client: PetstoreApiClient) -> None:
        pet = api_client.add_pet(name="DeprecatedDog", status="sold", photoUrls=[])
        try:
            assert_that(pet["status"]).equals("sold")
        finally:
            api_client.delete_pet(pet["id"])


@pytest.mark.api
class TestGetPet:
    """Tests for GET /pet/{petId}."""

    def test_get_existing_pet(
        self, api_client: PetstoreApiClient, new_pet: dict
    ) -> None:
        """Fetching a known pet by id should return the correct record."""
        fetched = api_client.get_pet(new_pet["id"])

        assert_that(fetched["id"]).equals(new_pet["id"])
        assert_that(fetched["name"]).equals(new_pet["name"])

    def test_get_nonexistent_pet_raises(self, api_client: PetstoreApiClient) -> None:
        """Fetching an id that does not exist should result in a 404 response."""
        response = api_client.raw_get("/pet/999999999999")

        assert_response(response).is_not_found()


@pytest.mark.api
class TestUpdatePet:
    """Tests for PUT /pet."""

    def test_update_pet_name(
        self, api_client: PetstoreApiClient, new_pet: dict
    ) -> None:
        """Updating a pet's name should persist the change."""
        updated = api_client.update_pet(new_pet["id"], name="UpdatedName")

        assert_that(updated["name"]).equals("UpdatedName")
        assert_that(updated["id"]).equals(new_pet["id"])

    def test_update_pet_status(
        self, api_client: PetstoreApiClient, new_pet: dict
    ) -> None:
        updated = api_client.update_pet(new_pet["id"], status="sold")

        assert_that(updated["status"]).equals("sold")


@pytest.mark.api
class TestDeletePet:
    """Tests for DELETE /pet/{petId}."""

    def test_delete_pet_removes_it(self, api_client: PetstoreApiClient) -> None:
        """A pet should no longer be found after deletion."""
        pet = api_client.add_pet(name="ToDelete", status="available", photoUrls=[])
        pet_id = pet["id"]

        api_client.delete_pet(pet_id)

        response = api_client.raw_get(f"/pet/{pet_id}")
        assert_response(response).is_not_found()


@pytest.mark.api
class TestFindByStatus:
    """Tests for GET /pet/findByStatus."""

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_by_status_returns_list(
        self, api_client: PetstoreApiClient, status: str
    ) -> None:
        """findByStatus should return a non-empty list for every valid status."""
        pets = api_client.find_pets_by_status(status)

        assert_that(pets).is_instance_of(list)
        for pet in pets:
            assert_that(pet).has_key("id")

    def test_all_returned_pets_match_requested_status(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Every pet returned for 'available' should have status == 'available'."""
        pets = api_client.find_pets_by_status("available")

        assert_that(pets).is_not_empty()
        for pet in pets:
            assert_that(pet.get("status")).equals("available")
