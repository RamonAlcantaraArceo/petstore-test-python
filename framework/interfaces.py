"""Common abstract interface shared by both API and UI petstore clients.

By programming tests against :class:`PetstoreClientProtocol` instead of a
concrete implementation, the same test body can run against either the REST
API (fast, no browser) or the Selenium UI (full browser, end-to-end).

Example
-------
::

    @pytest.mark.parametrize("client", ["api_client", "ui_client"], indirect=True)
    def test_login(client: PetstoreClientProtocol) -> None:
        result = client.login("user1", "password1")
        assert_that(result.is_logged_in()).is_true()
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PetstoreClientProtocol(Protocol):
    """Defines the common interface for API and UI petstore clients."""

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> PetstoreClientProtocol:
        """Log in with the given credentials.

        Returns *self* to allow method chaining::

            client.login("user", "pass").get_pets()
        """
        ...

    def logout(self) -> PetstoreClientProtocol:
        """Log out the current session."""
        ...

    def is_logged_in(self) -> bool:
        """Return ``True`` when the client has an active authenticated session."""
        ...

    # ------------------------------------------------------------------
    # Pets
    # ------------------------------------------------------------------

    def add_pet(
        self, name: str, status: str = "available", **kwargs: Any
    ) -> dict[str, Any]:
        """Add a new pet and return a dict with at least ``{"id": ..., "name": ...}``."""
        ...

    def get_pet(self, pet_id: int) -> dict[str, Any]:
        """Retrieve a single pet by id."""
        ...

    def update_pet(self, pet_id: int, **kwargs: Any) -> dict[str, Any]:
        """Update an existing pet; returns the updated pet dict."""
        ...

    def delete_pet(self, pet_id: int) -> None:
        """Delete a pet by id."""
        ...

    def find_pets_by_status(self, status: str) -> list[dict[str, Any]]:
        """Return a list of pets matching the given *status*."""
        ...

    # ------------------------------------------------------------------
    # Teardown
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release any resources held by the client (browser, sessions, …)."""
        ...
