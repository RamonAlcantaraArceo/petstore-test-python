"""Page Object Model for FullApplication (app).

Storybook title  : Petstore/App/Full Application
Story IDs        : ['petstore-app-full-application--default', 'petstore-app-full-application--chef-locale']
Dependencies     : none
Selector         : [data-component='PetstoreApp']
Strategy used    : data-component
Discovered children:
  - AppNavigation ×1  →  [data-component='AppNavigation']  [grouped]
  - PetManagementView ×1  →  [data-component='PetManagementView']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-app-full-application--default")
    pom = FullApplicationPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = FullApplicationPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class FullApplicationPOM(SeleniumBasePOM):
    STORY_ID = "petstore-app-full-application--default"
    SELECTOR = "[data-component='PetstoreApp']"

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

    def appnavigation(self):
        """Single AppNavigation inside FullApplication.  Selector: [data-component='AppNavigation'] (grouped)"""
        return self._child_pom("AppNavigation", "[data-component='AppNavigation']")

    def petmanagementview(self):
        """Single PetManagementView inside FullApplication.  Selector: [data-component='PetManagementView'] (grouped)"""
        return self._child_pom(
            "PetManagementView", "[data-component='PetManagementView']"
        )
