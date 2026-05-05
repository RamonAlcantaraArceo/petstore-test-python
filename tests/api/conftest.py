"""API-specific fixtures for the tests/api suite."""

from __future__ import annotations

from collections.abc import Generator

import pytest

from framework.api_client import PetstoreApiClient
from framework.factories import PetFactory, UserFactory


@pytest.fixture
def new_pet(api_client: PetstoreApiClient) -> Generator:
    """Create a pet via the API and yield it; delete it after the test."""
    data = PetFactory.build(status="available")
    created = api_client.add_pet(
        name=data["name"],
        status=data["status"],
        photoUrls=data["photoUrls"],
    )
    yield created
    # Cleanup – ignore 404 in case the test itself deleted the pet
    try:
        api_client.delete_pet(created["id"])
    except Exception:
        pass


@pytest.fixture
def new_user(api_client: PetstoreApiClient) -> Generator:
    """Create a user via the API and yield it; delete it after the test."""
    data = UserFactory.build(username="user1", password="password1")
    created = api_client.create_user(
        username=data["username"], password=data["password"]
    )
    yield created
    # Cleanup – ignore 404 in case the test itself deleted the user
    try:
        api_client.delete_user(created["id"])
    except Exception:
        pass
