import pytest

from framework.poms.atoms.modal_pom import ModalPOM


@pytest.mark.smoke
def test_modal_pom_class_imports():
    assert ModalPOM is not None


@pytest.mark.smoke
def test_modal_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(ModalPOM, "SELECTOR")
    assert (
        ModalPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_modal_story_id_defined():
    assert hasattr(ModalPOM, "STORY_ID")
    assert (
        ModalPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_modal_open_closed(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-modal--open-closed' and verify the component is visible."""
    pom = ModalPOM(driver)
    pom.navigate_to_story("common-atoms-modal--open-closed")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Modal should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_modal_sizes(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-modal--sizes' and verify the component is visible."""
    pom = ModalPOM(driver)
    pom.navigate_to_story("common-atoms-modal--sizes")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Modal should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_modal_focus_trap(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-modal--focus-trap' and verify the component is visible."""
    pom = ModalPOM(driver)
    pom.navigate_to_story("common-atoms-modal--focus-trap")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Modal should be displayed"
