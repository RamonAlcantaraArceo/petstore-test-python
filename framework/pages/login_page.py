"""Page object for the Petstore Sign In modal flow using generated POMs."""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.app.full_application_pom import FullApplicationPOM
from framework.poms.molecules.loginform_pom import LoginformPOM
from framework.poms.organisms.appnavigation_pom import AppnavigationPOM


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

        self.full_app.wait_for_visibility(
            timeout=10
        )  # Wait for the full app to load before checking for login form

        if not self._is_login_form_visible():
            self.app_navigation.primary_button().click_element()  # Click "Login" in nav to open login form
            self.login_form.wait_for_visibility(
                timeout=10
            )  # Wait for login form to be visible

        return self

    def login(self, username: str, password: str) -> LoginPage:
        """Submit credentials through the login form.

        Args:
            username: User name to submit.
            password: Password to submit.

        Returns:
            Self, to allow method chaining.
        """

        self.login_form.username_input().type_into(username)
        self.login_form.password_input().type_into(password)
        self.login_form.primary_button().click_element()

        return self

    def click_logout(self) -> LoginPage:
        """Click the logout button in the navigation bar.

        Returns:
            Self, to allow method chaining.
        """
        element = self.app_navigation.secondary_button().wait_for_visibility(timeout=2)
        assert element
        element.click()

        return self

    def is_logged_out(self) -> bool:
        """Return whether the login button is visible."""
        return (
            self.app_navigation.primary_button().wait_for_visibility(
                timeout=2, raise_on_timeout=False
            )
            is not None
        )

    def is_logged_in(self) -> bool:
        """Return whether the logout button is visible."""
        return (
            self.app_navigation.secondary_button().wait_for_visibility(
                timeout=2, raise_on_timeout=False
            )
            is not None
        )

    def _is_login_form_visible(self) -> bool:
        """Return whether the login form is currently visible."""
        return (
            self.login_form.wait_for_visibility(timeout=2, raise_on_timeout=False)
            is not None
        )

    def _is_login_form_absent(self) -> bool:
        """Return whether the login form is currently absent from the DOM."""
        return self.login_form.wait_for_absence(timeout=2, raise_on_timeout=False)
