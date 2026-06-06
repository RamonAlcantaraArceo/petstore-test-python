import pytest
from playwright.sync_api import expect



from poms.atoms.input_pom import InputPOM


@pytest.mark.smoke
def test_input_pom_class_imports():
    assert InputPOM is not None


@pytest.mark.smoke
def test_input_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(InputPOM, "SELECTOR")
    assert InputPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_input_story_id_defined():
    assert hasattr(InputPOM, "STORY_ID")
    assert InputPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_input_navigate_and_verify(page):
    """Verify Input POM can navigate to story and interact with the component."""
    pom = InputPOM(page)
    pom.navigate_to_story()

    root_locator = pom.root()
    expect(root_locator).to_be_visible(timeout=10_000)

    # Input-specific: verify we can type into the input
    input_elem = pom.root()
    test_input_value = "test_value_123"
    input_elem.fill(test_input_value)
    expect(input_elem).to_have_value(test_input_value)
