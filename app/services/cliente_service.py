from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def crear_cliente(self, db: Session, cliente_data: ClienteCreate):
        return self.repository.crear(db, cliente_data)

    def listar_clientes(self, db: Session):
        return self.repository.obtener_todos(db)

    def obtener_historial(self, db: Session, cliente_id: int):
        return self.repository.obtener_historial(db, cliente_id)
