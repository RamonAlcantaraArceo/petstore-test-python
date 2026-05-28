import pytest


from poms.atoms.select_pom import SelectPOM


@pytest.mark.smoke
def test_select_pom_class_imports():
    assert SelectPOM is not None


@pytest.mark.smoke
def test_select_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(SelectPOM, "SELECTOR")
    assert SelectPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_select_story_id_defined():
    assert hasattr(SelectPOM, "STORY_ID")
    assert SelectPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_select_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Select POM can navigate to story and interact with the component."""
    pom = SelectPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Select-specific: verify select can be interacted with
    select_elem = pom.root()
    assert select_elem.is_displayed(), "Select is not displayed"
    assert select_elem.is_enabled(), "Select is not enabled"
