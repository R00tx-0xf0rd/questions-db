import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем корень проекта в sys.path для корректного импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from db.db_helper import get_db_session


@pytest.fixture(scope="session")
def event_loop():
    """Переопределяем фикстуру event_loop для работы с pytest-asyncio."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def setup_database():
    """Предполагается, что схема базы данных уже создана Alembic миграциями."""
    yield


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для получения сессии базы данных."""
    async with get_db_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
