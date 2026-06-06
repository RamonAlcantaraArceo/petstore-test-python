"""Page Object Model for Confirmdialog (molecules).

Storybook title  : Petstore/Molecules/ConfirmDialog
Story IDs        : ['petstore-molecules-confirmdialog--default', 'petstore-molecules-confirmdialog--danger-variant', 'petstore-molecules-confirmdialog--custom-title']
Dependencies     : none
Selector         : [data-component='Button']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-confirmdialog--default")
    pom = ConfirmdialogPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = ConfirmdialogPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class ConfirmdialogPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-confirmdialog--default"
    ALL_STORY_IDS = [
        "petstore-molecules-confirmdialog--default",
        "petstore-molecules-confirmdialog--danger-variant",
        "petstore-molecules-confirmdialog--custom-title",
    ]
    SELECTOR = "[data-component='Button']"

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
