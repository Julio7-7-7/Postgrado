from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

class GeneroEnum(str, Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"

class AlumnoBase(BaseModel):
    ci: str
    nombre: str
    apellido: str
    fecha_nacimiento: date | None = None
    genero: GeneroEnum | None = None
    celular: str | None = None
    correo: str
    direccion: str | None = None

class AlumnoCreate(AlumnoBase):
    pass

class AlumnoResponse(AlumnoBase):
    id_alumno: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True