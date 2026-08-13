import pytest

from framework.poms.molecules.petcard_pom import PetcardPOM


@pytest.mark.smoke
def test_petcard_pom_class_imports():
    assert PetcardPOM is not None


@pytest.mark.smoke
def test_petcard_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(PetcardPOM, "SELECTOR")
    assert (
        PetcardPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_petcard_story_id_defined():
    assert hasattr(PetcardPOM, "STORY_ID")
    assert (
        PetcardPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_petcard_navigate_and_verify(driver):
    """Verify Petcard POM can navigate to story and interact with the component."""
    pom = PetcardPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = ["available_badge", "danger_button", "secondary_button"]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"PetcardPOM is missing expected atom: {atom_name}")
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"PetcardPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"PetcardPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pom.available_badge().assert_element_displayed()
    pom.danger_button().assert_element_displayed().assert_element_enabled()
    pom.secondary_button().assert_element_displayed().assert_element_enabled()
