"""DB-layer tests – pet persistence assertions.

These tests verify that pet CRUD operations are correctly reflected in the
underlying PostgreSQL database, independently of the API response.
"""

from __future__ import annotations

from typing import Any

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_db_record
from framework.db_client import PetstoreDbClient
from framework.factories import PetFactory


@allure.feature("Pets – DB layer")
@allure.story("Create pet persists to DB")
@pytest.mark.db
class TestPetDbCreate:
    """Assert that creating a pet via the API persists the row to the DB."""

    @allure.title("New pet row exists in DB with correct name and status")
    def test_create_pet_persists_in_db(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        data = PetFactory.build(status="available")
        pet = api_client.add_pet(
            name=data["name"],
            status=data["status"],
            photoUrls=data["photoUrls"],
        )
        try:
            with allure.step("Verify row exists in pets table"):
                row = db_client.get_pet(pet["id"])
                assert_db_record(row).exists().field_equals("name", pet["name"]).field_equals(
                    "status", "available"
                )
        finally:
            api_client.delete_pet(pet["id"])

    @allure.title("New pet row contains all expected fields")
    def test_create_pet_row_has_expected_fields(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        data = PetFactory.build(status="pending")
        pet = api_client.add_pet(
            name=data["name"],
            status=data["status"],
            photoUrls=data["photoUrls"],
        )
        try:
            with allure.step("Verify all expected columns are present"):
                row = db_client.get_pet(pet["id"])
                (
                    assert_db_record(row)
                    .exists()
                    .has_field("id")
                    .has_field("name")
                    .has_field("status")
                    .has_field("photo_urls")
                )
        finally:
            api_client.delete_pet(pet["id"])


@allure.feature("Pets – DB layer")
@allure.story("Update pet persists to DB")
@pytest.mark.db
class TestPetDbUpdate:
    """Assert that updating a pet via the API is reflected in the DB."""

    @allure.title("Updated pet name is persisted in DB")
    def test_update_pet_name_reflected_in_db(
        self,
        db_pet: dict[str, Any],
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        pet_id = db_pet["id"]
        with allure.step("Update pet name via API"):
            api_client.update_pet(pet_id, name="DbUpdatedName")

        with allure.step("Verify updated name in DB"):
            row = db_client.get_pet(pet_id)
            assert_db_record(row).exists().field_equals("name", "DbUpdatedName")

    @allure.title("Updated pet status is persisted in DB")
    def test_update_pet_status_reflected_in_db(
        self,
        db_pet: dict[str, Any],
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        pet_id = db_pet["id"]
        with allure.step("Update status to 'sold' via API"):
            api_client.update_pet(pet_id, status="sold")

        with allure.step("Verify status is 'sold' in DB"):
            row = db_client.get_pet(pet_id)
            assert_db_record(row).exists().field_equals("status", "sold")


@allure.feature("Pets – DB layer")
@allure.story("Delete pet removes row from DB")
@pytest.mark.db
class TestPetDbDelete:
    """Assert that deleting a pet via the API removes the row from the DB."""

    @allure.title("Deleted pet row is absent from DB")
    def test_delete_pet_removes_row_from_db(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        data = PetFactory.build(status="available")
        pet = api_client.add_pet(
            name=data["name"],
            status=data["status"],
            photoUrls=data["photoUrls"],
        )
        pet_id = pet["id"]

        with allure.step("Delete pet via API"):
            api_client.delete_pet(pet_id)

        with allure.step("Verify row is gone from DB"):
            row = db_client.get_pet(pet_id)
            assert_db_record(row).is_deleted()
