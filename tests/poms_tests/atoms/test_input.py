import pytest

from framework.poms.atoms.input_pom import InputPOM


@pytest.mark.smoke
def test_input_pom_class_imports():
    assert InputPOM is not None


@pytest.mark.smoke
def test_input_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(InputPOM, "SELECTOR")
    assert (
        InputPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_input_story_id_defined():
    assert hasattr(InputPOM, "STORY_ID")
    assert (
        InputPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_default(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--default' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--default")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Default input should be displayed"
    assert root_element.is_enabled(), "Default input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_text_input(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--text-input' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--text-input")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Text input should be displayed"
    assert root_element.is_enabled(), "Text input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_email_input(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--email-input' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--email-input")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Email input should be displayed"
    assert root_element.is_enabled(), "Email input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_password_input(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--password-input' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--password-input")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Password input should be displayed"
    assert root_element.is_enabled(), "Password input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_search_input(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--search-input' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--search-input")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Search input should be displayed"
    assert root_element.is_enabled(), "Search input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_small(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--small' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--small")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Small input should be displayed"
    assert root_element.is_enabled(), "Small input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_medium(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--medium' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--medium")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Medium input should be displayed"
    assert root_element.is_enabled(), "Medium input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_large(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--large' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--large")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Large input should be displayed"
    assert root_element.is_enabled(), "Large input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_success_state(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--success-state' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--success-state")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Success state input should be displayed"
    assert root_element.is_enabled(), "Success state input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_warning_state(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--warning-state' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--warning-state")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Warning state input should be displayed"
    assert root_element.is_enabled(), "Warning state input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_error_state(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--error-state' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--error-state")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Error state input should be displayed"
    assert (
        root_element.is_enabled()
    ), "Error state input should remain enabled for user correction"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_required(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--required' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--required")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Required input should be displayed"
    assert root_element.is_enabled(), "Required input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_disabled(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--disabled' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--disabled")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Disabled input should be displayed"
    assert not root_element.is_enabled(), "Disabled input should not be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_with_helper_text(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--with-helper-text' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--with-helper-text")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Input with helper text should be displayed"
    assert root_element.is_enabled(), "Input with helper text should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_full_width(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--full-width' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--full-width")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Full width input should be displayed"
    assert root_element.is_enabled(), "Full width input should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_all_sizes(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--all-sizes' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--all-sizes")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "All sizes input showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_all_validation_states(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--all-validation-states' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--all-validation-states")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "All validation states showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_all_input_types(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--all-input-types' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--all-input-types")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "All input types showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_accessibility_showcase(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--accessibility-showcase' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--accessibility-showcase")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Accessibility showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_internationalization_demo(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--internationalization-demo' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--internationalization-demo")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Internationalization demo should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_form_example(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-input--form-example' and verify the component is visible."""
    pom = InputPOM(driver)
    pom.navigate_to_story("common-atoms-input--form-example")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Form example should be displayed"
