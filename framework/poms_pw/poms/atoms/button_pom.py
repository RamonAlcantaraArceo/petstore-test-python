"""Page Object Model for Button (atoms).

Storybook title  : Common/Atoms/Button
Story IDs        : ['common-atoms-button--primary', 'common-atoms-button--secondary', 'common-atoms-button--danger', 'common-atoms-button--small', 'common-atoms-button--medium', 'common-atoms-button--large', 'common-atoms-button--disabled', 'common-atoms-button--loading', 'common-atoms-button--all-variants', 'common-atoms-button--all-sizes', 'common-atoms-button--accessibility-showcase', 'common-atoms-button--internationalization-demo', 'common-atoms-button--full-width', 'common-atoms-button--all-variants-comparison']
Dependencies     : none
Selector         : [data-component='Button']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = ButtonPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = ButtonPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class ButtonPOM(PlaywrightBasePOM):
    STORY_ID = "common-atoms-button--primary"
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
