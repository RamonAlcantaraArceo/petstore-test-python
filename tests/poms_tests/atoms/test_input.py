import pytest


from framework.poms.atoms.input_pom import InputPOM


@pytest.mark.smoke
def test_input_pom_class_imports():
    assert InputPOM is not None


@pytest.mark.smoke
def test_input_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(InputPOM, "SELECTOR")
    assert InputPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_input_story_id_defined():
    assert hasattr(InputPOM, "STORY_ID")
    assert InputPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Input POM can navigate to story and interact with the component."""
    pom = InputPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Input-specific: verify we can type into the input
    input_elem = pom.root()
    input_elem.clear()
    test_input_value = "test_value_123"
    input_elem.send_keys(test_input_value)
    assert input_elem.get_attribute("value") == test_input_value, "Input value not set correctly"
