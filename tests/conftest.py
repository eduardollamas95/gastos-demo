import pytest
from fastapi.testclient import TestClient

from app.almacen import Almacen
from app.main import app


@pytest.fixture(autouse=True)
def almacen_limpio(monkeypatch):
    """El almacén es un singleton en memoria: cada prueba parte de cero."""
    nuevo = Almacen()
    monkeypatch.setattr("app.almacen.almacen", nuevo)
    monkeypatch.setattr("app.main.almacen", nuevo)
    return nuevo


@pytest.fixture
def cliente():
    return TestClient(app)


@pytest.fixture
def grupo(cliente):
    cliente.post(
        "/grupos",
        json={"nombre": "Viaje", "participantes": ["Ana", "Bruno", "Carla"]},
    )
    return "Viaje"
