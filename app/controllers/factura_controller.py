from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.config.database import get_db
from app.schemas.factura_schema import (
    FacturaCreate, FacturaOut, PagoCreate, PagoOut, MovimientoOut
)
from app.services.factura_service import (
    FacturaService, PagoService, MovimientoService
)

router = APIRouter(prefix="/api/v1", tags=["Módulo de Facturación y Contabilidad (RF10 - RF12)"])

factura_service = FacturaService()
pago_service = PagoService()
movimiento_service = MovimientoService()


# ---------- FACTURAS ----------
@router.post("/facturas/", response_model=FacturaOut, summary="Emitir factura desde una reserva [RF10]")
def emitir_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    res = factura_service.emitir_factura(db, factura.reserva_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return res


@router.get("/facturas/", response_model=List[FacturaOut], summary="Listar todas las facturas")
def listar_facturas(db: Session = Depends(get_db)):
    return factura_service.listar_facturas(db)


@router.get("/facturas/{factura_id}", response_model=FacturaOut, summary="Obtener una factura por ID")
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    res = factura_service.obtener_factura(db, factura_id)
    if not res:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return res


# ---------- PAGOS ----------
@router.post("/pagos/", response_model=PagoOut, summary="Registrar pago y generar comprobante [RF11]")
def registrar_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    res = pago_service.registrar_pago(db, pago.factura_id, pago.monto, pago.metodo_pago)
    if not res:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return res


@router.get("/pagos/", response_model=List[PagoOut], summary="Listar todos los pagos")
def listar_pagos(db: Session = Depends(get_db)):
    return pago_service.listar_pagos(db)


# ---------- MOVIMIENTOS CONTABLES ----------
@router.get("/movimientos/", response_model=List[MovimientoOut], summary="Diario contable de ingresos/egresos [RF12]")
def listar_movimientos(
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    return movimiento_service.listar_movimientos(db, fecha_inicio, fecha_fin)
