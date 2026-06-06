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
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = StoreOrdersPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = StoreOrdersPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class StoreOrdersPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-views-store-orders--with-inventory"
    SELECTOR = "[data-component='StoreOrdersView']"

    def __init__(
        self,
        page: Page,
        selector_override: str | None = None,
        index_override: int | None = None,
    ) -> None:
        super().__init__(
            page=page,
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
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")

    def primary_button(self):
        """Single Button inside StoreOrders.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='primary']")

    def default_ordercard(self):
        """Single OrderCard inside StoreOrders.  Selector: [data-component='OrderCard'][data-variant='default'] (data-variant)"""
        return self._child_pom("OrderCard", "[data-component='OrderCard'][data-variant='default']")

    def table(self):
        """Single Table inside StoreOrders.  Selector: [data-component='Table'] (grouped)"""
        return self._child_pom("Table", "[data-component='Table']")
