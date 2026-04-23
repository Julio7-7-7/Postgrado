from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.modalidad_academica import ModalidadAcademica
from schemas.modalidad_academica import ModalidadAcademicaCreate, ModalidadAcademicaResponse

router = APIRouter(
    prefix="/modalidad-academica",
    tags=["Modalidad Academica"]
)

@router.post("/", response_model=ModalidadAcademicaResponse)
def crear(data: ModalidadAcademicaCreate, db: Session = Depends(get_db)):
    nueva = ModalidadAcademica(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[ModalidadAcademicaResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(ModalidadAcademica).all()

@router.get("/{id}", response_model=ModalidadAcademicaResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    modalidad = db.query(ModalidadAcademica).filter(ModalidadAcademica.id_modalidad_academica == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    return modalidad

@router.put("/{id}", response_model=ModalidadAcademicaResponse)
def editar(id: int, data: ModalidadAcademicaCreate, db: Session = Depends(get_db)):
    modalidad = db.query(ModalidadAcademica).filter(ModalidadAcademica.id_modalidad_academica == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(modalidad, key, value)
    db.commit()
    db.refresh(modalidad)
    return modalidad

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    modalidad = db.query(ModalidadAcademica).filter(ModalidadAcademica.id_modalidad_academica == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(modalidad)
    db.commit()
    return {"message": "Eliminado exitosamente"}