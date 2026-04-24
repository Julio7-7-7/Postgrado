from pydantic import BaseModel
from datetime import datetime

class RequisitoBase(BaseModel):
    id_modalidad_academica: int
    nombre: str
    descripcion: str | None = None
    obligatorio: bool = True

class RequisitoCreate(RequisitoBase):
    pass

class RequisitoResponse(RequisitoBase):
    id_requisito: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True