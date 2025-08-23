import os
from pathlib import Path
import sqlite3
from typing import Any, Optional

import pandas as pd

from pynanzas.constants import DIR_DATA, PROD_ID
from pynanzas.diccionario import Liquidez, Plazo, Riesgo
from pynanzas.sql.diccionario import PATH_DB, NomTablas, PathDB
from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds


def actualizar_tabla(nom_tabla: NomTablas,
                     esquema: EsquemaProds | EsquemaMovs,
                     nom_bd: PathDB = PATH_DB,
                     cursor: Optional[sqlite3.Cursor] = None
                     ) -> None:

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
                    crear_tabla_prods(path_db=nom_bd)
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

def _reset_sql_desde_csv(dir_data: Path = DIR_DATA,
                         path_db: PathDB = PATH_DB,
                         nom_tabla_prods: NomTablas = NomTablas.PRODS,
                         nom_tabla_movs: NomTablas = NomTablas.MOVS,
                         ) -> list[Any]:

    from pynanzas.limpiar_data import prods_csv_a_df
    df_prods: pd.DataFrame = prods_csv_a_df(nom_tabla_prods)
    from pynanzas.limpiar_data import movs_csv_a_df
    df_movs: pd.DataFrame = movs_csv_a_df(nom_tabla_movs)

    if os.path.exists(path_db): #TODO: Pasar a Path
        os.rename(path_db,path_db + '_old')

    from pynanzas.sql.movs import crear_tabla_movs
    from pynanzas.sql.prods import crear_tabla_prods

    crear_tabla_prods(path_db = path_db)
    crear_tabla_movs(path_db = path_db)

    with (sqlite3.connect(path_db) as con):
        cursor = con.cursor()
        from pynanzas import insertar_prod
        for i in df_prods.index:
            print(i)
            prod = EsquemaProds(
                i,
                df_prods.loc[i]["nombre"],
                df_prods.loc[i]["ticket"],
                bool(df_prods.loc[i]["simulado"]),
                str(df_prods.loc[i]["moneda"]).lower(),
                Riesgo(df_prods.loc[i]["riesgo"]),
                Liquidez(df_prods.loc[i]["liquidez"]),
                Plazo(df_prods.loc[i]["plazo"]),
                df_prods.loc[i]["objetivo"],
                df_prods.loc[i]["administrador"],
                df_prods.loc[i]["plataforma"],
                df_prods.loc[i]["tipo_producto"],
                df_prods.loc[i]["tipo_inversion"],
            )
            insertar_prod(prod,nom_tabla_prods,path_db)

        from pynanzas import insertar_mov
        for i in df_movs.index:
            mov = EsquemaMovs(
                df_movs.loc[i]["producto_id"],
                df_movs.loc[i]["fecha"].to_pydatetime(),
                df_movs.loc[i]["tipo"],
                df_movs.loc[i]["valor"],
                df_movs.loc[i]["unidades"],
                df_movs.loc[i]["valor_unidades"],
            )
            insertar_mov(mov, nom_tabla_movs, path_db)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        retorno: list[Any]= cursor.fetchall()
        if retorno:
            from pynanzas.export import exportar_sql_csv

            os.rename(dir_data / (nom_tabla_prods+'.csv'),
                      dir_data / ('_old_'+nom_tabla_prods+'.csv'))
            exportar_sql_csv(nom_tabla_prods)

            os.rename(dir_data / (nom_tabla_movs + ".csv"),
                      dir_data / ("_old_" + nom_tabla_movs + ".csv"))
            exportar_sql_csv(nom_tabla_movs)
            return retorno
        else:
            raise

        
