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
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = FullApplicationPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = FullApplicationPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class FullApplicationPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-app-full-application--default"
    SELECTOR = "[data-component='PetstoreApp']"

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

    def appnavigation(self):
        """Single AppNavigation inside FullApplication.  Selector: [data-component='AppNavigation'] (grouped)"""
        return self._child_pom("AppNavigation", "[data-component='AppNavigation']")

    def petmanagementview(self):
        """Single PetManagementView inside FullApplication.  Selector: [data-component='PetManagementView'] (grouped)"""
        return self._child_pom("PetManagementView", "[data-component='PetManagementView']")
