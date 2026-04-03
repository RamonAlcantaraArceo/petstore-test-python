# UI Tests

UI tests automate a real browser using [Selenium](https://selenium.dev) and the
**Page Object Model (POM)** pattern to keep locators and interactions organised
and reusable.

## Location

```
tests/ui/
└── test_login.py    # Selenium login tests

framework/pages/
├── base_page.py     # Base POM – common helpers
├── login_page.py    # Login page
└── pets_page.py     # Pets / swagger UI page
```

## Enabling UI Tests

UI tests are **disabled by default** to avoid requiring a browser in all environments.

```bash
RUN_UI_TESTS=1 uv run pytest tests/ui/ -m ui -v
```

Set `HEADLESS=false` to watch the browser:

```bash
RUN_UI_TESTS=1 HEADLESS=false uv run pytest tests/ui/ -m ui -v
```

## Example Test

```python
@skip_if_no_ui
class TestLoginUi:
    def test_successful_login_shows_secure_area(self, browser):
        self._page.login("tomsmith", "SuperSecretPassword!")

        assert_that(self._page.is_logged_in()).is_true()
        assert_that(self._page.get_flash_message()).contains(
            "You logged into a secure area!"
        )
```

Notice the assertion style is **identical** to the API login test — this is the
shared-interface pattern in action.

## Page Object Reference

::: framework.pages.login_page.LoginPage

::: framework.pages.base_page.BasePage
