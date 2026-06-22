from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import hotel_models
# Importamos los controladores:
from app.controllers import reserva_controller
from app.controllers import factura_controller
from app.controllers import reporte_controller  # <-- NUEVO: reportes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Reservas de Hoteles - UPS", #
    description="Estructura estricta: Modelo -> Repositorio -> Servicio -> Controlador", #
    version="1.0.0"
)

# AQUI ENCHUFAMOS LOS ENDPOINTS AL SWAGGER:
app.include_router(reserva_controller.router)
app.include_router(factura_controller.router)
app.include_router(reporte_controller.router)  # <-- NUEVO: reportes

@app.get("/", tags=["Inicio"])
def home():
    return {
        "estado": "Activo",
        "mensaje": "API del Hotel UPS operativa. Dirígete a /docs para abrir Swagger" #
    }
