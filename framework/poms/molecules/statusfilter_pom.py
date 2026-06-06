"""Page Object Model for Statusfilter (molecules).

Storybook title  : Petstore/Molecules/StatusFilter
Story IDs        : ['petstore-molecules-statusfilter--default', 'petstore-molecules-statusfilter--loading']
Dependencies     : none
Selector         : [data-component='StatusFilter']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Select ×1  →  [data-component='Select']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-statusfilter--default")
    pom = StatusfilterPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = StatusfilterPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class StatusfilterPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-statusfilter--default"
    ALL_STORY_IDS = [
        "petstore-molecules-statusfilter--default",
        "petstore-molecules-statusfilter--loading",
    ]
    SELECTOR = "[data-component='StatusFilter']"

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

    def secondary_button(self) -> SeleniumBasePOM:
        """Single Button inside Statusfilter.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='secondary']"
        )

    def select(self) -> SeleniumBasePOM:
        """Single Select inside Statusfilter.  Selector: [data-component='Select'] (grouped)"""
        return self._child_pom("Select", "[data-component='Select']")
