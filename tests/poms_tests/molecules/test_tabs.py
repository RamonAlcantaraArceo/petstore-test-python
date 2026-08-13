import pytest

from framework.poms.molecules.tabs_pom import TabsPOM


@pytest.mark.smoke
def test_tabs_pom_class_imports():
    assert TabsPOM is not None


@pytest.mark.smoke
def test_tabs_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(TabsPOM, "SELECTOR")
    assert (
        TabsPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_tabs_story_id_defined():
    assert hasattr(TabsPOM, "STORY_ID")
    assert (
        TabsPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabs_keyboard_navigation(driver, pom_interaction_helper):
    """Navigate to story 'petstore-molecules-tabs--keyboard-navigation' and verify the component is visible."""
    pom = TabsPOM(driver)
    pom.navigate_to_story("petstore-molecules-tabs--keyboard-navigation")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Tabs should be displayed"

    tabbuttons = pom.tabbuttons()
    assert len(tabbuttons) == 3, "Tabs should expose three TabButton children"
    for index, tabbutton in enumerate(tabbuttons, start=1):
        tab_root = tabbutton.wait_for_visibility(timeout=10, raise_on_timeout=False)
        assert tab_root is not None, f"TabButton {index} should be visible"
        assert tab_root.is_displayed(), f"TabButton {index} should be displayed"
        assert tab_root.is_enabled(), f"TabButton {index} should be enabled"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabs_three_tabs(driver, pom_interaction_helper):
    """Navigate to story 'petstore-molecules-tabs--three-tabs' and verify the component is visible."""
    pom = TabsPOM(driver)
    pom.navigate_to_story("petstore-molecules-tabs--three-tabs")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Tabs should be displayed"

    tabbuttons = pom.tabbuttons()
    assert len(tabbuttons) == 3, "Tabs should expose three TabButton children"

    for index, tabbutton in enumerate(tabbuttons, start=1):
        tab_root = tabbutton.wait_for_visibility(timeout=10, raise_on_timeout=False)
        assert tab_root is not None, f"TabButton {index} should be visible"
        assert tab_root.is_displayed(), f"TabButton {index} should be displayed"
        assert tab_root.is_enabled(), f"TabButton {index} should be enabled"

    initially_selected = pom.selected_tab_indices()
    assert (
        len(initially_selected) <= 1
    ), f"At most one tab should be selected before interaction, got {initially_selected}"

    target_index = 1
    if initially_selected == [target_index]:
        target_index = 2

    pom.select_tab(target_index, timeout=10)

    after_click_selected = pom.selected_tab_indices()
    assert after_click_selected == [
        target_index
    ], f"Selected tab should move to tab {target_index} after click, got {after_click_selected}"

    second_target_index = 3 if target_index != 3 else 1
    pom.select_tab(second_target_index, timeout=10)

    final_selected = pom.selected_tab_indices()
    assert final_selected == [
        second_target_index
    ], f"Selected tab should move to tab {second_target_index} after click, got {final_selected}"
