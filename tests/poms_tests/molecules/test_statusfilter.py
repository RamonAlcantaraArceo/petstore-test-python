import pytest

from framework.poms.molecules.statusfilter_pom import StatusfilterPOM


@pytest.mark.smoke
def test_statusfilter_pom_class_imports():
    assert StatusfilterPOM is not None


@pytest.mark.smoke
def test_statusfilter_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(StatusfilterPOM, "SELECTOR")
    assert (
        StatusfilterPOM.SELECTOR
    ), "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_statusfilter_story_id_defined():
    assert hasattr(StatusfilterPOM, "STORY_ID")
    assert (
        StatusfilterPOM.STORY_ID
    ), "STORY_ID is empty — no renderable story found for this component"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_statusfilter_navigate_and_verify(driver):
    """Verify Statusfilter POM can navigate to story and interact with the component."""
    pom = StatusfilterPOM(driver)
    pom.navigate_to_story()

    root_element = pom.wait_for_visibility(timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    required_atoms = ["select", "secondary_button"]
    for atom_name in required_atoms:
        if not hasattr(pom, atom_name):
            raise AssertionError(
                f"StatusfilterPOM is missing expected atom: {atom_name}"
            )
        atom_accessor = getattr(pom, atom_name)
        if atom_accessor is None:
            raise AssertionError(
                f"StatusfilterPOM atom {atom_name} is None; POM may be incomplete"
            )
        if not callable(atom_accessor):
            raise AssertionError(
                f"StatusfilterPOM atom {atom_name} is not callable; expected a POM accessor"
            )

    pom.select().assert_element_displayed().assert_element_enabled()
    pom.secondary_button().assert_element_displayed().assert_element_enabled()
