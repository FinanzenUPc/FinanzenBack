from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)  # ingreso/egreso
    categoria = Column(String, nullable=False)
    subcategoria = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    metodo_pago = Column(String, nullable=True)
    monto = Column(Float, nullable=False)
    usuario = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    # user = relationship("User", back_populates="transactions")
