"""ETL data-quality tests for the ``pets`` table using Great Expectations.

Each test builds a GX expectation suite against the ``pets`` table and
validates structural and domain constraints that the API alone cannot assert.
"""

from __future__ import annotations

from typing import Any

import allure
import great_expectations as gx
import pytest
from great_expectations.checkpoint.checkpoint import Checkpoint
from great_expectations.core.run_identifier import RunIdentifier
from great_expectations.core.validation_definition import ValidationDefinition

from tests.etl.gx_helpers import (
    assert_checkpoint_result_steps,
    get_or_create_batch_definition,
    get_or_create_query_asset,
)


@allure.feature("ETL – pets table")
@allure.story("Schema and data quality")
@pytest.mark.etl
class TestGxPets:
    """Great Expectations validations for the ``pets`` table."""

    @allure.title("pets table – schema and domain quality checks")
    def test_pets_table_quality(
        self, gx_context: Any, ge_run_id: RunIdentifier
    ) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = get_or_create_query_asset(
            ds,
            name="pets_quality_check",
            query="SELECT id, name, status::text AS status FROM pets",
        )
        batch_def = get_or_create_batch_definition(asset, name="whole_pets_quality")
        suite = gx_context.suites.add_or_update(
            gx.ExpectationSuite(name="pets_quality_suite")
        )
        suite.expectations = []
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="name")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="status")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValueLengthsToBeBetween(
                column="name",
                min_value=1,
                max_value=100,
            )
        )
        suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="id"))
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="status",
                value_set=["available", "pending", "sold"],
            )
        )
        validation = gx_context.validation_definitions.add_or_update(
            ValidationDefinition(
                name="pets_quality_validation",
                data=batch_def,
                suite=suite,
            )
        )
        checkpoint = gx_context.checkpoints.add_or_update(
            Checkpoint(
                name="pets_quality_checkpoint",
                validation_definitions=[validation],
            )
        )
        checkpoint_result = checkpoint.run(run_id=ge_run_id)
        assert_checkpoint_result_steps(checkpoint_result)
