from pydantic import BaseModel
from app.models.hotel_models import RolUsuario


class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    password: str
    rol: RolUsuario = RolUsuario.RECEPCIONISTA


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: RolUsuario

    class Config:
        from_attributes = True
