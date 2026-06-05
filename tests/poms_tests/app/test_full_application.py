import pytest


from framework.poms.app.full_application_pom import FullApplicationPOM


@pytest.mark.smoke
def test_full_application_pom_class_imports():
    assert FullApplicationPOM is not None


@pytest.mark.smoke
def test_full_application_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(FullApplicationPOM, "SELECTOR")
    assert FullApplicationPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_full_application_story_id_defined():
    assert hasattr(FullApplicationPOM, "STORY_ID")
    assert FullApplicationPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_full_application_navigate_and_verify(driver, pom_interaction_helper):
    """Verify FullApplication POM can navigate to story and interact with the component."""
    pom = FullApplicationPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Generic component verification
    assert root_element is not None, "Component is not visible"
