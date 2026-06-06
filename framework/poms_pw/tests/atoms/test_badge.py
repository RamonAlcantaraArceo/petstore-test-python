import pytest
from playwright.sync_api import expect



from poms.atoms.badge_pom import BadgePOM


@pytest.mark.smoke
def test_badge_pom_class_imports():
    assert BadgePOM is not None


@pytest.mark.smoke
def test_badge_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(BadgePOM, "SELECTOR")
    assert BadgePOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_badge_story_id_defined():
    assert hasattr(BadgePOM, "STORY_ID")
    assert BadgePOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_badge_navigate_and_verify(page):
    """Verify Badge POM can navigate to story and interact with the component."""
    pom = BadgePOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Generic component verification
    expect(root_locator).to_be_visible()
