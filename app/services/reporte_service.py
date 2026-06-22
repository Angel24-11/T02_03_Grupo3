from sqlalchemy.orm import Session
from app.repositories.reporte_repository import ReporteRepository
import datetime


class ReporteService:
    def __init__(self):
        self.repository = ReporteRepository()

    def generar_libro_diario(self, db: Session, fecha_inicio: datetime.datetime, fecha_fin: datetime.datetime):
        return self.repository.obtener_libro_diario(db, fecha_inicio, fecha_fin)

    def generar_registro_huespedes(self, db: Session, fecha_inicio: datetime.datetime, fecha_fin: datetime.datetime):
        return self.repository.obtener_registro_huespedes(db, fecha_inicio, fecha_fin)

    def generar_reporte_ocupacion(self, db: Session):
        return self.repository.obtener_reporte_ocupacion(db)
