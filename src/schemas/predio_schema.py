from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

# 1. Base: Atributos comunes
class PredioBase(BaseModel):
    coordenadas: Optional[str] = None
    id_encargado: Optional[UUID] = None  # Llave foránea hacia el usuario

# 2. Create: Lo que pedimos para registrar un nuevo predio
class PredioCreate(PredioBase):
    pass # No hay campos extra obligatorios para crear, hereda todo de Base

# 3. Update: Lo que pedimos para actualizar (todo opcional)
class PredioUpdate(BaseModel):
    coordenadas: Optional[str] = None
    id_encargado: Optional[UUID] = None

# 4. Response: Lo que le devolvemos a React
class PredioResponse(PredioBase):
    id_predio: UUID

    # Permite a Pydantic leer el objeto directamente de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class UsuarioPredioAsignacion(BaseModel):
    id_usuario: UUID
    id_predio: UUID