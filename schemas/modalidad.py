from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum

class EstadoModalidadEnum(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class ModalidadBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    estado: EstadoModalidadEnum = EstadoModalidadEnum.activo

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        if len(v.strip()) > 50:
            raise ValueError("El nombre no puede superar 50 caracteres")
        return v.strip().title()

class ModalidadCreate(ModalidadBase):
    pass

class ModalidadUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    estado: EstadoModalidadEnum | None = None

class ModalidadResponse(ModalidadBase):
    id_modalidad: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True