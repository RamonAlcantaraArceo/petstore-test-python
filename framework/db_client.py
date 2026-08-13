"""Synchronous PostgreSQL client for the Petstore database.

Provides direct read/write access to the petstore tables so tests can assert
that data has been correctly persisted, updated, or removed at the database
level — independent of the API or UI layers.

Example
-------
::

    client = PetstoreDbClient(dsn="postgresql+psycopg://petstore:pw@localhost:5432/petstore")
    pet = client.get_pet(42)
    assert pet is not None
    assert pet["name"] == "Fido"
    client.close()
"""

from __future__ import annotations

import logging
from typing import Any

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)


class PetstoreDbClient:
    """Synchronous psycopg3 client for direct petstore database access.

    Parameters
    ----------
    dsn:
        PostgreSQL connection string.  Accepts both the ``psycopg`` native
        format (``host=... dbname=...``) and the SQLAlchemy-style URL
        (``postgresql+psycopg://user:pw@host/db``), which is normalised
        automatically.
    """

    def __init__(self, dsn: str) -> None:
        # Strip the SQLAlchemy driver prefix so psycopg3 can parse the URL.
        clean_dsn = dsn.replace("postgresql+psycopg://", "postgresql://")
        self._conn: psycopg.Connection[dict[str, Any]] = psycopg.connect(
            clean_dsn, row_factory=dict_row
        )
        self._conn.autocommit = True
        logger.debug("DB connection established: %s", clean_dsn.split("@")[-1])

    # ------------------------------------------------------------------
    # Low-level helper
    # ------------------------------------------------------------------

    def execute_query(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a raw SQL query and return all rows as dicts.

        Parameters
        ----------
        query:
            Parameterised SQL statement (use ``%s`` placeholders).
        params:
            Positional parameters for the query.
        """
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        return list(rows)

    # ------------------------------------------------------------------
    # Pets
    # ------------------------------------------------------------------

    def get_pet(self, pet_id: int) -> dict[str, Any] | None:
        """Retrieve a single pet row by primary key.

        Returns ``None`` when the pet does not exist.
        """
        rows = self.execute_query("SELECT * FROM pets WHERE id = %s", (pet_id,))
        return rows[0] if rows else None

    def list_pets(self, status: str | None = None) -> list[dict[str, Any]]:
        """Return all pets, optionally filtered by *status*."""
        if status is not None:
            return self.execute_query(
                "SELECT * FROM pets WHERE status = %s ORDER BY id", (status,)
            )
        return self.execute_query("SELECT * FROM pets ORDER BY id")

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def get_user(self, username: str) -> dict[str, Any] | None:
        """Retrieve a single user row by *username*.

        Returns ``None`` when the user does not exist.
        """
        rows = self.execute_query(
            "SELECT * FROM users WHERE username = %s", (username,)
        )
        return rows[0] if rows else None

    def list_users(self) -> list[dict[str, Any]]:
        """Return all user rows ordered by id."""
        return self.execute_query("SELECT * FROM users ORDER BY id")

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def get_order(self, order_id: int) -> dict[str, Any] | None:
        """Retrieve a single order row by primary key.

        Returns ``None`` when the order does not exist.
        """
        rows = self.execute_query("SELECT * FROM orders WHERE id = %s", (order_id,))
        return rows[0] if rows else None

    def list_orders(self) -> list[dict[str, Any]]:
        """Return all order rows ordered by id."""
        return self.execute_query("SELECT * FROM orders ORDER BY id")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
        logger.debug("DB connection closed")
