"""DB-layer tests – user persistence assertions.

These tests verify that user CRUD operations are correctly reflected in the
underlying PostgreSQL database, independently of the API response.
"""

from __future__ import annotations

from typing import Any

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_db_record
from framework.db_client import PetstoreDbClient
from framework.factories import UserFactory


@allure.feature("Users – DB layer")
@allure.story("Create user persists to DB")
@pytest.mark.db
class TestUserDbCreate:
    """Assert that creating a user via the API persists the row to the DB."""

    @allure.title("New user row exists in DB with correct username and email")
    def test_create_user_persists_in_db(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        data = UserFactory.build()
        api_client.create_user(
            username=data["username"],
            firstName=data["firstName"],
            lastName=data["lastName"],
            email=data["email"],
            password=data["password"],
            phone=data["phone"],
            userStatus=data["userStatus"],
        )
        try:
            with allure.step("Verify row exists in users table"):
                row = db_client.get_user(data["username"])
                (
                    assert_db_record(row)
                    .exists()
                    .field_equals("username", data["username"])
                    .field_equals("email", data["email"])
                )
        finally:
            api_client.delete_user(data["username"])

    @allure.title("New user row contains all expected fields")
    def test_create_user_row_has_expected_fields(
        self,
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        data = UserFactory.build()
        api_client.create_user(
            username=data["username"],
            firstName=data["firstName"],
            lastName=data["lastName"],
            email=data["email"],
            password=data["password"],
            phone=data["phone"],
            userStatus=data["userStatus"],
        )
        try:
            with allure.step("Verify all expected columns are present"):
                row = db_client.get_user(data["username"])
                (
                    assert_db_record(row)
                    .exists()
                    .has_field("id")
                    .has_field("username")
                    .has_field("email")
                    .has_field("first_name")
                    .has_field("last_name")
                )
        finally:
            api_client.delete_user(data["username"])


@allure.feature("Users – DB layer")
@allure.story("Delete user removes row from DB")
@pytest.mark.db
class TestUserDbDelete:
    """Assert that deleting a user via the API removes the row from the DB."""

    @allure.title("Deleted user row is absent from DB")
    def test_delete_user_removes_row_from_db(
        self,
        db_user: dict[str, Any],
        api_client: PetstoreApiClient,
        db_client: PetstoreDbClient,
    ) -> None:
        username = db_user["username"]

        with allure.step("Delete user via API"):
            api_client.delete_user(username)

        with allure.step("Verify row is gone from DB"):
            row = db_client.get_user(username)
            assert_db_record(row).is_deleted()
