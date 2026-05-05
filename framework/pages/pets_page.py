"""Pets page object for the Petstore UI.

Models the interactive API explorer (originally inspired by https://petstore.swagger.io/, now intended for your local instance).
The swagger-UI exposes pets operations visually; this POM wraps those
interactions so UI tests can create/read pets through the browser.

Note: In a real project this would target your actual petstore web
application. The swagger-ui interactions shown here demonstrate the
POM pattern and can be adapted to any web front-end.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class PetsPage(BasePage):
    """Page Object for the Petstore UI pets section (local instance)."""

    URL = "/"

    # Section toggle
    _PET_SECTION = (By.CSS_SELECTOR, "#operations-tag-pet")
    # Add pet operation
    _ADD_PET_SECTION = (By.CSS_SELECTOR, "#operations-pet-addPet")
    _TRY_IT_OUT_BTN = (By.CSS_SELECTOR, ".try-out__btn")
    _REQUEST_BODY_TEXTAREA = (By.CSS_SELECTOR, "textarea.body-param__text")
    _EXECUTE_BTN = (By.CSS_SELECTOR, ".execute")
    _RESPONSE_BODY = (By.CSS_SELECTOR, ".responses-inner .highlight-code code")

    def expand_pet_section(self) -> PetsPage:
        """Expand the 'pet' tag section in the Swagger UI."""
        self.click(*self._PET_SECTION)
        return self

    def expand_add_pet(self) -> PetsPage:
        """Expand the POST /pet operation."""
        self.click(*self._ADD_PET_SECTION)
        return self

    def click_try_it_out(self) -> PetsPage:
        self.click(*self._TRY_IT_OUT_BTN)
        return self

    def set_request_body(self, body: str) -> PetsPage:
        self.type_text(*self._REQUEST_BODY_TEXTAREA, text=body)
        return self

    def execute(self) -> PetsPage:
        self.click(*self._EXECUTE_BTN)
        return self

    def get_response_body(self) -> str:
        try:
            return self.wait_for_visible(*self._RESPONSE_BODY, timeout=15).text
        except Exception:
            return ""
