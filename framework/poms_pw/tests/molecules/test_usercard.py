import pytest
from playwright.sync_api import expect



from poms.molecules.usercard_pom import UsercardPOM


@pytest.mark.smoke
def test_usercard_pom_class_imports():
    assert UsercardPOM is not None


@pytest.mark.smoke
def test_usercard_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(UsercardPOM, "SELECTOR")
    assert UsercardPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_usercard_story_id_defined():
    assert hasattr(UsercardPOM, "STORY_ID")
    assert UsercardPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_usercard_navigate_and_verify(page):
    """Verify Usercard POM can navigate to story and interact with the component."""
    pom = UsercardPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Form/Molecule-specific: verify root locator is visible
    expect(pom.root()).to_be_visible()
