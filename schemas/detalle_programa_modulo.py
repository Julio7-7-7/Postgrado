from pydantic import BaseModel
from datetime import datetime, date

class DetalleProgramaModuloBase(BaseModel):
    id_programa_version_edicion: int
    id_modulo: int
    id_docente: int
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    estado: str = "programado"

class DetalleProgramaModuloCreate(DetalleProgramaModuloBase):
    pass

class DetalleProgramaModuloResponse(DetalleProgramaModuloBase):
    id_detalle_programa_modulo: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True