from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.factura import FacturaCreate, FacturaResponse, FacturaDetalleResponse, FacturaListadoResponse
from app.services.factura_service import crear_factura, obtener_factura, obtener_factura_detalle, obtener_facturas_por_cliente

from typing import List

router = APIRouter()

@router.post("/", response_model=FacturaResponse)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    return crear_factura(db, factura)

@router.get("/{factura_id}", response_model=FacturaResponse)
def read_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = obtener_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.get("/{factura_id}/detalle", response_model=FacturaDetalleResponse)
def read_factura_detalle(factura_id: int, db: Session = Depends(get_db)):
    detalle = obtener_factura_detalle(db, factura_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return detalle


@router.get("/cliente/{cliente_id}", response_model=List[FacturaListadoResponse])
def read_facturas_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    facturas = obtener_facturas_por_cliente(db, cliente_id)
    if not facturas:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para este cliente")
    return facturas

