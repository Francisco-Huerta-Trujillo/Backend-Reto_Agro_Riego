from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.base import Base # Ajusta este import si Base está en otro lado
from src.models.associations import usuarios_predios



# 2. LA CLASE PRINCIPAL
class Predio(Base):
    __tablename__ = "predios"
    __table_args__ = {'extend_existing': True} # <--- OBLIGATORIO

    id_predio = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_encargado = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))
    coordenadas = Column(String(255))

    # Relación M:N
    usuarios = relationship("Usuario", secondary=usuarios_predios, backref="mis_predios")
    areas = relationship("AreaRiego", back_populates="predio")
