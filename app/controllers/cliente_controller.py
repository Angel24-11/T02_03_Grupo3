from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.schemas.cliente_schema import ClienteCreate, ClienteOut, ClienteHistorialOut
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/api/v1/clientes", tags=["Módulo de Clientes (RF02 - RF03)"])
service = ClienteService()


@router.post("/", response_model=ClienteOut, summary="Registrar nuevo cliente/huesped [RF02]")
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return service.crear_cliente(db, cliente)


@router.get("/", response_model=List[ClienteOut], summary="Listar todos los clientes")
def listar_clientes(db: Session = Depends(get_db)):
    return service.listar_clientes(db)


@router.get("/{cliente_id}/historial", response_model=ClienteHistorialOut, summary="Historial de reservas del cliente [RF03]")
def obtener_historial(cliente_id: int, db: Session = Depends(get_db)):
    res = service.obtener_historial(db, cliente_id)
    if not res:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return res
