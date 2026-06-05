"""Page Object Model for Select (atoms).

Storybook title  : Common/Atoms/Select
Story IDs        : ['common-atoms-select--default', 'common-atoms-select--disabled', 'common-atoms-select--with-options']
Dependencies     : none
Selector         : [data-component='Select']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-select--default")
    pom = SelectPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = SelectPOM(driver)
    root = pom.root()
"""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from framework.poms.base_selenium import SeleniumBasePOM


class SelectPOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-select--default"
    SELECTOR = "[data-component='Select']"

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
