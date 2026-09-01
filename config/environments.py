from dataclasses import dataclass
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {"dev": "Dev", "stage": "Stage"}[self.value]


@dataclass
class UserCredentials:
    email: str
    password: str


# Минимум 2 пользователя для разных окружений
common_users = {
    "user": UserCredentials(email="user_scooter@test.ru", password="qwerty123"),
    "admin": UserCredentials(email="admin_scooter@test.ru", password="admin123"),
}


@dataclass
class EnvironmentConfig:
    url: str
    default_user: str

    def __str__(self):
        return f"- URL: {self.url}"


environments = {
    Environment.DEV: EnvironmentConfig(
        url="https://qa-scooter.praktikum-services.ru",
        default_user="admin"
    ),
    Environment.STAGE: EnvironmentConfig(
        url="https://qa-scooter.praktikum-services.ru",  # Здесь мог бы быть другой URL
        default_user="user"
    )
}


def print_environment_info(env_name, user_type=None):
    """Выводит краткую сводку по тестовому окружению."""
    env = Environment(env_name)
    config = environments[env]
    final_user_type = user_type or config.default_user

    print()
    print(f"Окружение:    {env.value.upper()}")
    print(f"URL:          {config.url}")

    if final_user_type:
        user = common_users.get(final_user_type)
        if user:
            print(f"Пользователь: {user.email}")
    print()
