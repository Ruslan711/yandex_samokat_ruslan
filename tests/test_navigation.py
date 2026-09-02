# tests/test_navigation.py
import re

import allure
import pytest
from playwright.sync_api import expect

from config.application import Application
from config.environments import EnvironmentConfig


@allure.feature("Навигация по логотипам")
class TestNavigation:

    @pytest.mark.smoke
    @allure.title("Клик по логотипу Самоката открывает главную страницу")
    def test_scooter_logo_opens_main_page(
        self,
        app: Application,
        env_config: EnvironmentConfig,
    ) -> None:
        main_page_url = f"{env_config.url.rstrip('/')}/"

        with allure.step("Открыть страницу заказа"):
            app.order_page.open()

        with allure.step("Кликнуть на логотип Самоката"):
            app.main_page.click_scooter_logo()

        with allure.step("Проверить, что открылась главная в том же окне"):
            app.main_page.check_is_loaded()
            app.main_page.check_url_is(main_page_url)

    @pytest.mark.regression
    @allure.title("Клик по логотипу Яндекса открывает dzen/yandex в новом окне")
    def test_yandex_logo_opens_new_tab(self, app: Application) -> None:
        with allure.step("Открыть главную страницу"):
            app.main_page.open()

        with allure.step("Кликнуть на логотип Яндекса и дождаться нового окна"):
            with app.page.expect_popup() as popup_info:
                app.main_page.click_yandex_logo()
            new_page = popup_info.value

        with allure.step("Проверить URL нового окна"):
            new_page.wait_for_load_state()
            expect(new_page).to_have_url(re.compile(r".*(yandex|dzen).*"))
