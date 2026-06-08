"""Skipped GX failure demos to validate failure reporting flows when needed."""

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


@allure.feature("ETL – failure demos")
@allure.story("Intentional failure examples")
@pytest.mark.etl
@pytest.mark.skip(
    reason="Intentional failing demo. Unskip locally to view failure output."
)
class TestGxFailureDemos:
    """Demonstrate deterministic GX failures without affecting CI stability."""

    @allure.title("demo failure – numeric expectation mismatch")
    def test_demo_failure_numeric(
        self, gx_context: Any, ge_run_id: RunIdentifier
    ) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = get_or_create_query_asset(
            ds,
            name="demo_failure_numeric_asset",
            query="SELECT 1 AS demo_number",
        )
        batch_def = get_or_create_batch_definition(
            asset, name="whole_demo_failure_numeric"
        )
        suite = gx_context.suites.add_or_update(
            gx.ExpectationSuite(name="demo_failure_numeric_suite")
        )
        suite.expectations = []
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeBetween(
                column="demo_number",
                min_value=2,
            )
        )
        validation = gx_context.validation_definitions.add_or_update(
            ValidationDefinition(
                name="demo_failure_numeric_validation",
                data=batch_def,
                suite=suite,
            )
        )
        checkpoint = gx_context.checkpoints.add_or_update(
            Checkpoint(
                name="demo_failure_numeric_checkpoint",
                validation_definitions=[validation],
            )
        )
        checkpoint_result = checkpoint.run(run_id=ge_run_id)
        assert_checkpoint_result_steps(checkpoint_result)

    @allure.title("demo failure – string set mismatch")
    def test_demo_failure_set(self, gx_context: Any, ge_run_id: RunIdentifier) -> None:
        ds = gx_context.data_sources.get("petstore_postgres")
        asset = get_or_create_query_asset(
            ds,
            name="demo_failure_set_asset",
            query="SELECT 'active'::text AS demo_status",
        )
        batch_def = get_or_create_batch_definition(asset, name="whole_demo_failure_set")
        suite = gx_context.suites.add_or_update(
            gx.ExpectationSuite(name="demo_failure_set_suite")
        )
        suite.expectations = []
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="demo_status",
                value_set=["inactive"],
            )
        )
        validation = gx_context.validation_definitions.add_or_update(
            ValidationDefinition(
                name="demo_failure_set_validation",
                data=batch_def,
                suite=suite,
            )
        )
        checkpoint = gx_context.checkpoints.add_or_update(
            Checkpoint(
                name="demo_failure_set_checkpoint",
                validation_definitions=[validation],
            )
        )
        checkpoint_result = checkpoint.run(run_id=ge_run_id)
        assert_checkpoint_result_steps(checkpoint_result)
