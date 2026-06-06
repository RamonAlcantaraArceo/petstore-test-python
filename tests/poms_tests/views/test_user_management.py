import pytest

from framework.poms.views.user_management_pom import UserManagementPOM


@pytest.mark.smoke
def test_user_management_pom_class_imports():
    assert UserManagementPOM is not None


@pytest.mark.smoke
def test_user_management_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(UserManagementPOM, "SELECTOR")
    assert (
        UserManagementPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_user_management_story_id_defined():
    assert hasattr(UserManagementPOM, "STORY_ID")
    assert (
        UserManagementPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_user_management_navigate_and_verify(driver, pom_interaction_helper):
    """Verify UserManagement POM can navigate to story and interact with the component."""
    pom = UserManagementPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Generic component verification
    assert root_element is not None, "Component is not visible"
