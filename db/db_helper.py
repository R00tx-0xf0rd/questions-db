from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

# Создание асинхронного движка
engine = create_async_engine(url=settings.db_url)

# Создание фабрики асинхронных сессий
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db_session() -> AsyncSession:
    """Получение сессии базы данных."""
    return async_session()
