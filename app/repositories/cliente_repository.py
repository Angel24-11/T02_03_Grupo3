from sqlalchemy.orm import Session
from app.models.hotel_models import Cliente, Reserva
from app.schemas.cliente_schema import ClienteCreate


class ClienteRepository:

    def crear(self, db: Session, cliente_data: ClienteCreate):
        nuevo_cliente = Cliente(
            cedula=cliente_data.cedula,
            nombre=cliente_data.nombre,
            correo=cliente_data.correo,
            telefono=cliente_data.telefono,
            direccion=cliente_data.direccion
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente

    def obtener_todos(self, db: Session):
        return db.query(Cliente).all()

    def obtener_por_id(self, db: Session, cliente_id: int):
        return db.query(Cliente).filter(Cliente.id == cliente_id).first()

    # RF03: Historial completo de reservas del cliente
    def obtener_historial(self, db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            return None
        reservas = db.query(Reserva).filter(Reserva.cliente_id == cliente_id).all()
        return {
            "cliente": cliente,
            "historial_reservas": reservas
        }
