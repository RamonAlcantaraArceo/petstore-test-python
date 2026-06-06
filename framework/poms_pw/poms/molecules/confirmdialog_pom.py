"""Page Object Model for Confirmdialog (molecules).

Storybook title  : Petstore/Molecules/ConfirmDialog
Story IDs        : ['petstore-molecules-confirmdialog--default', 'petstore-molecules-confirmdialog--danger-variant', 'petstore-molecules-confirmdialog--custom-title']
Dependencies     : none
Selector         : [data-component='Button']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = ConfirmdialogPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = ConfirmdialogPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class ConfirmdialogPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-confirmdialog--default"
    SELECTOR = "[data-component='Button']"

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
