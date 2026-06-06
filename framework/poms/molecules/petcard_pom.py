"""Page Object Model for Petcard (molecules).

Storybook title  : Petstore/Molecules/PetCard
Story IDs        : ['petstore-molecules-petcard--available', 'petstore-molecules-petcard--pending', 'petstore-molecules-petcard--sold', 'petstore-molecules-petcard--readonly']
Dependencies     : none
Selector         : [data-component='PetCard']
Strategy used    : data-component
Discovered children:
  - Badge ×1  →  [data-component='Badge'][data-variant='available']  [data-variant]  key=available
  - Badge ×1  →  [data-component='Badge'][data-variant='pending']  [data-variant]  key=pending
  - Badge ×1  →  [data-component='Badge'][data-variant='sold']  [data-variant]  key=sold
  - Button ×1  →  [data-component='Button'][data-variant='danger']  [data-variant]  key=danger
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-petcard--available")
    pom = PetcardPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = PetcardPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class PetcardPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-petcard--available"
    ALL_STORY_IDS = [
        "petstore-molecules-petcard--available",
        "petstore-molecules-petcard--pending",
        "petstore-molecules-petcard--sold",
        "petstore-molecules-petcard--readonly",
    ]
    SELECTOR = "[data-component='PetCard']"

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

    def available_badge(self) -> SeleniumBasePOM:
        """Single Badge inside Petcard.  Selector: [data-component='Badge'][data-variant='available'] (data-variant)"""
        return self._child_pom(
            "Badge", "[data-component='Badge'][data-variant='available']"
        )

    def pending_badge(self) -> SeleniumBasePOM:
        """Single Badge inside Petcard.  Selector: [data-component='Badge'][data-variant='pending'] (data-variant)"""
        return self._child_pom(
            "Badge", "[data-component='Badge'][data-variant='pending']"
        )

    def sold_badge(self) -> SeleniumBasePOM:
        """Single Badge inside Petcard.  Selector: [data-component='Badge'][data-variant='sold'] (data-variant)"""
        return self._child_pom("Badge", "[data-component='Badge'][data-variant='sold']")

    def danger_button(self) -> SeleniumBasePOM:
        """Single Button inside Petcard.  Selector: [data-component='Button'][data-variant='danger'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='danger']"
        )

    def secondary_button(self) -> SeleniumBasePOM:
        """Single Button inside Petcard.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='secondary']"
        )
