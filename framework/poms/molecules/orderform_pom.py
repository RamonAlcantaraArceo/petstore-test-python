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
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-orderform--default")
    pom = OrderformPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = OrderformPOM(driver)
    root = pom.root()
"""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from framework.poms.base_selenium import SeleniumBasePOM


class OrderformPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-orderform--default"
    SELECTOR = "[data-component='OrderForm']"

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
