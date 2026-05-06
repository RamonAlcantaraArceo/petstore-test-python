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

import allure
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


@allure.feature("UI Authentication")
@allure.label("suite", "UI")
@skip_if_no_ui
class TestLoginUi:
    """Selenium tests for the login page using the Page Object Model."""

    @pytest.fixture(autouse=True)
    def _open_login_page(self, browser, ui_base_url: str) -> None:
        """Navigate to the login page before each test."""
        self._page = LoginPage(browser, base_url=ui_base_url)
        self._page.open()

    @allure.story("Successful login")
    @allure.title("Valid credentials show the secure area message")
    def test_successful_login_shows_secure_area(self, browser) -> None:
        """Logging in with valid credentials should show the secure area message.

        This mirrors tests/api/test_login.py::TestLogin::test_login_sets_authenticated_state
        using the identical assertion style.
        """
        with allure.step("Submit valid credentials"):
            self._page.login("tomsmith", "SuperSecretPassword!")

        with allure.step("Verify secure area is shown"):
            assert_that(self._page.is_logged_in()).is_true()
            assert_that(self._page.get_flash_message()).contains(
                "You logged into a secure area!"
            )

    @allure.story("Failed login")
    @allure.title("Invalid credentials show an error message")
    def test_failed_login_shows_error_message(self, browser) -> None:
        """Logging in with invalid credentials should show an error message."""
        with allure.step("Submit invalid credentials"):
            self._page.login("wrong_user", "wrong_pass")

        with allure.step("Verify login failed and error is displayed"):
            assert_that(self._page.is_logged_in()).is_false()
            assert_that(self._page.is_login_failed()).is_true()

    @allure.story("Session state")
    @allure.title("Logout after login returns to the login page")
    def test_login_then_logout_returns_to_login_page(
        self, browser, ui_base_url: str
    ) -> None:
        """After login and logout the user should be back on the login page."""
        with allure.step("Login with valid credentials"):
            self._page.login("tomsmith", "SuperSecretPassword!")
            assert_that(self._page.is_logged_in()).is_true()

        with allure.step("Click logout"):
            self._page.click_logout()

        with allure.step("Verify URL contains /login"):
            assert_that(self._page.current_url).contains("/login")

    @allure.story("Page structure")
    @allure.title("Login page title is 'The Internet'")
    def test_page_title_is_correct(self, browser) -> None:
        """The login page title should be 'The Internet'."""
        with allure.step("Verify page title"):
            assert_that(self._page.title).contains("The Internet")

    @allure.story("Page structure")
    @allure.title("Login page has username and password input fields")
    def test_login_form_has_username_and_password_fields(self, browser) -> None:
        """The login page should present username and password inputs."""
        with allure.step("Check username field is present"):
            assert_that(self._page.is_element_present(By.ID, "username")).is_true()

        with allure.step("Check password field is present"):
            assert_that(self._page.is_element_present(By.ID, "password")).is_true()
