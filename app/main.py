from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import hotel_models
# Importamos tu nuevo controlador:
from app.controllers import reserva_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Reservas de Hoteles - UPS", #
    description="Estructura estricta: Modelo -> Repositorio -> Servicio -> Controlador", #
    version="1.0.0"
)

# AQUI ENCHUFAMOS TUS 4 ENDPOINTS AL SWAGGER:
app.include_router(reserva_controller.router)

@app.get("/", tags=["Inicio"])
def home():
    return {
        "estado": "Activo",
        "mensaje": "API del Hotel UPS operativa. Dirígete a /docs para abrir Swagger" #
    }