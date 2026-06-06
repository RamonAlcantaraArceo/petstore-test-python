from __future__ import annotations

import os
from importlib import import_module
from typing import Any


class PlaywrightBasePOM:
    PACKAGE_ROOT = "poms"

    def __init__(
        self,
        *,
        page: Any,
        selector: str,
        story_id: str,
        dependencies: list[str],
        selector_override: str | None = None,
        index_override: int | None = None,
    ) -> None:
        self.page = page
        self.STORY_ID = story_id
        self._selector = selector_override or selector
        self._index = index_override
        self.dependencies = dependencies

    @staticmethod
    def _resolve_child_pom_class(component_name: str):
        module_stem = "".join(
            ("_" + ch.lower()) if ch.isupper() else ch for ch in component_name
        ).lstrip("_")
        module_name = module_stem + "_pom"
        class_name = component_name + "POM"
        for level in ("atoms", "molecules", "organisms", "views", "app"):
            try:
                module = import_module(
                    PlaywrightBasePOM.PACKAGE_ROOT + "." + level + "." + module_name
                )
                cls = getattr(module, class_name, None)
                if cls is not None:
                    return cls
            except Exception:
                continue
        raise ImportError(
            "Could not resolve child POM class for "
            + component_name
            + " ("
            + module_name
            + ")."
        )

    @staticmethod
    def storybook_url() -> str:
        return os.getenv("SBPOM_STORYBOOK_URL", "http://localhost:6006")

    def navigate_to_story(self, story_id: str | None = None) -> None:
        """Open the Storybook iframe for this component."""
        self.page.goto(
            f"{self.storybook_url()}/iframe.html?id={story_id or self.STORY_ID}"
        )

    def root(self):
        loc = self.page.locator(self._selector)
        return loc.nth(self._index) if self._index is not None else loc

    def _scoped_selector(self, child_selector: str) -> str:
        return f"{self._selector} {child_selector}"

    def _child_pom(self, component_name: str, child_selector: str):
        child_cls = self._resolve_child_pom_class(component_name)
        scoped = self._scoped_selector(child_selector)
        try:
            return child_cls(self.page, selector_override=scoped)
        except TypeError:
            child = child_cls(self.page)
            child.SELECTOR = scoped
            return child

    def _child_poms(self, component_name: str, child_selector: str):
        child_cls = self._resolve_child_pom_class(component_name)
        scoped = self._scoped_selector(child_selector)
        count = self.page.locator(scoped).count()
        items = []
        for idx in range(count):
            try:
                items.append(
                    child_cls(self.page, selector_override=scoped, index_override=idx)
                )
            except TypeError:
                child = child_cls(self.page)
                child.SELECTOR = scoped
                child._index = idx
                items.append(child)
        return items
