from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.modalidad import Modalidad
from schemas.modalidad import ModalidadCreate, ModalidadUpdate, ModalidadResponse

router = APIRouter(
    prefix="/modalidades",
    tags=["Modalidades"]
)

@router.post("/", response_model=ModalidadResponse, status_code=201)
def crear(data: ModalidadCreate, db: Session = Depends(get_db)):
    existente = db.query(Modalidad).filter(Modalidad.nombre == data.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una modalidad con ese nombre")
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

@router.patch("/{id}", response_model=ModalidadResponse)
def editar(id: int, data: ModalidadUpdate, db: Session = Depends(get_db)):
    modalidad = db.query(Modalidad).filter(Modalidad.id_modalidad == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(modalidad, key, value)
    db.commit()
    db.refresh(modalidad)
    return modalidad

@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    modalidad = db.query(Modalidad).filter(Modalidad.id_modalidad == id).first()
    if not modalidad:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(modalidad)
    db.commit()