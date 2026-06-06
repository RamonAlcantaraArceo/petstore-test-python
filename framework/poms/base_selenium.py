"""Shared Selenium Page Object Model helpers.

This module provides the base implementation for Storybook-backed Selenium
page objects and utilities for resolving child components dynamically.
"""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import Protocol, Self, cast

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from framework.config import get_storybook_base_url


class RootablePOM(Protocol):
    """Protocol for page objects that expose a root Selenium element."""

    driver: WebDriver
    SELECTOR: str

    def root(self) -> WebElement:
        """Return the root Selenium element for this page object."""
        ...

    def wait_for_visibility(
        self, timeout: int = 10, raise_on_timeout: bool = True
    ) -> WebElement | None:
        """Wait until this POM root element is visible."""
        ...

    def type_into(self, text: str) -> WebElement:
        """Clear and type text into this POM root element."""
        ...

    def click_element(self) -> WebElement:
        """Click this POM root element."""
        ...

    def select_option(self, option_text: str) -> WebElement:
        """Select an option by visible text on this POM root `<select>`."""
        ...

    def is_element_visible(self) -> bool:
        """Return whether this POM root element is visible."""
        ...

    def assert_element_visible(self) -> Self:
        """Assert that this POM root element is visible and return self."""
        ...

    def is_element_enabled(self) -> bool:
        """Return whether this POM root element is enabled."""
        ...

    def assert_element_enabled(self) -> Self:
        """Assert that this POM root element is enabled and return self."""
        ...

    def has_input_value(self, expected_value: str) -> bool:
        """Return whether this POM root input has the expected value."""
        ...

    def assert_input_value(self, expected_value: str) -> Self:
        """Assert that this POM root input has the expected value and return self."""
        ...


class POMInteractionMixin:
    """Provide reusable root-level interactions for Selenium POMs."""

    driver: WebDriver
    SELECTOR: str

    def root(self) -> WebElement:
        """Return the root element of the page object."""
        raise NotImplementedError("POMInteractionMixin requires root() implementation")

    def wait_for_visibility(
        self, timeout: int = 10, raise_on_timeout: bool = True
    ) -> WebElement | None:
        """Wait until this POM root element is visible.

        Args:
            timeout: Maximum wait time in seconds.
            raise_on_timeout: Whether to raise `TimeoutException` on timeout.

        Returns:
            The visible root element, or ``None`` when timeout occurs and
            ``raise_on_timeout`` is ``False``.

        Raises:
            TimeoutException: If visibility is not reached within ``timeout`` and
                ``raise_on_timeout`` is ``True``.
        """
        selector = getattr(self, "_selector", self.SELECTOR)
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            if raise_on_timeout:
                raise
            return None

    def wait_for_absence(
        self, timeout: int = 10, raise_on_timeout: bool = True
    ) -> bool:
        """Wait until this POM root element is no longer visible or present.

        Args:
            timeout: Maximum wait time in seconds.
            raise_on_timeout: Whether to raise `TimeoutException` on timeout.
        Returns:
            ``True`` if the element becomes invisible or is removed, or ``False``
            when timeout occurs and ``raise_on_timeout`` is ``False``.
        Raises:
            TimeoutException: If the element remains visible or present within ``timeout`` and
                ``raise_on_timeout`` is ``True``.
        """
        selector = getattr(self, "_selector", self.SELECTOR)
        wait = WebDriverWait(self.driver, timeout)
        try:
            result = wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            # TODO: I have doubs about this.
            return bool(result)
        except TimeoutException:
            if raise_on_timeout:
                raise
            return False

    def type_into(self, text: str) -> WebElement:
        """Clear and type text into this POM root element.

        Args:
            text: Text to enter into the root element.

        Returns:
            The root element after typing.
        """
        element = self.root()
        element.clear()
        element.send_keys(text)
        return element

    def click_element(self) -> WebElement:
        """Click this POM root element.

        Returns:
            The root element after click.
        """
        element = self.root()
        element.click()
        return element

    def select_option(self, option_text: str) -> WebElement:
        """Select an option by visible text on this POM root `<select>`.

        Args:
            option_text: Visible text of the option to select.

        Returns:
            The root select element after option selection.
        """
        from selenium.webdriver.support.select import Select

        element = self.root()
        Select(element).select_by_visible_text(option_text)
        return element

    def is_element_displayed(self) -> bool:
        """Return whether this POM root element is displayed.

        Returns:
            ``True`` when the root element is displayed, else ``False``.
        """
        return self.root().is_displayed()

    def assert_element_displayed(self) -> Self:
        """Assert that this POM root element is displayed and return self.

        Returns:
            This page object to allow method chaining.
        """
        assert self.is_element_displayed(), f"Element not displayed: {self}"
        return self

    def is_element_enabled(self) -> bool:
        """Return whether this POM root element is enabled.

        Returns:
            ``True`` when the root element is enabled, else ``False``.
        """
        return self.root().is_enabled()

    def assert_element_enabled(self) -> Self:
        """Assert that this POM root element is enabled and return self.

        Returns:
            This page object to allow method chaining.
        """
        assert self.is_element_enabled(), f"Element not enabled: {self}"
        return self

    def has_input_value(self, expected_value: str) -> bool:
        """Return whether this POM root input has the expected value.

        Args:
            expected_value: Expected input value.

        Returns:
            ``True`` when the value matches, else ``False``.
        """
        actual_value = self.root().get_attribute("value")
        return actual_value == expected_value

    def assert_input_value(self, expected_value: str) -> Self:
        """Assert that this POM root input has the expected value and return self.

        Args:
            expected_value: Expected input value.

        Returns:
            This page object to allow method chaining.
        """
        actual_value = self.root().get_attribute("value")
        assert self.has_input_value(expected_value), (
            f"Expected '{expected_value}' but got '{actual_value}'"
        )
        return self


