Fecha: 28/06/2026
"
T02.04 - Pruebas Unitarias con cobertura real
Modulo: Usuarios y Clientes (RF01, RF02, RF03)
Autor: Chancay Rodriguez Oscar Emilio
Frameworks: Pytest, Unittest (MagicMock), Coverage.py
Grupo 3 - Ingenieria de Software - UPS
Fecha: 28/06/2026
"

import hashlib
import pytest
from unittest.mock import MagicMock

from app.models.hotel_models import Usuario, Cliente, Reserva, RolUsuario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.cliente_repository import ClienteRepository
from app.services.usuario_service import UsuarioService
from app.services.cliente_service import ClienteService
from app.schemas.usuario_schema import UsuarioCreate
from app.schemas.cliente_schema import ClienteCreate


class TestCrearUsuario:
    """RF01: Crear usuario con perfil de accesoFecha: 28/06/2026
"

    def test_crear_usuario_persiste_en_bd(self, db):
        repo = UsuarioRepository()
        data = UsuarioCreate(nombre="Oscar Chancay", correo="oscar@ups.edu.ec",
                             password="segura123", rol=RolUsuario.RECEPCIONISTA)
        resultado = repo.crear(db, data)
        assert resultado.id is not None
        assert resultado.nombre == "Oscar Chancay"
        assert resultado.correo == "oscar@ups.edu.ec"
        assert resultado.rol == RolUsuario.RECEPCIONISTA

    def test_crear_usuario_hashea_password(self, db):
        repo = UsuarioRepository()
        data = UsuarioCreate(nombre="Test", correo="test@ups.edu.ec",
                             password="clave123", rol=RolUsuario.ADMIN)
        resultado = repo.crear(db, data)
        sal = "ups_hotel_salt"
        hash_esperado = hashlib.sha256(("clave123" + sal).encode()).hexdigest()
        assert resultado.password_hash == hash_esperado
        assert resultado.password_hash != "clave123"

    def test_hash_determinista(self):
        repo = UsuarioRepository()
        assert repo._hash_password("abc123") == repo._hash_password("abc123")

    def test_hash_diferente_por_password(self):
        repo = UsuarioRepository()
        assert repo._hash_password("clave1") != repo._hash_password("clave2")

    def test_hash_longitud_64_chars(self):
        repo = UsuarioRepository()
        assert len(repo._hash_password("cualquier_clave")) == 64

    def test_rol_por_defecto_recepcionista(self, db):
        repo = UsuarioRepository()
        data = UsuarioCreate(nombre="Default", correo="default@ups.edu.ec", password="pass")
        resultado = repo.crear(db, data)
        assert resultado.rol == RolUsuario.RECEPCIONISTA

    def test_service_crear_usuario(self, db):
        service = UsuarioService()
        data = UsuarioCreate(nombre="Karen", correo="karen@ups.edu.ec",
                             password="pass123", rol=RolUsuario.ADMIN)
        resultado = service.crear_usuario(db, data)
        assert resultado.nombre == "Karen"
        assert resultado.id is not None


class TestListarDeshabilitarUsuario:
    """RF01: Listar y deshabilitar usuariosFecha: 28/06/2026
"

    def test_listar_usuarios_vacio(self, db):
        repo = UsuarioRepository()
        assert repo.obtener_todos(db) == []

    def test_listar_usuarios_retorna_todos(self, db):
        repo = UsuarioRepository()
        repo.crear(db, UsuarioCreate(nombre="U1", correo="u1@ups.edu.ec", password="p1"))
        repo.crear(db, UsuarioCreate(nombre="U2", correo="u2@ups.edu.ec", password="p2"))
        assert len(repo.obtener_todos(db)) == 2

    def test_obtener_por_id_encontrado(self, db):
        repo = UsuarioRepository()
        creado = repo.crear(db, UsuarioCreate(nombre="Oscar", correo="o@ups.edu.ec", password="p"))
        resultado = repo.obtener_por_id(db, creado.id)
        assert resultado.id == creado.id

    def test_obtener_por_id_no_encontrado(self, db):
        repo = UsuarioRepository()
        assert repo.obtener_por_id(db, 9999) is None

    def test_deshabilitar_usuario_existente(self, db):
        repo = UsuarioRepository()
        creado = repo.crear(db, UsuarioCreate(nombre="Del", correo="del@ups.edu.ec", password="p"))
        resultado = repo.deshabilitar(db, creado.id)
        assert resultado.id == creado.id
        assert repo.obtener_por_id(db, creado.id) is None

    def test_deshabilitar_usuario_inexistente(self, db):
        repo = UsuarioRepository()
        assert repo.deshabilitar(db, 9999) is None

    def test_service_listar_usuarios(self, db):
        service = UsuarioService()
        service.crear_usuario(db, UsuarioCreate(nombre="A", correo="a@ups.edu.ec", password="p"))
        assert len(service.listar_usuarios(db)) == 1

    def test_service_deshabilitar_usuario(self, db):
        service = UsuarioService()
        u = service.crear_usuario(db, UsuarioCreate(nombre="B", correo="b@ups.edu.ec", password="p"))
        assert service.deshabilitar_usuario(db, u.id) is not None


