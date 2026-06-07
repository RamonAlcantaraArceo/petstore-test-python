import pytest

from framework.poms.atoms.select_pom import SelectPOM


@pytest.mark.smoke
def test_select_pom_class_imports():
    assert SelectPOM is not None


@pytest.mark.smoke
def test_select_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(SelectPOM, "SELECTOR")
    assert (
        SelectPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_select_story_id_defined():
    assert hasattr(SelectPOM, "STORY_ID")
    assert (
        SelectPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_select_default(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-select--default' and verify the component is visible."""
    pom = SelectPOM(driver)
    pom.navigate_to_story("common-atoms-select--default")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed()
    assert root_element.is_enabled()


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_select_disabled(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-select--disabled' and verify the component is visible."""
    pom = SelectPOM(driver)
    pom.navigate_to_story("common-atoms-select--disabled")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed()
    # Check for disabled attribute on the root element or find disabled input/select inside
    disabled_attr = root_element.get_attribute("disabled")
    if disabled_attr is None:
        # If not on wrapper, check for disabled input/select inside
        try:
            select_elements = root_element.find_elements("tag name", "select")
            if select_elements:
                disabled_attr = select_elements[0].get_attribute("disabled")
        except Exception:
            pass
    assert disabled_attr is not None, "Select should be disabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_select_with_options(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-select--with-options' and verify the component is visible."""
    pom = SelectPOM(driver)
    pom.navigate_to_story("common-atoms-select--with-options")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed()
    assert root_element.is_enabled()
