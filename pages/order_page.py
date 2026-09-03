# pages/order_page.py
from datetime import date

import allure
from playwright.sync_api import Locator, Page, expect

from data.order_data import COLOR_LABELS
from .base_page import BasePage


class OrderPage(BasePage):
    PAGE_PATH = "/order"

    def __init__(self, page: Page) -> None:
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
        # На /order кнопка «Заказать» в шапке тоже видна — берём последнюю (из формы)
        self.order_button: Locator = self.page.get_by_role("button", name="Заказать").last
        self.confirm_modal: Locator = self.page.get_by_text("Хотите оформить заказ?")
        self.confirm_button: Locator = self.page.locator("div").filter(
            has=self.page.get_by_text("Хотите оформить заказ?")
        ).get_by_role("button", name="Да")
        self.success_message: Locator = self.page.get_by_text("Заказ оформлен")

    @allure.step("Открыть страницу заказа")
    def open(self, path: str | None = None) -> None:
        """Открывает страницу оформления заказа."""
        super().open(path or self.PAGE_PATH)
        self.accept_cookies()

    @allure.step("Проверить, что открыта форма заказа")
    def check_is_loaded(self) -> None:
        """Проверяет, что форма заказа отображается."""
        expect(self.name_input).to_be_visible()
        expect(self.next_button).to_be_visible()

    @allure.step("Заполнить первую часть формы: имя, адрес, метро, телефон")
    def fill_personal_info(
        self,
        name: str,
        surname: str,
        address: str,
        metro: str,
        phone: str,
    ) -> None:
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
    def fill_rent_info(
        self,
        rent_days: str,
        color: str,
        comment: str,
        delivery_date: date,
        calendar_reference_date: date,
    ) -> None:
        """Заполняет данные об аренде на втором шаге."""
        if color not in COLOR_LABELS:
            raise ValueError(
                f"Неизвестный цвет: {color!r}. Допустимые значения: {list(COLOR_LABELS)}"
            )

        self.date_input.click()
        if (
            delivery_date.month != calendar_reference_date.month
            or delivery_date.year != calendar_reference_date.year
        ):
            self.page.locator(".react-datepicker__navigation--next").click()

        self.page.locator(
            f".react-datepicker__day--{delivery_date.day:03d}"
            f":not(.react-datepicker__day--outside-month)"
            f":not(.react-datepicker__day--disabled)"
        ).first.click()
        expect(self.date_input).not_to_have_value("")

        self.rent_dropdown.click()
        self.page.locator(".Dropdown-option").get_by_text(rent_days, exact=True).click()
        self.page.get_by_text(COLOR_LABELS[color]).click()
        self.comment_input.fill(comment)

    @allure.step("Подтвердить заказ")
    def confirm_order(self) -> None:
        """Нажимает Заказать и подтверждает в модалке."""
        self.order_button.scroll_into_view_if_needed()
        self.order_button.click()
        expect(self.confirm_modal).to_be_visible()
        self.confirm_button.click()

    @allure.step("Проверить, что заказ оформлен")
    def check_order_success(self) -> None:
        """Проверяет появление окна с текстом об успешном заказе."""
        expect(self.success_message).to_be_visible()
