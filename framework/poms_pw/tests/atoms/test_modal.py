import pytest
from playwright.sync_api import expect



from poms.atoms.modal_pom import ModalPOM


@pytest.mark.smoke
def test_modal_pom_class_imports():
    assert ModalPOM is not None


@pytest.mark.smoke
def test_modal_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(ModalPOM, "SELECTOR")
    assert ModalPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_modal_story_id_defined():
    assert hasattr(ModalPOM, "STORY_ID")
    assert ModalPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_modal_navigate_and_verify(page):
    """Verify Modal POM can navigate to story and interact with the component."""
    pom = ModalPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Generic component verification
    expect(root_locator).to_be_visible()
