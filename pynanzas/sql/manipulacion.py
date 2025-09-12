from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import sqlite3
from typing import Any, Optional

import duckdb

from pynanzas.constants import DIR_DATA, PROD_ID
from pynanzas.io.cargar_data import (
    _cargar_tabla_ddb_a_relation,
)
from pynanzas.producto import ProductoFinanciero
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
        movimientos: list[EsquemaMovs],
        nom_tabla_movs: NomTablas = NomTablas.MOVS,
        path_db: PathDB = PATH_DDB,
        local_con: duckdb.DuckDBPyConnection | None = None
) -> None:
    print("Insertar movimientos\n")
    print("====")
    try:
        if local_con is None:
            with duckdb.connect(path_db) as local_con:
                inicio_transaccion: str = "BEGIN TRANSACTION;\n"
                local_con.execute(inicio_transaccion)
                print(inicio_transaccion)
                for mov in movimientos:
                    m = asdict(mov)
                    m.pop('id', None)
                    m.pop('fecha_agregada', None)
                    columnas: str = ','.join(m.keys())
                    placeholders: str = ','.join(['?'] * len(m.keys()))
                    valores: tuple = tuple(m.values())

                    query = (f"INSERT INTO {nom_tabla_movs}\n"
                              f"({columnas}) VALUES ({placeholders});\n")
                    print(query)
                    print(valores)
                    local_con.execute(query, valores)
                commit = input('commit? s/n: ')
                if commit == 's':
                    local_con.execute("COMMIT;")
                    print('commit;')
                else:
                    local_con.execute("ROLLBACK;")
                    print('rollback;')
                print(_cargar_tabla_ddb_a_relation(nom_tabla_movs, path_db,
                                             local_con).select("producto_id","fecha","tipo","valor","id").order("id "
                                                              "desc").limit(len(movimientos)+3))
        else:
            print("No conn passed")
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

def fabricar_movs()-> list[EsquemaMovs]:
    insertar: bool = True
    movs: list[EsquemaMovs] = []
    while insertar:
        producto_id: str = input("producto_id: ")
        fecha: str = input("fecha: ")
        tipo: str = input("tipo: ")
        valor: float = float(input("valor: "))
        crear_mov: str = f"insertar: {producto_id}, {fecha}, {tipo}, {valor}? s/n: "
        append = input(crear_mov)
        if append == "s":
            mov: EsquemaMovs = EsquemaMovs(producto_id, fecha, tipo, valor)
            movs.append(mov)
            print(movs)
        else:
            pass

        insertar_otro: str = input("Insertar otro movimiento? s/n: ")
        if insertar_otro == "s":
            pass
        else:
            insertar = False
        print("========")
        print("\n")

    return movs

def update_prod_ddb(prod: ProductoFinanciero,
                    ask_commit: bool= True):
    query: str = ("""UPDATE productos
                  SET abierto = ?,
                      aportes = ?,
                      intereses = ?,
                      saldo = ?,
                      xirr = ?,
                      fecha_actualizacion = ?
                  WHERE producto_id = ?
                  """)
    valores: tuple = (prod.abierto,
                     prod.aportes,
                     prod.intereses,
                     prod.saldo,
                     prod.xirr,
                     datetime.now(),
                     prod.producto_id)
    if ask_commit:
        print(query, valores)
        commit = input("Confirmar UPDATE? s/n: ") if ask_commit else "s"
        if commit == "s":
            try:
                with duckdb.connect(PATH_DDB) as con:
                    con.execute(query, valores)
                    print(con.sql(f"""SELECT * FROM productos WHERE producto_id 
                    = '{prod.producto_id}'"""))
            except:
                raise
        else:
            print("Operation cancelled")
            return
    else:
        try:
            with duckdb.connect(PATH_DDB) as con:
                con.execute(query, valores)
        except Exception as e:
            raise e

if __name__ == '__main__':
    _insertar_mov_ddb(fabricar_movs())
