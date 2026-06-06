import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from framework.poms.molecules.loginform_pom import LoginformPOM


@pytest.mark.smoke
def test_loginform_pom_class_imports() -> None:
    """Validate that the Loginform POM class is importable.

    Returns:
        None
    """
    assert LoginformPOM is not None


@pytest.mark.smoke
def test_loginform_selector_defined() -> None:
    """Validate that the root selector is defined.

    Returns:
        None
    """
    assert hasattr(LoginformPOM, "SELECTOR")
    assert LoginformPOM.SELECTOR, (
        "SELECTOR is empty — run sbpom again with playwright installed"
    )


@pytest.mark.smoke
def test_loginform_story_id_defined() -> None:
    """Validate that the default Storybook story ID is defined.

    Returns:
        None
    """
    assert hasattr(LoginformPOM, "STORY_ID")
    assert LoginformPOM.STORY_ID, (
        "STORY_ID is empty — no renderable story found for this component"
    )


@pytest.mark.smoke
def test_loginform_all_story_ids_defined() -> None:
    """Validate that all story IDs are discoverable for this component.

    Returns:
        None
    """
    assert hasattr(LoginformPOM, "ALL_STORY_IDS")
    assert LoginformPOM.ALL_STORY_IDS, (
        "ALL_STORY_IDS is empty — expected at least one renderable story"
    )


@pytest.mark.smoke
def test_loginform_default_story_in_all_story_ids() -> None:
    """Validate that the default story is included in the full story list.

    Returns:
        None
    """
    assert LoginformPOM.STORY_ID in LoginformPOM.ALL_STORY_IDS, (
        "STORY_ID must be present in ALL_STORY_IDS"
    )


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_loginform_navigate_and_verify_default_story(driver: WebDriver) -> None:
    """Verify default story interactions for Loginform.

    Args:
        driver: Active Selenium WebDriver instance.

    Returns:
        None
    """
    pom = LoginformPOM(driver)
    pom.navigate_to_story(LoginformPOM.STORY_ID)

    root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert root_element is not None, (
        f"Root element not visible in default story: {LoginformPOM.STORY_ID}"
    )

    required_atoms = ["username_input", "password_input", "primary_button"]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(f"LoginformPOM is missing expected atom: {atom_name}")

        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"LoginformPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"LoginformPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    username_pom = pom.username_input()
    password_pom = pom.password_input()
    submit_pom = pom.primary_button()

    username_element = username_pom.wait_for_visibility(
        timeout=10,
        raise_on_timeout=False,
    )
    assert username_element is not None, "Username input not visible in default story"

    password_element = password_pom.wait_for_visibility(
        timeout=10,
        raise_on_timeout=False,
    )
    assert password_element is not None, "Password input not visible in default story"

    submit_element = submit_pom.wait_for_visibility(
        timeout=10,
        raise_on_timeout=False,
    )
    assert submit_element is not None, "Primary button not visible in default story"

    username_pom.assert_element_displayed().assert_element_enabled()
    password_pom.assert_element_displayed().assert_element_enabled()
    submit_pom.assert_element_displayed().assert_element_enabled()

    username_pom.type_into("demo_user")
    username_pom.assert_input_value("demo_user")
    password_pom.type_into("secure_password_123")
    password_pom.assert_input_value("secure_password_123")
    submit_pom.click_element()


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_loginform_with_error_story_shows_alert(driver: WebDriver) -> None:
    """Verify the error story renders an error alert.

    Args:
        driver: Active Selenium WebDriver instance.

    Returns:
        None
    """
    error_story_id = "petstore-molecules-loginform--with-error"
    assert error_story_id in LoginformPOM.ALL_STORY_IDS, (
        f"Expected error story not found in ALL_STORY_IDS: {error_story_id}"
    )

    pom = LoginformPOM(driver)
    pom.navigate_to_story(error_story_id)

    root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert root_element is not None, (
        f"Root element not visible in error story: {error_story_id}"
    )

    alert_element = pom.error_formalert().wait_for_visibility(
        timeout=10,
        raise_on_timeout=False,
    )
    assert alert_element is not None, (
        f"Expected error alert is not visible in story: {error_story_id}"
    )


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_loginform_loading_story_shows_disabled_primary_button(
    driver: WebDriver,
) -> None:
    """Verify the loading story exposes a disabled primary button state.

    Args:
        driver: Active Selenium WebDriver instance.

    Returns:
        None
    """
    loading_story_id = "petstore-molecules-loginform--loading"
    assert loading_story_id in LoginformPOM.ALL_STORY_IDS, (
        f"Expected loading story not found in ALL_STORY_IDS: {loading_story_id}"
    )

    pom = LoginformPOM(driver)
    pom.navigate_to_story(loading_story_id)

    root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert root_element is not None, (
        f"Root element not visible in loading story: {loading_story_id}"
    )

    submit_pom = pom.primary_button()
    submit_element = submit_pom.wait_for_visibility(
        timeout=10,
        raise_on_timeout=False,
    )
    assert submit_element is not None, (
        f"Primary button not visible in loading story: {loading_story_id}"
    )

    assert not submit_element.is_enabled(), (
        "Primary button should be disabled in loading story"
    )
