import pytest

from framework.poms.molecules.petform_pom import PetformPOM


@pytest.mark.smoke
def test_petform_pom_class_imports():
    assert PetformPOM is not None


@pytest.mark.smoke
def test_petform_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(PetformPOM, "SELECTOR")
    assert (
        PetformPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_petform_story_id_defined():
    assert hasattr(PetformPOM, "STORY_ID")
    assert (
        PetformPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_petform_navigate_and_verify(driver):
    """Verify Petform POM can navigate to story and interact with the component."""
    pom = PetformPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = [
        "category_name_input",
        "name_input",
        "photo_url_input",
        "select",
        "primary_button",
        "secondary_button",
    ]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"PetformPOM is missing expected atom: {atom_name}")
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"PetformPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"PetformPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pom.category_name_input().type_into("Dogs")
    pom.category_name_input().assert_input_value("Dogs")
    pom.name_input().type_into("Buddy")
    pom.name_input().assert_input_value("Buddy")
    pom.photo_url_input().type_into("https://example.com/buddy.jpg")
    pom.photo_url_input().assert_input_value("https://example.com/buddy.jpg")
    pom.select().assert_element_displayed().assert_element_enabled()
    pom.primary_button().assert_element_displayed().assert_element_enabled()
    pom.secondary_button().assert_element_displayed().assert_element_enabled()
