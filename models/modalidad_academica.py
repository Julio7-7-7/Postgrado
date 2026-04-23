from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class ModalidadAcademica(Base):
    __tablename__ = "modalidad_academica"

    id_modalidad_academica = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_modalidad = Column(String, nullable=False)
    vigente = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)