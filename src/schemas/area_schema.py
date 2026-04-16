from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class AreaBase(BaseModel):
    tipo_cultivo: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class AreaCreate(AreaBase):
    id_predio: UUID  # Es OBLIGATORIO saber a qué predio pertenece al crearla

class AreaUpdate(BaseModel):
    tipo_cultivo: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class AreaResponse(AreaBase):
    id_areariego: UUID
    id_predio: UUID

    model_config = ConfigDict(from_attributes=True)