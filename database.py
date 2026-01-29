from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Pega a URL do banco da variável de ambiente ou usa SQLite em memória como fallback seguro
db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

# Correção específica para Vercel/SQLAlchemy (postgres:// -> postgresql://)
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Se for SQLite local (teste), garante que usa o driver assíncrono
if db_url.startswith("sqlite") and "aiosqlite" not in db_url:
    db_url = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(db_url, echo=True)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
