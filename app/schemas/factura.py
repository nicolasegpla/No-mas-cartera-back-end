from pydantic import BaseModel
from datetime import datetime, date

class FacturaCreate(BaseModel):
    cliente_id: int
    monto_total: float
    fecha_vencimiento: date

class FacturaResponse(BaseModel):
    id: int
    cliente_id: int
    monto_total: float
    fecha_emision: datetime
    fecha_vencimiento: date
    estado: str

    class Config:
        from_attributes = True  # antes orm_mode

class FacturaDetalleResponse(BaseModel):
    id: int
    cliente_id: int
    monto_total: float
    total_abonado: float
    saldo_pendiente: float
    estado: str
    fecha_emision: datetime
    fecha_vencimiento: date

    class Config:
        from_attributes = True

class FacturaListadoResponse(BaseModel):
    id: int
    cliente_id: int
    monto_total: float
    total_abonado: float
    saldo_pendiente: float
    estado: str
    fecha_emision: datetime
    fecha_vencimiento: date

    class Config:
        from_attributes = True
