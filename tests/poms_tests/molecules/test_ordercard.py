import pytest

from framework.poms.molecules.ordercard_pom import OrdercardPOM


@pytest.mark.smoke
def test_ordercard_pom_class_imports():
    assert OrdercardPOM is not None


@pytest.mark.smoke
def test_ordercard_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(OrdercardPOM, "SELECTOR")
    assert (
        OrdercardPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_ordercard_story_id_defined():
    assert hasattr(OrdercardPOM, "STORY_ID")
    assert (
        OrdercardPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_ordercard_navigate_and_verify(driver):
    """Verify Ordercard POM can navigate to story and interact with the component."""
    pom = OrdercardPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = ["placed_badge", "danger_button"]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"OrdercardPOM is missing expected atom: {atom_name}")
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"OrdercardPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"OrdercardPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pom.placed_badge().assert_element_displayed()
    pom.danger_button().assert_element_displayed().assert_element_enabled()
    pom.danger_button().click_element()
