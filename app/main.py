from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   
from app.config.database import engine, Base
from app.models import hotel_models
from app.controllers import reserva_controller
from app.controllers import factura_controller
from app.controllers import reporte_controller
from app.controllers import usuario_controller
from app.controllers import cliente_controller
from app.controllers import habitacion_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Reservas de Hoteles - UPS",
    description="Estructura estricta: Modelo -> Repositorio -> Servicio -> Controlador",
    version="1.0.0"
)

# CORS: permite que el frontend en React consuma la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AQUI ENCHUFAMOS LOS ENDPOINTS AL SWAGGER:
app.include_router(usuario_controller.router)
app.include_router(cliente_controller.router)
app.include_router(habitacion_controller.router)
app.include_router(reserva_controller.router)
app.include_router(factura_controller.router)
app.include_router(reporte_controller.router)

@app.get("/", tags=["Inicio"])
def home():
    return {
        "estado": "Activo",
        "mensaje": "API del Hotel UPS operativa. Dirígete a /docs para abrir Swagger" #
    }
