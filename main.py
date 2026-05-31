import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.db_helper import get_db_session

from db.models import Theme, Question, Answer


async def create_test_data(session: AsyncSession):
    # Загрузка данных из JSON
    data_path = Path("mocs/questions_data.json")
    if not data_path.exists():
        print(f"Файл {data_path} не найден.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for theme_data in data:
        # Проверка существования темы
        result = await session.execute(select(Theme).where(Theme.name == theme_data["theme"]))
        theme = result.scalars().first()

        if not theme:
            theme = Theme(name=theme_data["theme"])
            session.add(theme)
            await session.flush()

        for q_data in theme_data["questions"]:
            # Проверка существования вопроса
            result = await session.execute(
                select(Question).where(Question.question == q_data["question"])
            )
            question = result.scalars().first()

            if not question:
                question = Question(question=q_data["question"], theme=theme)
                session.add(question)
                await session.flush()

            for a_data in q_data["answers"]:
                # Проверка существования ответа
                result = await session.execute(
                    select(Answer).where(
                        Answer.text == a_data["text"], Answer.question_id == question.id
                    )
                )
                answer = result.scalars().first()

                if not answer:
                    answer = Answer(
                        text=a_data["text"],
                        is_true=a_data["is_true"],
                        question=question,
                    )
                    session.add(answer)

    await session.commit()
    print("Тестовые данные успешно добавлены.")


async def select_questions_by_theme(session: AsyncSession, theme_id: int):
    # Загружаем тему с вопросами и ответами за один запрос, избегая lazy loading
    result = await session.execute(
        select(Theme)
        .where(Theme.id == theme_id)
        .options(joinedload(Theme.questions).joinedload(Question.answers))
    )
    theme = result.scalars().first()

    if not theme:
        print(f"Тема с ID {theme_id} не найдена.")
        return

    print(f"\nТема: {theme.name}")
    print("Вопросы:")

    for question in theme.questions:
        print(f"  - {question.question}")
        print("    Ответы:")
        for answer in question.answers:
            status = "Правильный" if answer.is_true else "Неправильный"
            print(f"    \t- {answer.text} ({status})")


async def main():
    # Работа с сессией для создания данных и выборки
    async with get_db_session() as session:
        try:
            # Заполнение базы данных тестовыми данными
            # await create_test_data(session)

            # Коммит изменений
            await session.commit()

            # Очистка сессии для свежей выборки
            await session.flush()
            session.expunge_all()

            # Выборка вопросов по ID темы (например, 1)
            await select_questions_by_theme(session, theme_id=1)

            # Повторная выборка по другой теме (например, 2)
            await select_questions_by_theme(session, theme_id=2)

        except Exception as e:
            await session.rollback()
            print(f"Ошибка при работе с базой данных: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
