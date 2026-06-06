"""Page Object Model for UserManagement (views).

Storybook title  : Petstore/Views/User Management
Story IDs        : ['petstore-views-user-management--with-user', 'petstore-views-user-management--read-only', 'petstore-views-user-management--no-user', 'petstore-views-user-management--accessibility-and-locale-showcase']
Dependencies     : none
Selector         : [data-component='UserManagementView']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Input ×1  →  [data-component='Input'][name='username']  [name]  key=username
  - UserCard ×1  →  [data-component='UserCard'][data-variant='default']  [data-variant]  key=default

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-views-user-management--with-user")
    pom = UserManagementPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = UserManagementPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class UserManagementPOM(SeleniumBasePOM):
    STORY_ID = "petstore-views-user-management--with-user"
    ALL_STORY_IDS = [
        "petstore-views-user-management--with-user",
        "petstore-views-user-management--read-only",
        "petstore-views-user-management--no-user",
        "petstore-views-user-management--accessibility-and-locale-showcase",
    ]
    SELECTOR = "[data-component='UserManagementView']"

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

    def primary_button(self) -> SeleniumBasePOM:
        """Single Button inside UserManagement.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='primary']"
        )

    def secondary_button(self) -> SeleniumBasePOM:
        """Single Button inside UserManagement.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='secondary']"
        )

    def username_input(self) -> SeleniumBasePOM:
        """Single Input inside UserManagement.  Selector: [data-component='Input'][name='username'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='username']")

    def default_usercard(self) -> SeleniumBasePOM:
        """Single UserCard inside UserManagement.  Selector: [data-component='UserCard'][data-variant='default'] (data-variant)"""
        return self._child_pom(
            "Usercard", "[data-component='UserCard'][data-variant='default']"
        )
