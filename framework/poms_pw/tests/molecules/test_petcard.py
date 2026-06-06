import pytest
from playwright.sync_api import expect



from poms.molecules.petcard_pom import PetcardPOM


@pytest.mark.smoke
def test_petcard_pom_class_imports():
    assert PetcardPOM is not None


@pytest.mark.smoke
def test_petcard_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(PetcardPOM, "SELECTOR")
    assert PetcardPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_petcard_story_id_defined():
    assert hasattr(PetcardPOM, "STORY_ID")
    assert PetcardPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_petcard_navigate_and_verify(page):
    """Verify Petcard POM can navigate to story and interact with the component."""
    pom = PetcardPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Form/Molecule-specific: verify root locator is visible
    expect(pom.root()).to_be_visible()
