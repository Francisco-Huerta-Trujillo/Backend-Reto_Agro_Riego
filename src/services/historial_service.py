from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.historial import HistorialCambios
from src.schemas.historial_schema import HistorialCreate

class HistorialService:
    # ------------------ CREATE ------------------
    @staticmethod
    async def create(db: AsyncSession, historial_in: HistorialCreate) -> HistorialCambios:
        db_historial = HistorialCambios(**historial_in.model_dump())
        db.add(db_historial)
        await db.commit()
        await db.refresh(db_historial)
        return db_historial

    # ------------------ READ (Solo lectura) ------------------
    @staticmethod
    async def get_all(db: AsyncSession, limite: int = 50) -> list[HistorialCambios]:
        # Traemos los últimos 50 cambios del sistema ordenados por el más reciente
        stmt = select(HistorialCambios).order_by(HistorialCambios.fecha.desc()).limit(limite)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_usuario(db: AsyncSession, id_usuario: UUID) -> list[HistorialCambios]:
        # Para ver qué ha hecho un usuario en específico
        stmt = select(HistorialCambios).where(HistorialCambios.id_usuario == id_usuario).order_by(HistorialCambios.fecha.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())