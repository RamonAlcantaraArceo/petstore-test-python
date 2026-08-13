"""Page Object Model for Card (atoms).

Storybook title  : Common/Atoms/Card
Story IDs        : ['common-atoms-card--default', 'common-atoms-card--basic-card', 'common-atoms-card--primary-card', 'common-atoms-card--secondary-card', 'common-atoms-card--success-card', 'common-atoms-card--warning-card', 'common-atoms-card--error-card', 'common-atoms-card--no-elevation', 'common-atoms-card--small-elevation', 'common-atoms-card--large-elevation', 'common-atoms-card--extra-large-elevation', 'common-atoms-card--interactive', 'common-atoms-card--selected', 'common-atoms-card--with-border', 'common-atoms-card--no-padding', 'common-atoms-card--small-padding', 'common-atoms-card--large-padding', 'common-atoms-card--extra-large-padding', 'common-atoms-card--all-elevations', 'common-atoms-card--all-variants', 'common-atoms-card--all-rounded-options', 'common-atoms-card--accessibility-showcase', 'common-atoms-card--internationalization-demo', 'common-atoms-card--card-grid', 'common-atoms-card--full-width-card', 'common-atoms-card--card-with-header', 'common-atoms-card--card-with-footer']
Dependencies     : none
Selector         : [data-component='Card']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-card--default")
    pom = CardPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = CardPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class CardPOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-card--default"
    ALL_STORY_IDS = [
        "common-atoms-card--default",
        "common-atoms-card--basic-card",
        "common-atoms-card--primary-card",
        "common-atoms-card--secondary-card",
        "common-atoms-card--success-card",
        "common-atoms-card--warning-card",
        "common-atoms-card--error-card",
        "common-atoms-card--no-elevation",
        "common-atoms-card--small-elevation",
        "common-atoms-card--large-elevation",
        "common-atoms-card--extra-large-elevation",
        "common-atoms-card--interactive",
        "common-atoms-card--selected",
        "common-atoms-card--with-border",
        "common-atoms-card--no-padding",
        "common-atoms-card--small-padding",
        "common-atoms-card--large-padding",
        "common-atoms-card--extra-large-padding",
        "common-atoms-card--all-elevations",
        "common-atoms-card--all-variants",
        "common-atoms-card--all-rounded-options",
        "common-atoms-card--accessibility-showcase",
        "common-atoms-card--internationalization-demo",
        "common-atoms-card--card-grid",
        "common-atoms-card--full-width-card",
        "common-atoms-card--card-with-header",
        "common-atoms-card--card-with-footer",
    ]
    SELECTOR = "[data-component='Card']"

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
