import sqlite3

import pandas as pd

from pynanzas.sql.diccionario import NomBD, NomTablas


def movs_filtrados_prod(producto_id, nom_bd=NomBD.BD_SQLITE,
                        nom_tabla_movs=NomTablas.MOVS) -> pd.DataFrame:
    try:
        with sqlite3.connect(nom_bd) as con:
            query = (f"SELECT * FROM {nom_tabla_movs} "
                     f"WHERE producto_id = '{producto_id}'")
            return pd.read_sql_query(query, con)
    except sqlite3.Error as e:
        print(f"Portafolio._movs.filtrados.prod() Error: -> {e}")
        return pd.DataFrame()