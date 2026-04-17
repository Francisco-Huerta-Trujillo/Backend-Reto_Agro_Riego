from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from uuid import UUID

from src.models.predio import Predio, tabla_usuarios_predios
from src.schemas.predio_schema import PredioCreate, PredioUpdate

async def get_predios(db: AsyncSession) -> list[Predio]:
    result = await db.execute(select(Predio))
    return list(result.scalars().all())

async def get_predio(db: AsyncSession, predio_id: UUID) -> Predio | None:
    result = await db.execute(select(Predio).where(Predio.id_predio == predio_id))
    return result.scalars().first()

async def create_predio(db: AsyncSession, predio_in: PredioCreate) -> Predio:
    db_predio = Predio(**predio_in.model_dump())
    db.add(db_predio)
    await db.commit()
    await db.refresh(db_predio)
    return db_predio

async def update_predio(db: AsyncSession, predio_id: UUID, predio_in: PredioUpdate) -> Predio | None:
    db_predio = await get_predio(db, predio_id)
    if not db_predio: return None
    update_data = predio_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_predio, key, value)
    await db.commit()
    await db.refresh(db_predio)
    return db_predio

async def delete_predio(db: AsyncSession, predio_id: UUID) -> bool:
    db_predio = await get_predio(db, predio_id)
    if not db_predio: return False
    await db.delete(db_predio)
    await db.commit()
    return True

async def get_predio_areas(db: AsyncSession, predio_id: UUID):
    # Esto deberá devolver las áreas del predio
    from src.models.area import AreaRiego
    result = await db.execute(select(AreaRiego).where(AreaRiego.id_predio == predio_id))
    return list(result.scalars().all())

async def asignar_usuario(db: AsyncSession, id_predio: UUID, id_usuario: UUID) -> bool:
    stmt = insert(tabla_usuarios_predios).values(id_usuario=id_usuario, id_predio=id_predio)
    try:
        await db.execute(stmt)
        await db.commit()
        return True
    except Exception:
        # Si da error (ej. el usuario ya estaba asignado), hacemos rollback para no trabar la base de datos
        await db.rollback()
        return False

async def remover_usuario(db: AsyncSession, id_predio: UUID, id_usuario: UUID) -> bool:
    stmt = delete(tabla_usuarios_predios).where(
        tabla_usuarios_predios.c.id_usuario == id_usuario,
        tabla_usuarios_predios.c.id_predio == id_predio
    )
    await db.execute(stmt)
    await db.commit()
    return True