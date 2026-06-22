from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.hotel_models import EstadoHabitacion


class HabitacionCreate(BaseModel):
    numero: str
    tipo: str  # Simple, Doble, Suite
    precio_noche: float
    estado: EstadoHabitacion = EstadoHabitacion.DISPONIBLE


class HabitacionOut(BaseModel):
    id: int
    numero: str
    tipo: str
    precio_noche: float
    estado: EstadoHabitacion

    class Config:
        from_attributes = True


# RF05: Disponibilidad filtrada por fechas y tipo
class DisponibilidadQuery(BaseModel):
    fecha_entrada: datetime
    fecha_salida: datetime
    tipo: Optional[str] = None
