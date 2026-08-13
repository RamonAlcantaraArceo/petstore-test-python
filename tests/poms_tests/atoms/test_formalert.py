import pytest

from framework.poms.atoms.formalert_pom import FormalertPOM


@pytest.mark.smoke
def test_formalert_pom_class_imports():
    assert FormalertPOM is not None


@pytest.mark.smoke
def test_formalert_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(FormalertPOM, "SELECTOR")
    assert (
        FormalertPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_formalert_story_id_defined():
    assert hasattr(FormalertPOM, "STORY_ID")
    assert (
        FormalertPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_formalert_error(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-formalert--error' and verify the component is visible."""
    pom = FormalertPOM(driver)
    pom.navigate_to_story("common-atoms-formalert--error")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Error alert should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_formalert_warning(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-formalert--warning' and verify the component is visible."""
    pom = FormalertPOM(driver)
    pom.navigate_to_story("common-atoms-formalert--warning")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Warning alert should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_formalert_info(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-formalert--info' and verify the component is visible."""
    pom = FormalertPOM(driver)
    pom.navigate_to_story("common-atoms-formalert--info")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Info alert should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_formalert_success(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-formalert--success' and verify the component is visible."""
    pom = FormalertPOM(driver)
    pom.navigate_to_story("common-atoms-formalert--success")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Success alert should be displayed"
