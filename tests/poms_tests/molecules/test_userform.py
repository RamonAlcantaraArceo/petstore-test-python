import pytest

from framework.poms.molecules.userform_pom import UserformPOM


@pytest.mark.smoke
def test_userform_pom_class_imports():
    assert UserformPOM is not None


@pytest.mark.smoke
def test_userform_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(UserformPOM, "SELECTOR")
    assert (
        UserformPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_userform_story_id_defined():
    assert hasattr(UserformPOM, "STORY_ID")
    assert (
        UserformPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_userform_navigate_and_verify(driver):
    """Verify Userform POM can navigate to story and interact with the component."""
    pom = UserformPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = [
        "username_input",
        "first_name_input",
        "last_name_input",
        "email_input",
        "phone_input",
        "password_input",
        "primary_button",
        "secondary_button",
    ]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"UserformPOM is missing expected atom: {atom_name}")
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"UserformPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"UserformPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pom.username_input().type_into("demo_user")
    pom.username_input().assert_input_value("demo_user")
    pom.first_name_input().type_into("Demo")
    pom.first_name_input().assert_input_value("Demo")
    pom.last_name_input().type_into("User")
    pom.last_name_input().assert_input_value("User")
    pom.email_input().type_into("demo@example.com")
    pom.email_input().assert_input_value("demo@example.com")
    pom.phone_input().type_into("1234567890")
    pom.phone_input().assert_input_value("1234567890")
    pom.password_input().type_into("secure_password")
    pom.password_input().assert_input_value("secure_password")
    pom.primary_button().assert_element_displayed().assert_element_enabled()
    pom.secondary_button().assert_element_displayed().assert_element_enabled()
