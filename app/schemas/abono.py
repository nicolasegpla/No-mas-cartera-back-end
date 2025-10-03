from pydantic import BaseModel
from datetime import datetime

class AbonoCreate(BaseModel):
    cliente_id: int
    factura_id: int
    monto_abono: float
    metodo_pago: str

class AbonoResponse(BaseModel):
    id: int
    cliente_id: int
    factura_id: int
    monto_abono: float
    fecha_abono: datetime
    metodo_pago: str

    class Config:
        from_attributes = True  # antes orm_mode