class SeleniumBasePOM(POMInteractionMixin):
    """Base class for Selenium page objects.

    Attributes:
        PACKAGE_ROOT: Root package used when resolving child POM modules.
    """

    PACKAGE_ROOT = "framework.poms"
    SELECTOR: str = ""

    def __init__(
        self,
        *,
        driver: WebDriver,
        selector: str,
        story_id: str,
        dependencies: list[str],
        selector_override: str | None = None,
        index_override: int | None = None,
    ) -> None:
        self.driver: WebDriver = driver
        self.STORY_ID = story_id
        self._selector = selector_override or selector
        self._index = index_override
        self.dependencies = dependencies

    @staticmethod
    def _resolve_child_pom_class(
        component_name: str,
    ) -> Callable[..., SeleniumBasePOM]:
        """Resolve a child POM class by component name.

        Args:
            component_name: Child component name without the ``POM`` suffix.

        Returns:
            The resolved child POM class.

        Raises:
            ImportError: If no matching child class can be imported.
        """

        module_stem = "".join(
            ("_" + ch.lower()) if ch.isupper() else ch for ch in component_name
        ).lstrip("_")
        module_name = module_stem + "_pom"
        class_name = component_name + "POM"
        for level in ("atoms", "molecules", "organisms", "views", "app"):
            try:
                module = import_module(
                    SeleniumBasePOM.PACKAGE_ROOT + "." + level + "." + module_name
                )
                cls = getattr(module, class_name, None)
                if cls is not None:
                    return cast(Callable[..., SeleniumBasePOM], cls)
            except Exception:
                continue
        raise ImportError(
            "Could not resolve child POM class for "
            + component_name
            + " ("
            + module_name
            + ")."
        )

    @staticmethod
    def storybook_url() -> str:
        """Return the Storybook base URL."""
        return get_storybook_base_url()

    def navigate_to_story(self, story_id: str | None = None) -> None:
        """Open the Storybook iframe for this component.

        Args:
            story_id: Optional Storybook story ID override.
        """

        self.driver.get(
            f"{self.storybook_url()}/iframe.html?id={story_id or self.STORY_ID}"
        )

    def root(self) -> WebElement:
        """Return the root element or indexed child element for this component."""

        if self._index is None:
            return self.driver.find_element("css selector", self._selector)
        return self.driver.find_elements("css selector", self._selector)[self._index]

    def _scoped_selector(self, child_selector: str) -> str:
        """Scope a selector to this component root.

        Args:
            child_selector: The child selector to scope.

        Returns:
            A selector scoped to the current component.
        """

        return f"{self._selector} {child_selector}"

    def _child_pom(self, component_name: str, child_selector: str) -> SeleniumBasePOM:
        """Instantiate a single child POM.

        Args:
            component_name: Child component name without the ``POM`` suffix.
            child_selector: Selector used to scope the child component.

        Returns:
            A child page object instance.
        """

        child_cls = self._resolve_child_pom_class(component_name)
        scoped = self._scoped_selector(child_selector)
        try:
            return child_cls(self.driver, selector_override=scoped)
        except TypeError:
            child = child_cls(self.driver)
            child.SELECTOR = scoped
            return child

    def _child_poms(
        self, component_name: str, child_selector: str
    ) -> list[SeleniumBasePOM]:
        """Instantiate all matching child POMs.

        Args:
            component_name: Child component name without the ``POM`` suffix.
            child_selector: Selector used to scope the child components.

        Returns:
            A list of child page object instances.
        """

        child_cls = self._resolve_child_pom_class(component_name)
        scoped = self._scoped_selector(child_selector)
        count = len(self.driver.find_elements("css selector", scoped))
        items: list[SeleniumBasePOM] = []
        for idx in range(count):
            try:
                items.append(
                    child_cls(self.driver, selector_override=scoped, index_override=idx)
                )
            except TypeError:
                child = child_cls(self.driver)
                child.SELECTOR = scoped
                child._index = idx
                items.append(child)
        return items
