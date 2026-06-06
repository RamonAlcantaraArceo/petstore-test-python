"""Page Object Model for Loginform (molecules).

Storybook title  : Petstore/Molecules/LoginForm
Story IDs        : ['petstore-molecules-loginform--default', 'petstore-molecules-loginform--with-error', 'petstore-molecules-loginform--loading']
Dependencies     : none
Selector         : [data-component='LoginForm']
Strategy used    : data-component
Discovered children:
  - Input ×1  →  [data-component='Input'][name='username']  [name]  key=username
  - Input ×1  →  [data-component='Input'][name='password']  [name]  key=password
  - Button ×1  →  [data-component='Button'][data-variant='primary']  [data-variant]  key=primary

Usage against Storybook (isolated component testing)
-----------------------------------------------------
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        pom = LoginformPOM(page)
        pom.navigate_to_story()
        pom.root().wait_for()

Usage against the application
------------------------------
    # Confirm the selector still works in your app's DOM.
    # Run `sbpom --verify` to re-check live selectors at any time.
    pom = LoginformPOM(page)
    pom.root().wait_for()
"""
from __future__ import annotations

from playwright.sync_api import Page

from poms.base_playwright import PlaywrightBasePOM


class LoginformPOM(PlaywrightBasePOM):
    STORY_ID = "petstore-molecules-loginform--default"
    SELECTOR = "[data-component='LoginForm']"

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
        """Single Input inside Loginform.  Selector: [data-component='Input'][name='username'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='username']")

    def password_input(self):
        """Single Input inside Loginform.  Selector: [data-component='Input'][name='password'] (name)"""
        return self._child_pom("Input", "[data-component='Input'][name='password']")

    def primary_button(self):
        """Single Button inside Loginform.  Selector: [data-component='Button'][data-variant='primary'] (data-variant)"""
        return self._child_pom("Button", "[data-component='Button'][data-variant='primary']")
