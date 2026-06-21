from sqlalchemy.orm import Session
from app.repositories.reserva_repository import ReservaRepository
from app.schemas.reserva_schema import ReservaCreate

class ReservaService:
    def __init__(self):
        self.repository = ReservaRepository()

    def obtener_reservas(self, db: Session):
        return self.repository.obtener_todas(db)

    def registrar_reserva(self, db: Session, reserva_data: ReservaCreate):
        return self.repository.crear(db, reserva_data)

    def procesar_checkin(self, db: Session, reserva_id: int):
        return self.repository.checkin(db, reserva_id)

    def procesar_checkout(self, db: Session, reserva_id: int):
        return self.repository.checkout(db, reserva_id)