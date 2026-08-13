"""Page Object Model for Tabs (molecules).

Storybook title  : Petstore/Molecules/Tabs
Story IDs        : ['petstore-molecules-tabs--keyboard-navigation', 'petstore-molecules-tabs--three-tabs']
Dependencies     : none
Selector         : [data-component='Tabs']
Strategy used    : data-component
Discovered children:
  - TabButton ×3  →  [data-component='TabButton']  [grouped]

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-tabs--keyboard-navigation")
    pom = TabsPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = TabsPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from framework.poms.base_selenium import SeleniumBasePOM


class TabsPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-tabs--keyboard-navigation"
    ALL_STORY_IDS = [
        "petstore-molecules-tabs--keyboard-navigation",
        "petstore-molecules-tabs--three-tabs",
    ]
    SELECTOR = "[data-component='Tabs']"

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
    # Child component accessors (discovered from live Storybook DOM)
    # ------------------------------------------------------------------

    def tabbuttons(self) -> list[SeleniumBasePOM]:
        """All TabButton instances (3) inside Tabs.  Selector: [data-component='TabButton'] (grouped)"""
        return self._child_poms("Tabbutton", "[data-component='TabButton']")

    # ------------------------------------------------------------------
    # Custom methods for interacting with Tabs
    # ------------------------------------------------------------------

    def selected_tab_indices(self) -> list[int]:
        """Return 1-based indices for the currently selected tab buttons."""
        from framework.poms.atoms.tabbutton_pom import TabbuttonPOM

        tabbuttons: list[TabbuttonPOM] = self.tabbuttons()  # type: ignore[assignment]
        return [
            index
            for index, tabbutton in enumerate(tabbuttons, start=1)
            if tabbutton.is_selected()
        ]

    def selected_tab_index(self) -> int | None:
        """Return the selected tab index when exactly one tab is selected."""
        selected = self.selected_tab_indices()
        if len(selected) != 1:
            return None
        return selected[0]

    def select_tab(
        self,
        index: int,
        *,
        timeout: int = 10,
        wait_for_transition: bool = True,
    ) -> SeleniumBasePOM:
        """Click a tab button and optionally wait for the selection to move.

        Args:
            index: 1-based tab index to select.
            timeout: Maximum time to wait for the selection transition.
            wait_for_transition: Whether to wait until the target tab is selected.

        Returns:
            The selected TabButton POM.
        """
        tabbuttons = self.tabbuttons()
        if index < 1 or index > len(tabbuttons):
            raise AssertionError(
                f"Tab index {index} is out of range for {len(tabbuttons)} tabs"
            )

        tabbutton = tabbuttons[index - 1]
        tabbutton.click_element()

        if wait_for_transition:
            WebDriverWait(self.driver, timeout).until(
                lambda _driver: self.selected_tab_indices() == [index]
            )

        return tabbutton
