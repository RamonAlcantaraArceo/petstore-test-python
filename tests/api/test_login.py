"""API tests – authentication / login.

These tests verify the Petstore login endpoint directly via HTTP.
The same assertion style is used in tests/ui/test_login.py so the
two suites are visually identical despite different underlying mechanics.
"""

from __future__ import annotations

import allure
import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_response, assert_that


@allure.feature("Authentication")
@pytest.mark.api
@pytest.mark.usefixtures("new_user")
class TestLogin:
    """Tests for the GET /user/login endpoint."""

    @allure.story("Successful login")
    @allure.title("Valid credentials return HTTP 200 with session token")
    def test_login_with_valid_credentials_returns_200(
        self, api_client: PetstoreApiClient
    ) -> None:
        """A valid login request should return HTTP 200 with a session token."""
        with allure.step("Send login request with valid credentials"):
            response = api_client.raw_get(
                "/user/login",
                params={"username": "user1", "password": "password1"},
            )

        with allure.step("Verify 200 OK and token present in body"):
            assert_response(response).is_ok().body_contains("token-user")

    @allure.story("Session state")
    @allure.title("Login sets authenticated state on client")
    def test_login_sets_authenticated_state(
        self, api_client: PetstoreApiClient
    ) -> None:
        """After login() the client should report is_logged_in() == True."""
        with allure.step("Verify client is not authenticated before login"):
            assert_that(api_client.is_logged_in()).is_false()

        with allure.step("Perform login"):
            api_client.login("user1", "password1")

        with allure.step("Verify client is authenticated after login"):
            assert_that(api_client.is_logged_in()).is_true()

    @allure.story("Successful login")
    @allure.title("Login response JSON contains a session token")
    def test_login_returns_session_token(self, api_client: PetstoreApiClient) -> None:
        """The login response JSON should contain a session token."""
        with allure.step("Send login request"):
            response = api_client.raw_get(
                "/user/login",
                params={"username": "user1", "password": "password1"},
            )

        with allure.step("Verify token key exists and value contains username"):
            assert_response(response).is_ok().json_has_key("token")
            token = response.json()["token"]
            assert_that(token).is_not_none().contains("user1")

    @allure.story("Session state")
    @allure.title("Logout after login clears the session")
    def test_login_then_logout_clears_session(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Calling logout() after login() should clear the session state."""
        with allure.step("Login and verify authenticated"):
            api_client.login("user1", "password1")
            assert_that(api_client.is_logged_in()).is_true()

        with allure.step("Logout"):
            api_client.logout()

        with allure.step("Verify session is cleared"):
            assert_that(api_client.is_logged_in()).is_false()

    @allure.story("Successful login")
    @allure.title("Login response has expected JSON structure")
    def test_login_response_structure(self, api_client: PetstoreApiClient) -> None:
        """The login response should have the expected JSON structure."""
        with allure.step("Send login request"):
            response = api_client.raw_get(
                "/user/login",
                params={"username": "user1", "password": "password1"},
            )

        with allure.step("Verify response has 'token' key"):
            assert_response(response).is_ok().json_has_key("token")
