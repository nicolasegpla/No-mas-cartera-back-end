from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.abono import AbonoCreate, AbonoResponse
from app.services.abono_service import crear_abono, obtener_abono
from app.services.abono_service import obtener_abonos_por_factura

router = APIRouter()

@router.post("/", response_model=AbonoResponse)
def create_abono(abono: AbonoCreate, db: Session = Depends(get_db)):
    return crear_abono(db, abono)

@router.get("/{abono_id}", response_model=AbonoResponse)
def read_abono(abono_id: int, db: Session = Depends(get_db)):
    abono = obtener_abono(db, abono_id)
    if not abono:
        raise HTTPException(status_code=404, detail="Abono no encontrado")
    return abono

@router.get("/listado/{factura_id}", response_model=list[AbonoResponse])
def get_abonos_por_factura(factura_id: int, db: Session = Depends(get_db)):
    return obtener_abonos_por_factura(db, factura_id)