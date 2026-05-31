import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from db import (
    create_answer,
    create_question,
    create_theme,
    get_answer_by_id,
    get_question_by_id,
    get_questions_by_theme_id,
    get_theme_by_id,
    get_theme_by_name,
)


@pytest.mark.asyncio
async def test_create_and_get_theme(db_session: AsyncSession):
    """Тест создания и получения темы."""
    # Создаем тему
    theme = await create_theme(db_session, "Python1")
    assert theme.id is not None
    assert theme.name == "Python1"

    # Получаем по ID
    retrieved_theme = await get_theme_by_id(db_session, theme.id)
    assert retrieved_theme is not None
    assert retrieved_theme.name == "Python1"

    # Получаем по имени
    retrieved_by_name = await get_theme_by_name(db_session, "Python1")
    assert retrieved_by_name is not None
    assert retrieved_by_name.id == theme.id


@pytest.mark.asyncio
async def test_create_and_get_question(db_session: AsyncSession):
    """Тест создания и получения вопроса."""
    # Сначала создаем тему
    theme = await create_theme(db_session, "SQLAlchemy3")

    # Создаем вопрос
    question = await create_question(
        db_session, "Что такое DeclarativeBase?3", theme.id
    )
    assert question.id is not None
    assert question.question == "Что такое DeclarativeBase?3"
    assert question.theme_id == theme.id

    # Получаем по ID
    retrieved_question = await get_question_by_id(db_session, question.id)
    assert retrieved_question is not None
    assert retrieved_question.question == "Что такое DeclarativeBase?3"


@pytest.mark.asyncio
async def test_get_questions_by_theme_id(db_session: AsyncSession):
    """Тест получения вопросов по ID темы."""
    # Создаем тему и вопросы
    theme = await create_theme(db_session, "Testing3")
    q1 = await create_question(db_session, "Тест 1", theme.id)
    q2 = await create_question(db_session, "Тест 2", theme.id)

    # Получаем вопросы по ID темы
    questions = await get_questions_by_theme_id(db_session, theme.id)
    assert len(questions) == 2
    assert {q.id for q in questions} == {q1.id, q2.id}



@pytest.mark.asyncio
async def test_create_and_get_answer(db_session: AsyncSession):
    """Тест создания и получения ответа."""
    # Создаем тему и вопрос
    theme = await create_theme(db_session, "Async3")
    question = await create_question(db_session, "Как работает async?3", theme.id)

    # Создаем ответ
    answer = await create_answer(db_session, "С помощью event loop3", True, question.id)
    assert answer.id is not None
    assert answer.text == "С помощью event loop3"
    assert answer.is_true is True
    assert answer.question_id == question.id

    # Получаем по ID
    retrieved_answer = await get_answer_by_id(db_session, answer.id)
    assert retrieved_answer is not None
    assert retrieved_answer.text == "С помощью event loop3"
