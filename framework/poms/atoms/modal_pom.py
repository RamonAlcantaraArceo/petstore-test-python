"""Page Object Model for Modal (atoms).

Storybook title  : Common/Atoms/Modal
Story IDs        : ['common-atoms-modal--open-closed', 'common-atoms-modal--sizes', 'common-atoms-modal--focus-trap']
Dependencies     : none
Selector         : [data-component='Button']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-modal--open-closed")
    pom = ModalPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = ModalPOM(driver)
    root = pom.root()
"""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from poms.base_selenium import SeleniumBasePOM


class ModalPOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-modal--open-closed"
    SELECTOR = "[data-component='Button']"

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
