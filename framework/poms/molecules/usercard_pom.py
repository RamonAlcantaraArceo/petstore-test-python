"""Page Object Model for Usercard (molecules).

Storybook title  : Petstore/Molecules/UserCard
Story IDs        : ['petstore-molecules-usercard--with-full-details', 'petstore-molecules-usercard--username-only', 'petstore-molecules-usercard--readonly']
Dependencies     : none
Selector         : [data-component='UserCard']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='danger']  [data-variant]  key=danger
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-usercard--with-full-details")
    pom = UsercardPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = UsercardPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class UsercardPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-usercard--with-full-details"
    ALL_STORY_IDS = [
        "petstore-molecules-usercard--with-full-details",
        "petstore-molecules-usercard--username-only",
        "petstore-molecules-usercard--readonly",
    ]
    SELECTOR = "[data-component='UserCard']"

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

    def danger_button(self) -> SeleniumBasePOM:
        """Single Button inside Usercard.  Selector: [data-component='Button'][data-variant='danger'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='danger']"
        )

    def secondary_button(self) -> SeleniumBasePOM:
        """Single Button inside Usercard.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='secondary']"
        )
