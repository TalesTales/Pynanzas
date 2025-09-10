from dataclasses import asdict
from pathlib import Path
import sqlite3
from typing import Any, Optional

import duckdb

from pynanzas.constants import DIR_DATA, PROD_ID
from pynanzas.io.cargar_data import (
    _cargar_tabla_ddb_a_lf,
    _cargar_tabla_ddb_a_relation,
)
from pynanzas.sql.definicion import (
    _crear_tabla_sqlite_movs,
    _crear_tabla_sqlite_prods,
)
from pynanzas.sql.diccionario import (
    PATH_DDB,
    PATH_SQLITE,
    NombreBD,
    NomTablas,
    PathDB,
)
from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds
from pynanzas.sql.sqlite import tabla_existe


def _sql_insertar_prod(producto: EsquemaProds,
                       nom_tabla_prods: NomTablas = NomTablas.PRODS,
                       path_db: PathDB = PATH_SQLITE
                       ) -> None:
    from pynanzas.sql.sqlite import tabla_existe
    prod = asdict(producto)
    prod.pop('fecha_actualizacion', None)
    columnas: str = ','.join(prod.keys())
    placeholders: str = ','.join(['?'] * len(prod))
    valores = tuple(prod.values())
    try:
        with sqlite3.connect(path_db) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_existe(cursor, nom_tabla_prods):
                _crear_tabla_sqlite_prods(nom_tabla_prods=nom_tabla_prods,
                                          path_db=path_db)
            query: str = (f"INSERT INTO {nom_tabla_prods} ({columnas}) VALUES "
                          f"({placeholders})")
            cursor.execute(query, valores)
            print(f'sql.insertar_prod:\n{query}, {valores}')  # TODO: logging
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.insertar_prod: error sql {e}")


def _insertar_mov_sqlite(
        movimiento: EsquemaMovs,
        nom_tabla_movs: NomTablas = NomTablas.MOVS,
        path_db: PathDB = PATH_SQLITE,
) -> None:
    from pynanzas.sql.sqlite import tabla_existe

    mov = asdict(movimiento)

    mov.pop('id', None)
    mov.pop('fecha_agregada', None)

    columnas: str = ','.join(mov.keys())
    placeholders: str = ','.join(['?'] * len(mov.keys()))
    valores: tuple = tuple(mov.values())

    with sqlite3.connect(path_db) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        if not tabla_existe(cursor, nom_tabla_movs):
            _crear_tabla_sqlite_movs(nom_tabla_movs=nom_tabla_movs, path_db=path_db)
        query: str = (f"INSERT INTO {nom_tabla_movs} "
                      f"({columnas}) "
                      f"VALUES ({placeholders})")
        cursor.execute(query, valores)
        conn.commit()

def _insertar_mov_ddb(
        movimiento: EsquemaMovs | dict[str, Any],
        nom_tabla_movs: NomTablas = NomTablas.MOVS,
        path_db: PathDB = PATH_DDB,
        local_con: duckdb.DuckDBPyConnection | None = None
) -> None:

    mov = asdict(movimiento) if isinstance(movimiento, EsquemaMovs) else movimiento
    
    # mov.pop('id', None)
    mov.pop('fecha_agregada', None)

    columnas: str = ','.join(mov.keys())
    placeholders: str = ','.join(['?'] * len(mov.keys()))
    valores: tuple = tuple(mov.values())

    query: str = (f"INSERT INTO {nom_tabla_movs} "
                  f"({columnas}) "
                  f"VALUES ({placeholders});")
    print(query)
    try:
        if local_con is None:
            with duckdb.connect(path_db) as local_con:
                local_con.execute(query, valores)
                print(_cargar_tabla_ddb_a_relation(nom_tabla_movs, path_db,
                                             local_con).order("id "
                                                              "desc").limit(3))
        else:
            local_con.execute(query, valores)
            print(
                _cargar_tabla_ddb_a_relation(
                    nom_tabla_movs, path_db, local_con
                )
                .order("id desc")
                .limit(3)
            )
    except Exception as e:
        print(f"sql.insertar_mov_ddb: error sql {e}")



def _sql_actualizar_tabla(nom_tabla: NomTablas,
                          esquema: EsquemaProds | EsquemaMovs,
                          nom_bd: PathDB = PATH_SQLITE,
                          cursor: Optional[sqlite3.Cursor] = None
                          ) -> None:

    from pynanzas.sql.definicion import (
        _crear_tabla_sqlite_movs,
        _crear_tabla_sqlite_prods,
    )

    with (sqlite3.connect(nom_bd) as con):
        if cursor is None:
            cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE "
                       "type='table' AND name=?", (nom_tabla,))
        if not cursor.fetchall():
            if isinstance(esquema, EsquemaProds):
                _crear_tabla_sqlite_prods(esquema, nom_tabla, nom_bd)
            elif isinstance(esquema, EsquemaMovs):
                if not tabla_existe(cursor, NomTablas.PRODS):
                    _crear_tabla_sqlite_prods(path_db=nom_bd)
                _crear_tabla_sqlite_movs(esquema, nom_tabla, NomTablas.PRODS,
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

def _copy_sqlite_ddb(nom_sqllite: NombreBD = NombreBD.SQLITE,
                     nom_ddb: NombreBD = NombreBD.DDB,
                     dir_data: Path = DIR_DATA)->None:

    with duckdb.connect() as con:
        try:
            q = (f"""ATTACH DATABASE '{dir_data / nom_sqllite}' AS sqlite;\n"""
                        f"""ATTACH DATABASE '{dir_data / nom_ddb}' AS ddb;\n"""
                        f"""COPY FROM DATABASE sqlite to ddb;\n"""
                        f"""DROP TABLE ddb.sqlite_sequence;""")
            print(q)
            con.execute(q)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    con = duckdb.connect(PATH_DDB)
    a = (_cargar_tabla_ddb_a_lf(NomTablas.MOVS, local_con = con))
    print(_cargar_tabla_ddb_a_lf(NomTablas.MOVS, local_con = con).collect().tail(2))
    mov = EsquemaMovs(
        "AltLiq","2025-08-18","retiro",-258196.56,id=145,
    )
    _insertar_mov_ddb(mov, local_con = con)
    con.close()