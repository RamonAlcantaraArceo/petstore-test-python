import pytest
from playwright.sync_api import expect



from poms.atoms.button_pom import ButtonPOM


@pytest.mark.smoke
def test_button_pom_class_imports():
    assert ButtonPOM is not None


@pytest.mark.smoke
def test_button_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(ButtonPOM, "SELECTOR")
    assert ButtonPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_button_story_id_defined():
    assert hasattr(ButtonPOM, "STORY_ID")
    assert ButtonPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_navigate_and_verify(page):
    """Verify Button POM can navigate to story and interact with the component."""
    pom = ButtonPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Button-specific: verify button is clickable
    button_elem = pom.root()
    expect(button_elem).to_be_visible()
    expect(button_elem).to_be_enabled()
