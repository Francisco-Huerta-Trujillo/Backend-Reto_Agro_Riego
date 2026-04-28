from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.models.user import Usuario 
from src.schemas.user_schema import UserCreate
from src.models.area import AreaRiego
from src.models.predio import Predio
from src.models.associations import usuarios_predios
from src.core.security import create_access_token, hash_password, verify_password

async def get_users(db: AsyncSession) -> list[Usuario]:
    result = await db.execute(select(Usuario))
    return list(result.scalars().all())

async def get_user(db: AsyncSession, user_id: UUID) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> Usuario:
    user_data = user_in.model_dump()
    user_data["contrasena"] = hash_password(user_data["contrasena"])
    db_user = Usuario(**user_data)
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
        .join(usuarios_predios, Predio.id_predio == usuarios_predios.c.id_predio)
        .where(usuarios_predios.c.id_usuario == user_id)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def login(db: AsyncSession, credenciales: OAuth2PasswordRequestForm):
    email_ingresado = credenciales.username
    password_ingresado = credenciales.password

    result = await db.execute(
        select(Usuario).where(Usuario.email == email_ingresado)
    )
    user = result.scalars().first()

    if not user or not verify_password(password_ingresado, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token_data = {
        "sub": str(user.id_usuario),
        "role" : user.rol
    }
    token = create_access_token(token_data)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user" : {
            "id" : str(user.id_usuario),
            "email" : user.email,
            "rol" : user.rol
         }
    }