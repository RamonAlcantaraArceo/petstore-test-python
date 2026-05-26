"""DB-layer tests – order persistence assertions.

These tests verify that order CRUD operations are correctly reflected in the
underlying PostgreSQL database, independently of the API response.
"""

from __future__ import annotations

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_db_record
from framework.db_client import PetstoreDbClient
from framework.factories import PetFactory


@allure.feature("Orders – DB layer")
@allure.story("Create order persists to DB")
@pytest.mark.db
class TestOrderDbCreate:
    """Assert that placing an order via the API persists the row to the DB."""

    @allure.title("New order row exists in DB with correct pet_id and status")
    def test_create_order_persists_in_db(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        pet_data = PetFactory.build(status="available")
        pet = api_client.add_pet(
            name=pet_data["name"],
            status=pet_data["status"],
            photoUrls=pet_data["photoUrls"],
        )
        order = api_client.place_order(pet_id=pet["id"], quantity=1, status="placed")
        try:
            with allure.step("Verify row exists in orders table"):
                row = db_client.get_order(order["id"])
                (
                    assert_db_record(row)
                    .exists()
                    .field_equals("pet_id", pet["id"])
                    .field_equals("status", "placed")
                )
        finally:
            api_client.delete_order(order["id"])
            api_client.delete_pet(pet["id"])

    @allure.title("New order row contains all expected fields")
    def test_create_order_row_has_expected_fields(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        pet_data = PetFactory.build(status="available")
        pet = api_client.add_pet(
            name=pet_data["name"],
            status=pet_data["status"],
            photoUrls=pet_data["photoUrls"],
        )
        order = api_client.place_order(pet_id=pet["id"], quantity=2, status="placed")
        try:
            with allure.step("Verify all expected columns are present"):
                row = db_client.get_order(order["id"])
                (
                    assert_db_record(row)
                    .exists()
                    .has_field("id")
                    .has_field("pet_id")
                    .has_field("quantity")
                    .has_field("status")
                    .has_field("complete")
                )
        finally:
            api_client.delete_order(order["id"])
            api_client.delete_pet(pet["id"])


@allure.feature("Orders – DB layer")
@allure.story("Delete order removes row from DB")
@pytest.mark.db
class TestOrderDbDelete:
    """Assert that deleting an order via the API removes the row from the DB."""

    @allure.title("Deleted order row is absent from DB")
    def test_delete_order_removes_row_from_db(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        pet_data = PetFactory.build(status="available")
        pet = api_client.add_pet(
            name=pet_data["name"],
            status=pet_data["status"],
            photoUrls=pet_data["photoUrls"],
        )
        order = api_client.place_order(pet_id=pet["id"], quantity=1, status="placed")
        order_id = order["id"]

        try:
            with allure.step("Delete order via API"):
                api_client.delete_order(order_id)

            with allure.step("Verify row is gone from DB"):
                row = db_client.get_order(order_id)
                assert_db_record(row).is_deleted()
        finally:
            api_client.delete_pet(pet["id"])
