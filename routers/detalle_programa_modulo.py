from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.detalle_programa_modulo import DetalleProgramaModulo
from schemas.detalle_programa_modulo import DetalleProgramaModuloCreate, DetalleProgramaModuloResponse

router = APIRouter(
    prefix="/detalle-programa-modulo",
    tags=["Detalle Programa Modulo"]
)

@router.post("/", response_model=DetalleProgramaModuloResponse)
def crear(data: DetalleProgramaModuloCreate, db: Session = Depends(get_db)):
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

@router.put("/{id}", response_model=DetalleProgramaModuloResponse)
def editar(id: int, data: DetalleProgramaModuloCreate, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_detalle_programa_modulo == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(detalle, key, value)
    db.commit()
    db.refresh(detalle)
    return detalle

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaModulo).filter(
        DetalleProgramaModulo.id_detalle_programa_modulo == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(detalle)
    db.commit()
    return {"message": "Eliminado exitosamente"}