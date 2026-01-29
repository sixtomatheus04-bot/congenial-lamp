from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# CONFIGURAÇÃO INTELIGENTE DO BANCO
# 1. Tenta pegar a URL do Postgres da Vercel
db_url = os.getenv("DATABASE_URL")

# 2. Se não tiver Postgres configurado, usa memória RAM (SQLite temporário)
# Isso evita o erro de "Read-only file system"
if not db_url:
    db_url = "sqlite+aiosqlite:///:memory:"

# 3. Correção para incompatibilidade do driver Postgres na Vercel
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Cria o motor do banco
engine = create_async_engine(db_url, echo=True)

async def create_db_and_tables():
    # Cria as tabelas
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
