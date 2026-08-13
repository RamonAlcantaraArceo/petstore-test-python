"""Shared Great Expectations helpers for ETL tests."""

from __future__ import annotations

import json
from typing import Any

import allure
from great_expectations.checkpoint.checkpoint import CheckpointResult
from great_expectations.core.expectation_validation_result import (
    ExpectationSuiteValidationResult,
)


def get_or_create_query_asset(ds: Any, *, name: str, query: str) -> Any:
    """Return existing query asset by name or create it when missing."""
    if name in ds.get_asset_names():
        return ds.get_asset(name)
    return ds.add_query_asset(name=name, query=query)


def get_or_create_batch_definition(asset: Any, *, name: str) -> Any:
    """Return existing whole-table batch definition by name or create it."""
    try:
        return asset.get_batch_definition(name)
    except KeyError:
        return asset.add_batch_definition_whole_table(name)


def assert_checkpoint_result_steps(result: CheckpointResult) -> None:
    """Expose checkpoint expectation outcomes as Allure steps and pytest asserts."""
    failures: list[str] = []

    for validation_id, suite_result in result.run_results.items():
        suite_label = str(validation_id)
        with allure.step(f"Suite validation: {suite_label}"):
            assert isinstance(suite_result, ExpectationSuiteValidationResult)
            allure.attach(
                json.dumps(suite_result.statistics, indent=2),
                name="suite_statistics",
                attachment_type=allure.attachment_type.JSON,
            )

        for idx, expectation_result in enumerate(suite_result.results, start=1):
            expectation_type = expectation_result.expectation_config.type
            column = expectation_result.expectation_config.kwargs.get("column", "n/a")
            step_name = f"{idx}. {expectation_type} (column={column})"
            with allure.step(step_name):
                if not expectation_result.success:
                    failures.append(f"{suite_label} -> {step_name}")
                    allure.attach(
                        json.dumps(
                            expectation_result.to_json_dict(),
                            indent=2,
                            default=str,
                        ),
                        name="expectation_failure",
                        attachment_type=allure.attachment_type.JSON,
                    )

    if failures:
        details = "\n".join(failures)
        raise AssertionError(f"Failed expectations:\n{details}")

    assert result.success, result.describe()
