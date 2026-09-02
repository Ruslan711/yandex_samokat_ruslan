from dataclasses import dataclass
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self) -> str:
        return {"dev": "Dev", "stage": "Stage"}[self.value]


@dataclass
class EnvironmentConfig:
    url: str

    def __str__(self) -> str:
        return f"- URL: {self.url}"


# На учебном стенде один URL. На реальном проекте DEV и STAGE отличаются адресом стенда.
environments: dict[Environment, EnvironmentConfig] = {
    Environment.DEV: EnvironmentConfig(
        url="https://qa-scooter.praktikum-services.ru",
    ),
    Environment.STAGE: EnvironmentConfig(
        url="https://qa-scooter.praktikum-services.ru",
    ),
}


def print_environment_info(env_name: str) -> None:
    """Выводит краткую сводку по тестовому окружению."""
    env = Environment(env_name)
    config = environments[env]

    print()
    print(f"Окружение:    {env.value.upper()}")
    print(f"URL:          {config.url}")
    print()
