from playwright.sync_api import Page
from pages.main_page import MainPage
from pages.order_page import OrderPage
# Сюда мы будем добавлять импорты для новых страниц


class Application:
    def __init__(self, page: Page):
        self.page = page

        # Инициализируем все наши Page Objects здесь
        self.main_page = MainPage(self.page)
        self.order_page = OrderPage(self.page)
