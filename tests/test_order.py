# tests/test_order.py
import pytest
import allure
from config.application import Application
from data.order_data import ORDER_DATA


@allure.feature("Оформление заказа самоката")
class TestOrder:

    @pytest.mark.smoke
    @pytest.mark.parametrize("order", ORDER_DATA)
    @allure.title("Успешный заказ самоката через кнопку {order[button]}")
    def test_create_order(self, app: Application, order):
        with allure.step("Открыть главную страницу"):
            app.main_page.open()

        with allure.step(f"Кликнуть кнопку Заказать ({order['button']})"):
            if order["button"] == "header":
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
            app.order_page.fill_rent_info(
                rent_days=order["rent_days"],
                color=order["color"],
                comment=order["comment"],
            )

        with allure.step("Подтвердить заказ"):
            app.order_page.confirm_order()

        with allure.step("Проверить окно 'Заказ оформлен'"):
            app.order_page.check_order_success()
