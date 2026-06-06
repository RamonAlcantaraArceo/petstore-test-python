import pytest
from playwright.sync_api import expect



from poms.organisms.appnavigation_pom import AppnavigationPOM


@pytest.mark.smoke
def test_appnavigation_pom_class_imports():
    assert AppnavigationPOM is not None


@pytest.mark.smoke
def test_appnavigation_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(AppnavigationPOM, "SELECTOR")
    assert AppnavigationPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_appnavigation_story_id_defined():
    assert hasattr(AppnavigationPOM, "STORY_ID")
    assert AppnavigationPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_appnavigation_navigate_and_verify(page):
    """Verify Appnavigation POM can navigate to story and interact with the component."""
    pom = AppnavigationPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Generic component verification
    expect(root_locator).to_be_visible()
