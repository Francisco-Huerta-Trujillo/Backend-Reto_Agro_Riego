from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database.connection import get_db
from src.schemas.user_schema import UserCreate, UserResponse, UserLogin
from src.services.user_service import (
    login, get_users, get_user, create_user, delete_user, get_user_areas
)
from src.schemas.area_schema import AreaResponse
from src.core.security import get_current_user

router = APIRouter()

@router.post("/login")
async def login_user(credenciales: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login(db, credenciales)

@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    return await get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: UUID, db: AsyncSession = Depends(get_db)):
    exito = await delete_user(db, user_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado exitosamente"}

@router.get("/{user_id}/areas", response_model=List[AreaResponse])
async def read_user_areas(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_user_areas(db, user_id)