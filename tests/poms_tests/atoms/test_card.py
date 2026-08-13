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
def test_card_default(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--default' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--default")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_basic_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--basic-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--basic-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_primary_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--primary-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--primary-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_secondary_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--secondary-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--secondary-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_success_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--success-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--success-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_warning_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--warning-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--warning-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_error_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--error-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--error-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_no_elevation(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--no-elevation' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--no-elevation")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_small_elevation(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--small-elevation' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--small-elevation")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_large_elevation(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--large-elevation' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--large-elevation")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_extra_large_elevation(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--extra-large-elevation' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--extra-large-elevation")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_interactive(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--interactive' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--interactive")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_selected(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--selected' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--selected")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_with_border(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--with-border' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--with-border")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_no_padding(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--no-padding' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--no-padding")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_small_padding(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--small-padding' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--small-padding")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_large_padding(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--large-padding' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--large-padding")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_extra_large_padding(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--extra-large-padding' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--extra-large-padding")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_all_elevations(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--all-elevations' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--all-elevations")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_all_variants(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--all-variants' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--all-variants")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_all_rounded_options(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--all-rounded-options' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--all-rounded-options")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_accessibility_showcase(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--accessibility-showcase' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--accessibility-showcase")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_internationalization_demo(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--internationalization-demo' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--internationalization-demo")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_card_grid(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--card-grid' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--card-grid")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_full_width_card(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--full-width-card' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--full-width-card")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_card_with_header(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--card-with-header' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--card-with-header")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"


@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_card_card_with_footer(driver, pom_interaction_helper):
    """Navigate to story 'common-atoms-card--card-with-footer' and verify the component is visible."""
    pom = CardPOM(driver)
    pom.navigate_to_story("common-atoms-card--card-with-footer")

    # Generic component verification
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"
    assert root_element.is_displayed(), "Card should be displayed"
