"""ETL data-quality tests for the ``users`` table using Great Expectations.

Validates structural and domain constraints on the ``users`` table that
complement the API-level assertions.
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


@allure.feature("ETL – users table")
@allure.story("Schema and data quality")
@pytest.mark.etl
class TestGxUsers:
    """Great Expectations validations for the ``users`` table."""

    @allure.title("users table – schema and domain quality checks")
    def test_users_table_quality(
        self, gx_context: Any, ge_run_id: RunIdentifier
    ) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = get_or_create_query_asset(
            ds,
            name="users_quality_check",
            query="SELECT id, username, email FROM users",
        )
        batch_def = get_or_create_batch_definition(asset, name="whole_users_quality")
        suite = gx_context.suites.add_or_update(
            gx.ExpectationSuite(name="users_quality_suite")
        )
        suite.expectations = []
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="id")
        )
        suite.add_expectation(
            gx.expectations.core.ExpectColumnValuesToNotBeNull(column="username")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="email")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValueLengthsToBeBetween(
                column="username",
                min_value=3,
                max_value=64,
            )
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToMatchRegex(
                column="email",
                regex=r"^[^@]+@[^@]+\.[^@]+$",
            )
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeUnique(column="username")
        )
        validation = gx_context.validation_definitions.add_or_update(
            ValidationDefinition(
                name="users_quality_validation",
                data=batch_def,
                suite=suite,
            )
        )
        checkpoint = gx_context.checkpoints.add_or_update(
            Checkpoint(
                name="users_quality_checkpoint",
                validation_definitions=[validation],
            )
        )
        checkpoint_result = checkpoint.run(run_id=ge_run_id)
        assert_checkpoint_result_steps(checkpoint_result)
