def test_crear_grupo(cliente):
    respuesta = cliente.post(
        "/grupos", json={"nombre": "Viaje", "participantes": ["Ana", "Bruno"]}
    )
    assert respuesta.status_code == 201
    assert respuesta.json()["participantes"] == ["Ana", "Bruno"]


def test_añadir_y_listar_un_gasto(cliente, grupo):
    respuesta = cliente.post(
        f"/grupos/{grupo}/gastos",
        json={
            "descripcion": "Cena del sabado",
            "importe": "60",
            "pagado_por": "Ana",
            "participantes": ["Ana", "Bruno", "Carla"],
            "fecha": "2026-01-10",
        },
    )
    assert respuesta.status_code == 201
    assert respuesta.json()["importe"] == 60.0

    listado = cliente.get(f"/grupos/{grupo}/gastos").json()
    assert len(listado) == 1
    assert listado[0]["descripcion"] == "Cena del sabado"


def test_gasto_en_grupo_inexistente_da_404(cliente):
    respuesta = cliente.post(
        "/grupos/Fantasma/gastos",
        json={
            "descripcion": "Taxi",
            "importe": "10",
            "pagado_por": "Ana",
            "participantes": ["Ana"],
            "fecha": "2026-01-10",
        },
    )
    assert respuesta.status_code == 404


def test_buscar_por_descripcion(cliente, grupo):
    for descripcion in ("Cena del sabado", "Taxi al hotel"):
        cliente.post(
            f"/grupos/{grupo}/gastos",
            json={
                "descripcion": descripcion,
                "importe": "20",
                "pagado_por": "Ana",
                "participantes": ["Ana", "Bruno"],
                "fecha": "2026-01-10",
            },
        )
    encontrados = cliente.get(f"/grupos/{grupo}/gastos?buscar=Taxi").json()
    assert len(encontrados) == 1
    assert encontrados[0]["descripcion"] == "Taxi al hotel"


def test_eliminar_un_gasto(cliente, grupo):
    creado = cliente.post(
        f"/grupos/{grupo}/gastos",
        json={
            "descripcion": "Museo",
            "importe": "15",
            "pagado_por": "Bruno",
            "participantes": ["Ana", "Bruno"],
            "fecha": "2026-01-11",
        },
    ).json()

    assert cliente.delete(f"/grupos/{grupo}/gastos/{creado['id']}").status_code == 204
    assert cliente.get(f"/grupos/{grupo}/gastos").json() == []
