from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL - configure for PostgreSQL or SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./ecommerce.db")
# For PostgreSQL: "postgresql+asyncpg://user:password@localhost/ecommerce"

engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
