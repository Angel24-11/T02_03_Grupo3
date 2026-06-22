from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.config.database import get_db
from app.schemas.reporte_schema import (
    LibroDiarioOut, RegistroHuespedesOut, ReporteOcupacionOut
)
from app.services.reporte_service import ReporteService

router = APIRouter(prefix="/api/v1/reportes", tags=["Módulo de Reportes (RF13 - RF15)"])
service = ReporteService()


@router.get("/libro-diario", response_model=LibroDiarioOut, summary="Reporte de Libro Diario [RF13]")
def libro_diario(
    fecha_inicio: datetime = Query(..., description="Fecha de inicio del período"),
    fecha_fin: datetime = Query(..., description="Fecha de fin del período"),
    db: Session = Depends(get_db)
):
    return service.generar_libro_diario(db, fecha_inicio, fecha_fin)


@router.get("/registro-huespedes", response_model=RegistroHuespedesOut, summary="Registro de Huéspedes [RF14]")
def registro_huespedes(
    fecha_inicio: datetime = Query(..., description="Fecha de inicio del período"),
    fecha_fin: datetime = Query(..., description="Fecha de fin del período"),
    db: Session = Depends(get_db)
):
    return service.generar_registro_huespedes(db, fecha_inicio, fecha_fin)


@router.get("/ocupacion", response_model=ReporteOcupacionOut, summary="Reporte de Ocupación por tipo [RF15]")
def reporte_ocupacion(db: Session = Depends(get_db)):
    return service.generar_reporte_ocupacion(db)
