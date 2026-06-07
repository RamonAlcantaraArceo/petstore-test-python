import pytest

from framework.poms.views.store_orders_pom import StoreOrdersPOM


@pytest.mark.smoke
def test_store_orders_pom_class_imports():
    assert StoreOrdersPOM is not None


@pytest.mark.smoke
def test_store_orders_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(StoreOrdersPOM, "SELECTOR")
    assert (
        StoreOrdersPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_store_orders_story_id_defined():
    assert hasattr(StoreOrdersPOM, "STORY_ID")
    assert (
        StoreOrdersPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_store_orders_with_inventory(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-store-orders--with-inventory' and verify the component is visible."""
    pom = StoreOrdersPOM(driver)
    pom.navigate_to_story("petstore-views-store-orders--with-inventory")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Store orders view should be displayed"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert primary_button is not None, "Primary button should be visible"
    assert primary_button.is_displayed(), "Primary button should be displayed"
    assert primary_button.is_enabled(), "Primary button should be enabled"

    secondary_button = pom.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert secondary_button is not None, "Secondary button should be visible"
    assert secondary_button.is_displayed(), "Secondary button should be displayed"
    assert not secondary_button.is_enabled(), "Secondary button should be disabled"

    order_id_input = pom.order_id_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert order_id_input is not None, "Order ID input should be visible"
    assert order_id_input.is_displayed(), "Order ID input should be displayed"
    assert order_id_input.is_enabled(), "Order ID input should be enabled"

    ordercard = pom.default_ordercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert ordercard is not None, "Order card should be visible"
    assert ordercard.is_displayed(), "Order card should be displayed"

    table = pom.table().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert table is not None, "Orders table should be visible"
    assert table.is_displayed(), "Orders table should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_store_orders_read_only(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-store-orders--read-only' and verify the component is visible."""
    pom = StoreOrdersPOM(driver)
    pom.navigate_to_story("petstore-views-store-orders--read-only")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Store orders view should be displayed"

    primary_button = pom.primary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert (
        primary_button is None
    ), "Read-only story should not render the primary button"

    secondary_button = pom.secondary_button().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert secondary_button is not None, "Secondary button should be visible"
    assert secondary_button.is_displayed(), "Secondary button should be displayed"
    assert not secondary_button.is_enabled(), "Secondary button should be disabled"

    order_id_input = pom.order_id_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert order_id_input is not None, "Order ID input should be visible"
    assert order_id_input.is_displayed(), "Order ID input should be displayed"
    assert order_id_input.is_enabled(), "Order ID input should be enabled"

    ordercard = pom.default_ordercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert ordercard is not None, "Order card should be visible"
    assert ordercard.is_displayed(), "Order card should be displayed"

    table = pom.table().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert table is not None, "Orders table should be visible"
    assert table.is_displayed(), "Orders table should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_store_orders_inventory_only(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-store-orders--inventory-only' and verify the component is visible."""
    pom = StoreOrdersPOM(driver)
    pom.navigate_to_story("petstore-views-store-orders--inventory-only")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "Inventory-only store orders view should be displayed"

    order_id_input = pom.order_id_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert order_id_input is not None, "Order ID input should be visible"
    assert order_id_input.is_displayed(), "Order ID input should be displayed"
    assert order_id_input.is_enabled(), "Order ID input should be enabled"

    table = pom.table().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert table is not None, "Orders table should be visible"
    assert table.is_displayed(), "Orders table should be displayed"

    ordercard = pom.default_ordercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert ordercard is None, "Inventory-only story should not render an order card"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_store_orders_empty_inventory(driver, pom_interaction_helper):
    """Navigate to story 'petstore-views-store-orders--empty-inventory' and verify the component is visible."""
    pom = StoreOrdersPOM(driver)
    pom.navigate_to_story("petstore-views-store-orders--empty-inventory")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "Empty inventory store orders view should be displayed"

    table = pom.table().wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert table is not None, "Orders table should be visible"
    assert table.is_displayed(), "Orders table should be displayed"

    order_id_input = pom.order_id_input().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert order_id_input is not None, "Order ID input should be visible"
    assert order_id_input.is_displayed(), "Order ID input should be displayed"
    assert order_id_input.is_enabled(), "Order ID input should be enabled"

    ordercard = pom.default_ordercard().wait_for_visibility(
        timeout=10, raise_on_timeout=False
    )
    assert ordercard is None, "Empty inventory story should not render an order card"
