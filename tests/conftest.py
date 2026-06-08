"""Global pytest configuration and shared fixtures.

Fixtures defined here are available to all tests without explicit import.
"""

from __future__ import annotations

import logging
import os
import platform
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any

import allure
import pytest
import pytest_asyncio
import requests
from petstore_openapi_client import ApiClient, Configuration
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.api.store_api import StoreApi
from petstore_openapi_client.api.user_api import UserApi
from r3a_logger.logger import (
    initialize_logging,
)
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions

from framework.config import get_api_base_url, get_ui_base_url
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
logging.getLogger("great_expectations").setLevel(logging.WARNING)

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
            f.write("API.Base.URL=" + get_api_base_url() + "\n")
            f.write("UI.Base.URL=" + get_ui_base_url() + "\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo,  # type: ignore[type-arg]
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
    return get_api_base_url()


def _extract_jwt_from_auth_response(payload: Any) -> str:
    """Extract a JWT from the auth endpoint response payload."""
    if isinstance(payload, str) and payload:
        return payload
    if isinstance(payload, dict):
        for key in ("token", "access_token", "jwt"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
        nested_data = payload.get("data")
        if isinstance(nested_data, dict):
            for key in ("token", "access_token", "jwt"):
                value = nested_data.get(key)
                if isinstance(value, str) and value:
                    return value
    raise ValueError("Auth response does not contain a JWT token")


@pytest.fixture(scope="session")
def bypass_key() -> str | None:
    """Optional rate-limit bypass key read from environment."""
    return os.getenv("X_BYPASS_KEY") or os.getenv("X-Bypass-Key")


@pytest.fixture(scope="session")
def authorization_header(api_base_url: str) -> str:
    """Resolve Authorization header from env or obtain one from /user/auth."""
    raw_value = os.getenv("AUTHORIZATION") or os.getenv("PETSTORE_AUTHORIZATION")
    if raw_value:
        return raw_value if raw_value.startswith("Bearer ") else f"Bearer {raw_value}"

    response = requests.post(
        f"{api_base_url}/user/auth",
        json={"username": "devuser"},
        timeout=10,
    )
    response.raise_for_status()
    token = _extract_jwt_from_auth_response(response.json())
    return token if token.startswith("Bearer ") else f"Bearer {token}"


@pytest.fixture
def api_client(
    api_base_url: str, authorization_header: str, bypass_key: str | None
) -> Generator[PetstoreApiClient, None, None]:
    """Provide a fresh :class:`PetstoreApiClient` for each test.

    The client is automatically closed after the test completes.
    """
    client = PetstoreApiClient(
        base_url=api_base_url,
        authorization=authorization_header,
        bypass_key=bypass_key,
    )
    yield client
    client.close()


@pytest.fixture
def new_user(
    api_client: PetstoreApiClient,
) -> Generator[tuple[dict[str, Any], dict[str, Any]], None, None]:
    """Create a user via the API and yield it; delete it after the test."""
    data = UserFactory.build(username="user1", password="password1")

    try:
        created = api_client.get_user(data["username"])
    except Exception:
        created = api_client.create_user(
            username=data["username"], password=data["password"]
        )
    yield data, created
    # Cleanup – ignore 404 in case the test itself deleted the user
    try:
        api_client.delete_user(created["username"])
    except Exception:
        pass


@pytest.fixture
def authenticated_api_client(
    api_client: PetstoreApiClient,
    new_user: tuple[dict[str, Any], dict[str, Any]],
) -> Generator[PetstoreApiClient, None, None]:
    """Provide an already-logged-in API client (uses the public demo credentials)."""
    data, _ = new_user
    api_client.login(data["username"], data["password"])
    yield api_client


# ---------------------------------------------------------------------------
# API generated client fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def gen_client_configuration(
    authorization_header: str, bypass_key: str | None
) -> Configuration:
    """Provide generated client configuration for integration tests."""
    api_keys: dict[str, str] = {"Authorization": authorization_header}
    if bypass_key:
        api_keys["X-Bypass-Key"] = bypass_key
    return Configuration(api_key=api_keys)


@pytest_asyncio.fixture
async def gen_api_client(
    gen_client_configuration: Configuration,
    authorization_header: str,
    bypass_key: str | None,
) -> AsyncGenerator[ApiClient, None]:
    """Provide an async generated API client instance."""
    async with ApiClient(configuration=gen_client_configuration) as client:
        if bypass_key:
            client.set_default_header("X-Bypass-Key", bypass_key)
        client.set_default_header("Authorization", authorization_header)
        yield client


@pytest_asyncio.fixture
async def gen_pet_api_client(gen_api_client: ApiClient) -> AsyncGenerator[PetApi, None]:
    """Provide PetApi backed by the generated API client."""
    yield PetApi(api_client=gen_api_client)


@pytest_asyncio.fixture
async def gen_user_api_client(
    gen_api_client: ApiClient,
) -> AsyncGenerator[UserApi, None]:
    """Provide UserApi backed by the generated API client."""
    yield UserApi(api_client=gen_api_client)


@pytest_asyncio.fixture
async def gen_store_api_client(
    gen_api_client: ApiClient,
) -> AsyncGenerator[StoreApi, None]:
    """Provide StoreApi backed by the generated API client."""
    yield StoreApi(api_client=gen_api_client)


# ---------------------------------------------------------------------------
# UI fixtures (imported lazily so non-UI tests don't need selenium)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ui_base_url() -> str:
    """Base URL for the Petstore web UI, read from the environment."""
    return get_ui_base_url()


def _build_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """Build a Chrome WebDriver with sensible CI and local defaults.

    Args:
        headless: Whether to run Chrome without a visible window.

    Returns:
        A configured Chrome WebDriver instance.
    """
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)

    # driver.set_window_position(2000, 100)

    return driver


