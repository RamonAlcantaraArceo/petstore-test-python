---
applyTo: 'tests/poms_tests/**/*.py'
name: storybook-derived-pom-testing
description: "Use when generating or updating Storybook-derived Selenium POM tests. Enforces POM-only interactions, explicit assertion failures for missing or invalid POM members, and Storybook-metadata-driven hierarchy validation."
---

# Storybook-Derived POM Testing Rules

This instruction defines a reusable policy for generating Selenium tests that rely exclusively on Storybook-derived Page Object Models (POMs).

The POM is the single source of truth.
Copilot must never invent locators, guess selectors, or bypass the POM hierarchy.

## Rules

- Use the existing POM class for all interactions.
- The authoritative list of expected atoms and molecules for a component is derived exclusively from that component's Storybook metadata.
- Do not infer expected atoms or molecules from DOM inspection, component source code, or general UI assumptions.
- Validate that each expected POM member exists and is interactable.
- Validate that each atom explicitly exposed as a POM member is interactable.
- Do not attempt to discover or validate `data-component` elements that are not already exposed as named members on the POM.
- Enforce Storybook hierarchy (molecule to atoms).
- For nested sub-molecules, validate each sub-molecule root before validating its atoms.
- Recursion depth is limited to what is explicitly documented in Storybook metadata.
- Do not create new selectors.
- Do not guess DOM structure or assumptions.
- Do not use role-based selectors, XPath, or CSS selectors outside the POM.
- Use Selenium waits only through existing suite mechanisms, such as `pom_interaction_helper.wait_for_visibility` or `WebDriverWait` with expected conditions.
- Do not use `time.sleep()` or custom retry loops.
- In tests for this layer, call `wait_for_visibility(..., raise_on_timeout=False)` and assert explicitly with a rich failure message.
- Do not use `pom.root()` as the primary visibility assertion path for component readiness.
- Use `pom.wait_for_visibility(..., raise_on_timeout=False)` first, then assert on the returned element.
- Do not rely on `TimeoutException` as the primary assertion signal in these tests.
- Do not modify or generate new POM classes.
- Do not add atoms or interactions not documented in Storybook metadata.
- Always start coverage from the default story defined in `STORY_ID`.
- If `ALL_STORY_IDS` exists, generate one dedicated test function per story ID in that list.
- If `ALL_STORY_IDS` is missing, generate at least one test using `STORY_ID`.
- Do not iterate through all stories inside a single test function.
- Story-specific assertions are required; do not reuse a single generic assertion set for every story.
- If the allowed Selenium wait mechanisms are insufficient for a scenario, raise an `AssertionError` describing the condition.
- When any of the following conditions are encountered, raise an `AssertionError` with a message identifying the specific condition: missing POM locators, missing Storybook metadata, incorrect `data-component` values, POM hierarchy mismatch, or interaction failure.
- Do not swallow these errors silently or document them only as comments.

## Build Instructions

1. Instantiate the component POM and resolve story IDs.

```python
pom = ComponentPOM(driver)

default_story_id = getattr(pom, "STORY_ID", None)
if not default_story_id:
    raise AssertionError("ComponentPOM is missing required story id: STORY_ID")

all_story_ids = getattr(pom, "ALL_STORY_IDS", [default_story_id])
if not all_story_ids:
    raise AssertionError("ComponentPOM has no stories to test")
```

2. Verify required navigation method availability before story navigation.

```python
if not hasattr(pom, "navigate_to_story"):
    raise AssertionError(
        "ComponentPOM is missing required navigation method: navigate_to_story"
    )
```

3. Generate dedicated tests per story.

```python
def test_component_default_story(driver):
    """..."""
    pom = ComponentPOM(driver)
    pom.navigate_to_story(ComponentPOM.STORY_ID)

    root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert root_element is not None, (
        f"Root element not visible in default story: {ComponentPOM.STORY_ID}"
    )


def test_component_error_story(driver):
    """..."""
    error_story_id = "<component-error-story-id>"
    pom = ComponentPOM(driver)
    pom.navigate_to_story(error_story_id)

    root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert root_element is not None, (
        f"Root element not visible in error story: {error_story_id}"
    )


def test_component_loading_story(driver):
    """..."""
    loading_story_id = "<component-loading-story-id>"
    pom = ComponentPOM(driver)
    pom.navigate_to_story(loading_story_id)

    root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
    assert root_element is not None, (
        f"Root element not visible in loading story: {loading_story_id}"
    )
```

4. Validate each expected atom exists on the POM before interaction.

```python
required_atoms = ["atom_accessor_one", "atom_accessor_two", "atom_accessor_three"]
for atom_name in required_atoms:
    if not hasattr(pom, atom_name):
        raise AssertionError(f"ComponentPOM is missing expected atom: {atom_name}")

    atom_member = getattr(pom, atom_name)
    if atom_member is None:
        raise AssertionError(
            f"ComponentPOM atom {atom_name} is None; POM may be incomplete"
        )
    if not callable(atom_member):
        raise AssertionError(
            f"ComponentPOM atom {atom_name} is not callable; expected a POM accessor"
        )
```

5. Validate atom visibility, interactivity, and scenario behavior in each dedicated story test.

```python
root_element = pom.wait_for_visibility(timeout=10, raise_on_timeout=False)
assert root_element is not None, (
    f"Root element not visible for story {story_id}: {pom.SELECTOR}"
)

atom_one = pom.atom_accessor_one().root()
atom_two = pom.atom_accessor_two().root()
atom_three = pom.atom_accessor_three().root()

assert atom_one.is_displayed() and atom_one.is_enabled()
assert atom_two.is_displayed() and atom_two.is_enabled()
assert atom_three.is_displayed() and atom_three.is_enabled()

atom_one.clear()
atom_one.send_keys("example-input")
atom_two.clear()
atom_two.send_keys("example-input")
atom_three.click()

# In the error story test
error_alert = pom.error_alert().wait_for_visibility(timeout=10, raise_on_timeout=False)
assert error_alert is not None, (
    f"Error alert not visible for story {story_id}: expected error state"
)

# In the loading story test
loading_button = pom.primary_button().wait_for_visibility(
    timeout=10,
    raise_on_timeout=False,
)
assert loading_button is not None, (
    f"Loading button not visible for story {story_id}: expected loading state"
)
assert not loading_button.is_enabled()
```

## Required Validation Coverage

Each test generated under this instruction must validate all of the following:

- Molecule root exists.
- Each expected atom exists as a POM-exposed member.
- Each expected atom is interactable.
- Interactions behave as expected for each Storybook story.
- Default story (`STORY_ID`) is always covered.
- Every story listed in `ALL_STORY_IDS` has its own dedicated test function.
- Story coverage is split into separate tests, not a single test that loops across stories.
- Story-specific behaviors are asserted per story (for example error and loading states when applicable).

If any locator is missing from the POM, fail explicitly with:

```python
raise AssertionError("ComponentPOM is missing expected atom: <name>")
```
