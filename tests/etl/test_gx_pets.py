"""ETL data-quality tests for the ``pets`` table using Great Expectations.

Each test builds a GX expectation suite against the ``pets`` table and
validates structural and domain constraints that the API alone cannot assert.
"""

from __future__ import annotations

from typing import Any

import allure
import great_expectations as gx
import pytest


@allure.feature("ETL – pets table")
@allure.story("Schema and data quality")
@pytest.mark.etl
class TestGxPets:
    """Great Expectations validations for the ``pets`` table."""

    @allure.title("pets table – id column is never null and always positive")
    def test_pets_id_not_null(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="pets_id_check", table_name="pets")
        batch_def = asset.add_batch_definition_whole_table("whole_pets_id")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="pets_id_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("pets table – name column is never null")
    def test_pets_name_not_null(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="pets_name_check", table_name="pets")
        batch_def = asset.add_batch_definition_whole_table("whole_pets_name")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="pets_name_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="name")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("pets table – status is one of allowed values")
    def test_pets_status_valid_values(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="pets_status_check", table_name="pets")
        batch_def = asset.add_batch_definition_whole_table("whole_pets_status")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="pets_status_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="status",
                value_set=["available", "pending", "sold"],
            )
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("pets table – id values are unique")
    def test_pets_id_unique(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="pets_unique_check", table_name="pets")
        batch_def = asset.add_batch_definition_whole_table("whole_pets_unique")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="pets_unique_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeUnique(column="id")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()
