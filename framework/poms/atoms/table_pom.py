"""Page Object Model for Table (atoms).

Storybook title  : Common/Atoms/Table
Story IDs        : ['common-atoms-table--with-data', 'common-atoms-table--empty-state']
Dependencies     : none
Selector         : [data-component='Table']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-table--with-data")
    pom = TablePOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = TablePOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class TablePOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-table--with-data"
    ALL_STORY_IDS = ["common-atoms-table--with-data", "common-atoms-table--empty-state"]
    SELECTOR = "[data-component='Table']"

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
