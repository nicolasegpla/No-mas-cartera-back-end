from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.factura import FacturaCreate, FacturaResponse, FacturaDetalleResponse, FacturaListadoResponse
from app.services.factura_service import crear_factura, obtener_factura, obtener_factura_detalle, obtener_facturas_por_cliente

from typing import List
from app.core.deps import get_current_empresa
from app.models.cliente import Cliente
from app.models.empresa import Empresa

router = APIRouter()

@router.post("/", response_model=FacturaResponse)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    print("Empresa actual:", empresa.id)
    return crear_factura(db, factura, empresa.id)

#@router.get("/{factura_id}", response_model=FacturaResponse)
#def read_factura(factura_id: int, db: Session = Depends(get_db)):
#    factura = obtener_factura(db, factura_id)
#    if not factura:
#        raise HTTPException(status_code=404, detail="Factura no encontrada")
#    return factura

@router.get("/{factura_id}/detalle", response_model=FacturaDetalleResponse)
def read_factura_detalle(factura_id: int, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    detalle = obtener_factura_detalle(db, factura_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    # Seguridad: evitar que una empresa acceda a facturas de otra empresa
    if detalle['empresa_id'] != empresa.id:
        raise HTTPException(
            status_code=403,
            detail="Factura no encontrada o no pertenece a tu empresa"
        )
    return detalle


@router.get("/cliente/{cliente_id}", response_model=List[FacturaListadoResponse])
def read_facturas_por_cliente(cliente_id: int, db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    facturas = obtener_facturas_por_cliente(db, cliente_id, empresa)
    if not facturas:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para este cliente")
    return facturas

@router.get("/listado-facturas", response_model=List[FacturaListadoResponse])
def read_todas_las_facturas(db: Session = Depends(get_db), empresa: Empresa = Depends(get_current_empresa)):
    from app.services.factura_service import obtener_todas_las_facturas
    facturas = obtener_todas_las_facturas(db, empresa)
    return facturas

