from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.detalle_programa_modulo import DetalleProgramaModulo
from models.historial_modulo import HistorialModulo
from schemas.detalle_programa_modulo import DetalleProgramaModuloCreate, DetalleProgramaModuloUpdate, DetalleProgramaModuloResponse

router = APIRouter(
    prefix="/detalle-programa-modulo",
    tags=["Detalle Programa Modulo"]
)

ESTADOS_CON_MOTIVO = {"pausado", "reprogramado", "cancelado"}

@router.post("/", response_model=DetalleProgramaModuloResponse, status_code=201)
def crear(data: DetalleProgramaModuloCreate, db: Session = Depends(get_db)):
    orden_existente = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_programa_version_edicion == data.id_programa_version_edicion,
        DetalleProgramaModulo.orden == data.orden
    ).first()
    if orden_existente:
        raise HTTPException(status_code=400, detail=f"Ya existe un módulo con orden {data.orden} en esta edición")
    nuevo = DetalleProgramaModulo(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[DetalleProgramaModuloResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(DetalleProgramaModulo).all()

@router.get("/{id}", response_model=DetalleProgramaModuloResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_detalle_programa_modulo == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")
    return detalle

@router.patch("/{id}", response_model=DetalleProgramaModuloResponse)
def editar(id: int, data: DetalleProgramaModuloUpdate, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_detalle_programa_modulo == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")

    # si cambia estado a uno que requiere motivo
    if data.estado and data.estado in ESTADOS_CON_MOTIVO:
        if not data.motivo:
            raise HTTPException(
                status_code=400,
                detail=f"El campo motivo es obligatorio cuando el estado es {data.estado}"
            )
        # guardar historial automáticamente
        historial = HistorialModulo(
            id_detalle_programa_modulo=id,
            estado_anterior=detalle.estado,
            estado_nuevo=data.estado,
            motivo=data.motivo,
            fecha_inicio_original=detalle.fecha_inicio,
            fecha_fin_original=detalle.fecha_fin
        )
        db.add(historial)

    # validar orden si se cambia
    if data.orden:
        orden_existente = db.query(DetalleProgramaModulo).filter(
            DetalleProgramaModulo.id_programa_version_edicion == detalle.id_programa_version_edicion,
            DetalleProgramaModulo.orden == data.orden,
            DetalleProgramaModulo.id_detalle_programa_modulo != id
        ).first()
        if orden_existente:
            raise HTTPException(status_code=400, detail=f"Ya existe un módulo con orden {data.orden} en esta edición")

    for key, value in data.model_dump(exclude_unset=True, exclude={"motivo"}).items():
        setattr(detalle, key, value)

    db.commit()
    db.refresh(detalle)
    return detalle

@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_detalle_programa_modulo == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(detalle)
    db.commit()