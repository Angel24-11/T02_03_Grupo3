from pydantic import BaseModel
from datetime import datetime

class ReservaBase(BaseModel):
    cliente_id: int
    habitacion_id: int
    fecha_checkout: datetime

class ReservaCreate(ReservaBase):
    pass

class ReservaOut(ReservaBase):
    id: int
    fecha_checkin: datetime
    estado: str

    class Config:
        orm_mode = True