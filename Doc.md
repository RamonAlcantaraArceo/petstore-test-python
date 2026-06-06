# Great Expectations + ETL Test Strategy

This repository uses Great Expectations (GX) in the `tests/etl/` suite to validate data quality directly at the database layer, complementing API/UI functional tests.

## Goals

- Verify critical table-level data quality rules in Postgres (`pets`, `users`, `orders`).
- Catch schema/domain regressions that API tests can miss.
- Produce readable evidence in:
  - pytest output (pass/fail)
  - Allure steps (expectation-by-expectation)
  - GX Data Docs (validation history and suites)

## Current Pattern

Each ETL test file executes **one consolidated validation run** per table:

- `test_gx_pets.py` → `pets_quality_suite`
- `test_gx_users.py` → `users_quality_suite`
- `test_gx_orders.py` → `orders_quality_suite`

For each file:

1. Create or reuse a GX query asset and batch definition.
2. Build/update one expectation suite with multiple expectations.
3. Build/update one validation definition.
4. Run one checkpoint with a shared run id (`ge_run_id`) for grouping.
5. Assert intermediate expectation outcomes (Allure steps) and final checkpoint success.

This produces one validation row per table per test run in Data Docs, with a common run name.

## Why this shape

- **Low noise in Data Docs**: one row per table instead of one row per expectation.
- **High debuggability**: each expectation still appears as an individual Allure step.
- **Stable reruns**: tests use get-or-create helpers for assets and batch definitions.
- **Enum-safe checks**: enum columns are cast to text in query assets where needed.

## Failure demonstration tests

`tests/etl/test_gx_failure_demos.py` contains intentionally failing examples, currently marked `@pytest.mark.skip` so CI remains green.

- They are deterministic failures.
- Unskip locally to validate how failures appear in pytest, Allure, and GX Data Docs.

## How to run

```bash
uv run pytest tests/etl -v
```

Optional custom run name (for Data Docs grouping):

```bash
GE_RUN_NAME=etl-local-debug uv run pytest tests/etl -v
```

Data Docs are built at session end from the GX file context under `.gx_context/gx/uncommitted/data_docs/local_site/`.
