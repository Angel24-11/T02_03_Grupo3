from sqlalchemy.orm import Session
from app.repositories.habitacion_repository import HabitacionRepository
from app.schemas.habitacion_schema import HabitacionCreate
from datetime import datetime
from typing import Optional


class HabitacionService:
    def __init__(self):
        self.repository = HabitacionRepository()

    def crear_habitacion(self, db: Session, habitacion_data: HabitacionCreate):
        return self.repository.crear(db, habitacion_data)

    def listar_habitaciones(self, db: Session):
        return self.repository.obtener_todas(db)

    def consultar_disponibilidad(
        self, db: Session,
        fecha_entrada: datetime,
        fecha_salida: datetime,
        tipo: Optional[str] = None
    ):
        return self.repository.consultar_disponibilidad(db, fecha_entrada, fecha_salida, tipo)
