from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.modalidad import Modalidad
from schemas.modalidad import ModalidadCreate, ModalidadResponse

router = APIRouter(
    prefix="/modalidad",
    tags=["Modalidad"]
)

@router.post("/", response_model=ModalidadResponse)
def crear(data: ModalidadCreate, db: Session = Depends(get_db)):
    nueva = Modalidad(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[ModalidadResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Modalidad).all()

@router.get("/{id}", response_model=ModalidadResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    modalidad = db.query(Modalidad).filter(Modalidad.id_modalidad == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    return modalidad

@router.put("/{id}", response_model=ModalidadResponse)
def editar(id: int, data: ModalidadCreate, db: Session = Depends(get_db)):
    modalidad = db.query(Modalidad).filter(Modalidad.id_modalidad == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(modalidad, key, value)
    db.commit()
    db.refresh(modalidad)
    return modalidad

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    modalidad = db.query(Modalidad).filter(Modalidad.id_modalidad == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(modalidad)
    db.commit()
    return {"message": "Eliminado exitosamente"}