"""Page Object Model for Input (atoms).

Storybook title  : Common/Atoms/Input
Story IDs        : ['common-atoms-input--default', 'common-atoms-input--text-input', 'common-atoms-input--email-input', 'common-atoms-input--password-input', 'common-atoms-input--search-input', 'common-atoms-input--small', 'common-atoms-input--medium', 'common-atoms-input--large', 'common-atoms-input--success-state', 'common-atoms-input--warning-state', 'common-atoms-input--error-state', 'common-atoms-input--required', 'common-atoms-input--disabled', 'common-atoms-input--with-helper-text', 'common-atoms-input--full-width', 'common-atoms-input--all-sizes', 'common-atoms-input--all-validation-states', 'common-atoms-input--all-input-types', 'common-atoms-input--accessibility-showcase', 'common-atoms-input--internationalization-demo', 'common-atoms-input--form-example']
Dependencies     : none
Selector         : [data-component='Input']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-input--default")
    pom = InputPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = InputPOM(driver)
    root = pom.root()
"""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from framework.poms.base_selenium import SeleniumBasePOM


class InputPOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-input--default"
    SELECTOR = "[data-component='Input']"

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
