from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

# 1. Base: Los atributos que comparten casi todos los schemas de usuario
class UserBase(BaseModel):
    nombre: str
    apellido_p: str
    apellido_m: Optional[str] = None
    rol: str

# 2. Create: Lo que React nos envía para CREAR un usuario
class UserCreate(UserBase):
    contrasena: str
    creado_por: Optional[UUID] = None

# 3. Update: Lo que React nos envía para ACTUALIZAR (todo es opcional)
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido_p: Optional[str] = None
    apellido_m: Optional[str] = None
    rol: Optional[str] = None
    # No permitimos actualizar la contraseña por esta misma ruta por seguridad

# 4. Response (Read): Lo que FastAPI le DEVUELVE a React (Nunca devolvemos la contraseña)
class UserResponse(UserBase):
    id_usuario: UUID
    creado_por: Optional[UUID] = None

    # Esto es CRÍTICO: Le dice a Pydantic que entienda los objetos de la base de datos (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: str
    password: str