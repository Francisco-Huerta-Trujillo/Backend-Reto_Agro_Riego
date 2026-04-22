from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from uuid import UUID

# 1. Base: Los atributos que comparten casi todos los schemas de usuario
class UserBase(BaseModel):
    email: str
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
    email: Optional[str] = None
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
    password: Optional[str] = None
    contrasena: Optional[str] = None

    @model_validator(mode="after")
    def validate_password_fields(self):
        if not self.password and not self.contrasena:
            raise ValueError("Se requiere password o contrasena")

        if not self.password and self.contrasena:
            self.password = self.contrasena

        return self

        