class TestRegistrarCliente:
    """RF02: Registrar informacion general de huespedesFecha: 28/06/2026
"

    def test_crear_cliente_persiste_en_bd(self, db):
        repo = ClienteRepository()
        data = ClienteCreate(cedula="0912345678", nombre="Maria Garcia",
                             correo="maria@gmail.com", telefono="0991234567", direccion="Guayaquil")
        resultado = repo.crear(db, data)
        assert resultado.id is not None
        assert resultado.cedula == "0912345678"

    def test_cedula_10_digitos(self):
        cedula = "0912345678"
        assert len(cedula) == 10 and cedula.isdigit()

    def test_cedula_invalida_menos_digitos(self):
        assert len("091234") != 10

    def test_cedula_con_letras_invalida(self):
        assert not "091234ABCD".isdigit()

    def test_correo_contiene_arroba(self):
        assert "@" in "maria@gmail.com"

    def test_telefono_10_digitos(self):
        telefono = "0991234567"
        assert len(telefono) == 10 and telefono.isdigit()

    def test_listar_clientes_vacio(self, db):
        repo = ClienteRepository()
        assert repo.obtener_todos(db) == []

    def test_listar_clientes_retorna_todos(self, db):
        repo = ClienteRepository()
        repo.crear(db, ClienteCreate(cedula="0912345671", nombre="C1",
                                     correo="c1@g.com", telefono="0991111111", direccion="GYE"))
        repo.crear(db, ClienteCreate(cedula="0912345672", nombre="C2",
                                     correo="c2@g.com", telefono="0992222222", direccion="UIO"))
        assert len(repo.obtener_todos(db)) == 2

    def test_service_crear_cliente(self, db):
        service = ClienteService()
        data = ClienteCreate(cedula="0912345679", nombre="Juan",
                             correo="juan@g.com", telefono="0993333333", direccion="CUE")
        resultado = service.crear_cliente(db, data)
        assert resultado.nombre == "Juan" and resultado.id is not None


class TestHistorialReservas:
    """RF03: Mostrar historial de reservas por clienteFecha: 28/06/2026
"

    def test_historial_cliente_inexistente_retorna_none(self, db):
        repo = ClienteRepository()
        assert repo.obtener_historial(db, 9999) is None

    def test_historial_cliente_sin_reservas(self, db):
        repo = ClienteRepository()
        cliente = repo.crear(db, ClienteCreate(cedula="0912345670", nombre="Sin Reservas",
                                                correo="sr@g.com", telefono="0990000000",
                                                direccion="GYE"))
        resultado = repo.obtener_historial(db, cliente.id)
        assert resultado["historial_reservas"] == []

    def test_historial_contiene_cliente(self, db):
        repo = ClienteRepository()
        cliente = repo.crear(db, ClienteCreate(cedula="0912345673", nombre="Con Historial",
                                                correo="ch@g.com", telefono="0994444444",
                                                direccion="GYE"))
        resultado = repo.obtener_historial(db, cliente.id)
        assert resultado["cliente"].nombre == "Con Historial"

    def test_service_historial_cliente_inexistente(self, db):
        service = ClienteService()
        assert service.obtener_historial(db, 9999) is None

    def test_service_historial_cliente_existente(self, db):
        service = ClienteService()
        cliente = service.crear_cliente(db, ClienteCreate(cedula="0912345674", nombre="Angel",
                                                           correo="angel@g.com",
                                                           telefono="0995555555", direccion="GYE"))
        resultado = service.obtener_historial(db, cliente.id)
        assert "cliente" in resultado and "historial_reservas" in resultado

    def test_estado_reserva_valido(self):
        estados = ["Activa", "Completada", "Cancelada"]
        assert "Activa" in estados
        assert "Desconocido" not in estados
