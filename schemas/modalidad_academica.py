from pydantic import BaseModel
from datetime import datetime

class ModalidadAcademicaBase(BaseModel):
    nombre_modalidad: str
    vigente: bool = True

class ModalidadAcademicaCreate(ModalidadAcademicaBase):
    pass

class ModalidadAcademicaResponse(ModalidadAcademicaBase):
    id_modalidad_academica: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True