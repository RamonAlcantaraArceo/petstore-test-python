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
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = StatusfilterPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = StatusfilterPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class StatusfilterPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-statusfilter--default"
    SELECTOR = "[data-component='StatusFilter']"

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

    def secondary_button(self):
        """Single Button inside Statusfilter.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")

    def select(self):
        """Single Select inside Statusfilter.  Selector: [data-component='Select'] (grouped)"""
        return self._child_pom("Select", "[data-component='Select']")
