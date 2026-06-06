import pytest
from playwright.sync_api import expect



from poms.views.pet_management_pom import PetManagementPOM


@pytest.mark.smoke
def test_pet_management_pom_class_imports():
    assert PetManagementPOM is not None


@pytest.mark.smoke
def test_pet_management_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(PetManagementPOM, "SELECTOR")
    assert PetManagementPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_pet_management_story_id_defined():
    assert hasattr(PetManagementPOM, "STORY_ID")
    assert PetManagementPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_pet_management_navigate_and_verify(page):
    """Verify PetManagement POM can navigate to story and interact with the component."""
    pom = PetManagementPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Generic component verification
    expect(root_locator).to_be_visible()
