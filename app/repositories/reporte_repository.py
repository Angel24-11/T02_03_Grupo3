from sqlalchemy.orm import Session
from app.models.hotel_models import (
    MovimientoContable, Reserva, Cliente, Habitacion,
    TipoMovimiento, EstadoHabitacion
)
import datetime


class ReporteRepository:

    # RF13: Libro Diario
    def obtener_libro_diario(self, db: Session, fecha_inicio: datetime.datetime, fecha_fin: datetime.datetime):
        movimientos = db.query(MovimientoContable).filter(
            MovimientoContable.fecha >= fecha_inicio,
            MovimientoContable.fecha <= fecha_fin
        ).all()

        total_ingresos = sum(m.monto for m in movimientos if m.tipo == TipoMovimiento.INGRESO)
        total_egresos = sum(m.monto for m in movimientos if m.tipo == TipoMovimiento.EGRESO)

        return {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "balance": total_ingresos - total_egresos,
            "movimientos": movimientos
        }

    # RF14: Registro de Huespedes
    def obtener_registro_huespedes(self, db: Session, fecha_inicio: datetime.datetime, fecha_fin: datetime.datetime):
        reservas = db.query(Reserva).filter(
            Reserva.fecha_checkin >= fecha_inicio,
            Reserva.fecha_checkin <= fecha_fin
        ).all()

        huespedes = []
        for r in reservas:
            cliente = db.query(Cliente).filter(Cliente.id == r.cliente_id).first()
            habitacion = db.query(Habitacion).filter(Habitacion.id == r.habitacion_id).first()
            huespedes.append({
                "reserva_id": r.id,
                "cliente_nombre": cliente.nombre if cliente else "N/A",
                "cliente_cedula": cliente.cedula if cliente else "N/A",
                "habitacion_numero": habitacion.numero if habitacion else "N/A",
                "fecha_checkin": r.fecha_checkin,
                "fecha_checkout": r.fecha_checkout,
                "estado": r.estado
            })

        return {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "total_estadias": len(huespedes),
            "huespedes": huespedes
        }

    # RF15: Reporte de Ocupacion
    def obtener_reporte_ocupacion(self, db: Session):
        habitaciones = db.query(Habitacion).all()
        total_habitaciones = len(habitaciones)
        total_ocupadas = len([h for h in habitaciones if h.estado == EstadoHabitacion.OCUPADA])

        # Agrupar por tipo
        tipos = {}
        for h in habitaciones:
            if h.tipo not in tipos:
                tipos[h.tipo] = {"total": 0, "ocupadas": 0}
            tipos[h.tipo]["total"] += 1
            if h.estado == EstadoHabitacion.OCUPADA:
                tipos[h.tipo]["ocupadas"] += 1

        detalle = []
        for tipo, datos in tipos.items():
            porcentaje = (datos["ocupadas"] / datos["total"] * 100) if datos["total"] > 0 else 0
            detalle.append({
                "tipo": tipo,
                "total_habitaciones": datos["total"],
                "ocupadas": datos["ocupadas"],
                "porcentaje_ocupacion": round(porcentaje, 2)
            })

        porcentaje_general = (total_ocupadas / total_habitaciones * 100) if total_habitaciones > 0 else 0

        return {
            "total_habitaciones": total_habitaciones,
            "total_ocupadas": total_ocupadas,
            "porcentaje_general": round(porcentaje_general, 2),
            "detalle_por_tipo": detalle
        }
