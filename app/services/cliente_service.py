from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.abono import Abono
from app.models.factura import Factura
from fastapi import HTTPException
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate
from sqlalchemy import exists, and_

def crear_cliente(db: Session, cliente_data: ClienteCreate) -> Cliente:
    cliente = Cliente(**cliente_data.dict())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def obtener_cliente_con_saldos(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Total facturas emitidas
    total_facturas = (
        db.query(func.coalesce(func.sum(Factura.monto_total), 0))
        .filter(Factura.cliente_id == cliente_id)
        .scalar()
    )

    # Total abonado
    total_abonos = (
        db.query(func.coalesce(func.sum(Abono.monto_abono), 0))
        .filter(Abono.cliente_id == cliente_id)
        .scalar()
    )

    # Revisar estado de cartera
    factura_vencida = db.query(
        exists().where(
            and_(
                Factura.cliente_id == cliente_id,
                Factura.estado == "vencida"
            )
        )
    ).scalar()

    estado_cartera = True if factura_vencida else False

    facturas = db.query(Factura).filter(Factura.cliente_id == cliente_id).all()
    for f in facturas:
        print(f"id={f.id}, estado={f.estado}")



    return {
        "id": cliente.id,
        "empresa_id": cliente.empresa_id,
        "nombre": cliente.nombre,
        "email": cliente.email,
        "telefono": cliente.telefono,
        "identificacion_tributaria": cliente.identificacion_tributaria,
        "deuda_total": total_facturas - total_abonos,
        "abonado_total": total_abonos,
        "estado_cartera": estado_cartera,
        "fecha_registro": cliente.fecha_registro
    }

def obtener_clientes(db: Session, empresa_id: int) -> list[dict]:
    clientes = db.query(Cliente).filter(Cliente.empresa_id == empresa_id).all()
    resultado = []

    for c in clientes:

        resultado.append({
            "id": c.id,
            "empresa_id": c.empresa_id,
            "nombre": c.nombre,
            "email": c.email,
            "telefono": c.telefono,
            "identificacion_tributaria": c.identificacion_tributaria,
            "deuda_total": c.deuda_total,
            "abonado_total": c.abonado_total,
            "estado_cartera": c.estado_cartera,
            "fecha_registro": c.fecha_registro
        })

    db.commit()

    return resultado