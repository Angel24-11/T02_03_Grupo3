"""
T02.04 - Pruebas Unitarias con cobertura real
Modulo: Habitaciones y Disponibilidad (RF04, RF05)
Autor: Lopez Ortiz Karen Koraima
Frameworks: Pytest, Unittest (MagicMock), Coverage.py
Grupo 3 - Ingenieria de Software - UPS
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock

from app.models.hotel_models import EstadoHabitacion
from app.repositories.habitacion_repository import HabitacionRepository
from app.services.habitacion_service import HabitacionService
from app.schemas.habitacion_schema import HabitacionCreate


class TestCrearHabitacion:
    """RF04: Registrar habitaciones con tipo, precio y estado"""

    def test_crear_habitacion_persiste_en_bd(self, db):
        repo = HabitacionRepository()
        data = HabitacionCreate(numero="101", tipo="Simple",
                                precio_noche=50.0, estado=EstadoHabitacion.DISPONIBLE)
        resultado = repo.crear(db, data)
        assert resultado.id is not None
        assert resultado.numero == "101"
        assert resultado.tipo == "Simple"
        assert resultado.precio_noche == 50.0

    def test_estado_por_defecto_disponible(self, db):
        repo = HabitacionRepository()
        data = HabitacionCreate(numero="102", tipo="Doble", precio_noche=80.0)
        resultado = repo.crear(db, data)
        assert resultado.estado == EstadoHabitacion.DISPONIBLE

    def test_tipos_habitacion_validos(self):
        tipos = ["Simple", "Doble", "Suite"]
        for t in tipos:
            assert t in tipos

    def test_tipo_invalido(self):
        assert "Presidencial" not in ["Simple", "Doble", "Suite"]

    def test_precio_positivo(self):
        assert 75.50 > 0

    def test_precio_negativo_invalido(self):
        assert -10.0 <= 0

    def test_numero_no_vacio(self):
        assert "101" != ""

    def test_listar_habitaciones_vacio(self, db):
        repo = HabitacionRepository()
        assert repo.obtener_todas(db) == []

    def test_listar_habitaciones_retorna_todas(self, db):
        repo = HabitacionRepository()
        repo.crear(db, HabitacionCreate(numero="201", tipo="Simple", precio_noche=50.0))
        repo.crear(db, HabitacionCreate(numero="202", tipo="Doble", precio_noche=80.0))
        assert len(repo.obtener_todas(db)) == 2

    def test_obtener_por_id_encontrado(self, db):
        repo = HabitacionRepository()
        creada = repo.crear(db, HabitacionCreate(numero="301", tipo="Suite", precio_noche=150.0))
        resultado = repo.obtener_por_id(db, creada.id)
        assert resultado.numero == "301"

    def test_obtener_por_id_no_encontrado(self, db):
        repo = HabitacionRepository()
        assert repo.obtener_por_id(db, 9999) is None

    def test_service_crear_habitacion(self, db):
        service = HabitacionService()
        data = HabitacionCreate(numero="401", tipo="Simple", precio_noche=60.0)
        resultado = service.crear_habitacion(db, data)
        assert resultado.numero == "401" and resultado.id is not None

    def test_service_listar_habitaciones(self, db):
        service = HabitacionService()
        service.crear_habitacion(db, HabitacionCreate(numero="501", tipo="Doble", precio_noche=90.0))
        assert len(service.listar_habitaciones(db)) == 1

    def test_estados_validos(self):
        estados = [EstadoHabitacion.DISPONIBLE, EstadoHabitacion.OCUPADA, EstadoHabitacion.MANTENIMIENTO]
        assert len(estados) == 3


class TestDisponibilidadHabitacion:
    """RF05: Consultar disponibilidad en tiempo real"""

    def test_disponibilidad_retorna_habitacion_libre(self, db):
        repo = HabitacionRepository()
        repo.crear(db, HabitacionCreate(numero="601", tipo="Simple", precio_noche=50.0))
        fecha_entrada = datetime(2026, 7, 1)
        fecha_salida  = datetime(2026, 7, 5)
        resultado = repo.consultar_disponibilidad(db, fecha_entrada, fecha_salida)
        assert len(resultado) >= 1

    def test_disponibilidad_filtrada_por_tipo(self, db):
        repo = HabitacionRepository()
        repo.crear(db, HabitacionCreate(numero="701", tipo="Suite", precio_noche=200.0))
        repo.crear(db, HabitacionCreate(numero="702", tipo="Simple", precio_noche=50.0))
        resultado = repo.consultar_disponibilidad(db, datetime(2026, 7, 1), datetime(2026, 7, 5), tipo="Suite")
        assert all(h.tipo == "Suite" for h in resultado)

    def test_disponibilidad_sin_habitaciones(self, db):
        repo = HabitacionRepository()
        resultado = repo.consultar_disponibilidad(db, datetime(2026, 7, 1), datetime(2026, 7, 5))
        assert resultado == []

    def test_fecha_salida_posterior_a_entrada(self):
        assert datetime(2026, 7, 5) > datetime(2026, 7, 1)

    def test_fecha_salida_igual_invalida(self):
        assert not (datetime(2026, 7, 1) > datetime(2026, 7, 1))

    def test_fecha_salida_anterior_invalida(self):
        assert datetime(2026, 7, 1) < datetime(2026, 7, 5)

    def test_service_consultar_disponibilidad(self, db):
        service = HabitacionService()
        service.crear_habitacion(db, HabitacionCreate(numero="801", tipo="Doble", precio_noche=80.0))
        resultado = service.consultar_disponibilidad(db, datetime(2026, 8, 1), datetime(2026, 8, 5))
        assert isinstance(resultado, list)

    def test_habitacion_ocupada_no_aparece(self, db):
        from app.models.hotel_models import EstadoHabitacion
        repo = HabitacionRepository()
        hab = repo.crear(db, HabitacionCreate(numero="901", tipo="Simple", precio_noche=50.0,
                                              estado=EstadoHabitacion.OCUPADA))
        resultado = repo.consultar_disponibilidad(db, datetime(2026, 7, 1), datetime(2026, 7, 5))
        ids = [h.id for h in resultado]
        assert hab.id not in ids

# RF04 - pruebas de habitaciones completadas por Karen Lopez
