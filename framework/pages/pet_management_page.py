"""Page object for Petstore pet-management interactions."""

from __future__ import annotations

import re
import zlib
from typing import Any, cast

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait

from framework.poms.app.full_application_pom import FullApplicationPOM
from framework.poms.molecules.petcard_pom import PetcardPOM
from framework.poms.molecules.petform_pom import PetformPOM
from framework.poms.molecules.statusfilter_pom import StatusfilterPOM
from framework.poms.organisms.appnavigation_pom import AppnavigationPOM
from framework.poms.views.pet_management_pom import PetManagementPOM


class PetManagementPage:
    """Handle Pet Management view interactions against the Petstore UI."""

    _VALID_STATUSES = {"available", "pending", "sold"}

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        """Create a pet-management page wrapper.

        Args:
            driver: Selenium WebDriver used to interact with the page.
            base_url: Root URL of the UI application.
        """
        self.driver = driver
        self.base_url = base_url.rstrip("/")

        self.full_app: FullApplicationPOM = FullApplicationPOM(driver)
        self.app_navigation: AppnavigationPOM = AppnavigationPOM(driver)
        self.pet_management: PetManagementPOM = PetManagementPOM(driver)
        self.pet_form: PetformPOM = PetformPOM(driver)
        self.status_filter: StatusfilterPOM = StatusfilterPOM(driver)

    def open(self) -> PetManagementPage:
        """Open the Pets route and wait until the view is visible."""
        self.driver.get(self._pets_url())
        self.full_app.wait_for_visibility(timeout=10)
        self.pet_management.wait_for_visibility(timeout=10)
        return self

    def add_pet(
        self, name: str, status: str = "available", **kwargs: Any
    ) -> dict[str, Any]:
        """Create a pet through the Pet Management form and return its card data.

        Args:
            name: Pet name.
            status: Desired pet status.
            **kwargs: Optional pet fields such as ``category``, ``categoryName``,
                ``photoUrl``, and ``photoUrls``.

        Returns:
            Parsed pet data from the created card.
        """
        normalized_status = self._normalize_status(status)
        self._ensure_view_ready()
        existing_rows = self._card_rows()
        existing_signatures = {self._pet_signature(pet) for _, pet in existing_rows}

        self.pet_management.primary_button().click_element()
        self._fill_pet_form(name=name, status=normalized_status, **kwargs)
        self.pet_form.primary_button().click_element()
        self.pet_form.wait_for_absence(timeout=10, raise_on_timeout=False)

        try:
            WebDriverWait(self.driver, 5).until(
                lambda _driver: len(self._card_rows()) >= len(existing_rows) + 1
            )
        except TimeoutException:
            # A status-filtered view may hide newly created pets.
            pass
        current_rows = self._card_rows()
        new_pets = [
            pet
            for _, pet in current_rows
            if self._pet_signature(pet) not in existing_signatures
        ]
        if not new_pets:
            new_pets = [pet for _, pet in current_rows if pet["name"] == name]
        exact_match = [
            pet
            for pet in new_pets
            if pet["name"] == name and pet["status"] == normalized_status
        ]
        if exact_match:
            return max(exact_match, key=lambda pet: pet["id"])
        if new_pets:
            return max(new_pets, key=lambda pet: pet["id"])

        self._apply_status_filter(normalized_status)
        status_rows = [pet for _, pet in self._card_rows()]
        status_exact_match = [pet for pet in status_rows if pet["name"] == name]
        if status_exact_match:
            return max(status_exact_match, key=lambda pet: pet["id"])

        raise AssertionError(
            f"Could not identify the created pet for name='{name}' status='{normalized_status}'."
        )

    def get_pet(self, pet_id: int) -> dict[str, Any]:
        """Return parsed pet card data by id.

        Args:
            pet_id: Identifier of the pet to retrieve.

        Raises:
            KeyError: If no visible pet card with this id exists.
        """
        self._ensure_view_ready()
        for _, pet in self._card_rows():
            if pet["id"] == pet_id:
                return pet
        raise KeyError(f"Pet with id {pet_id} was not found in the UI.")

    def update_pet(self, pet_id: int, **kwargs: Any) -> dict[str, Any]:
        """Update a pet via the card edit action and return updated card data.

        Args:
            pet_id: Identifier of the pet to update.
            **kwargs: Fields to update. Supported fields are ``name``, ``status``,
                ``category``, ``categoryName``, ``photoUrl``, and ``photoUrls``.
        """
        self._ensure_view_ready()
        card = self._pet_card_by_id(pet_id)
        self._click_card_button(card, variant="secondary")
        self.pet_form.wait_for_visibility(timeout=10)

        status = kwargs.get("status")
        normalized_status = (
            self._normalize_status(status) if status is not None else None
        )
        form_kwargs = {
            key: value for key, value in kwargs.items() if key not in {"name", "status"}
        }
        self._fill_pet_form(
            name=kwargs.get("name"),
            status=normalized_status,
            **form_kwargs,
        )
        self.pet_form.primary_button().click_element()
        self.pet_form.wait_for_absence(timeout=10, raise_on_timeout=False)

        expected_name = kwargs.get("name")
        expected_status = normalized_status
        if isinstance(expected_name, str) or expected_status is not None:
            matches = []
            for _, pet in self._card_rows():
                name_matches = (
                    True if expected_name is None else pet["name"] == expected_name
                )
                status_matches = (
                    True
                    if expected_status is None
                    else pet["status"] == expected_status
                )
                if name_matches and status_matches:
                    matches.append(pet)
            if matches:
                return max(matches, key=lambda pet: pet["id"])

        return self.get_pet(pet_id)

    def delete_pet(self, pet_id: int) -> None:
        """Delete a pet through the card delete action.

        Args:
            pet_id: Identifier of the pet to delete.
        """
        self._ensure_view_ready()
        card = self._pet_card_by_id(pet_id)
        self._click_card_button(card, variant="danger")
        self._confirm_delete_if_dialog_present()

        WebDriverWait(self.driver, 10).until(
            lambda _driver: all(pet["id"] != pet_id for _, pet in self._card_rows())
        )

    def find_pets_by_status(self, status: str) -> list[dict[str, Any]]:
        """Apply the status filter and return parsed cards for that status.

        Args:
            status: Pet status to search for.
        """
        normalized_status = self._normalize_status(status)
        self._ensure_view_ready()

        self._apply_status_filter(normalized_status)

        cards = [pet for _, pet in self._card_rows()]
        return [pet for pet in cards if pet["status"] == normalized_status]

    def _pets_url(self) -> str:
        """Return the canonical pets route URL."""
        base_without_hash = self.base_url.split("#", maxsplit=1)[0].rstrip("/")
        return f"{base_without_hash}/#/pets"

    def _ensure_view_ready(self) -> None:
        """Ensure the Pet Management view is visible without forcing navigation."""
        if (
            self.pet_management.wait_for_visibility(timeout=2, raise_on_timeout=False)
            is None
        ):
            self.open()

    def _apply_status_filter(self, status: str) -> None:
        """Apply the status filter in the pet management view."""
        select = self.status_filter.select()
        element = select.root().find_element(By.TAG_NAME, "select")
        select_element = Select(element)
        try:
            select_element.select_by_visible_text(status)
        except NoSuchElementException:
            select_element.select_by_visible_text(status.capitalize())
        self.status_filter.secondary_button().click_element()

    def _normalize_status(self, status: str) -> str:
        """Normalize and validate a status value."""
        normalized = status.strip().lower()
        if normalized not in self._VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Expected one of: {sorted(self._VALID_STATUSES)}."
            )
        return normalized

    def _fill_pet_form(
        self, name: str | None, status: str | None, **kwargs: Any
    ) -> None:
        """Populate the PetForm with provided values."""
        form_root = self.pet_form.wait_for_visibility(
            timeout=10, raise_on_timeout=False
        )
        if form_root is None:
            raise AssertionError("Pet form is not visible.")

        if name is not None:
            self.pet_form.name_input().type_into(name)

        category_name = kwargs.get("categoryName")
        category = kwargs.get("category")
        if category_name is None and isinstance(category, dict):
            raw_category_name = category.get("name")
            if isinstance(raw_category_name, str):
                category_name = raw_category_name
        if isinstance(category_name, str):
            self.pet_form.category_name_input().type_into(category_name)

        photo_url = kwargs.get("photoUrl")
        if photo_url is None:
            photo_urls = kwargs.get("photoUrls")
            if (
                isinstance(photo_urls, list)
                and photo_urls
                and isinstance(photo_urls[0], str)
            ):
                photo_url = photo_urls[0]
        if isinstance(photo_url, str):
            self.pet_form.photo_url_input().type_into(photo_url)

        if status is not None:
            select = self.pet_form.select()

            element = select.root().find_element(By.TAG_NAME, "select")

            select_element = Select(element)
            try:
                select_element.select_by_visible_text(status)
                # select.select_option(status)
            except NoSuchElementException:
                # select.select_option(status.capitalize())

                select_element.select_by_visible_text(status.capitalize())

    def _card_rows(self) -> list[tuple[PetcardPOM, dict[str, Any]]]:
        """Return visible pet cards with parsed data."""
        parsed: list[tuple[PetcardPOM, dict[str, Any]]] = []
        cards = self.pet_management.petcards()
        for index, card in enumerate(cards):
            card_pom = cast(PetcardPOM, card)
            for attempt in range(3):
                try:
                    root = card_pom.root()
                    if not root.is_displayed():
                        break
                    pet = self._pet_from_card(root, card_index=index)
                    parsed.append((card_pom, pet))
                    break
                except (IndexError, StaleElementReferenceException):
                    if attempt == 2:
                        break
        return parsed

    def _pet_signature(self, pet: dict[str, Any]) -> tuple[int, str, str]:
        """Build a stable signature for created-pet detection."""
        return (int(pet["id"]), str(pet["name"]), str(pet["status"]))

    def _pet_card_by_id(self, pet_id: int) -> PetcardPOM:
        """Return the PetCard POM matching ``pet_id``.

        Raises:
            KeyError: If no card for ``pet_id`` is visible.
        """
        for card, pet in self._card_rows():
            if pet["id"] == pet_id:
                return card
        raise KeyError(f"Pet with id {pet_id} was not found in the UI.")

    def _click_card_button(self, card: PetcardPOM, variant: str) -> None:
        """Click a card-local action button by variant."""
        button = card.root().find_element(
            By.CSS_SELECTOR, f"[data-component='Button'][data-variant='{variant}']"
        )
        button.click()

    def _pet_from_card(self, root: WebElement, card_index: int) -> dict[str, Any]:
        """Parse a card element into a protocol-compatible pet dict."""
        status = self._status_from_card(root)
        pet_id = self._id_from_card(root, fallback_id=-(card_index + 1))
        name = self._name_from_card(root, status=status)
        return {"id": pet_id, "name": name, "status": status}

    def _status_from_card(self, root: WebElement) -> str:
        """Infer the pet status from card badges or text."""
        text = root.text.lower()
        if "available" in text:
            return "available"
        if "pending" in text:
            return "pending"
        if "sold" in text:
            return "sold"
        return "available"

    def _id_from_card(self, root: WebElement, fallback_id: int) -> int:
        """Extract a numeric pet id from known attributes or card text."""
        attribute_candidates = [
            root.get_attribute("data-pet-id"),
            root.get_attribute("data-id"),
        ]
        for value in attribute_candidates:
            if not value:
                continue
            match = re.search(r"(\d+)", value)
            if match:
                return int(match.group(1))

        text = root.text
        id_match = re.search(
            r"\b(?:pet\s*id|id)\s*[:#]?\s*(\d+)\b", text, re.IGNORECASE
        )
        if id_match:
            return int(id_match.group(1))
        hash_match = re.search(r"#\s*(\d+)\b", text)
        if hash_match:
            return int(hash_match.group(1))
        if text:
            return self._stable_positive_int(self._canonical_card_text(text))
        return fallback_id

    def _stable_positive_int(self, raw_value: str) -> int:
        """Return a deterministic positive integer for a string token."""
        return max(1, zlib.crc32(raw_value.encode("utf-8")) & 0x7FFFFFFF)

    def _canonical_card_text(self, raw_text: str) -> str:
        """Normalize card text to a stable identity token."""
        lines = [line.strip().lower() for line in raw_text.splitlines() if line.strip()]
        filtered = [line for line in lines if line not in {"edit", "delete"}]
        return "|".join(filtered)

    def _name_from_card(self, root: WebElement, status: str) -> str:
        """Extract a pet name from card text."""
        for selector in ("[data-field='name']", "[data-testid='pet-name']"):
            candidates = root.find_elements(By.CSS_SELECTOR, selector)
            if candidates:
                value = candidates[0].text.strip()
                if value:
                    return value

        lines = [line.strip() for line in root.text.splitlines() if line.strip()]
        blocked_tokens = {"edit", "delete", status, status.capitalize()}
        for line in lines:
            lower = line.lower()
            if lower in blocked_tokens:
                continue
            if re.search(r"\b(?:pet\s*id|id)\b", lower):
                continue
            return line
        return "unknown-pet"

    def _confirm_delete_if_dialog_present(self) -> None:
        """Confirm delete when a modal confirmation dialog is shown."""
        dialog_selectors = [
            "[role='dialog'] [data-component='Button'][data-variant='danger']",
            "[data-component='Modal'] [data-component='Button'][data-variant='danger']",
        ]
        for selector in dialog_selectors:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if buttons:
                buttons[0].click()
                return

        try:
            modal_button = WebDriverWait(self.driver, 1).until(
                lambda _driver: _driver.find_element(
                    By.CSS_SELECTOR, "[data-component='Button'][data-variant='danger']"
                )
            )
            modal_button.click()
        except TimeoutException:
            return
