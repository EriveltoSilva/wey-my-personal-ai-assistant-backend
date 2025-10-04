"""Database connection and session management."""

import ssl

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings

engine = None

if settings.DEBUG:
    DATABASE_URL = settings.DATABASE_DEV_URL
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,  # Set to True to enable SQL logs
        pool_size=20,  # Increase pool size for better performance
        max_overflow=30,  # Allow overflow connections
        pool_pre_ping=True,  # Validate connections
        pool_recycle=3600,  # Recycle connections every hour
    )
else:
    DATABASE_URL = settings.DATABASE_PROD_URL.replace("?sslmode=require", "")
    ssl_context = ssl.create_default_context()
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"ssl": ssl_context},  # secure connection to PostgreSQL
        future=True,
        echo=True,  # Enable SQL logs in production
        pool_size=20,  # Increase pool size for better performance
        max_overflow=30,  # Allow overflow connections
        pool_pre_ping=True,  # Validate connections
        pool_recycle=3600,  # Recycle connections every hour
    )


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


async def create_and_seed_database(seed: bool):
    """Initialize the database."""
    if not seed:
        return

    import src.core.models_list
    from src.core.database.seeds import create_root_user, seed_interests_and_professional_areas

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Apenas se desejar recriar o banco (DROPAR TUDO!)
        await conn.run_sync(Base.metadata.create_all)

    # Criar dados iniciais
    await create_root_user()
    await seed_interests_and_professional_areas()

    await engine.dispose()


# Dependency injection para FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
