from sqlalchemy.orm import Session
from app.models.hotel_models import (
    Factura, Pago, MovimientoContable,
    Reserva, Habitacion, TipoMovimiento
)
import datetime


class FacturaRepository:

    # RF10: Emitir factura calculando noches * precio_noche
    def crear_factura(self, db: Session, reserva_id: int):
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            return None

        habitacion = db.query(Habitacion).filter(
            Habitacion.id == reserva.habitacion_id
        ).first()

        # Calcular noches entre checkin y checkout
        noches = (reserva.fecha_checkout - reserva.fecha_checkin).days
        if noches <= 0:
            noches = 1  # mínimo una noche

        subtotal = noches * habitacion.precio_noche
        impuestos = round(subtotal * 0.15, 2)  # IVA Ecuador 15%
        total = subtotal + impuestos

        nueva_factura = Factura(
            reserva_id=reserva_id,
            fecha_emision=datetime.datetime.utcnow(),
            subtotal=subtotal,
            impuestos=impuestos,
            total=total,
            estado="Pendiente"
        )
        db.add(nueva_factura)
        db.commit()
        db.refresh(nueva_factura)
        return nueva_factura

    def obtener_todas(self, db: Session):
        return db.query(Factura).all()

    def obtener_por_id(self, db: Session, factura_id: int):
        return db.query(Factura).filter(Factura.id == factura_id).first()


class PagoRepository:

    # RF11: Registrar pago y generar comprobante
    def registrar_pago(self, db: Session, factura_id: int, monto: float, metodo_pago):
        factura = db.query(Factura).filter(Factura.id == factura_id).first()
        if not factura:
            return None

        nuevo_pago = Pago(
            factura_id=factura_id,
            monto=monto,
            metodo_pago=metodo_pago,
            fecha_pago=datetime.datetime.utcnow()
        )
        db.add(nuevo_pago)
        db.commit()
        db.refresh(nuevo_pago)

        # Si el pago cubre el total, marcar factura como Pagada
        if monto >= factura.total:
            factura.estado = "Pagada"
            db.commit()

        # RF12: Generar movimiento contable automático (Ingreso)
        movimiento = MovimientoContable(
            pago_id=nuevo_pago.id,
            tipo=TipoMovimiento.INGRESO,
            descripcion=f"Pago factura #{factura_id} - {metodo_pago.value}",
            monto=monto,
            fecha=datetime.datetime.utcnow()
        )
        db.add(movimiento)
        db.commit()

        return nuevo_pago

    def obtener_todos(self, db: Session):
        return db.query(Pago).all()


class MovimientoRepository:

    def obtener_todos(self, db: Session, fecha_inicio=None, fecha_fin=None):
        query = db.query(MovimientoContable)
        if fecha_inicio:
            query = query.filter(MovimientoContable.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(MovimientoContable.fecha <= fecha_fin)
        return query.all()
