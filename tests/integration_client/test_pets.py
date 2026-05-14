"""Integration tests mirrored from tests/integration using generated client."""

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


@pytest.mark.integration
@pytest.mark.asyncio
class TestPetLifecycleIntegrationClient:
    """Full pet lifecycle: create -> read -> update -> delete."""

    async def test_create_read_update_delete_pet(self, pet_api_client: PetApi) -> None:
        """A pet should be readable/updatable after creation, then gone after deletion."""
        pet_data = PetFactory.build(status="available")

        created = await pet_api_client.add_pet(
            pet_create=PetCreate(
                name=pet_data["name"],
                status=PetStatus.AVAILABLE,
                photoUrls=pet_data["photoUrls"],
            )
        )
        assert_that(created.id).is_not_none()
        assert_that(created.name).equals(pet_data["name"])

        assert created.id is not None
        pet_id = created.id

        try:
            fetched = await pet_api_client.get_pet_by_id(pet_id=pet_id)
            assert_that(fetched.id).equals(pet_id)
            assert_that(fetched.name).equals(pet_data["name"])

            updated = await pet_api_client.update_pet(
                pet_update=PetUpdate(
                    id=pet_id,
                    name="UpdatedViaIntegration",
                    status=PetStatus.PENDING,
                    photoUrls=fetched.photo_urls,
                )
            )
            assert_that(updated.name).equals("UpdatedViaIntegration")
            assert_that(updated.status).equals(PetStatus.PENDING)

            re_fetched = await pet_api_client.get_pet_by_id(pet_id=pet_id)
            assert_that(re_fetched.name).equals("UpdatedViaIntegration")
        finally:
            await pet_api_client.delete_pet(pet_id=pet_id)

        with pytest.raises(ApiException) as exc_info:
            await pet_api_client.get_pet_by_id(pet_id=pet_id)
        assert_that(exc_info.value.status).equals(404)

    async def test_multiple_pets_findable_by_status(self, pet_api_client: PetApi) -> None:
        """Pets created with the same status should all appear in findByStatus."""
        created_ids: list[int] = []

        try:
            for _ in range(3):
                pet = await pet_api_client.add_pet(
                    pet_create=PetCreate(
                        name=PetFactory.build()["name"],
                        status=PetStatus.AVAILABLE,
                        photoUrls=[],
                    )
                )
                if pet.id is not None:
                    created_ids.append(pet.id)

            pets = await pet_api_client.find_pets_by_status(status=PetStatus.AVAILABLE)
            found_ids = {p.id for p in pets if p.id is not None}

            for pet_id in created_ids:
                assert_that(pet_id in found_ids).is_true()
        finally:
            for pet_id in created_ids:
                try:
                    await pet_api_client.delete_pet(pet_id=pet_id)
                except ApiException:
                    pass


@pytest.mark.integration
@pytest.mark.asyncio
class TestUserPetIntegrationClient:
    """Verify user operations and pet operations work together."""

    async def test_authenticated_user_can_add_and_retrieve_pet(
        self,
        user_api_client: UserApi,
        pet_api_client: PetApi,
    ) -> None:
        """A logged-in user should be able to create and retrieve pets."""
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

        pet_id: int | None = None
        try:
            login_result = await user_api_client.login_user(
                username=username,
                password=password,
            )
            assert_that(login_result).has_key("token")

            pet = await pet_api_client.add_pet(
                pet_create=PetCreate(
                    name="AuthenticatedPet",
                    status=PetStatus.AVAILABLE,
                    photoUrls=[],
                )
            )
            pet_id = pet.id
            assert_that(pet_id).is_not_none()

            assert pet_id is not None
            fetched = await pet_api_client.get_pet_by_id(pet_id=pet_id)
            assert_that(fetched.name).equals("AuthenticatedPet")

            logout_result = await user_api_client.logout_user()
            assert_that(logout_result).has_key("message")
        finally:
            if pet_id is not None:
                try:
                    await pet_api_client.delete_pet(pet_id=pet_id)
                except ApiException:
                    pass
            try:
                await user_api_client.delete_user(username=username)
            except ApiException:
                pass
