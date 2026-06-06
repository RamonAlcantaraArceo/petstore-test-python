"""Page Object Model for Orderform (molecules).

Storybook title  : Petstore/Molecules/OrderForm
Story IDs        : ['petstore-molecules-orderform--default', 'petstore-molecules-orderform--loading']
Dependencies     : none
Selector         : [data-component='OrderForm']
Strategy used    : data-component
Discovered children:
  - Input ×1  →  [data-component='Input'][name='petId']  [name]  key=pet_id
  - Input ×1  →  [data-component='Input'][name='quantity']  [name]  key=quantity
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = OrderformPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = OrderformPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class OrderformPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-orderform--default"
    SELECTOR = "[data-component='OrderForm']"

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

    def pet_id_input(self):
        """Single Input inside Orderform.  Selector: [data-component='Input'][name='petId'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='petId']")

    def quantity_input(self):
        """Single Input inside Orderform.  Selector: [data-component='Input'][name='quantity'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='quantity']")

    def primary_button(self):
        """Single Button inside Orderform.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='primary']")

    def secondary_button(self):
        """Single Button inside Orderform.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")
