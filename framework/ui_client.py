"""Selenium-based UI client implementing PetstoreClientProtocol.

This client drives a real browser using Selenium and exposes the same
interface as :class:`~framework.api_client.PetstoreApiClient`, allowing
tests to be written once and run against either the API or the UI.

Example
-------
::

    from framework.ui_client import PetstoreUiClient

    client = PetstoreUiClient(headless=True)
    client.login("tomsmith", "SuperSecretPassword!")
    assert client.is_logged_in()
    client.close()
"""

from __future__ import annotations

import logging
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from framework.config import get_ui_base_url
from framework.interfaces import PetstoreClientProtocol
from framework.pages.login_page import LoginPage
from framework.pages.pet_management_page import PetManagementPage

logger = logging.getLogger(__name__)


class PetstoreUiClient(PetstoreClientProtocol):
    """Browser-based client for the Petstore web UI.

    Implements the same interface as :class:`~framework.api_client.PetstoreApiClient`
    so tests can be parameterised across both implementations.

    Parameters
    ----------
    base_url:
        Root URL of the web application.
    headless:
        Run Chrome without a visible window (default: ``True``).
    driver:
        Provide a pre-configured WebDriver (e.g. for testing the client
        itself). When given, *headless* is ignored.
    """

    def __init__(
        self,
        driver: webdriver.Remote,
        base_url: str | None = None,
        headless: bool = True,
    ) -> None:
        """Create a browser-backed Petstore client.

        Args:
            base_url: Root URL of the UI application.
            headless: Whether to run Chrome in headless mode.
            driver: Optional pre-configured WebDriver to reuse.
        """
        resolved_base_url = base_url or get_ui_base_url()
        self._base_url = resolved_base_url.rstrip("/")
        self._driver = driver
        self._login_page = LoginPage(self._driver, base_url=self._base_url)
        self._pet_management_page = PetManagementPage(
            self._driver, base_url=self._base_url
        )
        self._logged_in = False

    @property
    def login_page(self) -> LoginPage:
        """Expose the LoginPage for direct interactions in tests."""
        return self._login_page

    @property
    def pet_management_page(self) -> PetManagementPage:
        """Expose the PetManagementPage for direct interactions in tests."""
        return self._pet_management_page

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> PetstoreUiClient:
        """Navigate to the login page and submit credentials.

        Args:
            username: User name to submit.
            password: Password to submit.

        Returns:
            Self, to allow method chaining.
        """
        if not self._login_page._is_login_form_visible():
            self._login_page.open()
        self._login_page.login(username, password)
        self._logged_in = self._login_page.is_logged_in()
        return self

    def logout(self) -> PetstoreUiClient:
        """Log out through the UI.

        Returns:
            Self, to allow method chaining.
        """
        self._login_page.click_logout()
        self._logged_in = self._login_page.is_logged_in()
        return self

    def is_logged_in(self) -> bool:
        """Return whether the client believes it is authenticated."""
        return self._logged_in

    def _require_authenticated_session(self, operation_name: str) -> None:
        """Require a logged-in session before mutating pet data.

        Args:
            operation_name: Name of the attempted operation.

        Raises:
            PermissionError: If the current UI session is not authenticated.
        """
        if not self._logged_in:
            raise PermissionError(
                f"{operation_name} requires an authenticated UI session. "
                "Log in before managing pets."
            )

    # ------------------------------------------------------------------
    # Pets
    # ------------------------------------------------------------------

    def add_pet(
        self, name: str, status: str = "available", **kwargs: Any
    ) -> dict[str, Any]:
        """Create a pet through the UI.

        Args:
            name: Pet name.
            status: Desired pet status.
            **kwargs: Additional fields for the pet payload.

        Raises:
            PermissionError: If called without an authenticated session.
        """
        self._require_authenticated_session("add_pet")
        return self._pet_management_page.add_pet(name=name, status=status, **kwargs)

    def get_pet(self, pet_id: int) -> dict[str, Any]:
        """Retrieve a pet by id from the UI.

        Args:
            pet_id: Identifier of the pet to retrieve.

        Returns:
            A parsed pet dictionary.
        """
        return self._pet_management_page.get_pet(pet_id)

    def update_pet(self, pet_id: int, **kwargs: Any) -> dict[str, Any]:
        """Update a pet through the UI.

        Args:
            pet_id: Identifier of the pet to update.
            **kwargs: Fields to update.

        Raises:
            PermissionError: If called without an authenticated session.
        """
        self._require_authenticated_session("update_pet")
        return self._pet_management_page.update_pet(pet_id=pet_id, **kwargs)

    def delete_pet(self, pet_id: int) -> None:
        """Delete a pet through the UI.

        Args:
            pet_id: Identifier of the pet to delete.

        Raises:
            PermissionError: If called without an authenticated session.
        """
        self._require_authenticated_session("delete_pet")
        self._pet_management_page.delete_pet(pet_id=pet_id)

    def find_pets_by_status(self, status: str) -> list[dict[str, Any]]:
        """Find pets by status through the UI filter.

        Args:
            status: Pet status to search for.

        Returns:
            List of parsed pet dictionaries matching the status.
        """
        return self._pet_management_page.find_pets_by_status(status=status)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Quit the underlying browser session."""
        try:
            self._driver.quit()
        except WebDriverException as exc:
            logger.warning("Exception while closing browser: %s", exc)
