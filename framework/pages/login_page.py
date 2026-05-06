"""Login Page Object.

Models the login page of the Petstore web UI.  The target demo site is
https://the-internet.herokuapp.com/login (a freely available test site
that provides a stable login form – it is a good stand-in while the
petstore does not ship a traditional login form in its swagger UI).

Set the ``PETSTORE_UI_BASE_URL`` environment variable or the ``base_url``
constructor argument to point at your actual application under test.

Example
-------
::

    page = LoginPage(driver, base_url="https://the-internet.herokuapp.com")
    page.open().login("tomsmith", "SuperSecretPassword!")
    assert page.is_logged_in()
"""

from __future__ import annotations

import os

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage

DEFAULT_UI_BASE_URL = os.getenv(
    "PETSTORE_UI_BASE_URL", "https://the-internet.herokuapp.com"
)


class LoginPage(BasePage):
    """Page Object for the Login page."""

    URL = "/login"

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    _USERNAME_INPUT = (By.ID, "username")
    _PASSWORD_INPUT = (By.ID, "password")
    _SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    _FLASH_MESSAGE = (By.ID, "flash")
    _LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary.radius")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def fill_username(self, username: str) -> LoginPage:
        self.type_text(*self._USERNAME_INPUT, text=username)
        return self

    def fill_password(self, password: str) -> LoginPage:
        self.type_text(*self._PASSWORD_INPUT, text=password)
        return self

    def click_login(self) -> LoginPage:
        self.click(*self._SUBMIT_BUTTON)
        return self

    def login(self, username: str, password: str) -> LoginPage:
        """Fill the form and submit it in one call."""
        return self.fill_username(username).fill_password(password).click_login()

    def get_flash_message(self) -> str:
        """Return the text of the flash / alert message."""
        try:
            return self.wait_for_visible(*self._FLASH_MESSAGE).text
        except Exception:
            return ""

    def click_logout(self) -> LoginPage:
        """Click the logout button (only available after login)."""
        self.click(*self._LOGOUT_BUTTON)
        return self

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_logged_in(self) -> bool:
        """Return True if a successful-login indicator is on the page."""
        message = self.get_flash_message()
        return "You logged into a secure area!" in message

    def is_login_failed(self) -> bool:
        """Return True when an error message is displayed."""
        message = self.get_flash_message()
        return (
            "Your username is invalid!" in message
            or "Your password is invalid!" in message
        )
