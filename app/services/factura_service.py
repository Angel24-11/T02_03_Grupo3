from sqlalchemy.orm import Session
from app.repositories.factura_repository import (
    FacturaRepository, PagoRepository, MovimientoRepository
)


class FacturaService:
    def __init__(self):
        self.repository = FacturaRepository()

    def emitir_factura(self, db: Session, reserva_id: int):
        return self.repository.crear_factura(db, reserva_id)

    def listar_facturas(self, db: Session):
        return self.repository.obtener_todas(db)

    def obtener_factura(self, db: Session, factura_id: int):
        return self.repository.obtener_por_id(db, factura_id)


class PagoService:
    def __init__(self):
        self.repository = PagoRepository()

    def registrar_pago(self, db: Session, factura_id: int, monto: float, metodo_pago):
        return self.repository.registrar_pago(db, factura_id, monto, metodo_pago)

    def listar_pagos(self, db: Session):
        return self.repository.obtener_todos(db)


class MovimientoService:
    def __init__(self):
        self.repository = MovimientoRepository()

    def listar_movimientos(self, db: Session, fecha_inicio=None, fecha_fin=None):
        return self.repository.obtener_todos(db, fecha_inicio, fecha_fin)
