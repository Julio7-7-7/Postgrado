from pydantic import BaseModel
from datetime import datetime, date

class ProgramaVersionEdicionBase(BaseModel):
    id_programa_version: int
    id_modalidad: int
    gestion: str
    vigente: bool = True
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    cupo_maximo: int | None = None

class ProgramaVersionEdicionCreate(ProgramaVersionEdicionBase):
    pass

class ProgramaVersionEdicionResponse(ProgramaVersionEdicionBase):
    id_programa_version_edicion: int
    edicion: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True