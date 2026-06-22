from pydantic import BaseModel
from datetime import datetime
from typing import List


# ---------- RF13: LIBRO DIARIO ----------
class MovimientoLibroDiario(BaseModel):
    id: int
    tipo: str
    descripcion: str
    monto: float
    fecha: datetime

    class Config:
        from_attributes = True


class LibroDiarioOut(BaseModel):
    fecha_inicio: datetime
    fecha_fin: datetime
    total_ingresos: float
    total_egresos: float
    balance: float
    movimientos: List[MovimientoLibroDiario]


# ---------- RF14: REGISTRO DE HUESPEDES ----------
class HuespedRegistro(BaseModel):
    reserva_id: int
    cliente_nombre: str
    cliente_cedula: str
    habitacion_numero: str
    fecha_checkin: datetime
    fecha_checkout: datetime
    estado: str

    class Config:
        from_attributes = True


class RegistroHuespedesOut(BaseModel):
    fecha_inicio: datetime
    fecha_fin: datetime
    total_estadias: int
    huespedes: List[HuespedRegistro]


# ---------- RF15: REPORTE DE OCUPACION ----------
class OcupacionPorTipo(BaseModel):
    tipo: str
    total_habitaciones: int
    ocupadas: int
    porcentaje_ocupacion: float


class ReporteOcupacionOut(BaseModel):
    total_habitaciones: int
    total_ocupadas: int
    porcentaje_general: float
    detalle_por_tipo: List[OcupacionPorTipo]
