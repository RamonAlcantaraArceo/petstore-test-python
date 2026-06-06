"""Page Object Model for Petform (molecules).

Storybook title  : Petstore/Molecules/PetForm
Story IDs        : ['petstore-molecules-petform--create-mode', 'petstore-molecules-petform--edit-mode', 'petstore-molecules-petform--loading']
Dependencies     : none
Selector         : [data-component='PetForm']
Strategy used    : data-component
Discovered children:
  - Input ×1  →  [data-component='Input'][name='name']  [name]  key=name
  - Input ×1  →  [data-component='Input'][name='categoryName']  [name]  key=category_name
  - Input ×1  →  [data-component='Input'][name='photoUrl']  [name]  key=photo_url
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Select ×1  →  [data-component='Select']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = PetformPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = PetformPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class PetformPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-petform--create-mode"
    SELECTOR = "[data-component='PetForm']"

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

    def name_input(self):
        """Single Input inside Petform.  Selector: [data-component='Input'][name='name'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='name']")

    def category_name_input(self):
        """Single Input inside Petform.  Selector: [data-component='Input'][name='categoryName'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='categoryName']")

    def photo_url_input(self):
        """Single Input inside Petform.  Selector: [data-component='Input'][name='photoUrl'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='photoUrl']")

    def primary_button(self):
        """Single Button inside Petform.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='primary']")

    def secondary_button(self):
        """Single Button inside Petform.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")

    def select(self):
        """Single Select inside Petform.  Selector: [data-component='Select'] (grouped)"""
        return self._child_pom("Select", "[data-component='Select']")
