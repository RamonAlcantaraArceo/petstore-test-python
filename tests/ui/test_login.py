"""BDD-style UI scenarios for Sign In / Sign Out.

These are scenario-first test cases for the Petstore UI login flow.
They intentionally focus on executable documentation and Allure metadata.
"""

from __future__ import annotations

import os

import allure
import pytest

from framework.ui_client import PetstoreUiClient

pytestmark = pytest.mark.ui


def _ui_enabled() -> bool:
    return os.getenv("RUN_UI_TESTS", "0") in ("1", "true", "yes")


skip_if_no_ui = pytest.mark.skipif(
    not _ui_enabled(),
    reason="UI tests are disabled. Set RUN_UI_TESTS=1 to enable.",
)

scenario_definition_only = pytest.mark.skip(
    reason="BDD scenario definition only; implementation steps will follow in next iteration."
)


@allure.feature("Authentication")
@allure.story("Sign In / Sign Out flow")
class TestSignInSignOutBddScenarios:
    """Scenario definitions for login/logout user journeys."""

    @skip_if_no_ui
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "auth", "bdd", "happy-path")
    @allure.title("Sign In with valid credentials")
    def test_sign_in_with_valid_credentials(self, ui_client: PetstoreUiClient) -> None:
        """Successful authentication grants access to the application.

        Instructions:
            Given the Petstore application is open at /petstore
            And the Sign In form is visible
            When the user enters username "admin"
            And enters password "secret"
            And submits the Sign In form
            Then the authenticated application navigation is visible
            And the user can see the Sign Out action
            And the Sign In form is no longer shown
        """

        with allure.step("Given the Petstore application is open at /petstore"):
            ui_client.login_page.open()
            assert ui_client.login_page.is_logged_out()

        with allure.step('When the user signs in with "admin" / "secret"'):
            ui_client.login(username="admin", password="secret")

        with allure.step("Then the authenticated application navigation is visible"):
            assert ui_client.login_page.is_logged_in()

        with allure.step("And the user can see the Sign Out action"):
            assert ui_client.login_page.is_logged_in()

        with allure.step("And the Sign In form is no longer shown"):
            assert ui_client.login_page._is_login_form_absent()

    @skip_if_no_ui
    @scenario_definition_only
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "auth", "bdd", "negative")
    @allure.title("Sign In with invalid password is rejected")
    def test_sign_in_with_invalid_password_is_rejected(self) -> None:
        """Authentication should fail with invalid credentials.
        d
                Instructions:
                    Given the Petstore application is open at /petstore
                    And the Sign In form is visible
                    When the user enters username "admin"
                    And enters password "invalid-secret"
                    And submits the Sign In form
                    Then an authentication error message is displayed
                    And the Sign In form remains visible
                    And the user does not see the authenticated navigation
        """

    @skip_if_no_ui
    @scenario_definition_only
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "auth", "bdd", "logout")
    @allure.title("Sign Out after successful Sign In returns to logged-out state")
    def test_sign_out_after_successful_sign_in(self) -> None:
        """A signed-in user can explicitly terminate the session.

        Instructions:
            Given the user is signed in with username "admin" and password "secret"
            And the authenticated application navigation is visible
            When the user clicks the Sign Out action
            Then the Sign In form is visible again
            And protected/authenticated navigation controls are hidden
            And no authenticated user session indicator remains
        """

    @skip_if_no_ui
    @scenario_definition_only
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("ui", "auth", "bdd", "validation")
    @allure.title("Sign In requires both username and password")
    def test_sign_in_requires_username_and_password(self) -> None:
        """Client-side validation blocks empty-credentials submission.

        Instructions:
            Given the Petstore application is open at /petstore
            And the Sign In form is visible
            When the user leaves username empty
            And leaves password empty
            And submits the Sign In form
            Then required-field validation is shown for username
            And required-field validation is shown for password
            And authentication is not attempted
        """
