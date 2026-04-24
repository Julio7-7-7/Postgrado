from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.alumno import Alumno
from schemas.alumno import AlumnoCreate, AlumnoResponse

router = APIRouter(
    prefix="/alumno",
    tags=["Alumno"]
)

@router.post("/", response_model=AlumnoResponse)
def crear(data: AlumnoCreate, db: Session = Depends(get_db)):
    nuevo = Alumno(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[AlumnoResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Alumno).all()

@router.get("/{id}", response_model=AlumnoResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    alumno = db.query(Alumno).filter(Alumno.id_alumno == id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="No encontrado")
    return alumno

@router.put("/{id}", response_model=AlumnoResponse)
def editar(id: int, data: AlumnoCreate, db: Session = Depends(get_db)):
    alumno = db.query(Alumno).filter(Alumno.id_alumno == id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(alumno, key, value)
    db.commit()
    db.refresh(alumno)
    return alumno

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    alumno = db.query(Alumno).filter(Alumno.id_alumno == id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(alumno)
    db.commit()
    return {"message": "Eliminado exitosamente"}