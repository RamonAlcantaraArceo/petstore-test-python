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
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-views-pet-management--with-pets")
    pom = PetManagementPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = PetManagementPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class PetManagementPOM(SeleniumBasePOM):
    STORY_ID = "petstore-views-pet-management--with-pets"
    SELECTOR = "[data-component='PetManagementView']"

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

    def primary_button(self):
        """Single Button inside PetManagement.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='primary']"
        )

    def statusfilter(self):
        """Single StatusFilter inside PetManagement.  Selector: [data-component='StatusFilter'] (grouped)"""
        return self._child_pom("StatusFilter", "[data-component='StatusFilter']")

    def petcards(self):
        """All PetCard instances (4) inside PetManagement.  Selector: [data-component='PetCard'] (grouped)"""
        return self._child_poms("PetCard", "[data-component='PetCard']")
