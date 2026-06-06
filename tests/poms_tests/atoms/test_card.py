import pytest

from framework.poms.atoms.card_pom import CardPOM


@pytest.mark.smoke
def test_card_pom_class_imports():
    assert CardPOM is not None


@pytest.mark.smoke
def test_card_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(CardPOM, "SELECTOR")
    assert (
        CardPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_card_story_id_defined():
    assert hasattr(CardPOM, "STORY_ID")
    assert (
        CardPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Card POM can navigate to story and interact with the component."""
    pom = CardPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Generic component verification
    assert root_element is not None, "Component is not visible"
