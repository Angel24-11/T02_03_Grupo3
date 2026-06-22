from sqlalchemy.orm import Session
from app.models.hotel_models import Usuario
from app.schemas.usuario_schema import UsuarioCreate
import hashlib


class UsuarioRepository:

    def _hash_password(self, password: str) -> str:
        # Hash simple con sal fija de ejemplo (en produccion usar bcrypt/passlib)
        sal = "ups_hotel_salt"
        return hashlib.sha256((password + sal).encode()).hexdigest()

    def crear(self, db: Session, usuario_data: UsuarioCreate):
        nuevo_usuario = Usuario(
            nombre=usuario_data.nombre,
            correo=usuario_data.correo,
            password_hash=self._hash_password(usuario_data.password),
            rol=usuario_data.rol
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    def obtener_todos(self, db: Session):
        return db.query(Usuario).all()

    def obtener_por_id(self, db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def deshabilitar(self, db: Session, usuario_id: int):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return None
        db.delete(usuario)
        db.commit()
        return usuario
