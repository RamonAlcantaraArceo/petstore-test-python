"""Integration tests – cross-component scenarios.

Integration tests verify that multiple components work together correctly
(e.g. creating a pet and then querying it, verifying the data round-trips
through the full API stack).
"""

from __future__ import annotations

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_that
from framework.factories import PetFactory


@allure.feature("Pet Lifecycle")
@allure.story("Full CRUD lifecycle")
@pytest.mark.integration
class TestPetLifecycleIntegration:
    """Full pet lifecycle: create → read → update → delete."""

    @allure.title("Pet can be created, read, updated, and deleted in sequence")
    def test_create_read_update_delete_pet(self, api_client: PetstoreApiClient) -> None:
        """A pet should be readable and updatable after creation, then gone after deletion."""
        pet_data = PetFactory.build(status="available")

        with allure.step("Create a new pet"):
            created = api_client.add_pet(
                name=pet_data["name"],
                status="available",
                photoUrls=pet_data["photoUrls"],
            )
            pet_id = created["id"]
            assert_that(created["name"]).equals(pet_data["name"])

        try:
            with allure.step("Read the created pet"):
                fetched = api_client.get_pet(pet_id)
                assert_that(fetched["id"]).equals(pet_id)
                assert_that(fetched["name"]).equals(pet_data["name"])

            with allure.step("Update pet name and status"):
                updated = api_client.update_pet(
                    pet_id, name="UpdatedViaIntegration", status="pending"
                )
                assert_that(updated["name"]).equals("UpdatedViaIntegration")
                assert_that(updated["status"]).equals("pending")

            with allure.step("Verify update persisted"):
                re_fetched = api_client.get_pet(pet_id)
                assert_that(re_fetched["name"]).equals("UpdatedViaIntegration")

        finally:
            with allure.step("Delete the pet"):
                api_client.delete_pet(pet_id)

        with allure.step("Verify pet is no longer found (404)"):
            response = api_client.raw_get(f"/pet/{pet_id}")
            assert_that(response.status_code).equals(404)

    @allure.title("Multiple pets with the same status all appear in findByStatus")
    def test_multiple_pets_findable_by_status(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Pets created with the same status should all appear in findByStatus."""
        created_ids: list[int] = []

        try:
            with allure.step("Create three pets with status 'available'"):
                for _ in range(3):
                    pet = api_client.add_pet(
                        name=PetFactory.build()["name"],
                        status="available",
                        photoUrls=[],
                    )
                    created_ids.append(pet["id"])

            with allure.step("Find all pets with status 'available'"):
                pets = api_client.find_pets_by_status("available")
                found_ids = {p["id"] for p in pets}

            with allure.step("Verify all created pets appear in results"):
                for pet_id in created_ids:
                    assert_that(pet_id in found_ids).is_true()

        finally:
            for pet_id in created_ids:
                try:
                    api_client.delete_pet(pet_id)
                except Exception:
                    pass


@allure.feature("User-Pet Interaction")
@allure.story("Authenticated user manages pets")
@pytest.mark.integration
class TestUserPetIntegration:
    """Verify user actions interact correctly with the pet data model."""

    @allure.title("Authenticated user can add and retrieve a pet")
    def test_authenticated_user_can_add_and_retrieve_pet(
        self, authenticated_api_client: PetstoreApiClient
    ) -> None:
        """A logged-in user should be able to create and retrieve pets."""
        with allure.step("Verify client is authenticated"):
            assert_that(authenticated_api_client.is_logged_in()).is_true()

        with allure.step("Add a pet as authenticated user"):
            pet = authenticated_api_client.add_pet(
                name="AuthenticatedPet", status="available", photoUrls=[]
            )
        try:
            with allure.step("Retrieve and verify the pet"):
                fetched = authenticated_api_client.get_pet(pet["id"])
                assert_that(fetched["name"]).equals("AuthenticatedPet")
        finally:
            authenticated_api_client.delete_pet(pet["id"])
