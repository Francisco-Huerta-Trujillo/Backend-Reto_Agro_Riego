# app/models/predio.py
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.base import Base
from src.models.associations import usuarios_predios

class Predio(Base):
    __tablename__ = "predios"

    id_predio = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_encargado = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))
    coordenadas = Column(String(255))

    # Relaciones (Opcionales para facilitar consultas)
    usuarios = relationship("Usuario", secondary=usuarios_predios, backref="mis_predios")

