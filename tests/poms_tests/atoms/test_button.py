import pytest

from framework.poms.atoms.button_pom import ButtonPOM


@pytest.mark.smoke
def test_button_pom_class_imports():
    assert ButtonPOM is not None


@pytest.mark.smoke
def test_button_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(ButtonPOM, "SELECTOR")
    assert ButtonPOM.SELECTOR, (
        "SELECTOR is empty — run sbpom again with playwright installed"
    )


@pytest.mark.smoke
def test_button_story_id_defined():
    assert hasattr(ButtonPOM, "STORY_ID")
    assert ButtonPOM.STORY_ID, (
        "STORY_ID is empty — no renderable story found for this component"
    )


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Button POM can navigate to story and interact with the component."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Button-specific: verify button is clickable
    button_elem = pom.root()
    assert button_elem.is_displayed(), "Button is not displayed"
    assert button_elem.is_enabled(), "Button is not enabled"
