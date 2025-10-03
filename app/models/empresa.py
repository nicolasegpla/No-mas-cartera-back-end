from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    identificacion_tributaria = Column(String(100), unique=True, nullable=False)
    email_contacto = Column(String(255), unique=True, nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con clientes
    clientes = relationship("Cliente", back_populates="empresa", cascade="all, delete")
    usuarios = relationship("Usuario", back_populates="empresa", cascade="all, delete")
