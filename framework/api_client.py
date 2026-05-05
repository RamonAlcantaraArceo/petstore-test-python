"""HTTP API client for the Swagger Petstore REST API.

Target: http://localhost:8000/api/v1  (Personal demo, still in development and pending deployment)

This client implements :class:`~framework.interfaces.PetstoreClientProtocol`
so it can be used interchangeably with the Selenium UI client wherever the
shared-interface pattern is applied.

Example
-------
::

    client = PetstoreApiClient()
    client.login("user1", "password1")
    pet = client.add_pet("Fido", status="available")
    assert pet["name"] == "Fido"
    client.delete_pet(pet["id"])
    client.close()
"""

from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "http://localhost:8000/api/v1"
DEFAULT_TIMEOUT = 10  # seconds


class PetstoreApiClient:
    """REST API client for the Swagger Petstore.

    Parameters
    ----------
    base_url:
        Root URL of the petstore API (default: public demo).
    timeout:
        Request timeout in seconds.
    api_key:
        Optional API key sent in the ``api_key`` header.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        api_key: str | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        if api_key:
            self._session.headers.update({"X-API-Key": api_key})
        self._logged_in = False
        self._auth_token: str | None = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> requests.Response:
        url = self._url(path)
        import json as _json

        # Prepare request log
        from urllib.parse import urlencode, urlparse

        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        path_and_query = parsed_url.path
        if parsed_url.query:
            path_and_query += f"?{parsed_url.query}"
        # If params are present, append as query string
        params = kwargs.get("params")
        if params:
            # If there is already a query, append with &
            sep = "&" if parsed_url.query else "?"
            path_and_query += f"{sep}{urlencode(params)}"
        summary = f"Request: {base_url} {method.upper()} {path_and_query}"

        request_log = {
            "event": "request",
            "method": method.upper(),
            "url": url,
            "headers": dict(self._session.headers),
            "extra_headers": kwargs.get("headers"),
            "params": params,
            "json": kwargs.get("json"),
            "data": kwargs.get("data"),
        }
        pretty_request = _json.dumps(
            request_log, default=str, ensure_ascii=False, indent=2
        )
        indented_request = "\n  " + pretty_request.replace("\n", "\n  ")
        logger.debug(f"{summary}{indented_request}")

        response = self._session.request(
            method,
            url,
            timeout=self._timeout,
            **kwargs,
        )

        # Prepare response log
        # If the body is JSON, include as native object; else as string
        try:
            body_obj = response.json()
        except Exception:
            body_obj = response.text

        # Parse the URL to split base, path, and query
        from urllib.parse import urlparse

        parsed_url = urlparse(response.url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        path_and_query = parsed_url.path
        if parsed_url.query:
            path_and_query += f"?{parsed_url.query}"

        # Compose summary line
        summary = f"Response: {base_url} {method.upper()} {path_and_query} [{response.status_code}]"

        response_log = {
            "event": "response",
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": dict(response.headers),
            "body": body_obj,
            "url": response.url,
        }
        pretty_response = _json.dumps(
            response_log, default=str, ensure_ascii=False, indent=2
        )
        indented_response = "\n  " + pretty_response.replace("\n", "\n  ")
        logger.debug(f"{summary}{indented_response}")
        return response

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> PetstoreApiClient:
        """Authenticate with the petstore API.

        On success, stores the session token and sets ``is_logged_in() == True``.
        """
        response = self._request(
            "GET",
            "/user/login",
            params={"username": username, "password": password},
        )
        response.raise_for_status()
        # The demo API returns a string token in the JSON message field
        data = response.json()
        token = data.get("message", "")
        if token:
            self._auth_token = token
            self._session.headers.update({"Authorization": f"Bearer {token}"})
        self._logged_in = True
        logger.info("Logged in as %s", username)
        return self

    def logout(self) -> PetstoreApiClient:
        """Log out the current session."""
        self._request("GET", "/user/logout")
        self._logged_in = False
        self._auth_token = None
        return self

    def is_logged_in(self) -> bool:
        """Return ``True`` when an active session exists."""
        return self._logged_in

    # ------------------------------------------------------------------
    # Pets
    # ------------------------------------------------------------------

    def add_pet(
        self,
        name: str,
        status: str = "available",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new pet.

        Parameters
        ----------
        name:    Pet name.
        status:  ``available`` | ``pending`` | ``sold``.
        kwargs:  Extra fields merged into the request body.
        """
        payload: dict[str, Any] = {
            "name": name,
            "status": status,
            "photoUrls": kwargs.pop("photoUrls", []),
            **kwargs,
        }
        response = self._request("POST", "/pet", json=payload)
        response.raise_for_status()
        return dict(response.json())

    def get_pet(self, pet_id: int) -> dict[str, Any]:
        """Retrieve a pet by id."""
        response = self._request("GET", f"/pet/{pet_id}")
        response.raise_for_status()
        return dict(response.json())

    def update_pet(self, pet_id: int, **kwargs: Any) -> dict[str, Any]:
        """Update an existing pet (full replacement)."""
        existing = self.get_pet(pet_id)
        payload = {**existing, **kwargs, "id": pet_id}
        response = self._request("PUT", "/pet", json=payload)
        response.raise_for_status()
        return dict(response.json())

    def delete_pet(self, pet_id: int) -> None:
        """Delete a pet by id."""
        response = self._request("DELETE", f"/pet/{pet_id}")
        response.raise_for_status()

    def find_pets_by_status(self, status: str) -> list[dict[str, Any]]:
        """Return a list of pets matching *status*."""
        response = self._request(
            "GET",
            "/pet/findByStatus",
            params={"status": status},
        )
        response.raise_for_status()
        return list(response.json())

    # ------------------------------------------------------------------
    # Users (convenience)
    # ------------------------------------------------------------------

    def create_user(
        self, username: str, password: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Create a new user account."""
        payload: dict[str, Any] = {
            "username": username,
            "password": password,
            "email": kwargs.pop("email", f"{username}@example.com"),
            "firstName": kwargs.pop("firstName", ""),
            "lastName": kwargs.pop("lastName", ""),
            "phone": kwargs.pop("phone", ""),
            "userStatus": 1,
            **kwargs,
        }
        response = self._request("POST", "/user", json=payload)
        response.raise_for_status()
        return dict(response.json())

    def get_user(self, username: str) -> dict[str, Any]:
        """Retrieve a user by username."""
        response = self._request("GET", f"/user/{username}")
        response.raise_for_status()
        return dict(response.json())

    def delete_user(self, username: str) -> None:
        """Delete a user by username."""
        response = self._request("DELETE", f"/user/{username}")
        response.raise_for_status()

    # ------------------------------------------------------------------
    # Raw request access (for advanced / negative tests)
    # ------------------------------------------------------------------

    def raw_get(self, path: str, **kwargs: Any) -> requests.Response:
        """Make a raw GET request and return the :class:`requests.Response`."""
        return self._request("GET", path, **kwargs)

    def raw_post(self, path: str, **kwargs: Any) -> requests.Response:
        """Make a raw POST request and return the :class:`requests.Response`."""
        return self._request("POST", path, **kwargs)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying :class:`requests.Session`."""
        self._session.close()
        logger.debug("Session closed")
