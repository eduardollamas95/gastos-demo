"""Cálculo de quién le debe cuánto a quién."""

from collections import defaultdict

from app.modelos import Gasto


def saldos(gastos: list[Gasto]) -> dict[str, float]:
    """Saldo por persona: positivo si le deben, negativo si debe."""
    saldo: dict[str, float] = defaultdict(float)
    for gasto in gastos:
        parte = round(gasto.importe / len(gasto.participantes), 2)
        saldo[gasto.pagado_por] += gasto.importe
        for participante in gasto.participantes:
            saldo[participante] -= parte
    return {persona: round(valor, 2) for persona, valor in saldo.items()}


def liquidacion(gastos: list[Gasto]) -> list[dict]:
    """Lista de transferencias que dejan todos los saldos a cero."""
    saldo = saldos(gastos)
    deben = sorted(
        ((p, -v) for p, v in saldo.items() if v < 0), key=lambda x: -x[1]
    )
    cobran = sorted(
        ((p, v) for p, v in saldo.items() if v > 0), key=lambda x: -x[1]
    )

    transferencias = []
    i = j = 0
    while i < len(deben) and j < len(cobran):
        deudor, debe = deben[i]
        acreedor, cobra = cobran[j]
        cantidad = round(min(debe, cobra), 2)
        if cantidad > 0:
            transferencias.append(
                {"de": deudor, "a": acreedor, "importe": cantidad}
            )
        deben[i] = (deudor, round(debe - cantidad, 2))
        cobran[j] = (acreedor, round(cobra - cantidad, 2))
        if deben[i][1] <= 0:
            i += 1
        if cobran[j][1] <= 0:
            j += 1
    return transferencias
