"""API de gastos compartidos.

Un grupo, sus participantes, los gastos que hace cada uno y el cálculo de
quién le debe cuánto a quién al final del viaje.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import reparto, validaciones
from app.almacen import NoEncontrado, almacen
from app.validaciones import DatoInvalido

app = FastAPI(title="Gastos compartidos")


class GrupoNuevo(BaseModel):
    nombre: str
    participantes: list[str]


class GastoNuevo(BaseModel):
    descripcion: str
    importe: str | float
    pagado_por: str
    participantes: list[str]
    fecha: str


def _serializar(gasto) -> dict:
    return {
        "id": gasto.id,
        "descripcion": gasto.descripcion,
        "importe": gasto.importe,
        "pagado_por": gasto.pagado_por,
        "participantes": gasto.participantes,
        "fecha": gasto.fecha.isoformat(),
    }


@app.post("/grupos", status_code=201)
def crear_grupo(datos: GrupoNuevo):
    try:
        nombre = validaciones.validar_nombre(datos.nombre)
        participantes = [validaciones.validar_nombre(p) for p in datos.participantes]
    except DatoInvalido as error:
        raise HTTPException(status_code=400, detail=str(error))
    grupo = almacen.crear_grupo(nombre, participantes)
    return {"nombre": grupo.nombre, "participantes": grupo.participantes}


@app.post("/grupos/{grupo}/gastos", status_code=201)
def añadir_gasto(grupo: str, datos: GastoNuevo):
    try:
        gasto = almacen.añadir_gasto(
            grupo,
            descripcion=validaciones.validar_descripcion(datos.descripcion),
            importe=validaciones.normalizar_importe(datos.importe),
            pagado_por=validaciones.validar_nombre(datos.pagado_por),
            participantes=datos.participantes,
            fecha=validaciones.validar_fecha(datos.fecha),
        )
    except DatoInvalido as error:
        raise HTTPException(status_code=400, detail=str(error))
    except NoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error))
    return _serializar(gasto)


@app.get("/grupos/{grupo}/gastos")
def listar_gastos(grupo: str, buscar: str | None = None):
    try:
        if buscar:
            gastos = almacen.buscar_gastos(grupo, buscar)
        else:
            gastos = almacen.listar_gastos(grupo)
    except NoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error))
    return [_serializar(gasto) for gasto in gastos]


@app.delete("/grupos/{grupo}/gastos/{gasto_id}", status_code=204)
def eliminar_gasto(grupo: str, gasto_id: int):
    almacen.eliminar_gasto(grupo, gasto_id)


@app.get("/grupos/{grupo}/liquidacion")
def liquidacion(grupo: str):
    try:
        gastos = almacen.listar_gastos(grupo)
    except NoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error))
    return {
        "saldos": reparto.saldos(gastos),
        "transferencias": reparto.liquidacion(gastos),
    }
