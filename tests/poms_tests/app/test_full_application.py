import pytest

from framework.poms.app.full_application_pom import FullApplicationPOM


@pytest.mark.smoke
def test_full_application_pom_class_imports():
    assert FullApplicationPOM is not None


@pytest.mark.smoke
def test_full_application_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(FullApplicationPOM, "SELECTOR")
    assert (
        FullApplicationPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_full_application_story_id_defined():
    assert hasattr(FullApplicationPOM, "STORY_ID")
    assert (
        FullApplicationPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_full_application_default(driver, pom_interaction_helper):
    """Navigate to story 'petstore-app-full-application--default' and verify the component is visible."""
    pom = FullApplicationPOM(driver)
    pom.navigate_to_story("petstore-app-full-application--default")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Full application should be displayed"

    appnavigation = pom.appnavigation()
    appnavigation_root = appnavigation.wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert appnavigation_root is not None, "App navigation should be visible"
    assert appnavigation_root.is_displayed(), "App navigation should be displayed"

    tabs = appnavigation.tabs().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert tabs is not None, "App navigation tabs should be visible"
    assert tabs.is_displayed(), "App navigation tabs should be displayed"

    primary_button = appnavigation.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert primary_button is not None, "App navigation primary button should be visible"
    assert (
        primary_button.is_displayed()
    ), "App navigation primary button should be displayed"
    assert (
        primary_button.is_enabled()
    ), "App navigation primary button should be enabled"

    secondary_button = appnavigation.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        secondary_button is None
    ), "Default app story should not render the secondary button"

    petmanagement = pom.petmanagementview()
    petmanagement_root = petmanagement.wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert petmanagement_root is not None, "Pet management view should be visible"
    assert petmanagement_root.is_displayed(), "Pet management view should be displayed"

    petcards = petmanagement.petcards()
    assert len(petcards) == 0, "App shell should not render pet cards in the view"

    statusfilter = petmanagement.statusfilter().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert statusfilter is not None, "Pet management status filter should be visible"
    assert (
        statusfilter.is_displayed()
    ), "Pet management status filter should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_full_application_chef_locale(driver, pom_interaction_helper):
    """Navigate to story 'petstore-app-full-application--chef-locale' and verify the component is visible."""
    pom = FullApplicationPOM(driver)
    pom.navigate_to_story("petstore-app-full-application--chef-locale")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Full application should be displayed"

    appnavigation = pom.appnavigation()
    appnavigation_root = appnavigation.wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert appnavigation_root is not None, "App navigation should be visible"
    assert appnavigation_root.is_displayed(), "App navigation should be displayed"

    tabs = appnavigation.tabs().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert tabs is not None, "App navigation tabs should be visible"
    assert tabs.is_displayed(), "App navigation tabs should be displayed"

    primary_button = appnavigation.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert primary_button is not None, "App navigation primary button should be visible"
    assert (
        primary_button.is_displayed()
    ), "App navigation primary button should be displayed"
    assert (
        primary_button.is_enabled()
    ), "App navigation primary button should be enabled"

    secondary_button = appnavigation.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        secondary_button is None
    ), "Chef locale app story should not render the secondary button"

    petmanagement = pom.petmanagementview()
    petmanagement_root = petmanagement.wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert petmanagement_root is not None, "Pet management view should be visible"
    assert petmanagement_root.is_displayed(), "Pet management view should be displayed"

    petcards = petmanagement.petcards()
    assert (
        len(petcards) == 0
    ), "Chef locale app story should not render pet cards in the view"

    statusfilter = petmanagement.statusfilter().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert statusfilter is not None, "Pet management status filter should be visible"
    assert (
        statusfilter.is_displayed()
    ), "Pet management status filter should be displayed"
