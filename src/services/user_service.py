from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException

from src.models.user import Usuario 
from src.schemas.user_schema import UserCreate
from src.models.area import AreaRiego
from src.models.predio import Predio, tabla_usuarios_predios
from src.core.security import create_access_token

async def get_users(db: AsyncSession) -> list[Usuario]:
    result = await db.execute(select(Usuario))
    return list(result.scalars().all())

async def get_user(db: AsyncSession, user_id: UUID) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> Usuario:
    db_user = Usuario(**user_in.model_dump()) 
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    db_user = await get_user(db, user_id)
    if not db_user: return False
    await db.delete(db_user)
    await db.commit()
    return True

async def get_user_areas(db: AsyncSession, user_id: UUID) -> list[AreaRiego]:
    stmt = (
        select(AreaRiego)
        .join(Predio, AreaRiego.id_predio == Predio.id_predio)
        .join(tabla_usuarios_predios, Predio.id_predio == tabla_usuarios_predios.c.id_predio)
        .where(tabla_usuarios_predios.c.id_usuario == user_id)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def login(db: AsyncSession, credenciales):
    result = await db.execute(
        select(Usuario).where(Usuario.email == credenciales["email"])
    )
    user = result.scalars().first()

    if not user or user.password != credenciales["password"]:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": str(user.id_usuario)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }