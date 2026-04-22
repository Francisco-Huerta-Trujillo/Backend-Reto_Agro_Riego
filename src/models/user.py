# app/models/user.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_p = Column(String(100), nullable=False)
    apellido_m = Column(String(100))
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    
    # Llave recursiva: un usuario es creado por otro usuario
    creado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))