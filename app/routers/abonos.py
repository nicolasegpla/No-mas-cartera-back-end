from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.abono import AbonoCreate, AbonoResponse
from app.services.abono_service import crear_abono, obtener_abono
from app.services.abono_service import obtener_abonos_por_factura
from app.core.deps import get_current_empresa
from app.models.cliente import Cliente
from app.models.empresa import Empresa
from app.models.factura import Factura
from app.models.abono import Abono
from app.services.abono_service import obtener_todos_los_abonos

router = APIRouter()

@router.post("/", response_model=AbonoResponse)
def create_abono(abono: AbonoCreate, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    client_data = db.query(Cliente).filter(Cliente.id == abono.cliente_id).first()
    if client_data.empresa_id != empresa.id:
        raise HTTPException(
            status_code=400,
            detail="El cliente no existe o no pertenece a la empresa actual."
        )
    factura_data = db.query(Factura).filter(Factura.id == abono.factura_id).first()
    if factura_data.cliente_id != abono.cliente_id:
        raise HTTPException(
            status_code=400,
            detail="La factura no existe o no pertenece al cliente proporcionado."
        )
    return crear_abono(db, abono)

@router.get("/{abono_id}", response_model=AbonoResponse)
def read_abono(abono_id: int, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    print("Obteniendo abono con ID:", abono_id)
    abono_data = db.query(Abono).filter(Abono.id == abono_id).first()
    if not abono_data:
        raise HTTPException(status_code=404, detail="Abono no encontrado o no pertenece a la empresa actual.")
    client_data = db.query(Cliente).filter(Cliente.id == abono_data.cliente_id).first()
    if client_data.empresa_id != empresa.id:
        raise HTTPException(status_code=404, detail="Abono no encontrado o no pertenece a la empresa actual ok.")
    print("Abono encontrado:", abono_data.cliente_id)
    abono = obtener_abono(db, abono_id)
    if not abono:
        raise HTTPException(status_code=404, detail="Abono no encontrado")
    return abono

@router.get("/listado/{factura_id}", response_model=list[AbonoResponse])
def get_abonos_por_factura(factura_id: int, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    factura_data = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura_data:
        raise HTTPException(status_code=404, detail="Factura no encontrada o no pertenece a la empresa actual.")
    client_data = db.query(Cliente).filter(Cliente.id == factura_data.cliente_id).first()
    if client_data.empresa_id != empresa.id:
        raise HTTPException(status_code=404, detail="Factura no encontrada o no pertenece a la empresa actual.")
    return obtener_abonos_por_factura(db, factura_id)


@router.get("/todos/", response_model=list[AbonoResponse])
def get_todos_los_abonos(db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    return obtener_todos_los_abonos(db, empresa.id)