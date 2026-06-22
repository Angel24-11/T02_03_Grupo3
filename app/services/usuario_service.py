from sqlalchemy.orm import Session
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate


class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def crear_usuario(self, db: Session, usuario_data: UsuarioCreate):
        return self.repository.crear(db, usuario_data)

    def listar_usuarios(self, db: Session):
        return self.repository.obtener_todos(db)

    def deshabilitar_usuario(self, db: Session, usuario_id: int):
        return self.repository.deshabilitar(db, usuario_id)
