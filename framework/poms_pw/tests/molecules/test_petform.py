import pytest
from playwright.sync_api import expect



from poms.molecules.petform_pom import PetformPOM


@pytest.mark.smoke
def test_petform_pom_class_imports():
    assert PetformPOM is not None


@pytest.mark.smoke
def test_petform_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(PetformPOM, "SELECTOR")
    assert PetformPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_petform_story_id_defined():
    assert hasattr(PetformPOM, "STORY_ID")
    assert PetformPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_petform_navigate_and_verify(page):
    """Verify Petform POM can navigate to story and interact with the component."""
    pom = PetformPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Form/Molecule-specific: verify root locator is visible
    expect(pom.root()).to_be_visible()
