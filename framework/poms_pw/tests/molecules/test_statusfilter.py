import pytest
from playwright.sync_api import expect



from poms.molecules.statusfilter_pom import StatusfilterPOM


@pytest.mark.smoke
def test_statusfilter_pom_class_imports():
    assert StatusfilterPOM is not None


@pytest.mark.smoke
def test_statusfilter_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(StatusfilterPOM, "SELECTOR")
    assert StatusfilterPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_statusfilter_story_id_defined():
    assert hasattr(StatusfilterPOM, "STORY_ID")
    assert StatusfilterPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_statusfilter_navigate_and_verify(page):
    """Verify Statusfilter POM can navigate to story and interact with the component."""
    pom = StatusfilterPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Form/Molecule-specific: verify root locator is visible
    expect(pom.root()).to_be_visible()
