from sqlalchemy.orm import Session
from app.models.abono import Abono
from app.schemas.abono import AbonoCreate
from app.models.factura import Factura
from fastapi import HTTPException
from sqlalchemy import func
from app.models.cliente import Cliente


def crear_abono(db: Session, abono_data: AbonoCreate) -> Abono:

    # 1️⃣ Obtener la factura asociada
    factura = db.query(Factura).filter(Factura.id == abono_data.factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # 2️⃣ Calcular el total de abonos existentes
    total_abonado = (
        db.query(Abono)
        .filter(Abono.factura_id == abono_data.factura_id)
        .with_entities(func.coalesce(func.sum(Abono.monto_abono), 0))
        .scalar()
    )
    
    saldo_pendiente = factura.monto_total - total_abonado

    # 3️⃣ Validar que el nuevo abono no supere el saldo pendiente
    if abono_data.monto_abono > saldo_pendiente:
        raise HTTPException(
            status_code=400,
            detail=f"El abono excede el saldo pendiente. Saldo actual: {saldo_pendiente:.2f}"
        )
    
    # 4️⃣ Crear el abono
    abono = Abono(
        cliente_id=abono_data.cliente_id,
        factura_id=abono_data.factura_id,
        monto_abono=abono_data.monto_abono,
        metodo_pago=abono_data.metodo_pago
    )
    db.add(abono)
    db.commit()
    db.refresh(abono)
    return abono

def obtener_abono(db: Session, abono_id: int) -> Abono:
    return db.query(Abono).filter(Abono.id == abono_id).first()

def obtener_abonos_por_factura(db: Session, factura_id: int) -> list[Abono]:
    abonos = db.query(Abono).filter(Abono.factura_id == factura_id).all()
    resultado = []
    for abono in abonos:
        resultado.append({
            "id": abono.id,
            "cliente_id": abono.cliente_id,
            "factura_id": abono.factura_id,
            "monto_abono": abono.monto_abono,
            "metodo_pago": abono.metodo_pago,
            "fecha_abono": abono.fecha_abono,
        })

    db.commit()

    return resultado

def obtener_todos_los_abonos(db: Session, empresa_id: int) -> list[Abono]:
    abonos = (
        db.query(Abono)
        .join(Cliente, Cliente.id == Abono.cliente_id)
        .filter(Cliente.empresa_id == empresa_id)
        .all()
    )

    if not abonos:
        raise HTTPException(status_code=404, detail="No se encontraron abonos para esta empresa")

    resultado = []

    for abono in abonos:
        resultado.append({
            "id": abono.id,
            "cliente_id": abono.cliente_id,
            "factura_id": abono.factura_id,
            "monto_abono": abono.monto_abono,
            "metodo_pago": abono.metodo_pago,
            "fecha_abono": abono.fecha_abono,
        })

    return resultado

def obtener_todos_los_abonos_por_cliente(db: Session, cliente_id: int, empresa_id: int) -> list[Abono]:
    abonos = (
        db.query(Abono)
        .join(Cliente, Cliente.id == Abono.cliente_id)
        .filter(Cliente.empresa_id == empresa_id)
        .filter(Abono.cliente_id == cliente_id)
        .all()
    )

    if not abonos:
        raise HTTPException(status_code=404, detail="No se encontraron abonos para este cliente en esta empresa")

    resultado = []

    for abono in abonos:
        resultado.append({
            "id": abono.id,
            "cliente_id": abono.cliente_id,
            "factura_id": abono.factura_id,
            "monto_abono": abono.monto_abono,
            "metodo_pago": abono.metodo_pago,
            "fecha_abono": abono.fecha_abono,
        })

    return resultado


