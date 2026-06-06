"""ETL-suite fixtures – Great Expectations file context backed by PostgreSQL."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

import great_expectations as gx
import pytest
from great_expectations.core.run_identifier import RunIdentifier


@pytest.fixture(scope="session")
def gx_context(db_dsn: str) -> Any:
    """Return a GX file context with a Postgres datasource configured.

    The context is reused across the entire test session.  The ``db_dsn``
    fixture provides the ``postgresql+psycopg://`` connection string which GX
    accepts natively (it uses the SQLAlchemy psycopg3 dialect).
    """
    context = gx.get_context(mode="file", project_root_dir="./.gx_context")
    context.data_sources.add_or_update_postgres(
        name="petstore_postgres",
        connection_string=db_dsn,
    )

    yield context

    context.build_data_docs()
    print("Data Docs built at:", context.root_directory)


@pytest.fixture(scope="session")
def ge_run_id() -> RunIdentifier:
    """Shared run identifier so ETL Data Docs entries are grouped per run."""
    run_name = os.getenv("GE_RUN_NAME")
    run_time = datetime.now(UTC)
    if not run_name:
        run_name = f"etl-{run_time:%Y%m%d-%H%M%S}"
    return RunIdentifier(run_name=run_name, run_time=run_time)


@pytest.fixture(scope="session")
def _petstore_ds(gx_context: Any) -> Any:
    """Convenience accessor for the petstore GX datasource."""
    return gx_context.data_sources.get("petstore_postgres")
