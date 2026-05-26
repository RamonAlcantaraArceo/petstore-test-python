"""ETL data-quality tests for the ``orders`` table using Great Expectations.

Validates structural and domain constraints on the ``orders`` table that
complement the API-level assertions.
"""

from __future__ import annotations

from typing import Any

import allure
import great_expectations as gx
import pytest


@allure.feature("ETL – orders table")
@allure.story("Schema and data quality")
@pytest.mark.etl
class TestGxOrders:
    """Great Expectations validations for the ``orders`` table."""

    @allure.title("orders table – id column is never null")
    def test_orders_id_not_null(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="orders_id_check", table_name="orders")
        batch_def = asset.add_batch_definition_whole_table("whole_orders_id")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="orders_id_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("orders table – status is one of allowed values")
    def test_orders_status_valid_values(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="orders_status_check", table_name="orders")
        batch_def = asset.add_batch_definition_whole_table("whole_orders_status")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="orders_status_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="status",
                value_set=["placed", "approved", "delivered"],
            )
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("orders table – quantity is a positive integer")
    def test_orders_quantity_positive(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="orders_qty_check", table_name="orders")
        batch_def = asset.add_batch_definition_whole_table("whole_orders_qty")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="orders_qty_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeBetween(
                column="quantity",
                min_value=1,
            )
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()

    @allure.title("orders table – id values are unique")
    def test_orders_id_unique(self, gx_context: Any) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = ds.add_table_asset(name="orders_unique_check", table_name="orders")
        batch_def = asset.add_batch_definition_whole_table("whole_orders_unique")
        suite = gx_context.suites.add(
            gx.ExpectationSuite(name="orders_unique_suite")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeUnique(column="id")
        )
        batch = batch_def.get_batch()
        result = batch.validate(suite)
        assert result.success, result.describe()
