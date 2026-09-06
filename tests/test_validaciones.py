import pytest

from app.validaciones import (
    DatoInvalido,
    normalizar_importe,
    validar_descripcion,
    validar_fecha,
    validar_nombre,
)


def test_nombre_se_limpia_de_espacios():
    assert validar_nombre("  Ana  ") == "Ana"


def test_nombre_vacio_no_vale():
    with pytest.raises(DatoInvalido):
        validar_nombre("   ")


def test_importe_desde_texto():
    assert normalizar_importe("12.50") == 12.50


def test_importe_negativo_no_vale():
    with pytest.raises(DatoInvalido):
        normalizar_importe("-3")


def test_fecha_iso():
    assert validar_fecha("2026-01-15").isoformat() == "2026-01-15"


def test_fecha_con_formato_raro_no_vale():
    with pytest.raises(DatoInvalido):
        validar_fecha("15/01/2026")


def test_descripcion_vacia_no_vale():
    with pytest.raises(DatoInvalido):
        validar_descripcion("  ")
