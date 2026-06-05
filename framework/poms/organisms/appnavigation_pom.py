"""Page Object Model for Appnavigation (organisms).

Storybook title  : Petstore/Organisms/AppNavigation
Story IDs        : ['petstore-organisms-appnavigation--logged-in', 'petstore-organisms-appnavigation--logged-out', 'petstore-organisms-appnavigation--orders-tab-active', 'petstore-organisms-appnavigation--users-tab-active']
Dependencies     : none
Selector         : [data-component='AppNavigation']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Tabs ×1  →  [data-component='Tabs']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-organisms-appnavigation--logged-in")
    pom = AppnavigationPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = AppnavigationPOM(driver)
    root = pom.root()
"""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from framework.poms.base_selenium import SeleniumBasePOM


class AppnavigationPOM(SeleniumBasePOM):
    STORY_ID = "petstore-organisms-appnavigation--logged-in"
    SELECTOR = "[data-component='AppNavigation']"

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

    def secondary_button(self):
        """Single Button inside Appnavigation.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")

    def tabs(self):
        """Single Tabs inside Appnavigation.  Selector: [data-component='Tabs'] (grouped)"""
        return self._child_pom("Tabs", "[data-component='Tabs']")
