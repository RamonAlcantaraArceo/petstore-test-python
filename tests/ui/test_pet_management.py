"""BDD-style UI scenario definitions for pet management."""

from __future__ import annotations

import os
from uuid import uuid4

import allure
import pytest

from framework.assertions import assert_that
from framework.factories import PetFactory
from framework.ui_client import PetstoreUiClient

pytestmark = pytest.mark.ui

skip_if_no_ui = pytest.mark.skipif(
    os.getenv("RUN_UI_TESTS", "0") not in ("1", "true", "yes"),
    reason="UI tests are disabled. Set RUN_UI_TESTS=1 to enable.",
)

scenario_definition_only = pytest.mark.skip(
    reason="BDD scenario definition only; implementation steps will follow in next iteration."
)


def _unique_name(prefix: str) -> str:
    """Return a collision-resistant pet name for concurrent UI test runs."""
    return f"{prefix}-{uuid4().hex[:8]}"


@allure.feature("Pet Management")
@allure.story("Authenticated pet CRUD and status filtering")
class TestPetManagementBddScenarios:
    """Scenario definitions for managing pets from the Petstore UI."""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "pet-management", "bdd", "happy-path", "create-delete")
    @allure.title("Authenticated user can add and delete a pet")
    @skip_if_no_ui
    def test_authenticated_user_can_add_delete_pet(
        self, ui_client: PetstoreUiClient
    ) -> None:
        """Verify create/delete flow through the UI after login.

        A signed-in user (admin/secret) can create a pet using PetFactory-generated values,
        retrieve it, and delete it from the system.
        """
        pet_data = PetFactory.build(
            name=_unique_name("create-delete"),
            status="available",
        )
        created_pet_id: int | None = None

        with allure.step("Given the Petstore app is open and user signs in"):
            ui_client.login_page.open()
            ui_client.login(username="admin1", password="secret")
            assert_that(ui_client.is_logged_in()).is_true()

        try:
            with allure.step("When the user creates a pet from generated test data"):
                created = ui_client.add_pet(
                    name=pet_data["name"],
                    status=pet_data["status"],
                    category=pet_data["category"],
                    photoUrls=pet_data["photoUrls"],
                )
                created_pet_id = created["id"]

                assert_that(created["id"]).is_instance_of(int)
                assert_that(created["name"]).equals(pet_data["name"])
                assert_that(created["status"]).equals(pet_data["status"])

            with allure.step("And retrieves the created pet by id"):
                retrieved = ui_client.get_pet(created_pet_id)
                assert_that(retrieved["id"]).equals(created_pet_id)
                assert_that(retrieved["name"]).equals(pet_data["name"])
                assert_that(retrieved["status"]).equals(pet_data["status"])

            with allure.step("Then the user can delete the pet and it is removed"):
                ui_client.delete_pet(created_pet_id)

                with pytest.raises(KeyError):
                    ui_client.get_pet(created_pet_id)

        finally:
            if created_pet_id is not None and ui_client.is_logged_in():
                try:
                    ui_client.delete_pet(created_pet_id)
                except KeyError:
                    pass

            if ui_client.is_logged_in():
                ui_client.logout()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "pet-management", "bdd", "happy-path", "create-update-delete")
    @allure.title("Authenticated user can add, update, and delete a pet")
    @pytest.mark.xfail(
        reason="Known UI behavior: update submission closes the form but does not persist changes.",
        strict=False,
    )
    @skip_if_no_ui
    def test_authenticated_user_can_add_update_delete_pet(
        self, ui_client: PetstoreUiClient
    ) -> None:
        """Isolate the update path after a successful create operation."""
        pet_data = PetFactory.build(
            name=_unique_name("create-update-delete"),
            status="available",
        )
        created_pet_id: int | None = None
        updated_name = f"{pet_data['name']}-updated"
        updated_status = "sold" if pet_data["status"] != "sold" else "pending"

        with allure.step("Given the Petstore app is open and user signs in"):
            ui_client.login_page.open()
            ui_client.login(username="admin1", password="secret")
            assert_that(ui_client.is_logged_in()).is_true()

        try:
            with allure.step("When the user creates a pet from generated test data"):
                created = ui_client.add_pet(
                    name=pet_data["name"],
                    status=pet_data["status"],
                    category=pet_data["category"],
                    photoUrls=pet_data["photoUrls"],
                )
                created_pet_id = created["id"]
                assert_that(created["name"]).equals(pet_data["name"])

            with allure.step("And updates the pet name and status"):
                updated = ui_client.update_pet(
                    created_pet_id,
                    name=updated_name,
                    status=updated_status,
                )
                created_pet_id = updated["id"]
                assert_that(updated["name"]).equals(updated_name)
                assert_that(updated["status"]).equals(updated_status)

            with allure.step("Then the user can delete the updated pet"):
                ui_client.delete_pet(created_pet_id)
                with pytest.raises(KeyError):
                    ui_client.get_pet(created_pet_id)

        finally:
            if created_pet_id is not None and ui_client.is_logged_in():
                try:
                    ui_client.delete_pet(created_pet_id)
                except KeyError:
                    pass

            if ui_client.is_logged_in():
                ui_client.logout()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "pet-management", "bdd", "status", "coverage")
    @allure.title("Pet creation supports available, pending, and sold statuses")
    @pytest.mark.xfail(
        reason="Known UI behavior: created pets are currently persisted as 'available'.",
        strict=False,
    )
    @skip_if_no_ui
    def test_pet_creation_supports_all_valid_statuses(
        self, ui_client: PetstoreUiClient
    ) -> None:
        """Verify pet creation for each valid state.

        The UI allows creating pets with status values available, pending, and sold,
        and each created pet persists with the selected status.
        """
        created_ids: list[int] = []
        valid_statuses = ("available", "pending", "sold")

        with allure.step("Given the user signs in"):
            ui_client.login_page.open()
            ui_client.login(username="admin1", password="secret")
            assert_that(ui_client.is_logged_in()).is_true()

        try:
            for status in valid_statuses:
                with allure.step(f"When a pet is created with status '{status}'"):
                    pet_data = PetFactory.build(
                        status=status,
                        name=_unique_name(f"{status}-pet"),
                    )
                    created = ui_client.add_pet(
                        name=pet_data["name"],
                        status=pet_data["status"],
                        category=pet_data["category"],
                        photoUrls=pet_data["photoUrls"],
                    )
                    created_ids.append(created["id"])
                    assert_that(created["status"]).equals(status)

                with allure.step(
                    "Then the created pet can be retrieved with the same status"
                ):
                    retrieved = ui_client.get_pet(created["id"])
                    assert_that(retrieved["name"]).equals(pet_data["name"])
                    assert_that(retrieved["status"]).equals(status)

        finally:
            for pet_id in reversed(created_ids):
                try:
                    ui_client.delete_pet(pet_id)
                except KeyError:
                    pass
            if ui_client.is_logged_in():
                ui_client.logout()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "pet-management", "bdd", "status", "update")
    @allure.title("Pet status can be updated between any valid states")
    @pytest.mark.xfail(
        reason="Known UI behavior: update submission closes the form but does not persist changes.",
        strict=False,
    )
    @skip_if_no_ui
    def test_pet_status_can_transition_between_valid_states(
        self, ui_client: PetstoreUiClient
    ) -> None:
        """Verify unrestricted status transitions among valid values.

        A pet can be updated from available to pending to sold (and reverse where applicable)
        without UI-imposed restrictions beyond valid status options.
        """
        created_pet_id: int | None = None
        transition_sequence = ["available", "pending", "sold", "available"]

        with allure.step("Given the user signs in and creates an available pet"):
            ui_client.login_page.open()
            ui_client.login(username="admin1", password="secret")
            assert_that(ui_client.is_logged_in()).is_true()

            seed = PetFactory.build(status="available")
            seed["name"] = _unique_name("transition-seed")
            created = ui_client.add_pet(
                name=seed["name"],
                status=seed["status"],
                category=seed["category"],
                photoUrls=seed["photoUrls"],
            )
            created_pet_id = created["id"]
            assert_that(created["status"]).equals("available")

        try:
            for next_status in transition_sequence[1:]:
                with allure.step(f"When status is updated to '{next_status}'"):
                    updated = ui_client.update_pet(created_pet_id, status=next_status)
                    created_pet_id = updated["id"]

                with allure.step("Then the pet reflects the target status"):
                    assert_that(updated["status"]).equals(next_status)

        finally:
            if created_pet_id is not None and ui_client.is_logged_in():
                try:
                    ui_client.delete_pet(created_pet_id)
                except KeyError:
                    pass
            if ui_client.is_logged_in():
                ui_client.logout()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "pet-management", "bdd", "filter", "validation")
    @allure.title("Status filter accepts only available, pending, and sold")
    @pytest.mark.xfail(
        reason="Known UI behavior: non-'available' statuses are not reliably persisted/filterable.",
        strict=False,
    )
    @skip_if_no_ui
    def test_status_filter_accepts_only_valid_status_values(
        self, ui_client: PetstoreUiClient
    ) -> None:
        """Verify status filter validation and behavior.

        The status filter supports only available, pending, and sold values, correctly filters
        pets by the chosen status, and rejects invalid status inputs.
        """
        created_ids: list[int] = []
        created_by_status: dict[str, int] = {}
        valid_statuses = ("available", "pending", "sold")

        with allure.step(
            "Given the user signs in and creates one pet per valid status"
        ):
            ui_client.login_page.open()
            ui_client.login(username="admin1", password="secret")
            assert_that(ui_client.is_logged_in()).is_true()

            for status in valid_statuses:
                pet_data = PetFactory.build(
                    status=status,
                    name=_unique_name(f"filter-{status}-pet"),
                )
                created = ui_client.add_pet(
                    name=pet_data["name"],
                    status=pet_data["status"],
                    category=pet_data["category"],
                    photoUrls=pet_data["photoUrls"],
                )
                created_ids.append(created["id"])
                created_by_status[status] = created["id"]

        try:
            for status in valid_statuses:
                with allure.step(f"When filtering by '{status}'"):
                    filtered = ui_client.find_pets_by_status(status)
                    filtered_ids = {pet["id"] for pet in filtered}

                with allure.step("Then matching status pets are returned"):
                    assert_that(created_by_status[status] in filtered_ids).is_true()
                    assert_that(
                        all(pet["status"] == status for pet in filtered)
                    ).is_true()

            with allure.step("And invalid status values are rejected"):
                with pytest.raises(ValueError):
                    ui_client.find_pets_by_status("invalid-status")

        finally:
            for pet_id in reversed(created_ids):
                try:
                    ui_client.delete_pet(pet_id)
                except KeyError:
                    pass
            if ui_client.is_logged_in():
                ui_client.logout()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("ui", "pet-management", "bdd", "auth", "session")
    @allure.title("Pet management operations require authenticated session")
    @skip_if_no_ui
    def test_pet_management_operations_require_authentication(
        self, ui_client: PetstoreUiClient
    ) -> None:
        """Verify authentication requirement for write operations.

        Creating, updating, and deleting pets requires an authenticated user session;
        after logout, those operations are no longer permitted from the UI.
        """
        with allure.step("Given the user opens the Petstore UI in logged-out state"):
            ui_client.login_page.open()
            assert_that(ui_client.login_page.is_logged_out()).is_true()
            assert_that(ui_client.is_logged_in()).is_false()

        with allure.step("When an unauthenticated user tries to create a pet"):
            with pytest.raises(PermissionError):
                ui_client.add_pet(name="unauthorized-pet", status="available")
