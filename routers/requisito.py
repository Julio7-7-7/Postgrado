from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.requisito import Requisito
from schemas.requisito import RequisitoCreate, RequisitoResponse

router = APIRouter(
    prefix="/requisito",
    tags=["Requisito"]
)

@router.post("/", response_model=RequisitoResponse)
def crear(data: RequisitoCreate, db: Session = Depends(get_db)):
    nuevo = Requisito(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[RequisitoResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Requisito).all()

@router.get("/{id}", response_model=RequisitoResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    requisito = db.query(Requisito).filter(Requisito.id_requisito == id).first()
    if not requisito:
        raise HTTPException(status_code=404, detail="No encontrado")
    return requisito

@router.put("/{id}", response_model=RequisitoResponse)
def editar(id: int, data: RequisitoCreate, db: Session = Depends(get_db)):
    requisito = db.query(Requisito).filter(Requisito.id_requisito == id).first()
    if not requisito:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(requisito, key, value)
    db.commit()
    db.refresh(requisito)
    return requisito

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    requisito = db.query(Requisito).filter(Requisito.id_requisito == id).first()
    if not requisito:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(requisito)
    db.commit()
    return {"message": "Eliminado exitosamente"}