"""End-to-end tests – full user journeys across the petstore system.

E2E tests exercise complete workflows from the user's perspective:
login → perform action → verify outcome → cleanup.
"""

from __future__ import annotations

import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_that
from framework.factories import PetFactory, UserFactory


@pytest.mark.e2e
class TestPetAdoptionJourney:
    """End-to-end: browsing and 'adopting' (status change) a pet."""

    def test_available_pet_can_be_marked_as_sold(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Simulate a user finding an available pet and purchasing it (→ sold)."""
        # 1. Browse available pets
        available_pets = api_client.find_pets_by_status("available")
        assert_that(available_pets).is_not_empty()

        # 2. Pick the first one and verify it is available
        target = available_pets[0]
        assert_that(target["status"]).equals("available")

        # 3. Add a new available pet to represent the scenario cleanly
        pet = api_client.add_pet(
            name=PetFactory.build()["name"],
            status="available",
            photoUrls=[],
        )
        try:
            assert_that(pet["status"]).equals("available")

            # 4. "Purchase" the pet (status → sold)
            updated = api_client.update_pet(pet["id"], status="sold")
            assert_that(updated["status"]).equals("sold")

            # 5. Verify it no longer appears in the available list
            available_after = api_client.find_pets_by_status("available")
            available_ids = {p["id"] for p in available_after}
            assert_that(pet["id"] in available_ids).is_false()

            # 6. Verify it appears in the sold list
            sold_pets = api_client.find_pets_by_status("sold")
            sold_ids = {p["id"] for p in sold_pets}
            assert_that(pet["id"] in sold_ids).is_true()

        finally:
            api_client.delete_pet(pet["id"])


@pytest.mark.e2e
class TestUserRegistrationJourney:
    """End-to-end: register a new user, log in, and log out."""

    def test_register_login_logout_journey(self, api_client: PetstoreApiClient) -> None:
        """A newly registered user should be able to log in and then log out."""
        user_data = UserFactory.build()
        username = user_data["username"]
        password = user_data["password"]

        # 1. Register
        api_client.create_user(username, password, email=user_data["email"])

        try:
            # 2. Log in
            api_client.login(username, password)
            assert_that(api_client.is_logged_in()).is_true()

            # 3. Verify user profile exists
            profile = api_client.get_user(username)
            assert_that(profile["username"]).equals(username)

            # 4. Log out
            api_client.logout()
            assert_that(api_client.is_logged_in()).is_false()

        finally:
            # Cleanup: remove the test user
            try:
                api_client.delete_user(username)
            except Exception:
                pass
