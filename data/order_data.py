# data/order_data.py
from typing import TypedDict

COLOR_LABELS: dict[str, str] = {
    "black": "чёрный жемчуг",
    "grey": "серая безысходность",
}

ORDER_BUTTONS: list[str] = ["header", "footer"]


class OrderData(TypedDict):
    name: str
    surname: str
    address: str
    metro: str
    phone: str
    rent_days: str
    color: str
    comment: str


ORDER_DATA: list[OrderData] = [
    {
        "name": "Иван",
        "surname": "Петров",
        "address": "ул. Ленина, 10",
        "metro": "Сокольники",
        "phone": "89001234567",
        "rent_days": "сутки",
        "color": "black",
        "comment": "Позвонить за час",
    },
    {
        "name": "Мария",
        "surname": "Смирнова",
        "address": "ул. Пушкина, 5",
        "metro": "Лубянка",
        "phone": "89109876543",
        "rent_days": "семеро суток",
        "color": "grey",
        "comment": "Оставить у двери",
    },
]
