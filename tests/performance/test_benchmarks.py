"""Performance / benchmark tests using pytest-benchmark.

These tests are **excluded from CI** and are intended to be run manually:

    uv run pytest tests/performance/ --benchmark-only

Results are saved in ``.benchmarks/`` and can be compared across runs
with ``pytest-benchmark``'s histogram and comparison features.
"""

from __future__ import annotations

import pytest

from framework.api_client import PetstoreApiClient
from framework.factories import PetFactory


@pytest.mark.performance
class TestApiPerformance:
    """Benchmark key API operations."""

    def test_find_pets_by_status_available_speed(
        self, benchmark, api_client: PetstoreApiClient
    ) -> None:
        """Measure response time for GET /pet/findByStatus?status=available."""

        def _call() -> list:
            return api_client.find_pets_by_status("available")

        result = benchmark(_call)
        assert isinstance(result, list)

    def test_get_individual_pet_speed(
        self, benchmark, api_client: PetstoreApiClient
    ) -> None:
        """Measure round-trip time for GET /pet/{petId}."""
        # Create a pet to benchmark against
        pet = api_client.add_pet(name="BenchmarkPet", status="available", photoUrls=[])
        pet_id = pet["id"]

        def _call() -> dict:
            return api_client.get_pet(pet_id)

        try:
            result = benchmark(_call)
            assert result["id"] == pet_id
        finally:
            api_client.delete_pet(pet_id)

    def test_add_and_delete_pet_speed(
        self, benchmark, api_client: PetstoreApiClient
    ) -> None:
        """Measure time to add then delete a pet (write path benchmark)."""

        def _call() -> None:
            pet = api_client.add_pet(
                name=PetFactory.build()["name"],
                status="available",
                photoUrls=[],
            )
            api_client.delete_pet(pet["id"])

        benchmark(_call)
