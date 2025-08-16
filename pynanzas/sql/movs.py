from dataclasses import asdict, dataclass, field
import sqlite3
from typing import Any, ItemsView, KeysView, Optional, ValuesView

from pynanzas.constants import PROD_ID
from pynanzas.sql.diccionario import ColumDDL, NomBD, NomTablas
from pynanzas.sql.prods import crear_tabla_prods, tabla_prods_existe
from pynanzas.sql.sqlite import EsquemaBase


@dataclass
class EsquemaMovs(EsquemaBase):
    id: str = field(default=ColumDDL.INT_PK_AUTO.value)
    producto_id: str = field(default=ColumDDL.TXT_NOT_NULL.value)

    fecha: str = field(default=ColumDDL.DATE_NOT_NULL.value)
    tipo: str = field(default=ColumDDL.TXT_NOT_NULL.value)
    valor: str = field(default=ColumDDL.REAL_NOT_NULL.value)
    unidades: str = field(default=ColumDDL.REAL.value)
    valor_unidades: str = field(default=ColumDDL.REAL.value)

    fecha_agregada: str = field(init=False, default=ColumDDL.DATE_ACTUAL.value)

    def obtener_colums(self) -> dict[str, str]:
        return asdict(self)

    def obtener_colums_oblig(self) -> list[str]:
        return ['id', 'producto_id', 'fecha', 'tipo', 'valor']

    def __len__(self) -> int:
        return len(asdict(self))

    def keys(self) -> KeysView[str]:
        return asdict(self).keys()

    def items(self) -> ItemsView[str, Any]:
        return asdict(self).items()

    def values(self) -> ValuesView[Any]:
        return asdict(self).values()


def crear_tabla_movs(esquema_movs: Optional[EsquemaMovs] = None,
                     nom_tabla_movs: NomTablas = NomTablas.MOVS,
                     nom_tabla_prods: NomTablas = NomTablas.PRODS,
                     producto_id: str = PROD_ID,
                     nom_bd: NomBD = NomBD.BD_SQLITE) -> None:
    if nom_tabla_movs == "":
        raise ValueError("crear_tabla_movs: nom_tabla_movs vacio")
    if nom_tabla_prods == "":
        raise ValueError("crear_tabla_movs: nom_tabla_prods vacio")
    if esquema_movs is None or len(esquema_movs) == 0:
        esquema_movs = EsquemaMovs()

    columnas_ddl: list[str] = []
    for k, v in esquema_movs.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl = (',\n'.join(columnas_ddl))
    orden_ddl += (f"\nFOREIGN KEY ({producto_id}) REFERENCES"
                 f" {nom_tabla_prods} ({producto_id})")
    try:
        with sqlite3.connect(nom_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_prods_existe(cursor, nom_tabla_prods):
                crear_tabla_prods(nom_tabla_prods=nom_tabla_prods,
                                  nom_bd=nom_bd)
            query: str = (f"CREATE TABLE IF NOT EXISTS {nom_tabla_movs}"
                                 f"(\n{orden_ddl}\n);")
            print(query)  # TODO: logging
            cursor.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_movs: error sql {e}")


def insertar_mov() -> None:
    pass