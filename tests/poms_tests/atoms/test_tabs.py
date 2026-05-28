import pytest


from poms.atoms.tabs_pom import TabsPOM


@pytest.mark.smoke
def test_tabs_pom_class_imports():
    assert TabsPOM is not None


@pytest.mark.smoke
def test_tabs_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(TabsPOM, "SELECTOR")
    assert TabsPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_tabs_story_id_defined():
    assert hasattr(TabsPOM, "STORY_ID")
    assert TabsPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_tabs_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Tabs POM can navigate to story and interact with the component."""
    pom = TabsPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Generic component verification
    assert root_element is not None, "Component is not visible"
