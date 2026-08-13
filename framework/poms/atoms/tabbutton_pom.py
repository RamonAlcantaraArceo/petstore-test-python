"""Page Object Model for Tabbutton (atoms).

Storybook title  : Common/Atoms/TabButton
Story IDs        : ['common-atoms-tabbutton--underline', 'common-atoms-tabbutton--pill', 'common-atoms-tabbutton--selected-and-disabled']
Dependencies     : none
Selector         : [data-component='TabButton']
Strategy used    : data-component
Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=common-atoms-tabbutton--underline")
    pom = TabbuttonPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = TabbuttonPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class TabbuttonPOM(SeleniumBasePOM):
    STORY_ID = "common-atoms-tabbutton--underline"
    ALL_STORY_IDS = [
        "common-atoms-tabbutton--underline",
        "common-atoms-tabbutton--pill",
        "common-atoms-tabbutton--selected-and-disabled",
    ]
    SELECTOR = "[data-component='TabButton']"

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

    # ------------------------------------------------------------------
    def is_selected(self) -> bool:
        """Returns True if the TabButton is selected, False otherwise."""
        root = self.root()
        aria_selected = root.get_attribute("aria-selected")
        return aria_selected == "true"
