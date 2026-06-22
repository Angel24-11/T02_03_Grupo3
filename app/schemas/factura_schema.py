from pydantic import BaseModel
from datetime import datetime
from app.models.hotel_models import MetodoPago, TipoMovimiento


# ---------- FACTURA ----------
class FacturaCreate(BaseModel):
    reserva_id: int


class FacturaOut(BaseModel):
    id: int
    reserva_id: int
    fecha_emision: datetime
    subtotal: float
    impuestos: float
    total: float
    estado: str

    class Config:
        from_attributes = True


# ---------- PAGO ----------
class PagoCreate(BaseModel):
    factura_id: int
    monto: float
    metodo_pago: MetodoPago


class PagoOut(BaseModel):
    id: int
    factura_id: int
    monto: float
    metodo_pago: MetodoPago
    fecha_pago: datetime

    class Config:
        from_attributes = True


# ---------- MOVIMIENTO CONTABLE ----------
class MovimientoOut(BaseModel):
    id: int
    pago_id: int | None
    tipo: TipoMovimiento
    descripcion: str
    monto: float
    fecha: datetime

    class Config:
        from_attributes = True
