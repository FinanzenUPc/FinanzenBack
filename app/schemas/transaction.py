from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class TransactionBase(BaseModel):
    fecha: date
    tipo: str  # ingreso/egreso
    categoria: str
    subcategoria: Optional[str] = None
    descripcion: Optional[str] = None
    metodo_pago: Optional[str] = None
    monto: float
    usuario: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    fecha: Optional[date] = None
    tipo: Optional[str] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    descripcion: Optional[str] = None
    metodo_pago: Optional[str] = None
    monto: Optional[float] = None
    usuario: Optional[str] = None


class TransactionInDB(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Transaction(TransactionInDB):
    pass


class TransactionPaginatedResponse(BaseModel):
    """Paginated response for transactions."""
    data: List[Transaction]
    total: int
    skip: int
    limit: int

    class Config:
        from_attributes = True
