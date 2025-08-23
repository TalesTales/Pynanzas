import sqlite3

import pandas as pd

from pynanzas.sql.diccionario import PATH_DB, NomTablas, PathDB


def movs_filtrados_prod(producto_id,
                        path_db: PathDB = PATH_DB,
                        nom_tabla_movs: NomTablas = NomTablas.MOVS) -> (
        pd.DataFrame):
    try:
        with sqlite3.connect(path_db) as con:
            query = (f"SELECT * FROM {nom_tabla_movs} "
                     f"WHERE producto_id = '{producto_id}'")
            return pd.read_sql_query(query, con)
    except sqlite3.Error as e:
        print(f"Portafolio._movs.filtrados.prod() Error: -> {e}")
        return pd.DataFrame()