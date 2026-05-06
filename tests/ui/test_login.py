"""UI tests – login feature (Page Object Model + Selenium).

These tests use the same assertion style as tests/api/test_login.py,
demonstrating the shared-interface pattern across API and UI.

The target site is https://the-internet.herokuapp.com/login
(a freely available Selenium practice site).  Override the target by
setting the ``PETSTORE_UI_BASE_URL`` environment variable.

Note: UI tests are skipped in CI unless the ``--run-ui`` flag is passed
or the ``RUN_UI_TESTS`` environment variable is set to ``1``.
"""

from __future__ import annotations

import os

import pytest
from selenium.webdriver.common.by import By

from framework.assertions import assert_that
from framework.pages.login_page import LoginPage

# Skip entire module when Selenium is unavailable or UI tests are disabled
pytestmark = pytest.mark.ui


def _ui_enabled() -> bool:
    return os.getenv("RUN_UI_TESTS", "0") in ("1", "true", "yes")


skip_if_no_ui = pytest.mark.skipif(
    not _ui_enabled(),
    reason="UI tests are disabled. Set RUN_UI_TESTS=1 to enable.",
)


@skip_if_no_ui
class TestLoginUi:
    """Selenium tests for the login page using the Page Object Model."""

    @pytest.fixture(autouse=True)
    def _open_login_page(self, browser, ui_base_url: str) -> None:
        """Navigate to the login page before each test."""
        self._page = LoginPage(browser, base_url=ui_base_url)
        self._page.open()

    def test_successful_login_shows_secure_area(self, browser) -> None:
        """Logging in with valid credentials should show the secure area message.

        This mirrors tests/api/test_login.py::TestLogin::test_login_sets_authenticated_state
        using the identical assertion style.
        """
        self._page.login("tomsmith", "SuperSecretPassword!")

        assert_that(self._page.is_logged_in()).is_true()
        assert_that(self._page.get_flash_message()).contains(
            "You logged into a secure area!"
        )

    def test_failed_login_shows_error_message(self, browser) -> None:
        """Logging in with invalid credentials should show an error message."""
        self._page.login("wrong_user", "wrong_pass")

        assert_that(self._page.is_logged_in()).is_false()
        assert_that(self._page.is_login_failed()).is_true()

    def test_login_then_logout_returns_to_login_page(
        self, browser, ui_base_url: str
    ) -> None:
        """After login and logout the user should be back on the login page."""
        self._page.login("tomsmith", "SuperSecretPassword!")
        assert_that(self._page.is_logged_in()).is_true()

        self._page.click_logout()

        assert_that(self._page.current_url).contains("/login")

    def test_page_title_is_correct(self, browser) -> None:
        """The login page title should be 'The Internet'."""
        assert_that(self._page.title).contains("The Internet")

    def test_login_form_has_username_and_password_fields(self, browser) -> None:
        """The login page should present username and password inputs."""
        assert_that(self._page.is_element_present(By.ID, "username")).is_true()
        assert_that(self._page.is_element_present(By.ID, "password")).is_true()
