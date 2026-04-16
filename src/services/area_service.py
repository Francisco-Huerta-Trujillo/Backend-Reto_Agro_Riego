from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.area import AreaRiego
from src.schemas.area_schema import AreaCreate, AreaUpdate

class AreaService:
    @staticmethod
    async def create(db: AsyncSession, area_in: AreaCreate) -> AreaRiego:
        db_area = AreaRiego(**area_in.model_dump())
        db.add(db_area)
        await db.commit()
        await db.refresh(db_area)
        return db_area

    @staticmethod
    async def get_by_id(db: AsyncSession, area_id: UUID) -> AreaRiego | None:
        result = await db.execute(select(AreaRiego).where(AreaRiego.id_areariego == area_id))
        return result.scalars().first()

    @staticmethod
    async def get_all_by_predio(db: AsyncSession, predio_id: UUID) -> list[AreaRiego]:
        # Para el Frontend: Traer todas las áreas de una granja específica
        result = await db.execute(select(AreaRiego).where(AreaRiego.id_predio == predio_id))
        return list(result.scalars().all())

    @staticmethod
    async def update(db: AsyncSession, area_id: UUID, area_in: AreaUpdate) -> AreaRiego | None:
        db_area = await AreaService.get_by_id(db, area_id)
        if not db_area: return None
        
        update_data = area_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_area, key, value)
            
        await db.commit()
        await db.refresh(db_area)
        return db_area

    @staticmethod
    async def delete(db: AsyncSession, area_id: UUID) -> bool:
        db_area = await AreaService.get_by_id(db, area_id)
        if not db_area: return False
        await db.delete(db_area)
        await db.commit()
        return True