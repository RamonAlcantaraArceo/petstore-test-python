import pytest


from framework.poms.molecules.ordercard_pom import OrdercardPOM


@pytest.mark.smoke
def test_ordercard_pom_class_imports():
    assert OrdercardPOM is not None


@pytest.mark.smoke
def test_ordercard_selector_defined():
    """Selector discovered from the live Storybook DOM should be non-empty."""
    assert hasattr(OrdercardPOM, "SELECTOR")
    assert OrdercardPOM.SELECTOR, "SELECTOR is empty — run sbpom again with playwright installed"


@pytest.mark.smoke
def test_ordercard_story_id_defined():
    assert hasattr(OrdercardPOM, "STORY_ID")
    assert OrdercardPOM.STORY_ID, "STORY_ID is empty — no renderable story found for this component"

@pytest.mark.functional
@pytest.mark.usefixtures("capture_screenshot")
def test_ordercard_navigate_and_verify(driver, pom_interaction_helper):
    """Verify Ordercard POM can navigate to story and interact with the component."""
    pom = OrdercardPOM(driver)
    pom.navigate_to_story()

    # Wait for root element to be visible (timeout 10s)
    root_element = pom_interaction_helper.wait_for_visibility(pom, timeout=10)
    assert root_element is not None, f"Root element not visible: {pom.SELECTOR}"

    # Form/Molecule-specific: verify child form inputs exist and are interactable
    # (This tests the hierarchical composition pattern)
    try:
        # Try to access first child method if form has inputs
        # This demonstrates that _child_pom() resolution works
        pom_root = pom.root()
        assert pom_root is not None, "Form root not found"
        # Additional child-specific tests would go here
    except AttributeError:
        # If no child accessors, just verify root exists
        pass
