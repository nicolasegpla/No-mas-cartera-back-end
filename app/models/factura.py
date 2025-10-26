from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    monto_total = Column(Float, nullable=False)
    fecha_emision = Column(DateTime(timezone=True), server_default=func.now())
    fecha_vencimiento = Column(DateTime(timezone=True), nullable=False)
    numero_factura = Column(String(100), unique=True, nullable=False)
    estado = Column(String(50), default="pendiente")  # pendiente, pagada, vencida

    # Relaciones
    cliente = relationship("Cliente", back_populates="facturas")
    abonos = relationship("Abono", back_populates="factura", cascade="all, delete")
