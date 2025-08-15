from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
import sqlite3
from typing import (
    Any,
    ItemsView,
    KeysView,
    Optional,
    ValuesView,
)

from . import NomBD, NomTablas
from .constants import (
    PROD_ID,
)
from .diccionario import ColumDDL


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

def actualizar_tabla(nom_tabla: NomTablas,
                     esquema: EsquemaProds | EsquemaMovs,
                     nom_bd: NomBD = NomBD.BD_SQLITE,
                     cursor: Optional[sqlite3.Cursor] = None
                     )->None:
    set_colums: dict[str, str] = esquema.obtener_colums()
    with (sqlite3.connect(nom_bd) as con):
        if cursor is None:
            cursor = con.cursor()
        cursor.execute ("SELECT name FROM sqlite_master WHERE "
                             "type='table' AND name=?", (nom_tabla,))
        if not cursor.fetchall():
            if isinstance(esquema, EsquemaProds):
                crear_tabla_prods(esquema, nom_tabla, nom_bd)
            elif isinstance(esquema, EsquemaMovs):
                if not tabla_prods_existe(cursor, nom_tabla):
                    crear_tabla_prods(nom_bd=nom_bd)
                crear_tabla_movs(esquema, nom_tabla,NomTablas.PRODS,
                PROD_ID, nom_bd)
            return
        query: str = f"PRAGMA table_info({nom_tabla})"
        cursor.execute(query)
        resultado: list[Any] = cursor.fetchall()
        set_colums_resultado: set[str] =set([n[1] for n in resultado])
        if set_colums_resultado == set_colums:
            return
        else:
            pass