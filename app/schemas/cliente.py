from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Esquema para crear un cliente
class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    identificacion_tributaria: str

# Esquema de respuesta (lo que devuelve la API)
class ClienteResponse(BaseModel):
    id: int
    empresa_id: int
    nombre: str
    email: EmailStr
    telefono: Optional[str]
    identificacion_tributaria: str
    deuda_total: int
    abonado_total: int
    estado_cartera: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True  # permite que FastAPI convierta desde SQLAlchemy