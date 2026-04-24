from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.programa_version_edicion import ProgramaVersionEdicion
from schemas.programa_version_edicion import ProgramaVersionEdicionCreate, ProgramaVersionEdicionResponse

router = APIRouter(
    prefix="/programa-version-edicion",
    tags=["Programa Version Edicion"]
)

@router.post("/", response_model=ProgramaVersionEdicionResponse)
def crear(data: ProgramaVersionEdicionCreate, db: Session = Depends(get_db)):
    ultima = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version == data.id_programa_version
    ).count()
    nueva = ProgramaVersionEdicion(
        **data.model_dump(),
        edicion=ultima + 1
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[ProgramaVersionEdicionResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(ProgramaVersionEdicion).all()

@router.get("/{id}", response_model=ProgramaVersionEdicionResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    pve = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version_edicion == id
    ).first()
    if not pve:
        raise HTTPException(status_code=404, detail="No encontrado")
    return pve

@router.put("/{id}", response_model=ProgramaVersionEdicionResponse)
def editar(id: int, data: ProgramaVersionEdicionCreate, db: Session = Depends(get_db)):
    pve = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version_edicion == id
    ).first()
    if not pve:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.model_dump().items():
        setattr(pve, key, value)
    db.commit()
    db.refresh(pve)
    return pve

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    pve = db.query(ProgramaVersionEdicion).filter(
        ProgramaVersionEdicion.id_programa_version_edicion == id
    ).first()
    if not pve:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(pve)
    db.commit()
    return {"message": "Eliminado exitosamente"}