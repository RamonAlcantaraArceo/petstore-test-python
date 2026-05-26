"""ETL-suite fixtures – Great Expectations ephemeral context backed by PostgreSQL."""

from __future__ import annotations

from typing import Any

import great_expectations as gx
import pytest


@pytest.fixture(scope="session")
def gx_context(db_dsn: str) -> Any:
    """Return a GX ephemeral context with a Postgres datasource configured.

    The context is reused across the entire test session.  The ``db_dsn``
    fixture provides the ``postgresql+psycopg://`` connection string which GX
    accepts natively (it uses the SQLAlchemy psycopg3 dialect).
    """
    context = gx.get_context(mode="ephemeral")
    context.data_sources.add_postgres(
        name="petstore_postgres",
        connection_string=db_dsn,
    )
    return context


@pytest.fixture(scope="session")
def _petstore_ds(gx_context: Any) -> Any:
    """Convenience accessor for the petstore GX datasource."""
    return gx_context.data_sources.get("petstore_postgres")
