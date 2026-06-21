from fastapi import FastAPI
from app.config.database import engine, Base
# Importamos los modelos para que SQLAlchemy los lea y sepa qué tablas crear
from app.models import hotel_models 

# ESTA ES LA LÍNEA QUE HACE EL "PARTO" DE LA BASE DE DATOS:
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Reservas de Hoteles - UPS",
    description="Estructura: Modelo -> Repositorio -> Servicio -> Controlador",
    version="1.0.0"
)

@app.get("/", tags=["Inicio"])
def home():
    return {
        "estado": "Activo",
        "mensaje": "Bienvenido a la API del Hotel UPS",
        "documentacion_swagger": "Ingresa a http://127.0.0.1:8000/docs en tu navegador"
    }