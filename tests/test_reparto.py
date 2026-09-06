from datetime import date

from app.modelos import Gasto
from app.reparto import liquidacion, saldos


def gasto(importe, pagado_por, participantes, id=1):
    return Gasto(
        id=id,
        descripcion="prueba",
        importe=importe,
        pagado_por=pagado_por,
        participantes=participantes,
        fecha=date(2026, 1, 10),
    )


def test_saldos_de_un_gasto_repartido_en_partes_iguales():
    resultado = saldos([gasto(60.0, "Ana", ["Ana", "Bruno", "Carla"])])
    assert resultado["Ana"] == 40.0
    assert resultado["Bruno"] == -20.0
    assert resultado["Carla"] == -20.0


def test_quien_paga_solo_para_si_mismo_queda_a_cero():
    assert saldos([gasto(10.0, "Ana", ["Ana"])]) == {"Ana": 0.0}


def test_liquidacion_devuelve_las_transferencias():
    transferencias = liquidacion([gasto(60.0, "Ana", ["Ana", "Bruno", "Carla"])])
    assert len(transferencias) == 2
    assert all(t["a"] == "Ana" for t in transferencias)
    assert sum(t["importe"] for t in transferencias) == 40.0


def test_sin_gastos_no_hay_transferencias():
    assert liquidacion([]) == []
