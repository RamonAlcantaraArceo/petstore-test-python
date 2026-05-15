"""Performance / benchmark tests using pytest-benchmark.

These tests are **excluded from CI** and are intended to be run manually:

    uv run pytest tests/performance/ --benchmark-only

Results are saved in ``.benchmarks/`` and can be compared across runs
with ``pytest-benchmark``'s histogram and comparison features.
"""

from __future__ import annotations

import asyncio
from collections.abc import Generator

import pytest
from petstore_openapi_client import ApiClient, Configuration
from petstore_openapi_client.api.pet_api import PetApi
from petstore_openapi_client.models.pet_create import PetCreate
from petstore_openapi_client.models.pet_status import PetStatus

from framework.factories import PetFactory


@pytest.fixture
def gen_pet_api_client_sync(
    gen_client_configuration: Configuration,
) -> Generator[tuple[PetApi, asyncio.AbstractEventLoop], None, None]:
    """Provide generated PetApi and a dedicated event loop for sync benchmarks."""
    loop = asyncio.new_event_loop()
    client = ApiClient(configuration=gen_client_configuration)
    loop.run_until_complete(client.__aenter__())
    pet_api = PetApi(api_client=client)

    try:
        yield pet_api, loop
    finally:
        loop.run_until_complete(client.close())
        loop.close()


@pytest.mark.performance
class TestApiPerformance:
    """Benchmark key API operations."""

    def test_find_pets_by_status_available_speed(
        self, benchmark, gen_pet_api_client_sync: tuple[PetApi, asyncio.AbstractEventLoop]
    ) -> None:
        """Measure response time for GET /pet/findByStatus?status=available."""
        pet_api, loop = gen_pet_api_client_sync

        def _call() -> list:
            return loop.run_until_complete(
                pet_api.find_pets_by_status(status=PetStatus.AVAILABLE)
            )

        result = benchmark(_call)
        assert isinstance(result, list)

    def test_get_individual_pet_speed(
        self, benchmark, gen_pet_api_client_sync: tuple[PetApi, asyncio.AbstractEventLoop]
    ) -> None:
        """Measure round-trip time for GET /pet/{petId}."""
        pet_api, loop = gen_pet_api_client_sync

        # Create a pet to benchmark against
        created_pet = loop.run_until_complete(
            pet_api.add_pet(
                pet_create=PetCreate(
                    name="BenchmarkPet",
                    status=PetStatus.AVAILABLE,
                    photoUrls=[],
                )
            )
        )
        assert created_pet.id is not None
        pet_id = created_pet.id

        def _call() -> object:
            return loop.run_until_complete(pet_api.get_pet_by_id(pet_id=pet_id))

        try:
            result = benchmark(_call)
            assert result.id == pet_id
        finally:
            loop.run_until_complete(pet_api.delete_pet(pet_id=pet_id))

    def test_add_and_delete_pet_speed(
        self, benchmark, gen_pet_api_client_sync: tuple[PetApi, asyncio.AbstractEventLoop]
    ) -> None:
        """Measure time to add then delete a pet (write path benchmark)."""
        pet_api, loop = gen_pet_api_client_sync

        def _call() -> None:
            pet = loop.run_until_complete(
                pet_api.add_pet(
                    pet_create=PetCreate(
                        name=PetFactory.build()["name"],
                        status=PetStatus.AVAILABLE,
                        photoUrls=[],
                    )
                )
            )
            assert pet.id is not None
            loop.run_until_complete(pet_api.delete_pet(pet_id=pet.id))

        benchmark(_call)
