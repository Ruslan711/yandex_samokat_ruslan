from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

# Стенд Самоката — Москва; фиксируем TZ, чтобы CI в UTC не ломал «завтра».
ORDER_TIMEZONE = ZoneInfo("Europe/Moscow")


def get_delivery_dates(days_ahead: int = 1) -> tuple[date, date]:
    """Возвращает (сегодня, дата доставки) в часовом поясе стенда."""
    today = datetime.now(ORDER_TIMEZONE).date()
    delivery_date = today + timedelta(days=days_ahead)
    return today, delivery_date
