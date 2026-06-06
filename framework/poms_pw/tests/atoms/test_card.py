import pytest
from playwright.sync_api import expect



from poms.atoms.card_pom import CardPOM


@pytest.mark.smoke
def test_card_pom_class_imports():
    assert CardPOM is not None


@pytest.mark.smoke
def test_card_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(CardPOM, "SELECTOR")
    assert CardPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_card_story_id_defined():
    assert hasattr(CardPOM, "STORY_ID")
    assert CardPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_navigate_and_verify(page):
    """Verify Card POM can navigate to story and interact with the component."""
    pom = CardPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Generic component verification
    expect(root_locator).to_be_visible()
