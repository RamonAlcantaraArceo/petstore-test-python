"""Shared runtime configuration defaults for the Petstore test framework."""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Load local env files once when configuration is imported.
# `override=False` keeps explicit shell/CI values as highest priority.
load_dotenv(".env.test", override=False)
# load_dotenv(".env.local", override=False)

DEFAULT_PETSTORE_API_BASE_URL = "http://localhost:8000/api/v1"
DEFAULT_PETSTORE_UI_BASE_URL = "http://localhost:8080/petstore/"
DEFAULT_STORYBOOK_BASE_URL = "http://localhost:8080/storybook/"


def get_api_base_url() -> str:
    """Return the configured API base URL."""
    return os.getenv("PETSTORE_API_BASE_URL", DEFAULT_PETSTORE_API_BASE_URL)


def get_ui_base_url() -> str:
    """Return the configured UI base URL."""
    return os.getenv("PETSTORE_UI_BASE_URL", DEFAULT_PETSTORE_UI_BASE_URL)


def get_storybook_base_url() -> str:
    """Return the configured Storybook base URL."""
    return os.getenv("SBPOM_STORYBOOK_URL", DEFAULT_STORYBOOK_BASE_URL)
