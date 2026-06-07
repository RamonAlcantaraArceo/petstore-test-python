import pytest

from framework.poms.molecules.usercard_pom import UsercardPOM


@pytest.mark.smoke
def test_usercard_pom_class_imports():
    assert UsercardPOM is not None


@pytest.mark.smoke
def test_usercard_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(UsercardPOM, "SELECTOR")
    assert (
        UsercardPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_usercard_story_id_defined():
    assert hasattr(UsercardPOM, "STORY_ID")
    assert (
        UsercardPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_usercard_navigate_and_verify(driver):
    """Verify Usercard POM can navigate to story and interact with the component."""
    pom = UsercardPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = ["danger_button", "secondary_button"]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"UsercardPOM is missing expected atom: {atom_name}")
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"UsercardPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"UsercardPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pom.danger_button().assert_element_displayed().assert_element_enabled()
    pom.secondary_button().assert_element_displayed().assert_element_enabled()
