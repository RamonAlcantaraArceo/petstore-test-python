import pytest

from framework.poms.molecules.confirmdialog_pom import ConfirmdialogPOM


@pytest.mark.smoke
def test_confirmdialog_pom_class_imports():
    assert ConfirmdialogPOM is not None


@pytest.mark.smoke
def test_confirmdialog_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(ConfirmdialogPOM, "SELECTOR")
    assert (
        ConfirmdialogPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_confirmdialog_story_id_defined():
    assert hasattr(ConfirmdialogPOM, "STORY_ID")
    assert (
        ConfirmdialogPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_confirmdialog_navigate_and_verify(driver):
    """Verify Confirmdialog POM can navigate to story and interact with the component."""
    pom = ConfirmdialogPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    pom.assert_element_displayed().assert_element_enabled()
    pom.click_element()
