from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.services.cliente_service import crear_cliente, obtener_cliente_con_saldos
from app.models.cliente import Cliente
from app.services.cliente_service import obtener_clientes
router = APIRouter()
from app.core.deps import get_current_empresa
from app.models.empresa import Empresa

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db), empresa: Cliente = Depends(get_current_empresa)):
    return crear_cliente(db, cliente, empresa)

@router.get("/listado", response_model=list[ClienteResponse])
def read_clientes_por_empresa(db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    return obtener_clientes(db, empresa.id)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    cliente = obtener_cliente_con_saldos(db, cliente_id)
    print("Cliente obtenido:", cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    #Seguridad: evitar que una empresa acceda a clientes de otra empresa
    if cliente.empresa_id != empresa.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para acceder a este cliente"
        )
    return cliente


