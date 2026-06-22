from sqlalchemy.orm import Session
from app.models.hotel_models import Habitacion, Reserva, EstadoHabitacion
from app.schemas.habitacion_schema import HabitacionCreate
from datetime import datetime
from typing import Optional


class HabitacionRepository:

    def crear(self, db: Session, habitacion_data: HabitacionCreate):
        nueva_habitacion = Habitacion(
            numero=habitacion_data.numero,
            tipo=habitacion_data.tipo,
            precio_noche=habitacion_data.precio_noche,
            estado=habitacion_data.estado
        )
        db.add(nueva_habitacion)
        db.commit()
        db.refresh(nueva_habitacion)
        return nueva_habitacion

    def obtener_todas(self, db: Session):
        return db.query(Habitacion).all()

    def obtener_por_id(self, db: Session, habitacion_id: int):
        return db.query(Habitacion).filter(Habitacion.id == habitacion_id).first()

    # RF05: Disponibilidad en tiempo real filtrada por fechas y tipo
    def consultar_disponibilidad(
        self, db: Session,
        fecha_entrada: datetime,
        fecha_salida: datetime,
        tipo: Optional[str] = None
    ):
        query = db.query(Habitacion).filter(Habitacion.estado == EstadoHabitacion.DISPONIBLE)

        if tipo:
            query = query.filter(Habitacion.tipo == tipo)

        habitaciones_candidatas = query.all()

        # Excluir habitaciones que ya tienen una reserva activa que se cruce con las fechas
        disponibles = []
        for hab in habitaciones_candidatas:
            cruce = db.query(Reserva).filter(
                Reserva.habitacion_id == hab.id,
                Reserva.estado.in_(["Activa", "Check-in Realizado"]),
                Reserva.fecha_checkin < fecha_salida,
                Reserva.fecha_checkout > fecha_entrada
            ).first()
            if not cruce:
                disponibles.append(hab)

        return disponibles
