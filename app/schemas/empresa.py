from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# 🧩 Base Schema (campos comunes)
class EmpresaBase(BaseModel):
    nombre: str = Field(..., example="Distrines Ltda")
    identificacion_tributaria: str = Field(..., example="900123456-7")
    email_contacto: Optional[EmailStr] = Field(None, example="contacto@distrines.com")
    telefono_contacto: Optional[str] = Field(None, example="+57 3101234567")
    direccion: Optional[str] = Field(None, example="Calle 10 # 25-30")
    pais: Optional[str] = Field(None, example="Colombia")
    ciudad: Optional[str] = Field(None, example="Bogotá")


# 🧾 Schema para creación (registro inicial)
class EmpresaCreate(EmpresaBase):
    password: str = Field(..., min_length=6, example="123456")


# 🔑 Schema para login
class EmpresaLogin(BaseModel):
    email_contacto: EmailStr
    password: str


# 🛠️ Schema para actualización
class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono_contacto: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None
    ciudad: Optional[str] = None
    whatsapp_habilitado: Optional[bool] = None
    activa: Optional[bool] = None


# 📤 Schema de respuesta (sin exponer contraseña)
class EmpresaResponse(EmpresaBase):
    id: int
    activa: bool
    fecha_registro: Optional[datetime] = None
    creada_en: Optional[datetime] = None
    actualizada_en: Optional[datetime] = None
    whatsapp_habilitado: bool
    whatsapp_conectado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Distrines Ltda",
                "identificacion_tributaria": "900123456-7",
                "email_contacto": "contacto@distrines.com",
                "telefono_contacto": "+57 3101234567",
                "direccion": "Calle 10 # 25-30",
                "pais": "Colombia",
                "ciudad": "Bogotá",
                "activa": True,
                "whatsapp_habilitado": False,
                "fecha_registro": "2025-10-25T10:00:00Z",
            }
        }
