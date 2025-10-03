from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.services.cliente_service import crear_cliente, obtener_cliente_con_saldos
router = APIRouter()

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crear_cliente(db, cliente)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return obtener_cliente_con_saldos(db, cliente_id)
