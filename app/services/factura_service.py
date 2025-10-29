from fastapi import HTTPException, status
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.abono import Abono
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate
from app.models.cliente import Cliente
from app.models.empresa import Empresa

def crear_factura(db: Session, factura_data: FacturaCreate, empresa_id: int) -> Factura:

    existe_factura = db.query(Factura).join(Cliente).filter(
        Factura.numero_factura == factura_data.numero_factura,
        Cliente.empresa_id == empresa_id
    ).first()


    if existe_factura:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una factura con número {factura_data.numero_factura} en esta empresa"
        )


    factura_id_clinete = factura_data.cliente_id
    print("factura id clinete", factura_id_clinete)
    print("empresa id", empresa_id)

    cliente = db.query(Cliente).filter(Cliente.id == factura_id_clinete).first()


    if cliente.empresa_id != empresa_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente no pertenece a la empresa actual."
        )

    factura = Factura(
        cliente_id=factura_data.cliente_id,
        monto_total=factura_data.monto_total,
        fecha_vencimiento=factura_data.fecha_vencimiento,
        estado="pendiente",
        numero_factura=factura_data.numero_factura
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura

def obtener_factura(db: Session, factura_id: int) -> Factura:
    return db.query(Factura).filter(Factura.id == factura_id).first()

def obtener_factura_detalle(db: Session, factura_id: int):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    cliente = db.query(Cliente).filter(Cliente.id == factura.cliente_id).first()
    if not factura:
        return None
    
    total_abonado = (
        db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
        .filter(Abono.factura_id == factura_id)
        .scalar()
    )

    saldo_pendiente = factura.monto_total - total_abonado
    estado = factura.estado

    if saldo_pendiente == 0:
        estado = "pagada"
    elif factura.fecha_vencimiento < datetime.now():
        estado = "vencida"

    return {
        "id": factura.id,
        "cliente_id": factura.cliente_id,
        "monto_total": factura.monto_total,
        "total_abonado": total_abonado,
        "saldo_pendiente": saldo_pendiente,
        "estado": estado,
        "fecha_emision": factura.fecha_emision,
        "fecha_vencimiento": factura.fecha_vencimiento,
        "numero_factura": factura.numero_factura,
        "empresa_id": cliente.empresa_id
    }

def obtener_facturas_por_cliente(db: Session, cliente_id: int, empresa: Empresa) -> List[dict]:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    facturas = db.query(Factura).filter(Factura.cliente_id == cliente_id).all()
    resultado = []

    if cliente.empresa_id != empresa.id:
        raise HTTPException(
            status_code=403,
            detail="El cliente no existe o no pertenece a tu empresa"
        )

    for f in facturas:
        total_abonado = (
            db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
            .filter(Abono.factura_id == f.id)
            .scalar()
        )
        saldo_pendiente = f.monto_total - total_abonado
        estado = f.estado

        if saldo_pendiente == 0:
            estado = "pagada"
        elif f.fecha_vencimiento < datetime.now():
            estado = "vencida"

        
        if f.estado != estado:
            print(f"[ACTUALIZANDO] Factura {f.id} de '{f.estado}' → '{estado}'")
            f.estado = estado
            db.add(f)


        resultado.append({
            "id": f.id,
            "cliente_id": f.cliente_id,
            "monto_total": f.monto_total,
            "total_abonado": total_abonado,
            "saldo_pendiente": saldo_pendiente,
            "estado": estado,
            "fecha_emision": f.fecha_emision,
            "fecha_vencimiento": f.fecha_vencimiento,
            "numero_factura": f.numero_factura,
        })
    
    db.commit()

    return resultado

def obtener_todas_las_facturas(db: Session, empresa: Empresa) -> List[dict]:
    facturas = (
        db.query(Factura)
        .join(Cliente, Cliente.id == Factura.cliente_id)
        .filter(Cliente.empresa_id == empresa.id)
        .all()
    )

    if not facturas:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para esta empresa")

    resultado = []

    for facturas in facturas:
        resultado.append({
            "id": facturas.id,
            "cliente_id": facturas.cliente_id,
            "monto_total": facturas.monto_total,
            "estado": facturas.estado,
            "fecha_emision": facturas.fecha_emision,
            "fecha_vencimiento": facturas.fecha_vencimiento,
            "numero_factura": facturas.numero_factura,
            "total_abonado": str(
                db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
                .filter(Abono.factura_id == facturas.id)
                .scalar()
            ),
            "saldo_pendiente": str(
                facturas.monto_total - db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
                .filter(Abono.factura_id == facturas.id)
                .scalar()
            )
        })

    return resultado