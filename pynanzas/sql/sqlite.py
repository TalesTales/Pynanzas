from abc import ABC, abstractmethod
import sqlite3
from typing import Any, Optional

from pynanzas.constants import PROD_ID
from pynanzas.sql.diccionario import NomBD, NomTablas
from pynanzas.sql.movs import EsquemaMovs, crear_tabla_movs
from pynanzas.sql.prods import (
    EsquemaProds,
    crear_tabla_prods,
    tabla_prods_existe,
)


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


def actualizar_tabla(nom_tabla: NomTablas,
                     esquema: EsquemaProds | EsquemaMovs,
                     nom_bd: NomBD = NomBD.BD_SQLITE,
                     cursor: Optional[sqlite3.Cursor] = None
                     )->None:
    with (sqlite3.connect(nom_bd) as con):
        if cursor is None:
            cursor = con.cursor()
        cursor.execute ("SELECT name FROM sqlite_master WHERE "
                             "type='table' AND name=?", (nom_tabla,))
        if not cursor.fetchall():
            if isinstance(esquema, EsquemaProds):
                crear_tabla_prods(esquema, nom_tabla, nom_bd)
            else:
                if not tabla_prods_existe(cursor, nom_tabla):
                    crear_tabla_prods(nom_bd=nom_bd)
                crear_tabla_movs(esquema, nom_tabla, NomTablas.PRODS,
                                 PROD_ID, nom_bd)
            return
        cursor.execute(f"PRAGMA table_info ({nom_tabla})")
        resultado: list[Any] = cursor.fetchall()
        set_colums_pragma: set[str] =set([n[1] for n in resultado])
        if set_colums_pragma == set(esquema.keys()):
            return
        else:
            colums_drop: set[str] = set_colums_pragma - set(esquema.keys())
            colums_add: set[str] = set(esquema.keys()) - set_colums_pragma
            if len(colums_add) > 0:
                for colum in colums_add:
                    tipo = esquema.obtener_colums()[colum]
                    cursor.execute(
                        f"ALTER TABLE {nom_tabla} ADD COLUMN {colum} {tipo}")
                con.commit()
            if len(colums_drop) > 0:
                for colum in colums_drop:
                    cursor.execute(
                        f"ALTER TABLE {nom_tabla} DROP COLUMN {colum}")
                con.commit()
            return
