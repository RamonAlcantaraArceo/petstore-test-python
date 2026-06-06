"""Page Object Model for PetManagement (views).

Storybook title  : Petstore/Views/Pet Management
Story IDs        : ['petstore-views-pet-management--with-pets', 'petstore-views-pet-management--read-only', 'petstore-views-pet-management--empty']
Dependencies     : none
Selector         : [data-component='PetManagementView']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - StatusFilter ×1  →  [data-component='StatusFilter']  [grouped]
  - PetCard ×4  →  [data-component='PetCard']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = PetManagementPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = PetManagementPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class PetManagementPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-views-pet-management--with-pets"
    SELECTOR = "[data-component='PetManagementView']"

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

    def primary_button(self):
        """Single Button inside PetManagement.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='primary']")

    def statusfilter(self):
        """Single StatusFilter inside PetManagement.  Selector: [data-component='StatusFilter'] (grouped)"""
        return self._child_pom("StatusFilter", "[data-component='StatusFilter']")

    def petcards(self):
        """All PetCard instances (4) inside PetManagement.  Selector: [data-component='PetCard'] (grouped)"""
        return self._child_poms("PetCard", "[data-component='PetCard']")
