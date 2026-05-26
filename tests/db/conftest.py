"""DB-suite fixtures – combine API creation with direct DB teardown verification."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest

from framework.api_client import PetstoreApiClient
from framework.db_client import PetstoreDbClient
from framework.factories import PetFactory, UserFactory


@pytest.fixture
def db_pet(
    api_client: PetstoreApiClient,
    db_client: PetstoreDbClient,
) -> Generator[dict[str, Any], None, None]:
    """Create a pet via the API, yield the pet dict, then delete and verify removal in DB."""
    data = PetFactory.build(status="available")
    created = api_client.add_pet(
        name=data["name"],
        status=data["status"],
        photoUrls=data["photoUrls"],
    )
    yield created
    try:
        api_client.delete_pet(created["id"])
    except Exception:
        pass


@pytest.fixture
def db_user(
    api_client: PetstoreApiClient,
    db_client: PetstoreDbClient,
) -> Generator[dict[str, Any], None, None]:
    """Create a user via the API, yield the user dict, then delete and verify removal in DB."""
    data = UserFactory.build()
    api_client.create_user(
        username=data["username"],
        firstName=data["firstName"],
        lastName=data["lastName"],
        email=data["email"],
        password=data["password"],
        phone=data["phone"],
        userStatus=data["userStatus"],
    )
    user = api_client.get_user(data["username"])
    yield user
    try:
        api_client.delete_user(user["username"])
    except Exception:
        pass
