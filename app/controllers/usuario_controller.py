from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/api/v1/usuarios", tags=["Módulo de Usuarios (RF01)"])
service = UsuarioService()


@router.post("/", response_model=UsuarioOut, summary="Crear nuevo usuario con perfil de acceso [RF01]")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return service.crear_usuario(db, usuario)


@router.get("/", response_model=List[UsuarioOut], summary="Listar todos los usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return service.listar_usuarios(db)


@router.delete("/{usuario_id}", summary="Deshabilitar usuario [RF01]")
def deshabilitar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    res = service.deshabilitar_usuario(db, usuario_id)
    if not res:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario deshabilitado correctamente"}
