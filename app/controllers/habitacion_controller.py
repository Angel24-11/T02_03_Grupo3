from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.config.database import get_db
from app.schemas.habitacion_schema import HabitacionCreate, HabitacionOut
from app.services.habitacion_service import HabitacionService

router = APIRouter(prefix="/api/v1/habitaciones", tags=["Módulo de Habitaciones (RF04 - RF05)"])
service = HabitacionService()


@router.post("/", response_model=HabitacionOut, summary="Registrar habitacion [RF04]")
def crear_habitacion(habitacion: HabitacionCreate, db: Session = Depends(get_db)):
    return service.crear_habitacion(db, habitacion)


@router.get("/", response_model=List[HabitacionOut], summary="Listar todas las habitaciones")
def listar_habitaciones(db: Session = Depends(get_db)):
    return service.listar_habitaciones(db)


@router.get("/disponibilidad", response_model=List[HabitacionOut], summary="Consultar disponibilidad en tiempo real [RF05]")
def consultar_disponibilidad(
    fecha_entrada: datetime = Query(..., description="Fecha de entrada"),
    fecha_salida: datetime = Query(..., description="Fecha de salida"),
    tipo: Optional[str] = Query(None, description="Tipo de habitacion: Simple, Doble, Suite"),
    db: Session = Depends(get_db)
):
    return service.consultar_disponibilidad(db, fecha_entrada, fecha_salida, tipo)
