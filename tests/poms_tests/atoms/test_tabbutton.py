import pytest

from framework.poms.atoms.tabbutton_pom import TabbuttonPOM


@pytest.mark.smoke
def test_tabbutton_pom_class_imports():
    assert TabbuttonPOM is not None


@pytest.mark.smoke
def test_tabbutton_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(TabbuttonPOM, "SELECTOR")
    assert (
        TabbuttonPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_tabbutton_story_id_defined():
    assert hasattr(TabbuttonPOM, "STORY_ID")
    assert (
        TabbuttonPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabbutton_underline(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-tabbutton--underline' and verify the component is visible."""
    pom = TabbuttonPOM(driver)
    pom.navigate_to_story("common-atoms-tabbutton--underline")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Underline tab button should be displayed"
    assert root_element.is_enabled(), "Underline tab button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabbutton_pill(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-tabbutton--pill' and verify the component is visible."""
    pom = TabbuttonPOM(driver)
    pom.navigate_to_story("common-atoms-tabbutton--pill")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Pill tab button should be displayed"
    assert root_element.is_enabled(), "Pill tab button should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabbutton_selected_and_disabled(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-tabbutton--selected-and-disabled' and verify the component is visible."""
    pom = TabbuttonPOM(driver)
    pom.navigate_to_story("common-atoms-tabbutton--selected-and-disabled")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "Selected and disabled tab button should be displayed"
    assert (
        not root_element.is_enabled()
    ), "Selected and disabled tab button should not be enabled"
