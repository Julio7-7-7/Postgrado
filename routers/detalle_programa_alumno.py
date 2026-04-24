from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.detalle_programa_alumno import DetalleProgramaAlumno
from schemas.detalle_programa_alumno import DetalleProgramaAlumnoCreate, DetalleProgramaAlumnoResponse

router = APIRouter(
    prefix="/detalle-programa-alumno",
    tags=["Detalle Programa Alumno"]
)

@router.post("/", response_model=DetalleProgramaAlumnoResponse)
def crear(data: DetalleProgramaAlumnoCreate, db: Session = Depends(get_db)):
    nuevo = DetalleProgramaAlumno(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[DetalleProgramaAlumnoResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(DetalleProgramaAlumno).all()

@router.get("/{id}", response_model=DetalleProgramaAlumnoResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaAlumno).filter(
        DetalleProgramaAlumno.id_detalle_programa_alumno == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")
    return detalle

@router.put("/{id}", response_model=DetalleProgramaAlumnoResponse)
def editar(id: int, data: DetalleProgramaAlumnoCreate, db: Session = Depends(get_db)):
    detalle = db.query(DetalleProgramaAlumno).filter(
        DetalleProgramaAlumno.id_detalle_programa_alumno == id
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
    detalle = db.query(DetalleProgramaAlumno).filter(
        DetalleProgramaAlumno.id_detalle_programa_alumno == id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(detalle)
    db.commit()
    return {"message": "Eliminado exitosamente"}