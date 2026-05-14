"""End-to-end tests mirrored from tests/e2e using generated client."""

from __future__ import annotations

import pytest
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.api.user_api import UserApi
from petstore_openapi_client.exceptions import ApiException
from petstore_openapi_client.models.pet_create import PetCreate
from petstore_openapi_client.models.pet_status import PetStatus
from petstore_openapi_client.models.pet_update import PetUpdate
from petstore_openapi_client.models.user_create import UserCreate

from framework.assertions import assert_that
from framework.factories import PetFactory, UserFactory


@pytest.mark.e2e
@pytest.mark.asyncio
class TestPetAdoptionJourneyClient:
    """End-to-end: browsing and adopting a pet via generated client."""

    async def test_available_pet_can_be_marked_as_sold(
        self,
        pet_api_client: PetApi,
    ) -> None:
        """Simulate a user finding an available pet and purchasing it."""
        pet = await pet_api_client.add_pet(
            pet_create=PetCreate(
                name=PetFactory.build()["name"],
                status=PetStatus.AVAILABLE,
                photoUrls=[],
            )
        )

        assert_that(pet.id).is_not_none()
        assert_that(pet.status).equals(PetStatus.AVAILABLE)

        assert pet.id is not None
        pet_id = pet.id
        try:
            updated = await pet_api_client.update_pet(
                pet_update=PetUpdate(
                    id=pet_id,
                    name=pet.name,
                    status=PetStatus.SOLD,
                    photoUrls=pet.photo_urls,
                )
            )
            assert_that(updated.status).equals(PetStatus.SOLD)

            available_after = await pet_api_client.find_pets_by_status(
                status=PetStatus.AVAILABLE
            )
            available_ids = {p.id for p in available_after if p.id is not None}
            assert_that(pet_id in available_ids).is_false()

            sold_pets = await pet_api_client.find_pets_by_status(status=PetStatus.SOLD)
            sold_ids = {p.id for p in sold_pets if p.id is not None}
            assert_that(pet_id in sold_ids).is_true()
        finally:
            await pet_api_client.delete_pet(pet_id=pet_id)


@pytest.mark.e2e
@pytest.mark.asyncio
class TestUserRegistrationJourneyClient:
    """End-to-end: register user, log in, view profile, and log out."""

    async def test_register_login_logout_journey(
        self,
        user_api_client: UserApi,
    ) -> None:
        """A newly registered user should be able to log in and out."""
        user_data = UserFactory.build()
        username = user_data["username"]
        password = user_data["password"]

        await user_api_client.create_user(
            user_create=UserCreate(
                username=username,
                password=password,
                email=user_data["email"],
            )
        )

        try:
            login_result = await user_api_client.login_user(
                username=username,
                password=password,
            )
            assert_that(login_result).has_key("token")

            profile = await user_api_client.get_user_by_name(username=username)
            assert_that(profile.username).equals(username)

            logout_result = await user_api_client.logout_user()
            assert_that(logout_result).has_key("message")
        finally:
            try:
                await user_api_client.delete_user(username=username)
            except ApiException:
                pass
