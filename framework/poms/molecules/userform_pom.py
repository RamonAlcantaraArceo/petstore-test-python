"""Page Object Model for Userform (molecules).

Storybook title  : Petstore/Molecules/UserForm
Story IDs        : ['petstore-molecules-userform--create-mode', 'petstore-molecules-userform--edit-mode', 'petstore-molecules-userform--loading', 'petstore-molecules-userform--accessibility-showcase']
Dependencies     : none
Selector         : [data-component='UserForm']
Strategy used    : data-component
Discovered children:
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary
  - Input ×1  →  [data-component='Input'][name='email']  [name]  key=email
  - Input ×1  →  [data-component='Input'][name='firstName']  [name]  key=first_name
  - Input ×1  →  [data-component='Input'][name='lastName']  [name]  key=last_name
  - Input ×1  →  [data-component='Input'][name='password']  [name]  key=password
  - Input ×1  →  [data-component='Input'][name='phone']  [name]  key=phone
  - Input ×1  →  [data-component='Input'][name='username']  [name]  key=username

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    driver.get(f"{STORYBOOK_URL}/iframe.html?id=petstore-molecules-userform--create-mode")
    pom = UserformPOM(driver)
    root = pom.root()   # uses the discovered selector above

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = UserformPOM(driver)
    root = pom.root()
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.base_selenium import SeleniumBasePOM


class UserformPOM(SeleniumBasePOM):
    STORY_ID = "petstore-molecules-userform--create-mode"
    ALL_STORY_IDS = [
        "petstore-molecules-userform--create-mode",
        "petstore-molecules-userform--edit-mode",
        "petstore-molecules-userform--loading",
        "petstore-molecules-userform--accessibility-showcase",
    ]
    SELECTOR = "[data-component='UserForm']"

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
        """Single Button inside Userform.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='primary']"
        )

    def secondary_button(self) -> SeleniumBasePOM:
        """Single Button inside Userform.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom(
            "Button", "[data-component='Button'][data-variant='secondary']"
        )

    def email_input(self) -> SeleniumBasePOM:
        """Single Input inside Userform.  Selector: [data-component='Input'][name='email'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='email']")

    def first_name_input(self) -> SeleniumBasePOM:
        """Single Input inside Userform.  Selector: [data-component='Input'][name='firstName'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='firstName']")

    def last_name_input(self) -> SeleniumBasePOM:
        """Single Input inside Userform.  Selector: [data-component='Input'][name='lastName'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='lastName']")

    def password_input(self) -> SeleniumBasePOM:
        """Single Input inside Userform.  Selector: [data-component='Input'][name='password'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='password']")

    def phone_input(self) -> SeleniumBasePOM:
        """Single Input inside Userform.  Selector: [data-component='Input'][name='phone'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='phone']")

    def username_input(self) -> SeleniumBasePOM:
        """Single Input inside Userform.  Selector: [data-component='Input'][name='username'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='username']")
