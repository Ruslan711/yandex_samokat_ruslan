# pages/base_page.py
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str = "/"):
        """Открывает страницу по указанному пути."""
        self.page.goto(path)

    def check_url_contains(self, path: str):
        """Проверяет, что текущий URL содержит указанный путь."""
        expect(self.page).to_have_url(path)

    def accept_cookies(self):
        """Закрывает баннер с куки, если он есть."""
        cookie_button = self.page.locator(".App_CookieButton__3cvqF")
        if cookie_button.is_visible():
            cookie_button.click()
