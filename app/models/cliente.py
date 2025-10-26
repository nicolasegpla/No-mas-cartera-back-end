from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    telefono = Column(String(50), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    identificacion_tributaria = Column(String(100), unique=True, nullable=False)
    deuda_total = Column(Integer, default=0)  # Deuda en centavos para evitar problemas con float
    abonado_total = Column(Integer, default=0)  # Total abonado en centavos
    estado_cartera = Column(Boolean, default=False)  # True si tiene facturas vencidas, False si está al dia o sin facturas vencidas
    
    # Relación con empresa
    empresa = relationship("Empresa", back_populates="clientes")
    facturas = relationship("Factura", back_populates="cliente", cascade="all, delete")
    abonos = relationship("Abono", back_populates="cliente", cascade="all, delete")