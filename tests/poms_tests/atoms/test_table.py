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
def test_table_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Table POM can navigate to story and interact with the component."""
    pom = TablePOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Generic component verification
    assert root_element is not None, "Component is not visible"
