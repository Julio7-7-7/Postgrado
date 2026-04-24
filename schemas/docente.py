from pydantic import BaseModel
from datetime import datetime

class DocenteBase(BaseModel):
    ci: str
    nombre: str
    apellido: str
    celular: str | None = None
    correo: str
    vigente: bool = True

class DocenteCreate(DocenteBase):
    pass

class DocenteResponse(DocenteBase):
    id_docente: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True