from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Abono(Base):
    __tablename__ = "abonos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    factura_id = Column(Integer, ForeignKey("facturas.id", ondelete="CASCADE"), nullable=False)
    monto_abono = Column(Float, nullable=False)
    fecha_abono = Column(DateTime(timezone=True), server_default=func.now())
    metodo_pago = Column(String(100), nullable=True)  # efectivo, transferencia, tarjeta, etc.

    # Relaciones
    cliente = relationship("Cliente", back_populates="abonos")
    factura = relationship("Factura", back_populates="abonos")
