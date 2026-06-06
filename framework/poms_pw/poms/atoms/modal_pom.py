"""Page Object Model for Modal (atoms).

Storybook title  : Common/Atoms/Modal
Story IDs        : ['common-atoms-modal--open-closed', 'common-atoms-modal--sizes', 'common-atoms-modal--focus-trap']
Dependencies     : none
Selector         : [data-component='Button']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = ModalPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = ModalPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class ModalPOM(PlaywrightBasePOM):
    STORY_ID = "common-atoms-modal--open-closed"
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
