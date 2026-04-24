from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.docente import Docente
from schemas.docente import DocenteCreate, DocenteResponse

router = APIRouter(
    prefix="/docente",
    tags=["Docente"]
)

@router.post("/", response_model=DocenteResponse)
def crear(data: DocenteCreate, db: Session = Depends(get_db)):
    nuevo = Docente(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[DocenteResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Docente).all()

@router.get("/{id}", response_model=DocenteResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id_docente == id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="No encontrado")
    return docente

@router.put("/{id}", response_model=DocenteResponse)
def editar(id: int, data: DocenteCreate, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id_docente == id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(docente, key, value)
    db.commit()
    db.refresh(docente)
    return docente

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.id_docente == id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(docente)
    db.commit()
    return {"message": "Eliminado exitosamente"}