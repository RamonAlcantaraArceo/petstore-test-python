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
- Do not modify or generate new POM classes.
- Do not add atoms or interactions not documented in Storybook metadata.
- If the allowed Selenium wait mechanisms are insufficient for a scenario, raise an `AssertionError` describing the condition.
- When any of the following conditions are encountered, raise an `AssertionError` with a message identifying the specific condition: missing POM locators, missing Storybook metadata, incorrect `data-component` values, POM hierarchy mismatch, or interaction failure.
- Do not swallow these errors silently or document them only as comments.

## Build Instructions

1. Instantiate the component POM.

```python
pom = ComponentPOM(driver)
```

2. Verify required navigation method availability before navigation.

```python
if not hasattr(pom, "navigate_to_story"):
   raise AssertionError(
      "ComponentPOM is missing required navigation method: navigate_to_story"
   )

pom.navigate_to_story()
```

3. Validate molecule root existence and visibility.

```python
root_element = pom.root()
assert root_element is not None, f"Root element not found: {pom.SELECTOR}"
assert root_element.is_displayed(), f"Root element not visible: {pom.SELECTOR}"
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

5. Validate atom visibility and interactivity.

```python
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
```

## Required Validation Coverage

Each test generated under this instruction must validate all of the following:

- Molecule root exists.
- Each expected atom exists as a POM-exposed member.
- Each expected atom is interactable.
- Interactions behave as expected for the Storybook scenario.

If any locator is missing from the POM, fail explicitly with:

```python
raise AssertionError("ComponentPOM is missing expected atom: <name>")
```
