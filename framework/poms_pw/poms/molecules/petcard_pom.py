"""Page Object Model for Petcard (molecules).

Storybook title  : Petstore/Molecules/PetCard
Story IDs        : ['petstore-molecules-petcard--available', 'petstore-molecules-petcard--pending', 'petstore-molecules-petcard--sold', 'petstore-molecules-petcard--readonly']
Dependencies     : none
Selector         : [data-component='PetCard']
Strategy used    : data-component
Discovered children:
  - Badge ×1  →  [data-component='Badge'][data-variant='available']  [data-variant]  key=available
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Button ×1  →  [data-component='Button'][data-variant='danger']  [data-variant]  key=danger

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = PetcardPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = PetcardPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class PetcardPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-petcard--available"
    SELECTOR = "[data-component='PetCard']"

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

    def available_badge(self):
        """Single Badge inside Petcard.  Selector: [data-component='Badge'][data-variant='available'] (data-variant)"""
        return self._child_pom("Badge", "[data-component='Badge'][data-variant='available']")

    def secondary_button(self):
        """Single Button inside Petcard.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")

    def danger_button(self):
        """Single Button inside Petcard.  Selector: [data-component='Button'][data-variant='danger'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='danger']")
