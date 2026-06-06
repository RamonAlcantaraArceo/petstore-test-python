"""Page object for the Petstore Sign In modal flow using generated POMs."""

from __future__ import annotations

import time
from typing import Any, Protocol

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.app.full_application_pom import FullApplicationPOM
from framework.poms.molecules.loginform_pom import LoginformPOM
from framework.poms.organisms.appnavigation_pom import AppnavigationPOM


class RootablePOM(Protocol):
    def root(self) -> Any:
        """Return the underlying Selenium element or elements."""
        ...


class LoginPage:
    """Handle Sign In / Sign Out interactions against the Petstore UI."""

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Create a login page wrapper.

        Args:
            driver: Selenium WebDriver used to interact with the page.
            base_url: Root URL of the UI application.
        """
        self.driver = driver
        self.base_url = base_url.rstrip("/")

        self.full_app: FullApplicationPOM = FullApplicationPOM(driver)
        self.app_navigation: AppnavigationPOM = AppnavigationPOM(driver)
        self.login_form: LoginformPOM = LoginformPOM(driver)

    def open(self) -> LoginPage:
        """Open the application and wait for the login surface to be ready.

        Returns:
            Self, to allow method chaining.
        """
        self.driver.get(self.base_url)

        self._wait_for_pom_visible(self.full_app, timeout=10)

        if not self._is_login_form_visible():
            self.app_navigation.primary_button().root().click()
            self._wait_for_pom_visible(self.login_form, timeout=10)

        return self

    def login(self, username: str, password: str) -> LoginPage:
        """Submit credentials through the login form.

        Args:
            username: User name to submit.
            password: Password to submit.

        Returns:
            Self, to allow method chaining.
        """
        self.open()
        username_input = self.login_form.username_input().root()
        password_input = self.login_form.password_input().root()
        submit_button = self.login_form.primary_button().root()

        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        submit_button.click()
        return self

    def click_logout(self) -> LoginPage:
        """Click the logout button in the navigation bar.

        Returns:
            Self, to allow method chaining.
        """
        secondary_button_pom = self.app_navigation.secondary_button()
        self._wait_for_pom_visible(secondary_button_pom, timeout=2)
        secondary_button_pom.root().click()

        return self

    def is_logged_out(self) -> bool:
        """Return whether the login button is visible."""
        primary_button_pom = self.app_navigation.primary_button()
        return self._wait_for_pom_visible(primary_button_pom, timeout=2)

    def is_logged_in(self) -> bool:
        """Return whether the logout button is visible."""
        secondary_button_pom = self.app_navigation.secondary_button()
        return self._wait_for_pom_visible(secondary_button_pom, timeout=2)

    def _is_login_form_visible(self) -> bool:
        """Return whether the login form is currently visible."""
        return bool(self._wait_for_pom_visible(self.login_form, timeout=2))

    def _wait_for_pom_visible(self, pom: RootablePOM, timeout: int = 10) -> bool:
        """Wait for a page object root element to become visible.

        Args:
            pom: Page object exposing a ``root()`` method.
            timeout: Maximum number of seconds to wait.

        Returns:
            ``True`` when at least one root element is visible, otherwise ``False``.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                root = pom.root()
                if isinstance(root, list):
                    return any(element.is_displayed() for element in root)
                return bool(root.is_displayed())
            except (
                NoSuchElementException,
                RuntimeError,
                StaleElementReferenceException,
            ):
                time.sleep(0.1)
        return False
