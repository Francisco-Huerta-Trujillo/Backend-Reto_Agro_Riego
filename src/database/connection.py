import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

# 1. Agregamos override=True para obligarlo a leer el .env fresco
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")


# Creamos el Motor ASÍNCRONO
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()