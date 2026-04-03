"""Global pytest configuration and shared fixtures.

Fixtures defined here are available to all tests without explicit import.
"""

from __future__ import annotations

import os

import pytest

from framework.api_client import PetstoreApiClient

# ---------------------------------------------------------------------------
# Configuration / environment
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers and apply global settings."""
    # Markers are declared in pyproject.toml; this hook runs early.
    pass


# ---------------------------------------------------------------------------
# API client fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL for the Petstore REST API, read from the environment."""
    return os.getenv("PETSTORE_API_BASE_URL", "https://petstore.swagger.io/v2")


@pytest.fixture
def api_client(api_base_url: str) -> PetstoreApiClient:
    """Provide a fresh :class:`PetstoreApiClient` for each test.

    The client is automatically closed after the test completes.
    """
    client = PetstoreApiClient(base_url=api_base_url)
    yield client
    client.close()


@pytest.fixture
def authenticated_api_client(api_client: PetstoreApiClient) -> PetstoreApiClient:
    """Provide an already-logged-in API client (uses the public demo credentials)."""
    api_client.login("user1", "password1")
    return api_client


# ---------------------------------------------------------------------------
# UI fixtures (imported lazily so non-UI tests don't need selenium)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ui_base_url() -> str:
    """Base URL for the Petstore web UI, read from the environment."""
    return os.getenv("PETSTORE_UI_BASE_URL", "https://the-internet.herokuapp.com")


@pytest.fixture
def browser(ui_base_url: str):  # type: ignore[no-untyped-def]
    """Provide a configured Selenium WebDriver for each UI test.

    Automatically quits the browser after the test completes.
    Skips (does not fail) when the ``--no-ui`` flag is passed.
    """
    pytest.importorskip("selenium", reason="selenium is required for UI tests")

    from framework.ui_client import _build_chrome_driver  # noqa: PLC0415

    headless = os.getenv("HEADLESS", "true").lower() not in ("0", "false", "no")
    driver = _build_chrome_driver(headless=headless)
    driver.implicitly_wait(0)  # rely on explicit waits in page objects
    yield driver
    driver.quit()


@pytest.fixture
def ui_client(browser, ui_base_url: str):  # type: ignore[no-untyped-def]
    """Provide a :class:`PetstoreUiClient` backed by the ``browser`` fixture."""
    from framework.ui_client import PetstoreUiClient  # noqa: PLC0415

    client = PetstoreUiClient(base_url=ui_base_url, driver=browser)
    yield client
    client.close()
