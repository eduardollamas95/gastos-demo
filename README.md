# Gastos compartidos

API para llevar los gastos de un grupo —un viaje, un piso, una cena grande— y calcular al final
quién le debe cuánto a quién.

## Instalar y arrancar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La documentación interactiva queda en <http://localhost:8000/docs>.

## Pruebas

```bash
pytest
```

Ese es el comando completo: no hace falta ningún servicio levantado ni variable de entorno. La
suite tarda menos de un segundo.

## Estructura

| Archivo | Qué hay dentro |
|---|---|
| `app/main.py` | Los endpoints HTTP y la traducción de errores a códigos de estado |
| `app/validaciones.py` | Todo lo que entra del formulario pasa por aquí antes de guardarse |
| `app/reparto.py` | Saldos por persona y las transferencias que los dejan a cero |
| `app/almacen.py` | Almacén en memoria: se reinicia con el proceso |
| `app/modelos.py` | Las dos entidades: `Grupo` y `Gasto` |

## Cómo funciona el reparto

Cada gasto tiene quién lo pagó y entre quiénes se reparte. El saldo de una persona es lo que ha
pagado menos lo que le corresponde de cada gasto en el que participa. `GET /grupos/{grupo}/liquidacion`
devuelve esos saldos y la lista de transferencias que los salda.
