# pages/base_page.py
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, path: str = "/") -> None:
        """Открывает страницу по указанному пути."""
        self.page.goto(path)

    def check_url_is(self, url: str) -> None:
        """Проверяет, что текущий URL точно совпадает с ожидаемым."""
        expect(self.page).to_have_url(url)

    def accept_cookies(self) -> None:
        """Закрывает баннер с куки, если он появится."""
        cookie_button = self.page.get_by_role("button", name="да все привыкли")
        try:
            expect(cookie_button).to_be_visible(timeout=3000)
        except AssertionError:
            return
        cookie_button.click()
