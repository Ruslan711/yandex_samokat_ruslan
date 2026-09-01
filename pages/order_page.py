# pages/order_page.py
from datetime import datetime, timedelta
import allure
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class OrderPage(BasePage):
    PAGE_PATH = "/order"

    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input: Locator = self.page.get_by_placeholder("* Имя")
        self.surname_input: Locator = self.page.get_by_placeholder("* Фамилия")
        self.address_input: Locator = self.page.get_by_placeholder("* Адрес: куда привезти заказ")
        self.metro_input: Locator = self.page.get_by_placeholder("* Станция метро")
        self.phone_input: Locator = self.page.get_by_placeholder("* Телефон: на него позвонит курьер")
        self.next_button: Locator = self.page.get_by_role("button", name="Далее")

        self.date_input: Locator = self.page.get_by_placeholder("* Когда привезти самокат")
        self.rent_dropdown: Locator = self.page.locator(".Dropdown-control")
        self.comment_input: Locator = self.page.get_by_placeholder("Комментарий для курьера")
        self.order_button: Locator = self.page.locator(
            "button.Button_Middle__1CSJM", has_text="Заказать"
        )
        # Кнопка Да именно в модалке (не путать с кнопками формы)
        self.confirm_button: Locator = self.page.locator(
            ".Order_Modal__YZ-d3"
        ).get_by_role("button", name="Да")
        self.success_modal: Locator = self.page.locator(".Order_ModalHeader__3FDaJ")

    @allure.step("Открыть страницу заказа")
    def open(self):
        """Открывает страницу оформления заказа."""
        super().open(self.PAGE_PATH)
        self.accept_cookies()

    @allure.step("Проверить, что открыта форма заказа")
    def check_is_loaded(self):
        """Проверяет, что форма заказа отображается."""
        expect(self.name_input).to_be_visible()
        expect(self.next_button).to_be_visible()

    @allure.step("Заполнить первую часть формы: имя, адрес, метро, телефон")
    def fill_personal_info(self, name: str, surname: str, address: str, metro: str, phone: str):
        """Заполняет данные о пользователе на первом шаге."""
        self.name_input.fill(name)
        self.surname_input.fill(surname)
        self.address_input.fill(address)

        self.metro_input.click()
        self.page.locator(".select-search__option").get_by_text(metro, exact=True).click()

        self.phone_input.fill(phone)
        self.next_button.click()
        expect(self.date_input).to_be_visible()

    @allure.step("Заполнить вторую часть формы: дата, срок, цвет, комментарий")
    def fill_rent_info(self, rent_days: str, color: str, comment: str):
        """Заполняет данные об аренде на втором шаге."""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        self.date_input.click()
        if tomorrow.month != today.month or tomorrow.year != today.year:
            self.page.locator(".react-datepicker__navigation--next").click()

        self.page.locator(
            f".react-datepicker__day--{tomorrow.day:03d}"
            f":not(.react-datepicker__day--outside-month)"
            f":not(.react-datepicker__day--disabled)"
        ).first.click()
        expect(self.date_input).not_to_have_value("")

        self.rent_dropdown.click()
        self.page.locator(".Dropdown-option").get_by_text(rent_days, exact=True).click()

        if color == "black":
            self.page.get_by_text("чёрный жемчуг").click()
        elif color == "grey":
            self.page.get_by_text("серая безысходность").click()

        self.comment_input.fill(comment)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        """Нажимает Заказать и подтверждает в модалке."""
        self.order_button.scroll_into_view_if_needed()
        self.order_button.click()
        expect(self.success_modal).to_contain_text("Хотите оформить заказ?")
        self.confirm_button.click()

    @allure.step("Проверить, что заказ оформлен")
    def check_order_success(self):
        """Проверяет появление окна с текстом об успешном заказе."""
        expect(self.success_modal).to_contain_text("Заказ оформлен", timeout=15000)
