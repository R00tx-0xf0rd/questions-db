from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models import Theme, Question, Answer


# --- CRUD для Theme ---


async def create_theme(session: AsyncSession, name: str) -> Theme:
    """Создание новой темы."""
    theme = Theme(name=name)
    session.add(theme)
    await session.flush()
    return theme


async def get_theme_by_id(session: AsyncSession, theme_id: int) -> Theme | None:
    """Получение темы по ID."""
    result = await session.execute(select(Theme).where(Theme.id == theme_id))
    return result.scalars().first()


async def get_theme_by_name(session: AsyncSession, name: str) -> Theme | None:
    """Получение темы по имени."""
    result = await session.execute(select(Theme).where(Theme.name == name))
    return result.scalars().first()


async def get_all_themes(session: AsyncSession) -> list[Theme]:
    """Получение всех тем."""
    result = await session.execute(select(Theme))
    return list(result.unique().scalars().all())


# --- CRUD для Question ---


async def create_question(session: AsyncSession, question_text: str, theme_id: int) -> Question:
    """Создание нового вопроса."""
    question = Question(question=question_text, theme_id=theme_id)
    session.add(question)
    await session.flush()
    return question


async def get_question_by_id(session: AsyncSession, question_id: int) -> Question | None:
    """Получение вопроса по ID."""
    result = await session.execute(
        select(Question).where(Question.id == question_id).options(joinedload(Question.answers))
    )
    return result.scalars().first()


async def get_questions_by_theme_id(session: AsyncSession, theme_id: int) -> list[Question]:
    """Получение всех вопросов по ID темы."""
    result = await session.execute(
        select(Question).where(Question.theme_id == theme_id).options(joinedload(Question.answers))
    )
    return list(result.unique().scalars().all())


# --- CRUD для Answer ---


async def create_answer(
    session: AsyncSession, text: str, is_true: bool, question_id: int
) -> Answer:
    """Создание нового ответа."""
    answer = Answer(text=text, is_true=is_true, question_id=question_id)
    session.add(answer)
    await session.flush()
    return answer


async def get_answer_by_id(session: AsyncSession, answer_id: int) -> Answer | None:
    """Получение ответа по ID."""
    result = await session.execute(select(Answer).where(Answer.id == answer_id))
    return result.scalars().first()
