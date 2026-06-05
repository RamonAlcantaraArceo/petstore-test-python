"""UI tests – login feature (Page Object Model + Selenium).

These tests use the same assertion style as tests/api/test_login.py,
demonstrating the shared-interface pattern across API and UI.

The target site is https://the-internet.herokuapp.com/login
(a freely available Selenium practice site).  Override the target by
setting the ``PETSTORE_UI_BASE_URL`` environment variable.

Note: UI tests are skipped in CI unless the ``--run-ui`` flag is passed
or the ``RUN_UI_TESTS`` environment variable is set to ``1``.
"""

from __future__ import annotations

import os

import allure
import pytest
from selenium.webdriver.common.by import By

from framework.assertions import assert_that

# Skip entire module when Selenium is unavailable or UI tests are disabled
pytestmark = pytest.mark.ui


def _ui_enabled() -> bool:
    return os.getenv("RUN_UI_TESTS", "0") in ("1", "true", "yes")


skip_if_no_ui = pytest.mark.skipif(
    not _ui_enabled(),
    reason="UI tests are disabled. Set RUN_UI_TESTS=1 to enable.",
)

