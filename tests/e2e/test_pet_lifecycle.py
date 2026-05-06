"""End-to-end tests – full user journeys across the petstore system.

E2E tests exercise complete workflows from the user's perspective:
login → perform action → verify outcome → cleanup.
"""

from __future__ import annotations

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_that
from framework.factories import PetFactory, UserFactory


@allure.feature("Pet Adoption Journey")
@pytest.mark.e2e
class TestPetAdoptionJourney:
    """End-to-end: browsing and 'adopting' (status change) a pet."""

    @allure.story("Pet adoption flow")
    @allure.title("Available pet can be purchased and status changes to sold")
    def test_available_pet_can_be_marked_as_sold(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Simulate a user finding an available pet and purchasing it (→ sold)."""
        with allure.step("Add a new available pet"):
            pet = api_client.add_pet(
                name=PetFactory.build()["name"],
                status="available",
                photoUrls=[],
            )
        try:
            with allure.step("Verify pet is available"):
                assert_that(pet["status"]).equals("available")

            with allure.step("Purchase the pet (status → sold)"):
                updated = api_client.update_pet(pet["id"], status="sold")
                assert_that(updated["status"]).equals("sold")

            with allure.step("Verify pet no longer appears in available list"):
                available_after = api_client.find_pets_by_status("available")
                available_ids = {p["id"] for p in available_after}
                assert_that(pet["id"] in available_ids).is_false()

            with allure.step("Verify pet appears in sold list"):
                sold_pets = api_client.find_pets_by_status("sold")
                sold_ids = {p["id"] for p in sold_pets}
                assert_that(pet["id"] in sold_ids).is_true()

        finally:
            api_client.delete_pet(pet["id"])


@allure.feature("User Registration Journey")
@pytest.mark.e2e
class TestUserRegistrationJourney:
    """End-to-end: register a new user, log in, and log out."""

    @allure.story("Full registration and login flow")
    @allure.title("New user can register, log in, view profile, and log out")
    def test_register_login_logout_journey(self, api_client: PetstoreApiClient) -> None:
        """A newly registered user should be able to log in and then log out."""
        user_data = UserFactory.build()
        username = user_data["username"]
        password = user_data["password"]

        with allure.step("Register a new user"):
            api_client.create_user(username, password, email=user_data["email"])

        try:
            with allure.step("Log in with the new user credentials"):
                api_client.login(username, password)
                assert_that(api_client.is_logged_in()).is_true()

            with allure.step("Verify user profile is accessible"):
                profile = api_client.get_user(username)
                assert_that(profile["username"]).equals(username)

            with allure.step("Log out and verify session is cleared"):
                api_client.logout()
                assert_that(api_client.is_logged_in()).is_false()

        finally:
            try:
                api_client.delete_user(username)
            except Exception:
                pass
