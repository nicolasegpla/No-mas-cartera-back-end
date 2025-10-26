from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.services.cliente_service import crear_cliente, obtener_cliente_con_saldos
from app.models.cliente import Cliente
from app.services.cliente_service import obtener_clientes
router = APIRouter()

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crear_cliente(db, cliente)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return obtener_cliente_con_saldos(db, cliente_id)

@router.get("/listado/{empresa_id}", response_model=list[ClienteResponse])
def read_clientes_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    return obtener_clientes(db, empresa_id)
