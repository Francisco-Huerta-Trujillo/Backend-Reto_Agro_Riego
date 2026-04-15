# app/models/area.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.base import Base

class AreaRiego(Base):
    __tablename__ = "areas_riego"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    predio_id = Column(UUID(as_uuid=True), ForeignKey("predios.id"))
    nombre = Column(String)
    tipo_cultivo = Column(String)