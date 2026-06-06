"""Auto-generated conftest.py for the Selenium test suite.
Test files import POM classes using the configured package path, e.g.:
    from poms.atoms.badge_pom import BadgePOM
"""

import os
from pathlib import Path
from typing import Any

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from framework.config import DEFAULT_STORYBOOK_BASE_URL
from framework.poms.base_selenium import RootablePOM


def pytest_addoption(parser):
    parser.addoption(
        "--storybook-url",
        action="store",
        default=None,
        help="Storybook base URL used by generated POM navigate_to_story()",
    )
    parser.addini(
        "storybook_url",
        "Default Storybook URL for generated POM navigation",
        default=DEFAULT_STORYBOOK_BASE_URL,
    )


def pytest_configure(config):
    storybook_url = config.getoption("--storybook-url") or config.getini(
        "storybook_url"
    )
    if storybook_url:
        os.environ["SBPOM_STORYBOOK_URL"] = storybook_url


@pytest.fixture()
def driver():
    """Fixture to initialize and quit the Selenium WebDriver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    # options.add_argument("--headless=new")  # modern headless mode
    options.add_argument("--disable-gpu")  # optional, good for CI
    options.add_argument("--no-sandbox")  # optional, for Docker

    driver = webdriver.Chrome(
        options=options
    )  # or webdriver.Firefox(), etc.  Make sure to have the appropriate WebDriver installed and in PATH.
    yield driver
    driver.quit()


@pytest.fixture
def capture_screenshot(request: pytest.FixtureRequest, driver: Any | Any):
    """Fixture to capture a screenshot of the page at test level."""
    yield
    # Capture screenshot on test teardown
    if hasattr(request, "node"):
        test_name = request.node.name
        screenshot_dir = Path(__file__).parent / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        screenshot_path = screenshot_dir / f"{test_name}.png"
        driver.save_screenshot(str(screenshot_path))
        print(f"Screenshot saved to: {screenshot_path}")


@pytest.fixture
def wait_for_element():
    """Fixture that returns a helper function to wait for elements with custom conditions.

    Usage:
        def test_something(driver, wait_for_element):
            wait_for_element(driver, "[data-component=\'Button\']", EC.element_to_be_clickable)
    """

    def _wait_for(
        driver,
        selector: str,
        condition=EC.presence_of_element_located,
        timeout: int = 10,
    ):
        wait = WebDriverWait(driver, timeout)
        return wait.until(condition((By.CSS_SELECTOR, selector)))

    return _wait_for


@pytest.fixture
def pom_interaction_helper():
    """Fixture that returns a helper for common multi-step POM interactions."""

    class POMInteractionHelper:
        """Compatibility wrapper exposing POM interaction methods."""

        @staticmethod
        def wait_for_visibility(
            pom: RootablePOM,
            timeout: int = 10,
            raise_on_timeout: bool = True,
        ):
            """Wait until the POM root element is visible.

            Args:
                pom: POM instance containing root-level interactions.
                timeout: Maximum wait time in seconds.
                raise_on_timeout: Whether to raise on timeout.

            Returns:
                The visible root element, or ``None`` on timeout when
                ``raise_on_timeout`` is ``False``.
            """
            return pom.wait_for_visibility(
                timeout=timeout, raise_on_timeout=raise_on_timeout
            )

        @staticmethod
        def type_into(pom: RootablePOM, text: str):
            """Clear and type text into the POM root element.

            Args:
                pom: POM instance containing root-level interactions.
                text: Text to enter.

            Returns:
                The root element after typing.
            """
            return pom.type_into(text)

        @staticmethod
        def click_element(pom: RootablePOM):
            """Click the POM root element.

            Args:
                pom: POM instance containing root-level interactions.

            Returns:
                The root element after click.
            """
            return pom.click_element()

        @staticmethod
        def select_option(pom: RootablePOM, option_text: str):
            """Select an option in the POM root `<select>` by visible text.

            Args:
                pom: POM instance containing root-level interactions.
                option_text: Visible text of the option to select.

            Returns:
                The root select element after option selection.
            """
            return pom.select_option(option_text)

        @staticmethod
        def is_element_visible(pom: RootablePOM) -> bool:
            """Return whether the POM root element is visible.

            Args:
                pom: POM instance containing root-level interactions.

            Returns:
                ``True`` when the root element is visible, else ``False``.
            """
            return pom.is_element_visible()

        @staticmethod
        def assert_element_visible(pom: RootablePOM) -> RootablePOM:
            """Assert that the POM root element is visible.

            Args:
                pom: POM instance containing root-level interactions.

            Returns:
                The same POM instance to allow chaining.
            """
            return pom.assert_element_visible()

        @staticmethod
        def is_element_enabled(pom: RootablePOM) -> bool:
            """Return whether the POM root element is enabled.

            Args:
                pom: POM instance containing root-level interactions.

            Returns:
                ``True`` when the root element is enabled, else ``False``.
            """
            return pom.is_element_enabled()

        @staticmethod
        def assert_element_enabled(pom: RootablePOM) -> RootablePOM:
            """Assert that the POM root element is enabled.

            Args:
                pom: POM instance containing root-level interactions.

            Returns:
                The same POM instance to allow chaining.
            """
            return pom.assert_element_enabled()

        @staticmethod
        def has_input_value(pom: RootablePOM, expected_value: str) -> bool:
            """Return whether the POM root input has the expected value.

            Args:
                pom: POM instance containing root-level interactions.
                expected_value: Expected value of the element.

            Returns:
                ``True`` when the root input value matches, else ``False``.
            """
            return pom.has_input_value(expected_value)

        @staticmethod
        def assert_input_value(pom: RootablePOM, expected_value: str) -> RootablePOM:
            """Assert that the POM root input has the expected value.

            Args:
                pom: POM instance containing root-level interactions.
                expected_value: Expected value of the element.

            Returns:
                The same POM instance to allow chaining.
            """
            return pom.assert_input_value(expected_value)

    return POMInteractionHelper()
