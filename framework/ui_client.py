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
import os
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

try:
    from webdriver_manager.chrome import ChromeDriverManager

    _WDM_AVAILABLE = True
except ImportError:
    _WDM_AVAILABLE = False

from framework.pages.login_page import LoginPage

logger = logging.getLogger(__name__)

DEFAULT_UI_BASE_URL = os.getenv(
    "PETSTORE_UI_BASE_URL", "https://the-internet.herokuapp.com"
)


def _build_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """Build a Chrome WebDriver with sensible CI/local defaults."""
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")

    if _WDM_AVAILABLE:
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    return webdriver.Chrome(options=options)


class PetstoreUiClient:
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
        base_url: str = DEFAULT_UI_BASE_URL,
        headless: bool = True,
        driver: webdriver.Remote | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._driver = driver or _build_chrome_driver(headless=headless)
        self._login_page = LoginPage(self._driver, base_url=self._base_url)
        self._logged_in = False

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> PetstoreUiClient:
        """Navigate to the login page and submit the form."""
        self._login_page.open().login(username, password)
        self._logged_in = self._login_page.is_logged_in()
        return self

    def logout(self) -> PetstoreUiClient:
        """Click the logout button."""
        self._login_page.click_logout()
        self._logged_in = False
        return self

    def is_logged_in(self) -> bool:
        return self._logged_in

    # ------------------------------------------------------------------
    # Pets (stub – wire up to your real UI once the front-end exists)
    # ------------------------------------------------------------------

    def add_pet(
        self, name: str, status: str = "available", **kwargs: Any
    ) -> dict[str, Any]:
        raise NotImplementedError(
            "add_pet via UI is not yet implemented. "
            "Use PetstoreApiClient for pet CRUD operations."
        )

    def get_pet(self, pet_id: int) -> dict[str, Any]:
        raise NotImplementedError("get_pet via UI is not yet implemented.")

    def update_pet(self, pet_id: int, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError("update_pet via UI is not yet implemented.")

    def delete_pet(self, pet_id: int) -> None:
        raise NotImplementedError("delete_pet via UI is not yet implemented.")

    def find_pets_by_status(self, status: str) -> list[dict[str, Any]]:
        raise NotImplementedError("find_pets_by_status via UI is not yet implemented.")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Quit the browser."""
        try:
            self._driver.quit()
        except Exception as exc:
            logger.warning("Exception while closing browser: %s", exc)
