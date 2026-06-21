from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.reserva_schema import ReservaCreate, ReservaOut
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/api/v1/reservas", tags=["Módulo de Reservas (RF06 - RF09)"])
service = ReservaService()

@router.get("/", response_model=List[ReservaOut], summary="Obtener todas las reservas")
def listar_reservas(db: Session = Depends(get_db)):
    return service.obtener_reservas(db)

@router.post("/", response_model=ReservaOut, summary="Crear nueva reserva [RF06]")
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    return service.registrar_reserva(db, reserva)

@router.put("/{reserva_id}/checkin", summary="Ejecutar Check-in de huésped [RF08]")
def hacer_checkin(reserva_id: int, db: Session = Depends(get_db)):
    res = service.procesar_checkin(db, reserva_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return res

@router.put("/{reserva_id}/checkout", summary="Ejecutar Check-out y liberar habitación [RF09]")
def hacer_checkout(reserva_id: int, db: Session = Depends(get_db)):
    res = service.procesar_checkout(db, reserva_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return res