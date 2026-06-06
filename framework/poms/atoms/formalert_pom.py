"""Page Object Model for Badge (atoms).

Storybook title  : Common/Atoms/FormAlert
Story IDs        : ['common-atoms-formalert--error', 'common-atoms-formalert--warning', 'common-atoms-formalert--info', 'common-atoms-formalert--success']
Dependencies     : none
Selector         : #storybook-root > *:first-child
Strategy used    : storybook-root
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-formalert--error")
    pom = BadgePOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = BadgePOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class BadgePOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-badge--error"
    SELECTOR = "[data-component='FormAlert']"

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
