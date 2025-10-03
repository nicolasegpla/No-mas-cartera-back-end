from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.abono import Abono
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate

def crear_factura(db: Session, factura_data: FacturaCreate) -> Factura:
    factura = Factura(
        cliente_id=factura_data.cliente_id,
        monto_total=factura_data.monto_total,
        fecha_vencimiento=factura_data.fecha_vencimiento,
        estado="pendiente"
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura

def obtener_factura(db: Session, factura_id: int) -> Factura:
    return db.query(Factura).filter(Factura.id == factura_id).first()

def obtener_factura_detalle(db: Session, factura_id: int):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        return None
    
    total_abonado = (
        db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
        .filter(Abono.factura_id == factura_id)
        .scalar()
    )

    saldo_pendiente = factura.monto_total - total_abonado

    return {
        "id": factura.id,
        "cliente_id": factura.cliente_id,
        "monto_total": factura.monto_total,
        "total_abonado": total_abonado,
        "saldo_pendiente": saldo_pendiente,
        "estado": factura.estado,
        "fecha_emision": factura.fecha_emision,
        "fecha_vencimiento": factura.fecha_vencimiento,
    }

def obtener_facturas_por_cliente(db: Session, cliente_id: int) -> List[dict]:
    facturas = db.query(Factura).filter(Factura.cliente_id == cliente_id).all()
    resultado = []

    for f in facturas:
        total_abonado = (
            db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
            .filter(Abono.factura_id == f.id)
            .scalar()
        )
        saldo_pendiente = f.monto_total - total_abonado

        resultado.append({
            "id": f.id,
            "cliente_id": f.cliente_id,
            "monto_total": f.monto_total,
            "total_abonado": total_abonado,
            "saldo_pendiente": saldo_pendiente,
            "estado": f.estado,
            "fecha_emision": f.fecha_emision,
            "fecha_vencimiento": f.fecha_vencimiento,
        })

    return resultado