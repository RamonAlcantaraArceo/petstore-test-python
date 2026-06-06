import pytest
from playwright.sync_api import expect



from poms.molecules.userform_pom import UserformPOM


@pytest.mark.smoke
def test_userform_pom_class_imports():
    assert UserformPOM is not None


@pytest.mark.smoke
def test_userform_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(UserformPOM, "SELECTOR")
    assert UserformPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_userform_story_id_defined():
    assert hasattr(UserformPOM, "STORY_ID")
    assert UserformPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_userform_navigate_and_verify(page):
    """Verify Userform POM can navigate to story and interact with the component."""
    pom = UserformPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Form/Molecule-specific: verify root locator is visible
    expect(pom.root()).to_be_visible()
