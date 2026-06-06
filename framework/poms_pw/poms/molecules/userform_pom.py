"""Page Object Model for Userform (molecules).

Storybook title  : Petstore/Molecules/UserForm
Story IDs        : ['petstore-molecules-userform--create-mode', 'petstore-molecules-userform--edit-mode', 'petstore-molecules-userform--loading', 'petstore-molecules-userform--accessibility-showcase']
Dependencies     : none
Selector         : [data-component='UserForm']
Strategy used    : data-component
Discovered children:
  - Input ×1  →  [data-component='Input'][name='username']  [name]  key=username
  - Input ×1  →  [data-component='Input'][name='firstName']  [name]  key=first_name
  - Input ×1  →  [data-component='Input'][name='lastName']  [name]  key=last_name
  - Input ×1  →  [data-component='Input'][name='email']  [name]  key=email
  - Input ×1  →  [data-component='Input'][name='password']  [name]  key=password
  - Input ×1  →  [data-component='Input'][name='phone']  [name]  key=phone
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary
  - Button ×1  →  [data-component='Button'][data-variant='secondary']  [data-variant]  key=secondary

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = UserformPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = UserformPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class UserformPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-userform--create-mode"
    SELECTOR = "[data-component='UserForm']"

    def __init__(
        self,
        page: Page,
        selector_override: str | None = None,
        index_override: int | None = None,
    ) -> None:
        super().__init__(
            page=page,
            selector=self.SELECTOR,
            story_id=self.STORY_ID,
            dependencies=[],
            selector_override=selector_override,
            index_override=index_override,
        )

    # ------------------------------------------------------------------
    # Child component accessors (discovered from live Storybook DOM)
    # ------------------------------------------------------------------

    def username_input(self):
        """Single Input inside Userform.  Selector: [data-component='Input'][name='username'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='username']")

    def first_name_input(self):
        """Single Input inside Userform.  Selector: [data-component='Input'][name='firstName'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='firstName']")

    def last_name_input(self):
        """Single Input inside Userform.  Selector: [data-component='Input'][name='lastName'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='lastName']")

    def email_input(self):
        """Single Input inside Userform.  Selector: [data-component='Input'][name='email'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='email']")

    def password_input(self):
        """Single Input inside Userform.  Selector: [data-component='Input'][name='password'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='password']")

    def phone_input(self):
        """Single Input inside Userform.  Selector: [data-component='Input'][name='phone'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='phone']")

    def primary_button(self):
        """Single Button inside Userform.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='primary']")

    def secondary_button(self):
        """Single Button inside Userform.  Selector: [data-component='Button'][data-variant='secondary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='secondary']")
