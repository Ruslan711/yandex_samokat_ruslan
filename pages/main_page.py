# pages/main_page.py
import allure
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class MainPage(BasePage):
    PAGE_PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logo_yandex: Locator = self.page.locator(".Header_LogoYandex__3TSOI")
        self.logo_scooter: Locator = self.page.locator(".Header_LogoScooter__3lsAR")
        self.order_button_header: Locator = self.page.locator(".Header_Nav__AGCXC .Button_Button__ra12g")
        self.order_button_footer: Locator = self.page.locator(".Button_UltraBig__UU3Lp")
        self.faq_section: Locator = self.page.locator(".accordion")

    @allure.step("Открыть главную страницу")
    def open(self):
        """Открывает главную страницу Самоката."""
        super().open(self.PAGE_PATH)
        self.accept_cookies()

    @allure.step("Проверить, что открыта главная страница")
    def check_is_loaded(self):
        """Проверяет, что главная страница загрузилась."""
        expect(self.logo_scooter).to_be_visible()
        expect(self.faq_section).to_be_visible()

    @allure.step("Кликнуть на кнопку Заказать в шапке")
    def click_order_header(self):
        """Кликает по верхней кнопке Заказать."""
        self.order_button_header.click()

    @allure.step("Кликнуть на кнопку Заказать внизу страницы")
    def click_order_footer(self):
        """Кликает по нижней кнопке Заказать."""
        self.order_button_footer.scroll_into_view_if_needed()
        self.order_button_footer.click()

    @allure.step("Кликнуть на вопрос FAQ #{question_id}")
    def click_faq_question(self, question_id: int):
        """Кликает на стрелочку/вопрос по номеру."""
        question = self.page.locator(f"#accordion__heading-{question_id}")
        question.scroll_into_view_if_needed()
        question.click()

    @allure.step("Проверить текст ответа FAQ #{question_id}")
    def check_faq_answer(self, question_id: int, expected_text: str):
        """Проверяет, что открылся правильный текст ответа."""
        answer = self.page.locator(f"#accordion__panel-{question_id}")
        expect(answer).to_be_visible()
        expect(answer).to_have_text(expected_text)

    @allure.step("Кликнуть на логотип Самоката")
    def click_scooter_logo(self):
        """Кликает на логотип Самоката."""
        self.logo_scooter.click()

    @allure.step("Кликнуть на логотип Яндекса")
    def click_yandex_logo(self):
        """Кликает на логотип Яндекса (откроется в новом окне)."""
        self.logo_yandex.click()
