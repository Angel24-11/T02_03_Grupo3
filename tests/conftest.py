"""
Configuracion compartida de pytest para T02.04
Crea una base de datos SQLite en memoria para todos los tests.
"""
import sys
import os

# Asegura que la raiz del proyecto este en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base


@pytest.fixture(scope="function")
def db():
    """BD SQLite en memoria, se crea y destruye en cada test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
