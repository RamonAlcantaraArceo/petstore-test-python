"""Page Object Model for Badge (atoms).

Storybook title  : Common/Atoms/Badge
Story IDs        : ['common-atoms-badge--default', 'common-atoms-badge--all-variants', 'common-atoms-badge--sizes']
Dependencies     : none
Selector         : #storybook-root > *:first-child
Strategy used    : storybook-root
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = BadgePOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = BadgePOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class BadgePOM(PlaywrightBasePOM):
    STORY_ID = "common-atoms-badge--default"
    SELECTOR = "#storybook-root > *:first-child"

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
