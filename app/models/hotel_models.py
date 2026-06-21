from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
import datetime
from app.config.database import Base

class EstadoHabitacion(str, enum.Enum):
    DISPONIBLE = "Disponible"
    OCUPADA = "Ocupada"
    MANTENIMIENTO = "Mantenimiento"

class RolUsuario(str, enum.Enum):
    ADMIN = "Administrador"
    RECEPCIONISTA = "Recepcionista"
    ENCARGADO = "Encargado de Habitaciones"
    GERENTE = "Gerente"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    password_hash = Column(String)
    rol = Column(Enum(RolUsuario), default=RolUsuario.RECEPCIONISTA)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True) #
    nombre = Column(String) #
    correo = Column(String) #
    telefono = Column(String) #
    direccion = Column(String) #

class Habitacion(Base):
    __tablename__ = "habitaciones"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True)
    tipo = Column(String) # Simple, Doble, Suite
    precio_noche = Column(Float)
    estado = Column(Enum(EstadoHabitacion), default=EstadoHabitacion.DISPONIBLE)

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    habitacion_id = Column(Integer, ForeignKey("habitaciones.id"))
    fecha_checkin = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_checkout = Column(DateTime)
    estado = Column(String, default="Activa") # Activa, Completada, Cancelada

    cliente = relationship("Cliente")
    habitacion = relationship("Habitacion")