"""Modelos de dominio: un grupo tiene participantes y gastos."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Gasto:
    id: int
    descripcion: str
    importe: float
    pagado_por: str
    participantes: list[str]
    fecha: date


@dataclass
class Grupo:
    nombre: str
    participantes: list[str] = field(default_factory=list)
    gastos: list[Gasto] = field(default_factory=list)
