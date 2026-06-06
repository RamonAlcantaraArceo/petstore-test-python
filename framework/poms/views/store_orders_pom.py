"""Page Object Model for StoreOrders (views).

Storybook title  : Petstore/Views/Store Orders
Story IDs        : ['petstore-views-store-orders--with-inventory', 'petstore-views-store-orders--read-only', 'petstore-views-store-orders--inventory-only', 'petstore-views-store-orders--empty-inventory']
Dependencies     : none
Selector         : [data-component='StoreOrdersView']
Strategy used    : data-component
Discovered children:
  - Input ×1  →  [data-component='Input'][name='orderId']  [name]  key=order_id
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - OrderCard ×1  →  [data-component='OrderCard'][data-variant='default']  [data-variant]  key=default
  - Table ×1  →  [data-component='Table']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-views-store-orders--with-inventory")
    pom = StoreOrdersPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = StoreOrdersPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class StoreOrdersPOM(SeleniumBasePOM):
    STORY_ID = "petstore-views-store-orders--with-inventory"
    SELECTOR = "[data-component='StoreOrdersView']"

    def __init__(
        self,
        driver: WebDriver,
        selector_override: str | None = None,
        index_override: int | None = None,
    ) -> None:
        super().__init__(
            driver=driver,
            selector=self.SELECTOR,
            story_id=self.STORY_ID,
            dependencies=[],
            selector_override=selector_override,
            index_override=index_override,
        )

    # ------------------------------------------------------------------
    # Child component accessors (discovered from live Storybook DOM)
    # ------------------------------------------------------------------

    def order_id_input(self):
        """Single Input inside StoreOrders.  Selector: [data-component='Input'][name='orderId'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='orderId']")

    def secondary_button(self):
        """Single Button inside StoreOrders.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='secondary']"
        )

    def primary_button(self):
        """Single Button inside StoreOrders.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='primary']"
        )

    def default_ordercard(self):
        """Single OrderCard inside StoreOrders.  Selector: [data-component='OrderCard'][data-variant='default'] (data-variant)"""
        return self._child_pom(
            "OrderCard", "[data-component='OrderCard'][data-variant='default']"
        )

    def table(self):
        """Single Table inside StoreOrders.  Selector: [data-component='Table'] (grouped)"""
        return self._child_pom("Table", "[data-component='Table']")