@pytest.fixture
def browser(ui_base_url: str) -> Generator[Any, None, None]:
    """Provide a configured Selenium WebDriver for each UI test.

    Automatically quits the browser after the test completes.
    Skips (does not fail) when the ``--no-ui`` flag is passed.
    """
    pytest.importorskip("selenium", reason="selenium is required for UI tests")

    headless = os.getenv("HEADLESS", "true").lower() not in ("0", "false", "no")
    try:
        driver = _build_chrome_driver(headless=headless)
    except WebDriverException as exc:
        if "cannot find Chrome binary" in str(exc):
            pytest.skip(
                "Chrome browser binary is not available on this host. "
                "Install Chrome/Chromium to run UI tests."
            )
        raise
    driver.implicitly_wait(0)  # rely on explicit waits in page objects
    yield driver
    driver.quit()


@pytest.fixture
def ui_client(browser: Any, ui_base_url: str) -> Generator[Any, None, None]:
    """Provide a :class:`PetstoreUiClient` backed by the ``browser`` fixture."""
    from framework.ui_client import PetstoreUiClient  # noqa: PLC0415

    client = PetstoreUiClient(browser, base_url=ui_base_url)
    yield client
    client.close()


# ---------------------------------------------------------------------------
# Database client fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def db_dsn() -> str:
    """PostgreSQL DSN for direct database access, read from the environment.

    Raises:
        ValueError: if PETSTORE_DB_DSN is not set.
    """
    dsn = os.getenv("PETSTORE_DB_DSN")
    if not dsn:
        raise ValueError("PETSTORE_DB_DSN environment variable must be set")
    return dsn


@pytest.fixture(scope="session")
def db_client(db_dsn: str) -> Generator[Any, None, None]:
    """Provide a session-scoped :class:`~framework.db_client.PetstoreDbClient`.

    A single database connection is reused across all tests in the session.
    The connection is closed when the session ends.
    """
    from framework.db_client import PetstoreDbClient  # noqa: PLC0415

    client = PetstoreDbClient(dsn=db_dsn)
    yield client
    client.close()
