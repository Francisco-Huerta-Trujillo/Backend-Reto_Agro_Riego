from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from src.models.mediciones import Medicion
from src.schemas.mediciones_schema import MedicionCreate

class MedicionService:
    # ------------------ CREATE (Ingesta IoT) ------------------
    @staticmethod
    async def create(db: AsyncSession, medicion_in: MedicionCreate) -> Medicion:
        db_medicion = Medicion(**medicion_in.model_dump())
        db.add(db_medicion)
        await db.commit()
        await db.refresh(db_medicion)
        return db_medicion

    # ------------------ READ (Para las Gráficas de React) ------------------
    # En lugar de un 'get_all' que colapsaría el servidor trayendo 1 millón de filas,
    # hacemos un método inteligente para las gráficas.
    @staticmethod
    async def get_historial_por_area(
        db: AsyncSession, 
        area_id: UUID, 
        limite: int = 100
    ) -> list[Medicion]:
        """
        Devuelve las últimas N mediciones de un área específica para graficar.
        Gracias al índice que creamos en SQL, esto será instantáneo.
        """
        stmt = (
            select(Medicion)
            .where(Medicion.id_areariego == area_id)
            .order_by(Medicion.fecha.desc())
            .limit(limite)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())