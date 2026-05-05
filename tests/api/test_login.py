"""API tests – authentication / login.

These tests verify the Petstore login endpoint directly via HTTP.
The same assertion style is used in tests/ui/test_login.py so the
two suites are visually identical despite different underlying mechanics.
"""

from __future__ import annotations

import pytest

from framework.api_client import PetstoreApiClient
from framework.assertions import assert_response, assert_that


@pytest.mark.api
class TestLogin:
    """Tests for the GET /user/login endpoint."""

    def test_login_with_valid_credentials_returns_200(
        self, api_client: PetstoreApiClient
    ) -> None:
        """A valid login request should return HTTP 200 with a session token."""
        response = api_client.raw_get(
            "/user/login",
            params={"username": "user", "password": "user"},
        )

        assert_response(response).is_ok().body_contains("token-user")

    def test_login_sets_authenticated_state(
        self, api_client: PetstoreApiClient
    ) -> None:
        """After login() the client should report is_logged_in() == True."""
        assert_that(api_client.is_logged_in()).is_false()

        api_client.login("user1", "password1")

        assert_that(api_client.is_logged_in()).is_true()

    def test_login_returns_session_token(self, api_client: PetstoreApiClient) -> None:
        """The login response JSON should contain a session token."""
        response = api_client.raw_get(
            "/user/login",
            params={"username": "user1", "password": "password1"},
        )

        assert_response(response).is_ok().json_has_key("token")
        token = response.json()["token"]
        assert_that(token).is_not_none().contains("user1")

    def test_login_then_logout_clears_session(
        self, api_client: PetstoreApiClient
    ) -> None:
        """Calling logout() after login() should clear the session state."""
        api_client.login("user1", "password1")
        assert_that(api_client.is_logged_in()).is_true()

        api_client.logout()

        assert_that(api_client.is_logged_in()).is_false()

    def test_login_response_structure(self, api_client: PetstoreApiClient) -> None:
        """The login response should have the expected JSON structure."""
        response = api_client.raw_get(
            "/user/login",
            params={"username": "user1", "password": "password1"},
        )

        assert_response(response).is_ok().json_has_key("token")
