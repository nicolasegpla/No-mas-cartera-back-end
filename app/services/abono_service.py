from sqlalchemy.orm import Session
from app.models.abono import Abono
from app.schemas.abono import AbonoCreate

def crear_abono(db: Session, abono_data: AbonoCreate) -> Abono:
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
