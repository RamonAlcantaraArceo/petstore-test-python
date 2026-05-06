"""Base Page Object – common helpers for all Selenium page objects.

Every concrete page class should extend :class:`BasePage`.

Example
-------
::

    class LoginPage(BasePage):
        URL = "/login"

        def fill_username(self, username: str) -> "LoginPage":
            self.find(By.ID, "username").send_keys(username)
            return self
"""

from __future__ import annotations

import logging
from typing import Any, Self, cast

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10  # seconds


class BasePage:
    """Thin Selenium wrapper shared by all page objects."""

    URL: str = ""  # Relative URL; subclasses should override

    def __init__(self, driver: webdriver.Remote, base_url: str = "") -> None:
        self._driver = driver
        self._base_url = base_url.rstrip("/")
        self._wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open(self) -> Self:
        """Navigate to the page's canonical URL."""
        url = f"{self._base_url}{self.URL}"
        logger.debug("Navigating to %s", url)
        self._driver.get(url)
        return self

    def navigate_to(self, url: str) -> Self:
        """Navigate to an arbitrary URL."""
        logger.debug("Navigating to %s", url)
        self._driver.get(url)
        return self

    @property
    def title(self) -> str:
        """Return the current page title."""
        return str(self._driver.title)

    @property
    def current_url(self) -> str:
        """Return the current URL."""
        return str(self._driver.current_url)

    # ------------------------------------------------------------------
    # Element helpers
    # ------------------------------------------------------------------

    def find(self, by: str, value: str) -> WebElement:
        """Find a single element (no explicit wait)."""
        return cast(WebElement, self._driver.find_element(by, value))

    def find_all(self, by: str, value: str) -> list[WebElement]:
        """Find all matching elements (no explicit wait)."""
        return cast(list[WebElement], self._driver.find_elements(by, value))

    def wait_for_visible(
        self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT
    ) -> WebElement:
        """Wait until an element is visible and return it."""
        wait = WebDriverWait(self._driver, timeout)
        result: WebElement = wait.until(EC.visibility_of_element_located((by, value)))
        return result

    def wait_for_clickable(
        self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT
    ) -> WebElement:
        """Wait until an element is clickable and return it."""
        wait = WebDriverWait(self._driver, timeout)
        result: WebElement = wait.until(EC.element_to_be_clickable((by, value)))
        return result

    def wait_for_text(
        self, by: str, value: str, text: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """Wait until an element contains *text*."""
        wait = WebDriverWait(self._driver, timeout)
        try:
            return bool(wait.until(EC.text_to_be_present_in_element((by, value), text)))
        except TimeoutException:
            return False

    def wait_for_url_contains(
        self, fragment: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """Wait until the current URL contains *fragment*."""
        wait = WebDriverWait(self._driver, timeout)
        try:
            return bool(wait.until(EC.url_contains(fragment)))
        except TimeoutException:
            return False

    def is_element_present(self, by: str, value: str) -> bool:
        """Return True if the element exists in the DOM."""
        return len(self.find_all(by, value)) > 0

    def click(self, by: str, value: str) -> Self:
        """Wait for an element to be clickable then click it."""
        self.wait_for_clickable(by, value).click()
        return self

    def type_text(self, by: str, value: str, text: str, clear: bool = True) -> Self:
        """Clear (optionally) then type *text* into the element."""
        element = self.wait_for_visible(by, value)
        if clear:
            element.clear()
        element.send_keys(text)
        return self

    def get_text(self, by: str, value: str) -> str:
        """Return the visible text of an element."""
        return str(self.wait_for_visible(by, value).text)

    def get_attribute(self, by: str, value: str, attribute: str) -> Any:
        """Return *attribute* of the first matching element."""
        return self.find(by, value).get_attribute(attribute)

    def scroll_to(self, element: WebElement) -> Self:
        """Scroll the element into view."""
        self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self

    def take_screenshot(self, path: str) -> None:
        """Save a screenshot to *path*."""
        self._driver.save_screenshot(path)
