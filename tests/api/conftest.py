"""API-specific fixtures for the tests/api suite."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest

from framework.api_client import PetstoreApiClient
from framework.factories import PetFactory


@pytest.fixture
def new_pet(api_client: PetstoreApiClient) -> Generator[dict[str, Any], None, None]:
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
