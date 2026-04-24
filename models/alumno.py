from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Alumno(Base):
    __tablename__ = "alumno"

    id_alumno = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ci = Column(String, nullable=False, unique=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    genero = Column(String, nullable=True)
    celular = Column(String, nullable=True)
    correo = Column(String, nullable=False, unique=True)
    direccion = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)