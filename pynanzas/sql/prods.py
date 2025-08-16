from dataclasses import asdict, dataclass, field
import sqlite3
from typing import Any, ItemsView, KeysView, Optional, ValuesView

from pynanzas.sql.diccionario import ColumDDL, NomBD, NomTablas
from pynanzas.sql.sqlite import EsquemaBase


@dataclass
class EsquemaProds(EsquemaBase):
    producto_id: str = field(default=ColumDDL.TXT_PK.value)
    nombre: str = field(default=ColumDDL.TXT_UNIQUE.value)
    ticket: str = field(default=ColumDDL.TXT_UNIQUE.value)
    simulado: str | bool = field(default=ColumDDL.BOOL_FALSE.value)
    moneda:str = field(default=ColumDDL.txt_default('cop'))
    riesgo: str = field(default=ColumDDL.TXT_NOT_NULL.value)
    liquidez:  str = field(default=ColumDDL.TXT_NOT_NULL.value)
    plazo:  str = field(default=ColumDDL.TXT_NOT_NULL.value)
    asignacion: float | str = field(default=ColumDDL.REAL_DEFAULT_CERO.value)
    objetivo:  str = field(default=ColumDDL.TXT_NOT_NULL.value)
    administrador:  str = field(default=ColumDDL.TXT_NOT_NULL.value)
    plataforma:  str = field(default=ColumDDL.TXT_NOT_NULL.value)
    tipo_producto:  str = field(default=ColumDDL.TXT_NOT_NULL.value)
    tipo_inversion: str = field(default=ColumDDL.TXT_NOT_NULL.value)

    abierto: bool | str = field(init=False, default=ColumDDL.BOOL_TRUE.value)
    saldo: float | str = field(init=False,
                           default=ColumDDL.REAL_DEFAULT_CERO.value)
    aportes: float | str = field(init=False,
                           default=ColumDDL.REAL_DEFAULT_CERO.value)
    intereses: float | str = field(init=False,
                           default=ColumDDL.REAL_DEFAULT_CERO.value)
    xirr: float | str = field(init=False,
                            default=ColumDDL.REAL_DEFAULT_CERO.value)

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


def crear_tabla_prods(esquema_prods: Optional[EsquemaProds] = None,
                      nom_tabla_prods: NomTablas = NomTablas.PRODS,
                      nom_bd: NomBD = NomBD.BD_SQLITE) -> None:
    """Crea una tabla de productos financieros en una base de datos SQLite.
    """
    if esquema_prods is None or len(esquema_prods) == 0:
        esquema_prods = EsquemaProds()

    columnas_ddl: list[str] = []
    for k, v in esquema_prods.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl: str = ",\n".join(columnas_ddl)

    try:
        with sqlite3.connect(nom_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            query: str = f"CREATE TABLE IF NOT EXISTS {nom_tabla_prods}"
            query += f"(\n{orden_ddl}\n);"
            print(f'crear_tabla_prod:\n{query}')  # TODO: logging
            cursor.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_prods: error sql {e}")


def tabla_prods_existe(
    cursor: sqlite3.Cursor,
    nom_tabla_prods: NomTablas = NomTablas.PRODS,
) -> bool:
    query: str = ("SELECT name FROM sqlite_master WHERE type='table' AND "
                  "name=?")
    cursor.execute(query, nom_tabla_prods)
    return bool(cursor.fetchall())


def insertar_prod(
    producto: EsquemaProds,
    nom_tabla_prods: NomTablas = NomTablas.PRODS,
    nom_bd: NomBD = NomBD.BD_SQLITE
)->None:
    columnas: str = ','.join(producto.keys())
    placeholders: str = ','.join(['?'] * len(producto))
    valores = tuple(producto.values())
    try:
        with sqlite3.connect(nom_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_prods_existe(cursor, nom_tabla_prods):
                crear_tabla_prods(nom_tabla_prods=nom_tabla_prods,
                                  nom_bd=nom_bd)
            query: str = (f"INSERT INTO {nom_tabla_prods} ({columnas}) VALUES "
                          f"(\n{placeholders}\n);")
            cursor.execute(query, valores)
            print(f'sql.insertar_prod:\n{query},{valores}')  # TODO: logging
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.insertar_prod: error sql {e}")
