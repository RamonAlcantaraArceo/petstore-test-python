import pytest

from framework.poms.atoms.badge_pom import BadgePOM


@pytest.mark.smoke
def test_badge_pom_class_imports():
    assert BadgePOM is not None


@pytest.mark.smoke
def test_badge_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(BadgePOM, "SELECTOR")
    assert (
        BadgePOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_badge_story_id_defined():
    assert hasattr(BadgePOM, "STORY_ID")
    assert (
        BadgePOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_badge_default(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-badge--default' and verify the component is visible."""
    pom = BadgePOM(driver)
    pom.navigate_to_story("common-atoms-badge--default")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Default badge should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_badge_all_variants(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-badge--all-variants' and verify the component is visible."""
    pom = BadgePOM(driver)
    pom.navigate_to_story("common-atoms-badge--all-variants")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert (
        root_element.is_displayed()
    ), "All variants badge showcase should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_badge_sizes(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-badge--sizes' and verify the component is visible."""
    pom = BadgePOM(driver)
    pom.navigate_to_story("common-atoms-badge--sizes")

    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Badge sizes showcase should be displayed"
