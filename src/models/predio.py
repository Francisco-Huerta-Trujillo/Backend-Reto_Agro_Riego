from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.base import Base # Ajusta este import si Base está en otro lado

# 1. LA TABLA INTERMEDIA (Solo una vez)
tabla_usuarios_predios = Table(
    'usuarios_predios',
    Base.metadata,
    Column('id_usuario', UUID(as_uuid=True), ForeignKey('usuarios.id_usuario', ondelete="CASCADE"), primary_key=True),
    Column('id_predio', UUID(as_uuid=True), ForeignKey('predios.id_predio', ondelete="CASCADE"), primary_key=True),
    extend_existing=True # 
)

# 2. LA CLASE PRINCIPAL
class Predio(Base):
    __tablename__ = "predios"
    __table_args__ = {'extend_existing': True} # <--- OBLIGATORIO

    id_predio = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_encargado = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))
    coordenadas = Column(String(255))

    # Relación M:N
    usuarios = relationship("Usuario", secondary=tabla_usuarios_predios, backref="mis_predios")