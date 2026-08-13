import pytest

from framework.poms.molecules.orderform_pom import OrderformPOM


@pytest.mark.smoke
def test_orderform_pom_class_imports():
    assert OrderformPOM is not None


@pytest.mark.smoke
def test_orderform_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(OrderformPOM, "SELECTOR")
    assert (
        OrderformPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_orderform_story_id_defined():
    assert hasattr(OrderformPOM, "STORY_ID")
    assert (
        OrderformPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_orderform_navigate_and_verify(driver):
    """Verify Orderform POM can navigate to story and interact with the component."""
    pom = OrderformPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = [
        "pet_id_input",
        "quantity_input",
        "primary_button",
        "secondary_button",
    ]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"OrderformPOM is missing expected atom: {atom_name}")
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"OrderformPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"OrderformPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pet_id_input = pom.pet_id_input()
    quantity_input = pom.quantity_input()
    primary_button = pom.primary_button()
    secondary_button = pom.secondary_button()

    pet_id_input.wait_for_visibility(timeout=10)
    quantity_input.wait_for_visibility(timeout=10)
    primary_button.wait_for_visibility(timeout=10)
    secondary_button.wait_for_visibility(timeout=10)

    pet_id_input.type_into("123")
    pet_id_input.assert_input_value("123")
    quantity_input.type_into("2")
    quantity_input.assert_input_value("2")
    primary_button.assert_element_displayed().assert_element_enabled()
    secondary_button.assert_element_displayed().assert_element_enabled()
