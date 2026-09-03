# pages/main_page.py
import allure
from playwright.sync_api import Locator, Page, expect

from .base_page import BasePage


class MainPage(BasePage):
    PAGE_PATH = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.logo_yandex: Locator = self.page.get_by_role("link", name="Yandex")
        self.logo_scooter: Locator = self.page.get_by_role("link", name="Scooter")
        self.order_button_header: Locator = self.page.get_by_role("button", name="Заказать").first
        self.faq_section: Locator = self.page.get_by_text("Вопросы о важном")

    @allure.step("Открыть главную страницу")
    def open(self, path: str | None = None) -> None:
        """Открывает главную страницу Самоката."""
        super().open(path or self.PAGE_PATH)
        self.accept_cookies()

    @allure.step("Проверить, что открыта главная страница")
    def check_is_loaded(self) -> None:
        """Проверяет, что главная страница загрузилась."""
        expect(self.logo_scooter).to_be_visible()
        expect(self.faq_section).to_be_visible()

    @allure.step("Кликнуть на кнопку Заказать в шапке")
    def click_order_header(self) -> None:
        """Кликает по верхней кнопке Заказать."""
        self.accept_cookies()
        self.order_button_header.click()
        expect(self.page.get_by_placeholder("* Имя")).to_be_visible()

    @allure.step("Кликнуть на кнопку Заказать внизу страницы")
    def click_order_footer(self) -> None:
        """Кликает по нижней кнопке Заказать (перед блоком FAQ)."""
        self.accept_cookies()
        self.page.get_by_text("Когда аренда заканчивается").scroll_into_view_if_needed()
        footer_button = self.page.get_by_role("button", name="Заказать").nth(1)
        footer_button.scroll_into_view_if_needed()
        footer_button.click()
        expect(self.page.get_by_placeholder("* Имя")).to_be_visible()

    @allure.step("Кликнуть на вопрос FAQ #{question_id}")
    def click_faq_question(self, question_id: int) -> None:
        """Кликает на стрелочку/вопрос по номеру."""
        question = self.page.locator(f"#accordion__heading-{question_id}")
        question.scroll_into_view_if_needed()
        question.click()

    @allure.step("Проверить текст ответа FAQ #{question_id}")
    def check_faq_answer(self, question_id: int, expected_text: str) -> None:
        """Проверяет, что открылся правильный текст ответа."""
        answer = self.page.locator(f"#accordion__panel-{question_id}")
        expect(answer).to_be_visible()
        expect(answer).to_have_text(expected_text)

    @allure.step("Кликнуть на логотип Самоката")
    def click_scooter_logo(self) -> None:
        """Кликает на логотип Самоката."""
        self.logo_scooter.click()

    @allure.step("Кликнуть на логотип Яндекса")
    def click_yandex_logo(self) -> None:
        """Кликает на логотип Яндекса (откроется в новом окне)."""
        self.accept_cookies()
        self.logo_yandex.click()
