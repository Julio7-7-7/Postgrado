from pydantic import BaseModel
from datetime import datetime

class ModalidadBase(BaseModel):
    nombre: str
    vigente: bool = True

class ModalidadCreate(ModalidadBase):
    pass

class ModalidadResponse(ModalidadBase):
    id_modalidad: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True