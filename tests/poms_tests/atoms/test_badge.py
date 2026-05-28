import pytest


from poms.atoms.badge_pom import BadgePOM


@pytest.mark.smoke
def test_badge_pom_class_imports():
    assert BadgePOM is not None


@pytest.mark.smoke
def test_badge_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(BadgePOM, "SELECTOR")
    assert BadgePOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_badge_story_id_defined():
    assert hasattr(BadgePOM, "STORY_ID")
    assert BadgePOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_badge_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Badge POM can navigate to story and interact with the component."""
    pom = BadgePOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Generic component verification
    assert root_element is not None, "Component is not visible"
