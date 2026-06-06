"""Page Object Model for Card (atoms).

Storybook title  : Common/Atoms/Card
Story IDs        : ['common-atoms-card--default', 'common-atoms-card--basic-card', 'common-atoms-card--primary-card', 'common-atoms-card--secondary-card', 'common-atoms-card--success-card', 'common-atoms-card--warning-card', 'common-atoms-card--error-card', 'common-atoms-card--no-elevation', 'common-atoms-card--small-elevation', 'common-atoms-card--large-elevation', 'common-atoms-card--extra-large-elevation', 'common-atoms-card--interactive', 'common-atoms-card--selected', 'common-atoms-card--with-border', 'common-atoms-card--no-padding', 'common-atoms-card--small-padding', 'common-atoms-card--large-padding', 'common-atoms-card--extra-large-padding', 'common-atoms-card--all-elevations', 'common-atoms-card--all-variants', 'common-atoms-card--all-rounded-options', 'common-atoms-card--accessibility-showcase', 'common-atoms-card--internationalization-demo', 'common-atoms-card--card-grid', 'common-atoms-card--full-width-card', 'common-atoms-card--card-with-header', 'common-atoms-card--card-with-footer']
Dependencies     : none
Selector         : [data-component='Card']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = CardPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = CardPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class CardPOM(PlaywrightBasePOM):
    STORY_ID = "common-atoms-card--default"
    SELECTOR = "[data-component='Card']"

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
