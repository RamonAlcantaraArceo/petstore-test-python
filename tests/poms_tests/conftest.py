"""Auto-generated conftest.py for the Selenium test suite.
Test files import POM classes using the configured package path, e.g.:
    from poms.atoms.badge_pom import BadgePOM
"""
import os
from pathlib import Path
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
        default="http://localhost:6006",
    )

def pytest_configure(config):
    storybook_url = config.getoption("--storybook-url") or config.getini("storybook_url")
    if storybook_url:
        os.environ["SBPOM_STORYBOOK_URL"] = storybook_url

@pytest.fixture()
def driver():
    """Fixture to initialize and quit the Selenium WebDriver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless=new")   # modern headless mode
    options.add_argument("--disable-gpu")    # optional, good for CI
    options.add_argument("--no-sandbox")     # optional, for Docker

    driver = webdriver.Chrome(options=options) # or webdriver.Firefox(), etc.  Make sure to have the appropriate WebDriver installed and in PATH.
    yield driver
    driver.quit()

@pytest.fixture
def capture_screenshot(request, driver):
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
    def _wait_for(driver, selector: str, condition=EC.presence_of_element_located, timeout: int = 10):
        wait = WebDriverWait(driver, timeout)
        return wait.until(condition((By.CSS_SELECTOR, selector)))
    return _wait_for

@pytest.fixture
def pom_interaction_helper():
    """Fixture that returns a helper for common multi-step POM interactions."""
    class InteractionHelper:
        @staticmethod
        def wait_for_visibility(pom, timeout: int = 10, raise_on_timeout: bool = True):
            selector = getattr(pom, "_selector", pom.SELECTOR)
            wait = WebDriverWait(pom.driver, timeout)
            try:
                return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            except TimeoutException:
                if raise_on_timeout:
                    raise
                return None
        
        @staticmethod
        def type_into(element, text: str):
            element.clear()
            element.send_keys(text)
            return element
        
        @staticmethod
        def click_element(element):
            element.click()
            return element
        
        @staticmethod
        def select_option(select_element, option_text: str):
            from selenium.webdriver.support.select import Select
            select = Select(select_element)
            select.select_by_visible_text(option_text)
            return select_element
        
        @staticmethod
        def assert_element_visible(element):
            assert element.is_displayed(), f"Element not visible: {element}"
            return True
        
        @staticmethod
        def assert_element_enabled(element):
            assert element.is_enabled(), f"Element not enabled: {element}"
            return True
        
        @staticmethod
        def assert_input_value(element, expected_value: str):
            actual_value = element.get_attribute("value")
            assert actual_value == expected_value, f"Expected \'{expected_value}\' but got \'{actual_value}\'"
            return True
    
    return InteractionHelper()
