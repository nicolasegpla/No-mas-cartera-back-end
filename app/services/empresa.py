from sqlalchemy.orm import Session
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate
from app.core.security import hash_password, verify_password


def crear_empresa(db: Session, data: EmpresaCreate):
    empresa = Empresa(
        nombre=data.nombre,
        identificacion_tributaria=data.identificacion_tributaria,
        email_contacto=data.email_contacto,
        hashed_password=hash_password(data.password),
        telefono_contacto=data.telefono_contacto,
        direccion=data.direccion,
        pais=data.pais,
        ciudad=data.ciudad,
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa


def autenticar_empresa(db: Session, email: str, password: str):
    empresa = db.query(Empresa).filter(Empresa.email_contacto == email).first()
    if not empresa:
        return None
    if not verify_password(password, empresa.hashed_password):
        return None
    return empresa
