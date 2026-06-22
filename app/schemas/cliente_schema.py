from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ClienteCreate(BaseModel):
    cedula: str
    nombre: str
    correo: str
    telefono: str
    direccion: str


class ClienteOut(BaseModel):
    id: int
    cedula: str
    nombre: str
    correo: str
    telefono: str
    direccion: str

    class Config:
        from_attributes = True


# RF03: Historial de reservas del cliente
class ReservaHistorial(BaseModel):
    id: int
    habitacion_id: int
    fecha_checkin: datetime
    fecha_checkout: Optional[datetime]
    estado: str

    class Config:
        from_attributes = True


class ClienteHistorialOut(BaseModel):
    cliente: ClienteOut
    historial_reservas: List[ReservaHistorial]
