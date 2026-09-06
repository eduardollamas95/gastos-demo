"""Almacén en memoria. Se reinicia con el proceso: es una demo."""

from app.modelos import Gasto, Grupo


class NoEncontrado(KeyError):
    """El identificador pedido no existe."""


class Almacen:
    def __init__(self) -> None:
        self.grupos: dict[str, Grupo] = {}
        self._siguiente_id = 1

    def crear_grupo(self, nombre: str, participantes: list[str]) -> Grupo:
        grupo = Grupo(nombre=nombre, participantes=participantes)
        self.grupos[nombre] = grupo
        return grupo

    def obtener_grupo(self, nombre: str) -> Grupo:
        if nombre not in self.grupos:
            raise NoEncontrado(f"No existe el grupo '{nombre}'")
        return self.grupos[nombre]

    def añadir_gasto(self, grupo: str, **datos) -> Gasto:
        gasto = Gasto(id=self._siguiente_id, **datos)
        self._siguiente_id += 1
        self.obtener_grupo(grupo).gastos.append(gasto)
        return gasto

    def listar_gastos(self, grupo: str) -> list[Gasto]:
        """Los gastos del grupo, del más reciente al más antiguo."""
        return self.obtener_grupo(grupo).gastos

    def buscar_gastos(self, grupo: str, texto: str) -> list[Gasto]:
        """Los gastos cuya descripción contiene el texto buscado."""
        return [
            gasto
            for gasto in self.obtener_grupo(grupo).gastos
            if texto in gasto.descripcion
        ]

    def eliminar_gasto(self, grupo: str, gasto_id: int) -> None:
        gastos = self.obtener_grupo(grupo).gastos
        indice = [g.id for g in gastos].index(gasto_id)
        gastos.pop(indice)


almacen = Almacen()
