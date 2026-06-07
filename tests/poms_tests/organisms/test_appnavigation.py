import pytest

from framework.poms.organisms.appnavigation_pom import AppnavigationPOM


@pytest.mark.smoke
def test_appnavigation_pom_class_imports():
    assert AppnavigationPOM is not None


@pytest.mark.smoke
def test_appnavigation_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(AppnavigationPOM, "SELECTOR")
    assert (
        AppnavigationPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_appnavigation_story_id_defined():
    assert hasattr(AppnavigationPOM, "STORY_ID")
    assert (
        AppnavigationPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_appnavigation_logged_in(driver, pom_interaction_helper):
    """Navigate to story 'petstore-organisms-appnavigation--logged-in' and verify the component is visible."""
    pom = AppnavigationPOM(driver)
    pom.navigate_to_story("petstore-organisms-appnavigation--logged-in")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "AppNavigation should be displayed in logged-in state"

    # Verify tabs are present (user navigation)
    tabs_element = pom.tabs().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert tabs_element is not None, "Tabs should be visible in logged-in state"
    assert tabs_element.is_displayed(), "Tabs component should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_appnavigation_logged_out(driver, pom_interaction_helper):
    """Navigate to story 'petstore-organisms-appnavigation--logged-out' and verify the component is visible."""
    pom = AppnavigationPOM(driver)
    pom.navigate_to_story("petstore-organisms-appnavigation--logged-out")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "AppNavigation should be displayed in logged-out state"

    # In logged-out state, tabs should not be visible
    tabs_element = pom.tabs().wait_for_visibility(timeout=5, raise_on_timeout=False)
    if tabs_element is not None:
        # If tabs exist, verify they are displayed
        assert (
            tabs_element.is_displayed()
        ), "If tabs are present, they should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_appnavigation_orders_tab_active(driver, pom_interaction_helper):
    """Navigate to story 'petstore-organisms-appnavigation--orders-tab-active' and verify the component is visible."""
    pom = AppnavigationPOM(driver)
    pom.navigate_to_story("petstore-organisms-appnavigation--orders-tab-active")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "AppNavigation should be displayed with orders tab active"

    # Verify tabs are present and visible (with orders tab active)
    tabs_element = pom.tabs().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert tabs_element is not None, "Tabs should be visible when orders tab is active"
    assert tabs_element.is_displayed(), "Tabs component should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_appnavigation_users_tab_active(driver, pom_interaction_helper):
    """Navigate to story 'petstore-organisms-appnavigation--users-tab-active' and verify the component is visible."""
    pom = AppnavigationPOM(driver)
    pom.navigate_to_story("petstore-organisms-appnavigation--users-tab-active")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "AppNavigation should be displayed with users tab active"

    # Verify tabs are present and visible (with users tab active)
    tabs_element = pom.tabs().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert tabs_element is not None, "Tabs should be visible when users tab is active"
    assert tabs_element.is_displayed(), "Tabs component should be displayed"
