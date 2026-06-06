"""Page Object Model for Ordercard (molecules).

Storybook title  : Petstore/Molecules/OrderCard
Story IDs        : ['petstore-molecules-ordercard--placed', 'petstore-molecules-ordercard--approved', 'petstore-molecules-ordercard--delivered', 'petstore-molecules-ordercard--readonly']
Dependencies     : none
Selector         : [data-component='OrderCard']
Strategy used    : data-component
Discovered children:
  - Badge ×1  →  [data-component='Badge'][data-variant='placed']  [data-variant]  key=placed
  - Button ×1  →  [data-component='Button'][data-variant='danger']  [data-variant]  key=danger

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = OrdercardPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = OrdercardPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class OrdercardPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-ordercard--placed"
    SELECTOR = "[data-component='OrderCard']"

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

    def placed_badge(self):
        """Single Badge inside Ordercard.  Selector: [data-component='Badge'][data-variant='placed'] (data-variant)"""
        return self._child_pom("Badge", "[data-component='Badge'][data-variant='placed']")

    def danger_button(self):
        """Single Button inside Ordercard.  Selector: [data-component='Button'][data-variant='danger'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='danger']")
