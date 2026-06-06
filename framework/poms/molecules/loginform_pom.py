"""Page Object Model for Loginform (molecules).

Storybook title  : Petstore/Molecules/LoginForm
Story IDs        : ['petstore-molecules-loginform--default', 'petstore-molecules-loginform--with-error', 'petstore-molecules-loginform--loading']
Dependencies     : none
Selector         : [data-component='LoginForm']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - FormAlert ×1  →  [data-component='FormAlert'][data-variant='error']  [data-variant]  key=error
  - Input ×1  →  [data-component='Input'][name='password']  [name]  key=password
  - Input ×1  →  [data-component='Input'][name='username']  [name]  key=username

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-loginform--default")
    pom = LoginformPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = LoginformPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class LoginformPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-loginform--default"
    ALL_STORY_IDS = [
        "petstore-molecules-loginform--default",
        "petstore-molecules-loginform--with-error",
        "petstore-molecules-loginform--loading",
    ]
    SELECTOR = "[data-component='LoginForm']"

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
        """Single Button inside Loginform.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='primary']"
        )

    def error_formalert(self) -> SeleniumBasePOM:
        """Single FormAlert inside Loginform.  Selector: [data-component='FormAlert'][data-variant='error'] (data-variant)"""
        return self._child_pom(
            "Formalert", "[data-component='FormAlert'][data-variant='error']"
        )

    def password_input(self) -> SeleniumBasePOM:
        """Single Input inside Loginform.  Selector: [data-component='Input'][name='password'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='password']")

    def username_input(self) -> SeleniumBasePOM:
        """Single Input inside Loginform.  Selector: [data-component='Input'][name='username'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='username']")
