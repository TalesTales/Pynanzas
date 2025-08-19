import sqlite3
from typing import Any, Optional

from pynanzas.constants import PROD_ID
from pynanzas.sql.diccionario import NomBD, NomTablas
from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds


def actualizar_tabla(nom_tabla: NomTablas,
                     esquema: EsquemaProds | EsquemaMovs,
                     nom_bd: NomBD = NomBD.BD_SQLITE,
                     cursor: Optional[sqlite3.Cursor] = None
                     ) -> None:
    # Importaciones locales para evitar ciclos
    from pynanzas.sql.movs import crear_tabla_movs
    from pynanzas.sql.prods import crear_tabla_prods

    with (sqlite3.connect(nom_bd) as con):
        if cursor is None:
            cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE "
                       "type='table' AND name=?", (nom_tabla,))
        if not cursor.fetchall():
            if isinstance(esquema, EsquemaProds):
                crear_tabla_prods(esquema, nom_tabla, nom_bd)
            elif isinstance(esquema, EsquemaMovs):
                if not tabla_existe(cursor, NomTablas.PRODS):
                    crear_tabla_prods(nom_bd=nom_bd)
                crear_tabla_movs(esquema, nom_tabla, NomTablas.PRODS,
                                 PROD_ID, nom_bd)
            return
        cursor.execute(f"PRAGMA table_info ({nom_tabla})")
        resultado: list[Any] = cursor.fetchall()
        set_colums_pragma: set[str] = set([n[1] for n in resultado])
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


def tabla_existe(
        cursor: sqlite3.Cursor,
        nom_tabla: NomTablas,
) -> bool:
    query: str = ("SELECT name FROM sqlite_master WHERE type='table' AND "
                  "name=?")
    cursor.execute(query, (nom_tabla,))
    return bool(cursor.fetchall())