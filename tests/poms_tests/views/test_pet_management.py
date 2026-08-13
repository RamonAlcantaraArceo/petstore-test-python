import pytest

from framework.poms.molecules.petcard_pom import PetcardPOM
from framework.poms.views.pet_management_pom import PetManagementPOM


@pytest.mark.smoke
def test_pet_management_pom_class_imports():
    assert PetManagementPOM is not None


@pytest.mark.smoke
def test_pet_management_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(PetManagementPOM, "SELECTOR")
    assert (
        PetManagementPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_pet_management_story_id_defined():
    assert hasattr(PetManagementPOM, "STORY_ID")
    assert (
        PetManagementPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_pet_management_with_pets(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-pet-management--with-pets' and verify the component is visible."""
    pom = PetManagementPOM(driver)
    pom.navigate_to_story("petstore-views-pet-management--with-pets")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Pet management view should be displayed"

    petcards: list[PetcardPOM] = pom.petcards()
    assert len(petcards) == 4, "With pets story should expose four pet cards"
    for index, petcard in enumerate(petcards, start=1):
        petcard_root = petcard.wait_for_visibility(timeout=10, raise_on_timeout=False)
        assert petcard_root is not None, f"Pet card {index} should be visible"
        assert petcard_root.is_displayed(), f"Pet card {index} should be displayed"
        assert (
            petcard.danger_button().is_element_displayed()
        ), f"Pet card {index} should show the danger button"
        assert (
            petcard.secondary_button().is_element_displayed()
        ), f"Pet card {index} should show the secondary button"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert primary_button is not None, "Primary action button should be visible"
    assert primary_button.is_displayed(), "Primary action button should be displayed"
    assert primary_button.is_enabled(), "Primary action button should be enabled"

    statusfilter = pom.statusfilter().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert statusfilter is not None, "Status filter should be visible"
    assert statusfilter.is_displayed(), "Status filter should be displayed"
    assert statusfilter.is_enabled(), "Status filter should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_pet_management_read_only(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-pet-management--read-only' and verify the component is visible."""
    pom = PetManagementPOM(driver)
    pom.navigate_to_story("petstore-views-pet-management--read-only")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Pet management view should be displayed"

    petcards: list[PetcardPOM] = pom.petcards()
    assert len(petcards) == 4, "Read-only story should still show the pet cards"
    for index, petcard in enumerate(petcards, start=1):
        petcard_root = petcard.wait_for_visibility(timeout=10, raise_on_timeout=False)
        assert petcard_root is not None, f"Pet card {index} should be visible"
        assert petcard_root.is_displayed(), f"Pet card {index} should be displayed"
        assert (
            petcard.danger_button().is_element_absent()
        ), f"Pet card {index} should not show the danger button"
        assert (
            petcard.secondary_button().is_element_absent()
        ), f"Pet card {index} should not show the secondary button"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        primary_button is None
    ), "Read-only story should not render the primary button"

    statusfilter = pom.statusfilter().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert statusfilter is not None, "Status filter should be visible"
    assert statusfilter.is_displayed(), "Status filter should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_pet_management_empty(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-pet-management--empty' and verify the component is visible."""
    pom = PetManagementPOM(driver)
    pom.navigate_to_story("petstore-views-pet-management--empty")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Empty pet management view should be displayed"

    petcards = pom.petcards()
    assert len(petcards) == 0, "Empty story should not render any pet cards"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert primary_button is not None, "Primary action button should be visible"
    assert primary_button.is_displayed(), "Primary action button should be displayed"
    assert primary_button.is_enabled(), "Primary action button should be enabled"

    statusfilter = pom.statusfilter().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert statusfilter is not None, "Status filter should be visible"
    assert statusfilter.is_displayed(), "Status filter should be displayed"
