from playwright.sync_api import Page

from pages.main_page import MainPage
from pages.order_page import OrderPage


class Application:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.main_page = MainPage(self.page)
        self.order_page = OrderPage(self.page)
