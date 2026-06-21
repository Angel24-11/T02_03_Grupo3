from sqlalchemy.orm import Session
from app.models.hotel_models import Reserva, Habitacion, EstadoHabitacion
from app.schemas.reserva_schema import ReservaCreate
import datetime

class ReservaRepository:
    def obtener_todas(self, db: Session):
        return db.query(Reserva).all()

    def crear(self, db: Session, reserva_data: ReservaCreate):
        nueva_reserva = Reserva(
            cliente_id=reserva_data.cliente_id,
            habitacion_id=reserva_data.habitacion_id,
            fecha_checkin=datetime.datetime.utcnow(),
            fecha_checkout=reserva_data.fecha_checkout,
            estado="Activa"
        )
        db.add(nueva_reserva)
        db.commit()
        db.refresh(nueva_reserva)
        return nueva_reserva

    def checkin(self, db: Session, reserva_id: int):
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            return None
        
        # RF08: Actualizar estado de la habitacion a Ocupada
        habitacion = db.query(Habitacion).filter(Habitacion.id == reserva.habitacion_id).first()
        if habitacion:
            habitacion.estado = EstadoHabitacion.OCUPADA
            db.commit()

        reserva.estado = "Check-in Realizado"
        db.commit()
        db.refresh(reserva)
        return reserva

    def checkout(self, db: Session, reserva_id: int):
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            return None
        
        # RF09: Volver a liberar la habitacion a Disponible
        habitacion = db.query(Habitacion).filter(Habitacion.id == reserva.habitacion_id).first()
        if habitacion:
            habitacion.estado = EstadoHabitacion.DISPONIBLE
            db.commit()

        reserva.estado = "Completada"
        db.commit()
        db.refresh(reserva)
        return reserva