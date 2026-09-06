"""Validación y normalización de los datos que llegan del formulario.

Todo lo que entra por la API pasa por aquí antes de tocar el almacén.
"""

import re
from datetime import date

LARGO_MAXIMO_DESCRIPCION = 100

_NOMBRE_VALIDO = re.compile(r"^[A-Za-z ]+$")


class DatoInvalido(ValueError):
    """El dato no se puede aceptar. El mensaje va tal cual al usuario."""


def validar_nombre(nombre: str) -> str:
    """Un nombre de persona o de grupo: letras y espacios."""
    nombre = nombre.strip()
    if not nombre:
        raise DatoInvalido("El nombre no puede estar vacío")
    if not _NOMBRE_VALIDO.match(nombre):
        raise DatoInvalido(f"El nombre '{nombre}' contiene caracteres no permitidos")
    return nombre


def normalizar_importe(valor: str | float) -> float:
    """Acepta el importe tal como lo escribe la persona y lo deja en float."""
    if isinstance(valor, (int, float)):
        importe = float(valor)
    else:
        try:
            importe = float(valor.strip())
        except ValueError:
            raise DatoInvalido(f"'{valor}' no es un importe válido")
    if importe < 0:
        raise DatoInvalido("El importe no puede ser negativo")
    return round(importe, 2)


def validar_fecha(valor: str) -> date:
    """La fecha del gasto, en formato ISO."""
    try:
        fecha = date.fromisoformat(valor)
    except ValueError:
        raise DatoInvalido(f"'{valor}' no es una fecha válida, usa AAAA-MM-DD")
    return fecha


def validar_descripcion(texto: str) -> str:
    """La descripción que aparece en el listado."""
    texto = texto.strip()
    if not texto:
        raise DatoInvalido("La descripción no puede estar vacía")
    return texto[:LARGO_MAXIMO_DESCRIPCION]
