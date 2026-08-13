import pytest

from framework.poms.atoms.button_pom import ButtonPOM


@pytest.mark.smoke
def test_button_pom_class_imports():
    assert ButtonPOM is not None


@pytest.mark.smoke
def test_button_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(ButtonPOM, "SELECTOR")
    assert (
        ButtonPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_button_story_id_defined():
    assert hasattr(ButtonPOM, "STORY_ID")
    assert (
        ButtonPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_primary(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--primary' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--primary")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Primary button should be displayed"
    assert root_element.is_enabled(), "Primary button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_secondary(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--secondary' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--secondary")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Secondary button should be displayed"
    assert root_element.is_enabled(), "Secondary button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_danger(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--danger' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--danger")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Danger button should be displayed"
    assert root_element.is_enabled(), "Danger button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_small(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--small' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--small")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Small button should be displayed"
    assert root_element.is_enabled(), "Small button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_medium(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--medium' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--medium")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Medium button should be displayed"
    assert root_element.is_enabled(), "Medium button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_large(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--large' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--large")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Large button should be displayed"
    assert root_element.is_enabled(), "Large button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_disabled(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--disabled' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--disabled")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Disabled button should be displayed"
    assert not root_element.is_enabled(), "Disabled button should not be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_loading(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--loading' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--loading")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Loading button should be displayed"
    assert (
        not root_element.is_enabled()
    ), "Loading button should not be enabled (in loading state)"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_all_variants(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--all-variants' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--all-variants")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "All variants button showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_all_sizes(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--all-sizes' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--all-sizes")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "All sizes button showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_accessibility_showcase(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--accessibility-showcase' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--accessibility-showcase")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Accessibility showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_internationalization_demo(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--internationalization-demo' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--internationalization-demo")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Internationalization demo should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_full_width(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--full-width' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--full-width")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Full width button should be displayed"
    assert root_element.is_enabled(), "Full width button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_button_all_variants_comparison(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-button--all-variants-comparison' and verify the component is visible."""
    pom = ButtonPOM(driver)
    pom.navigate_to_story("common-atoms-button--all-variants-comparison")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "All variants comparison should be displayed"
