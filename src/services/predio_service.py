from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from uuid import UUID

# Importamos el modelo y los schemas
from src.models.predio import Predio
from src.schemas.predio_schema import PredioCreate, PredioUpdate
from src.models.predio import tabla_usuarios_predios

class PredioService:

    # ------------------ CREATE ------------------
    @staticmethod
    async def create(db: AsyncSession, predio_in: PredioCreate) -> Predio:
        db_predio = Predio(**predio_in.model_dump())
        
        db.add(db_predio)
        await db.commit()
        await db.refresh(db_predio)
        return db_predio

    # ------------------ READ (Obtener uno por ID) ------------------
    @staticmethod
    async def get_by_id(db: AsyncSession, predio_id: UUID) -> Predio | None:
        result = await db.execute(select(Predio).where(Predio.id_predio == predio_id))
        return result.scalars().first()

    # ------------------ READ (Obtener todos) ------------------
    @staticmethod
    async def get_all(db: AsyncSession) -> list[Predio]:
        result = await db.execute(select(Predio))
        return list(result.scalars().all())

    # ------------------ UPDATE ------------------
    @staticmethod
    async def update(db: AsyncSession, predio_id: UUID, predio_in: PredioUpdate) -> Predio | None:
        db_predio = await PredioService.get_by_id(db, predio_id)
        if not db_predio:
            return None
        
        # Actualizamos solo los campos que vienen en el request
        update_data = predio_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_predio, key, value)
            
        await db.commit()
        await db.refresh(db_predio)
        return db_predio

    # ------------------ DELETE ------------------
    @staticmethod
    async def delete(db: AsyncSession, predio_id: UUID) -> bool:
        db_predio = await PredioService.get_by_id(db, predio_id)
        if not db_predio:
            return False
            
        await db.delete(db_predio)
        await db.commit()
        return True
    
# ------------------ ASIGNAR USUARIO A PREDIO ------------------
    @staticmethod
    async def asignar_usuario(db: AsyncSession, id_predio: UUID, id_usuario: UUID) -> bool:
        # 1. Ejecutamos un INSERT directo en la tabla intermedia
        stmt = insert(tabla_usuarios_predios).values(
            id_usuario=id_usuario, 
            id_predio=id_predio
        )
        try:
            await db.execute(stmt)
            await db.commit()
            return True
        except Exception as e:
            # Si da error (ej. el usuario ya estaba asignado), hacemos rollback
            await db.rollback()
            return False

    # ------------------ REMOVER USUARIO DE PREDIO ------------------
    @staticmethod
    async def remover_usuario(db: AsyncSession, id_predio: UUID, id_usuario: UUID) -> bool:
        # Borramos el registro de la tabla intermedia
        stmt = delete(tabla_usuarios_predios).where(
            tabla_usuarios_predios.c.id_usuario == id_usuario,
            tabla_usuarios_predios.c.id_predio == id_predio
        )
        await db.execute(stmt)
        await db.commit()
        return True

    # ------------------ OBTENER LOS PREDIOS DE UN USUARIO ------------------
    # Este método es CRÍTICO para el Login. Cuando el usuario entra a React, 
    # necesitamos saber qué predios mostrarle en el Dashboard.
    @staticmethod
    async def obtener_predios_por_usuario(db: AsyncSession, id_usuario: UUID):
        # Hacemos un JOIN entre Predios y la tabla intermedia
        stmt = (
            select(Predio)
            .join(tabla_usuarios_predios, Predio.id_predio == tabla_usuarios_predios.c.id_predio)
            .where(tabla_usuarios_predios.c.id_usuario == id_usuario)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())