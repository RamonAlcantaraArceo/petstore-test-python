"""Auto-generated conftest.py — adds the poms/ directory to sys.path so that
test files can import POM classes with simple absolute imports like:
    from atoms.badge_pom import BadgePOM
"""
import sys
import os
from pathlib import Path
import pytest

# sys.path.insert(0, str(Path(__file__).parent / "poms"))

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
def page():
    """Fixture to initialize and quit a Playwright page."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.fixture
def capture_screenshot(request, page):
    """Fixture to capture a screenshot of the page at test level."""
    yield
    if hasattr(request, "node"):
        test_name = request.node.name
        screenshot_dir = Path(__file__).parent / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        screenshot_path = screenshot_dir / f"{test_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"Screenshot saved to: {screenshot_path}")
