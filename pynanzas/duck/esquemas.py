from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, ItemsView, KeysView, ValuesView

from pynanzas.dicc import Liquidez, Plazo, Riesgo


@dataclass
class EsquemaBase(ABC):

    @abstractmethod
    def obtener_columns_oblig(self) -> list[str]:
        pass

    def validar_esquema_propio(self, colums_propias: dict[str, str]) -> bool:
        obligatorias = set(self.obtener_columns_oblig())
        propias = set(colums_propias.keys())

        faltantes = obligatorias - propias
        if faltantes:
            raise ValueError(
                f"Faltan columnas requeridas en schema personalizado: {faltantes}"
            )
        return True

    @property
    def columns(self) -> dict[str, str]:
        return asdict(self)

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
    producto_id: str | Any
    nombre: str
    ticker: str
    simulado: bool | str
    moneda: str
    riesgo: str | Riesgo
    liquidez: str | Liquidez
    plazo: str | Plazo
    objetivo:  str
    administrador: str
    plataforma: str
    tipo_producto: str
    tipo_inversion: str
    abierto: str | bool = True
    asignacion: str | float = 0
    saldo: float | str = 0
    aportes: float | str = 0
    intereses: float | str  = 0
    xirr: float | str = 0
    fecha_actualizacion: str | None = None

    def obtener_columns_oblig(self) -> list[str]:
        return ['producto_id']

@dataclass
class EsquemaMovs(EsquemaBase):
    producto_id: str
    fecha: str
    tipo: str
    valor: str | float
    unidades: str | float | None =  None
    valor_unidades: str | float |  None = None
    id: str |  int | None = None
    fecha_agregada: str | datetime | None = None
    saldo_hist: str | float | None = None
    xirr_hist: str |  float | None = None

    def obtener_columns_oblig(self) -> list[str]:
        return [ 'producto_id', 'fecha', 'tipo', 'valor']