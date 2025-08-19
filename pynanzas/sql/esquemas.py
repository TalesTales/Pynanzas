from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, ItemsView, KeysView, ValuesView

from pynanzas.diccionario import Liquidez, Plazo, Riesgo
from pynanzas.sql.diccionario import ColumDDL


class EsquemaBase(ABC):
    """Clase base abstracta para esquemas de tabla."""

    @abstractmethod
    def obtener_colums(self) -> dict[str, str]:
        """Retorna el diccionario de columnas y sus definiciones SQL."""
        pass

    @abstractmethod
    def obtener_colums_oblig(self) -> list[str]:
        """Retorna lista de columnas que son obligatorias."""
        pass

    def validar_esquema_propio(self, colums_propias: dict[str, str]) -> bool:
        """Valida que un schema personalizado tenga las columnas requeridas."""
        obligatorias = set(self.obtener_colums_oblig())
        propias = set(colums_propias.keys())

        faltantes = obligatorias - propias
        if faltantes:
            raise ValueError(
                f"Faltan columnas requeridas en schema personalizado: {faltantes}"
            )
        return True

@dataclass
class EsquemaMovs(EsquemaBase):
    producto_id: str | ColumDDL
    fecha: str | ColumDDL
    tipo: str | ColumDDL
    valor: str | float | ColumDDL
    unidades: str | float | ColumDDL
    valor_unidades: str | float | ColumDDL
    id: ColumDDL | None = None
    fecha_agregada: ColumDDL | None = None

    def obtener_colums(self) -> dict[str, str]:
        return asdict(self)

    def obtener_colums_oblig(self) -> list[str]:
        return [ 'producto_id', 'fecha', 'tipo', 'valor']

    def __len__(self) -> int:
        return len(asdict(self))

    def keys(self) -> KeysView[str]:
        return asdict(self).keys()

    def items(self) -> ItemsView[str, Any]:
        return asdict(self).items()

    def values(self) -> ValuesView[Any]:
        return asdict(self).values()


@dataclass
class EsquemaProds(EsquemaBase):
    producto_id: str
    nombre: str
    ticket: str
    simulado: ColumDDL | bool
    moneda: str
    riesgo: str | ColumDDL | Riesgo
    liquidez:  str | ColumDDL | Liquidez
    plazo:  str | ColumDDL | Plazo
    objetivo:  str
    administrador:  str
    plataforma:  str
    tipo_producto:  str
    tipo_inversion: str
    abierto:ColumDDL |  bool = True
    asignacion: ColumDDL | float = 0
    saldo: float | ColumDDL = 0
    aportes: float | ColumDDL = 0
    intereses: float | ColumDDL = 0
    xirr: float | ColumDDL = 0

    def obtener_colums(self) -> dict[str, str]:
        return asdict(self)

    def obtener_colums_oblig(self) -> list[str]:
        return ['producto_id']

    def __len__(self) -> int:
        return len(asdict(self))

    def keys(self) -> KeysView[str]:
        return asdict(self).keys()

    def items(self) -> ItemsView[str, Any]:
        return asdict(self).items()

    def values(self) -> ValuesView[Any]:
        return asdict(self).values()
