"""Global pytest configuration and shared fixtures.

Fixtures defined here are available to all tests without explicit import.
"""

from __future__ import annotations

import logging
import os
import platform
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from r3a_logger.logger import (
    initialize_logging,
)

from framework.factories import UserFactory

# Call r3a_logger's initialize_logging with new signature
log_dir = Path("./.logs")
initialize_logging(
    log_dir=log_dir,
    log_level="DEBUG",
    console_logging=True,
    logger_name="petstore-test-python",
    patch_root_logger=True,
)

logging.getLogger("faker").setLevel(logging.WARNING)

from framework.api_client import PetstoreApiClient  # noqa: E402

# ---------------------------------------------------------------------------
# Configuration / environment
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers and apply global settings."""
    # Markers are declared in pyproject.toml; this hook runs early.
    pass


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Write environment metadata to the Allure results directory."""
    allure_dir = getattr(session.config.option, "allure_report_dir", None)
    if allure_dir:
        env_file = Path(allure_dir) / "environment.properties"
        env_file.parent.mkdir(parents=True, exist_ok=True)
        with env_file.open("w") as f:
            f.write(f"Python.Version={platform.python_version()}\n")
            f.write(
                "API.Base.URL="
                + os.getenv("PETSTORE_API_BASE_URL", "http://localhost:8000/api/v1")
                + "\n"
            )
            f.write(
                "UI.Base.URL="
                + os.getenv(
                    "PETSTORE_UI_BASE_URL", "https://the-internet.herokuapp.com"
                )
                + "\n"
            )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo  # type: ignore[type-arg]
) -> Generator[None, None, None]:
    """Attach a screenshot to the Allure report when a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "browser" in item.fixturenames:
        try:
            driver = item.funcargs.get("browser")
            if driver is not None:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception:
            pass


# ---------------------------------------------------------------------------
# API client fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL for the Petstore REST API, read from the environment."""
    return os.getenv("PETSTORE_API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.fixture(scope="session")
def api_key() -> str:
    """API key for authenticated requests, read from the environment.

    Raises:
        ValueError: if PETSTORE_API_KEY is not set.
    """
    api_key = os.getenv("PETSTORE_API_KEY")
    if not api_key:
        raise ValueError("PETSTORE_API_KEY environment variable must be set")
    return api_key


@pytest.fixture
def api_client(
    api_base_url: str, api_key: str | None
) -> Generator[PetstoreApiClient, None, None]:
    """Provide a fresh :class:`PetstoreApiClient` for each test.

    The client is automatically closed after the test completes.
    """
    client = PetstoreApiClient(base_url=api_base_url, api_key=api_key)
    yield client
    client.close()


@pytest.fixture
def new_user(api_client: PetstoreApiClient) -> Generator:
    """Create a user via the API and yield it; delete it after the test."""
    data = UserFactory.build(username="user1", password="password1")
    created = api_client.create_user(
        username=data["username"], password=data["password"]
    )
    yield data, created
    # Cleanup – ignore 404 in case the test itself deleted the user
    try:
        api_client.delete_user(created["id"])
    except Exception:
        pass


@pytest.fixture
def authenticated_api_client(
    api_client: PetstoreApiClient,
    new_user: tuple,
) -> Generator[PetstoreApiClient, None, None]:
    """Provide an already-logged-in API client (uses the public demo credentials)."""
    data, _ = new_user
    api_client.login(data["username"], data["password"])
    yield api_client


# ---------------------------------------------------------------------------
# UI fixtures (imported lazily so non-UI tests don't need selenium)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ui_base_url() -> str:
    """Base URL for the Petstore web UI, read from the environment."""
    return os.getenv("PETSTORE_UI_BASE_URL", "https://the-internet.herokuapp.com")


@pytest.fixture
def browser(ui_base_url: str) -> Generator[Any, None, None]:
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
def ui_client(browser: Any, ui_base_url: str) -> Generator[Any, None, None]:
    """Provide a :class:`PetstoreUiClient` backed by the ``browser`` fixture."""
    from framework.ui_client import PetstoreUiClient  # noqa: PLC0415

    client = PetstoreUiClient(base_url=ui_base_url, driver=browser)
    yield client
    client.close()
