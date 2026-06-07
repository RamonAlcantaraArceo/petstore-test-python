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
def test_user_management_with_user(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-user-management--with-user' and verify the component is visible."""
    pom = UserManagementPOM(driver)
    pom.navigate_to_story("petstore-views-user-management--with-user")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "User management view should be displayed"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        primary_button is None
    ), "With-user story should not render the primary button"

    secondary_button = pom.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert secondary_button is not None, "Secondary button should be visible"
    assert secondary_button.is_displayed(), "Secondary button should be displayed"
    assert not secondary_button.is_enabled(), "Secondary button should be disabled"

    username_input = pom.username_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert username_input is not None, "Username input should be visible"
    assert username_input.is_displayed(), "Username input should be displayed"
    assert username_input.is_enabled(), "Username input should be enabled"

    usercard = pom.default_usercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert usercard is not None, "User card should be visible"
    assert usercard.is_displayed(), "User card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_user_management_read_only(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-user-management--read-only' and verify the component is visible."""
    pom = UserManagementPOM(driver)
    pom.navigate_to_story("petstore-views-user-management--read-only")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "Read-only user management view should be displayed"

    secondary_button = pom.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        secondary_button is None
    ), "Read-only story should not render the secondary button"

    username_input = pom.username_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        username_input is None
    ), "Read-only story should not render the username input"

    usercard = pom.default_usercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert usercard is not None, "User card should be visible"
    assert usercard.is_displayed(), "User card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_user_management_no_user(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-user-management--no-user' and verify the component is visible."""
    pom = UserManagementPOM(driver)
    pom.navigate_to_story("petstore-views-user-management--no-user")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "No-user management view should be displayed"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert primary_button is None, "No-user story should not render the primary button"

    secondary_button = pom.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert secondary_button is not None, "Secondary button should be visible"
    assert secondary_button.is_displayed(), "Secondary button should be displayed"
    assert not secondary_button.is_enabled(), "Secondary button should be disabled"

    username_input = pom.username_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert username_input is not None, "Username input should be visible"
    assert username_input.is_displayed(), "Username input should be displayed"
    assert username_input.is_enabled(), "Username input should be enabled"

    usercard = pom.default_usercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert usercard is None, "No-user story should not render a user card"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_user_management_accessibility_and_locale_showcase(
    driver, pom_interaction_helper
):
    """Navigate to story 'petstore-views-user-management--accessibility-and-locale-showcase' and verify the component is visible."""
    pom = UserManagementPOM(driver)
    pom.navigate_to_story(
        "petstore-views-user-management--accessibility-and-locale-showcase"
    )

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "Accessibility and locale showcase should be displayed"

    username_input = pom.username_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        username_input is None
    ), "Accessibility and locale showcase should not render the username input"

    usercard = pom.default_usercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        usercard is None
    ), "Accessibility and locale showcase should not render a user card"
