# conftest.py
from __future__ import annotations

from typing import Any, cast

import allure
import pytest
from _pytest.python import Function
from playwright.sync_api import Page

from config.application import Application
from config.environments import (
    Environment,
    EnvironmentConfig,
    environments,
    print_environment_info,
)

CHROMIUM_ORDER_BUG_REASON = (
    "Баг учебного стенда: в Chromium не работает кнопка «Да» в модалке заказа "
    "(на фронте проверка browser.name === 'chrome'). Баг нужно завести в Jira."
)

# ============================================================
#
#   Хуки Pytest (Настройка и отчетность)
#
# ============================================================


def pytest_addoption(parser: pytest.Parser) -> None:
    """Добавляем опцию для выбора окружения."""
    parser.addoption(
        "--env",
        default="dev",
        choices=[environment.value for environment in Environment],
        help="Выберите окружение: dev или stage",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Выводит информацию о тестовом окружении перед запуском."""
    env_name = config.getoption("--env")
    print_environment_info(env_name)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Помечает order-тесты как xfail в Chromium — баг стенда, а не скрытие через user-agent."""
    chromium_order_bug = pytest.mark.xfail(
        reason=CHROMIUM_ORDER_BUG_REASON,
        strict=False,
    )
    for item in items:
        test_name = getattr(item, "originalname", item.name)
        if test_name != "test_create_order":
            continue
        if "chromium" in item.nodeid.lower():
            item.add_marker(chromium_order_bug)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Any:
    """Создает скриншот в Allure при падении теста."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        try:
            test_item = cast(Function, item)
            page = cast(Page, test_item.funcargs["page"])
            allure.attach(
                page.screenshot(full_page=True),
                name=f"screenshot_{item.nodeid}",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as error:
            print(f"Не удалось сделать скриншот: {error}")


# ============================================================
#
#   Базовые фикстуры фреймворка (Браузер и Приложение)
#
# ============================================================


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, Any],
    env_config: EnvironmentConfig,
) -> dict[str, Any]:
    """Настраивает контекст браузера (URL и игнор HTTPS-ошибок)."""
    return {
        **browser_context_args,
        "base_url": env_config.url,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    """Основная фикстура, предоставляющая точку входа ко всем страницам."""
    return Application(page)


# ============================================================
#
#   Фикстуры конфигурации и данных
#
# ============================================================


@pytest.fixture(scope="session")
def env_config(request: pytest.FixtureRequest) -> EnvironmentConfig:
    """Предоставляет конфигурацию окружения (URL стенда)."""
    env_name = request.config.getoption("--env")
    return environments[Environment(env_name)]
