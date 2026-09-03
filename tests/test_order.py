# tests/test_order.py
import pytest
import allure
from config.application import Application
from data.delivery_date import get_delivery_dates
from data.order_data import ORDER_BUTTONS, ORDER_DATA, OrderData


@allure.feature("Оформление заказа самоката")
class TestOrder:

    @pytest.mark.smoke
    @pytest.mark.parametrize("order_button", ORDER_BUTTONS)
    @pytest.mark.parametrize("order", ORDER_DATA)
    @allure.title("Успешный заказ самоката через кнопку {order_button}")
    def test_create_order(
        self,
        app: Application,
        order_button: str,
        order: OrderData,
    ) -> None:
        with allure.step("Открыть главную страницу"):
            app.main_page.open()

        with allure.step(f"Кликнуть кнопку Заказать ({order_button})"):
            if order_button == "header":
                app.main_page.click_order_header()
            else:
                app.main_page.click_order_footer()

        with allure.step("Проверить, что открылась форма заказа"):
            app.order_page.check_is_loaded()

        with allure.step("Заполнить данные пользователя"):
            app.order_page.fill_personal_info(
                name=order["name"],
                surname=order["surname"],
                address=order["address"],
                metro=order["metro"],
                phone=order["phone"],
            )

        with allure.step("Заполнить данные аренды"):
            today, delivery_date = get_delivery_dates()
            app.order_page.fill_rent_info(
                rent_days=order["rent_days"],
                color=order["color"],
                comment=order["comment"],
                delivery_date=delivery_date,
                calendar_reference_date=today,
            )

        with allure.step("Подтвердить заказ"):
            app.order_page.confirm_order()

        with allure.step("Проверить окно 'Заказ оформлен'"):
            app.order_page.check_order_success()
