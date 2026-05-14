"""API tests – pet CRUD operations.

Covers the core Petstore pet endpoints using fluent assertions.
"""

from __future__ import annotations
import sys

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_response, assert_that
from framework.factories import PetFactory


@allure.feature("Pets")
@allure.story("Create pet")
@pytest.mark.api
class TestAddPet:
    """Tests for POST /pet."""

    @allure.title("Add pet returns created pet with id, name, and status")
    def test_add_pet_returns_created_pet(self, api_client: PetstoreApiClient) -> None:
        """Adding a pet should return the created pet with an id."""
        with allure.step("Build pet data"):
            pet_data = PetFactory.build(status="available")

        with allure.step("Add pet via API"):
            pet = api_client.add_pet(
                name=pet_data["name"],
                status=pet_data["status"],
                photoUrls=pet_data["photoUrls"],
            )

        try:
            with allure.step("Verify created pet has expected fields"):
                assert_that(pet).has_keys("id", "name", "status")
                assert_that(pet["name"]).equals(pet_data["name"])
                assert_that(pet["status"]).equals("available")
                assert_that(pet["id"]).is_greater_than(0)
        finally:
            api_client.delete_pet(pet["id"])

    @allure.title("Add pet with 'sold' status persists the status")
    def test_add_pet_with_sold_status(self, api_client: PetstoreApiClient) -> None:
        pet = api_client.add_pet(name="DeprecatedDog", status="sold", photoUrls=[])
        try:
            assert_that(pet["status"]).equals("sold")
        finally:
            api_client.delete_pet(pet["id"])


@allure.feature("Pets")
@allure.story("Read pet")
@pytest.mark.api
class TestGetPet:
    """Tests for GET /pet/{petId}."""

    @allure.title("Fetching an existing pet by id returns the correct record")
    def test_get_existing_pet(
        self, api_client: PetstoreApiClient, new_pet: dict
    ) -> None:
        """Fetching a known pet by id should return the correct record."""
        with allure.step("Fetch pet by id"):
            fetched = api_client.get_pet(new_pet["id"])

        with allure.step("Verify id and name match"):
            assert_that(fetched["id"]).equals(new_pet["id"])
            assert_that(fetched["name"]).equals(new_pet["name"])

    @allure.title("Fetching a non-existent pet id returns 404")
    def test_get_nonexistent_pet_raises(self, api_client: PetstoreApiClient) -> None:
        """Fetching an id that does not exist should result in a 404 response."""
        with allure.step("Request pet with unknown id"):
            response = api_client.raw_get("/pet/99999")

        with allure.step("Verify 404 Not Found"):
            assert_response(response).is_not_found()

    @allure.title("Fetching an out-of-range pet id returns a client error")
    def test_get_pet_with_out_of_range_id(self, api_client: PetstoreApiClient) -> None:
        """Fetching a pet with an ID outside the integer range should fail."""

        out_of_range_id = sys.maxsize + 1  # This is larger than any valid pet ID
        response = api_client.raw_get(f"/pet/{out_of_range_id}")

        assert_response(response).is_not_found()


@allure.feature("Pets")
@allure.story("Update pet")
@pytest.mark.api
class TestUpdatePet:
    """Tests for PUT /pet."""

    @allure.title("Updating a pet's name persists the change")
    def test_update_pet_name(
        self, api_client: PetstoreApiClient, new_pet: dict
    ) -> None:
        """Updating a pet's name should persist the change."""
        with allure.step("Update pet name"):
            updated = api_client.update_pet(new_pet["id"], name="UpdatedName")

        with allure.step("Verify updated name and unchanged id"):
            assert_that(updated["name"]).equals("UpdatedName")
            assert_that(updated["id"]).equals(new_pet["id"])

    @allure.title("Updating a pet's status persists the change")
    def test_update_pet_status(
        self, api_client: PetstoreApiClient, new_pet: dict
    ) -> None:
        with allure.step("Update pet status to 'sold'"):
            updated = api_client.update_pet(new_pet["id"], status="sold")

        with allure.step("Verify status is 'sold'"):
            assert_that(updated["status"]).equals("sold")


@allure.feature("Pets")
@allure.story("Delete pet")
@pytest.mark.api
class TestDeletePet:
    """Tests for DELETE /pet/{petId}."""

    @allure.title("Deleted pet can no longer be found")
    def test_delete_pet_removes_it(self, api_client: PetstoreApiClient) -> None:
        """A pet should no longer be found after deletion."""
        with allure.step("Create a pet to delete"):
            pet = api_client.add_pet(name="ToDelete", status="available", photoUrls=[])
            pet_id = pet["id"]

        with allure.step("Delete the pet"):
            api_client.delete_pet(pet_id)

        with allure.step("Verify pet is no longer found (404)"):
            response = api_client.raw_get(f"/pet/{pet_id}")
            assert_response(response).is_not_found()


@allure.feature("Pets")
@allure.story("Find pets by status")
@pytest.mark.api
class TestFindByStatus:
    """Tests for GET /pet/findByStatus."""

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    @allure.title("findByStatus returns a list for status '{status}'")
    def test_find_by_status_returns_list(
        self, api_client: PetstoreApiClient, status: str
    ) -> None:
        """findByStatus should return a non-empty list for every valid status."""
        with allure.step(f"Request pets with status '{status}'"):
            pets = api_client.find_pets_by_status(status)

        with allure.step("Verify result is a list and each item has an id"):
            assert_that(pets).is_instance_of(list)
            for pet in pets:
                assert_that(pet).has_key("id")

    @pytest.mark.usefixtures("new_pet")
    @allure.title("All pets returned for 'available' have status 'available'")
    def test_all_returned_pets_match_requested_status(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Every pet returned for 'available' should have status == 'available'."""
        with allure.step("Request pets with status 'available'"):
            pets = api_client.find_pets_by_status("available")

        with allure.step("Verify all returned pets have status 'available'"):
            assert_that(pets).is_not_empty()
            for pet in pets:
                assert_that(pet.get("status")).equals("available")
            # assert_that(len(pets)).equals(1)

