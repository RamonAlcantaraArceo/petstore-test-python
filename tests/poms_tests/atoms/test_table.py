import pytest

from framework.poms.atoms.table_pom import TablePOM


@pytest.mark.smoke
def test_table_pom_class_imports():
    assert TablePOM is not None


@pytest.mark.smoke
def test_table_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(TablePOM, "SELECTOR")
    assert (
        TablePOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_table_story_id_defined():
    assert hasattr(TablePOM, "STORY_ID")
    assert (
        TablePOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_table_with_data(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-table--with-data' and verify the component is visible."""
    pom = TablePOM(driver)
    pom.navigate_to_story("common-atoms-table--with-data")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Table should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_table_empty_state(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-table--empty-state' and verify the component is visible."""
    pom = TablePOM(driver)
    pom.navigate_to_story("common-atoms-table--empty-state")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Table should be displayed"
