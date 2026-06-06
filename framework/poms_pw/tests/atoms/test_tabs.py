import pytest
from playwright.sync_api import expect



from poms.atoms.tabs_pom import TabsPOM


@pytest.mark.smoke
def test_tabs_pom_class_imports():
    assert TabsPOM is not None


@pytest.mark.smoke
def test_tabs_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(TabsPOM, "SELECTOR")
    assert TabsPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_tabs_story_id_defined():
    assert hasattr(TabsPOM, "STORY_ID")
    assert TabsPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabs_navigate_and_verify(page):
    """Verify Tabs POM can navigate to story and interact with the component."""
    pom = TabsPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Generic component verification
    expect(root_locator).to_be_visible()
