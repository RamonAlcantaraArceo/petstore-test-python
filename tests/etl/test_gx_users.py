"""ETL data-quality tests for the ``users`` table using Great Expectations.

Validates structural and domain constraints on the ``users`` table that
complement the API-level assertions.
"""

from __future__ import annotations

from typing import Any

import allure
import great_expectations as gx
import pytest


@allure.feature("ETL – users table")
@allure.story("Schema and data quality")
@pytest.mark.etl
class TestGxUsers:
    """Great Expectations validations for the ``users`` table."""

    @allure.title("users table – id column is never null")
    def test_users_id_not_null(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="users_id_check", table_name="users")
        batch_def = asset.add_batch_definition_whole_table("whole_users_id")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="users_id_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("users table – username column is never null")
    def test_users_username_not_null(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="users_username_check", table_name="users")
        batch_def = asset.add_batch_definition_whole_table("whole_users_username")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="users_username_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="username")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("users table – email column is never null")
    def test_users_email_not_null(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="users_email_check", table_name="users")
        batch_def = asset.add_batch_definition_whole_table("whole_users_email")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="users_email_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="email")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("users table – username values are unique")
    def test_users_username_unique(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="users_unique_check", table_name="users")
        batch_def = asset.add_batch_definition_whole_table("whole_users_unique")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="users_unique_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeUnique(column="username")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()
