from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

# Importamos el modelo de DB y los schemas que acabas de crear
from src.models.user import Usuario 
from src.schemas.user_schema import UserCreate, UserUpdate

class UserService:

    # ------------------ CREATE ------------------
    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> Usuario:
        # En la vida real, aquí debes hashear la contraseña antes de guardarla.
        # Por ahora lo guardamos directo para la prueba:
        db_user = Usuario(**user_in.model_dump()) 
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user) # Refresca para obtener el ID generado (UUID)
        return db_user

    # ------------------ READ (Obtener uno) ------------------
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID) -> Usuario | None:
        result = await db.execute(select(Usuario).where(Usuario.id_usuario == user_id))
        return result.scalars().first()

    # ------------------ READ (Obtener todos) ------------------
    @staticmethod
    async def get_all(db: AsyncSession) -> list[Usuario]:
        result = await db.execute(select(Usuario))
        return list(result.scalars().all())

    # ------------------ UPDATE ------------------
    @staticmethod
    async def update(db: AsyncSession, user_id: UUID, user_in: UserUpdate) -> Usuario | None:
        db_user = await UserService.get_by_id(db, user_id)
        if not db_user:
            return None
        
        # Actualizamos solo los campos que React nos envió (exclude_unset=True)
        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        await db.commit()
        await db.refresh(db_user)
        return db_user

    # ------------------ DELETE ------------------
    @staticmethod
    async def delete(db: AsyncSession, user_id: UUID) -> bool:
        db_user = await UserService.get_by_id(db, user_id)
        if not db_user:
            return False
            
        await db.delete(db_user)
        await db.commit()
        return True