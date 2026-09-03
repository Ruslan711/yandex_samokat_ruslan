# tests/test_faq.py
import allure
import pytest

from config.application import Application
from data.faq_data import FAQ_DATA


@allure.feature("Раздел Вопросы о важном")
class TestFAQ:

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "question_id, expected_answer",
        FAQ_DATA,
        ids=[f"question_{question_id}" for question_id, _ in FAQ_DATA],
    )
    @allure.title("Проверка ответа на вопрос FAQ #{question_id}")
    def test_faq_answer(
        self,
        app: Application,
        question_id: int,
        expected_answer: str,
    ) -> None:
        with allure.step("Открыть главную страницу"):
            app.main_page.open()

        with allure.step(f"Кликнуть на вопрос номер {question_id}"):
            app.main_page.click_faq_question(question_id)

        with allure.step("Проверить текст ответа"):
            app.main_page.check_faq_answer(question_id, expected_answer)
