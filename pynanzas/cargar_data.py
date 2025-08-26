from pathlib import Path
import sqlite3

import polars as pl

from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import PATH_DB, NomTablas, PathDB


def cargar_csv_a_df(
    nom_tabla: NomTablas,
    dir_data: Path = DIR_DATA
) -> pl.LazyFrame:
    try:
        df_read = pl.scan_csv(dir_data/(nom_tabla + '.csv'))
        return df_read
    except FileNotFoundError:
        print("data_loader.cargar_datos(): ERROR: No se encontró csv.")
        raise
    except Exception as e:
        print(f"data_loader.cargar_datos(): ERROR: {e}")
        raise

def cargar_sql_a_df(nom_tabla: NomTablas,
                    nom_bd: PathDB = PATH_DB) -> pl.DataFrame:
    try:
        with sqlite3.connect(nom_bd) as conn:
            query = f"SELECT * FROM {nom_tabla}"
            df = pl.read_database(query, conn)
            return df
    except sqlite3.Error as e:
        print(
            f"data_loader.tabla_sql_a_df: Error al leer la tabla "
            f"'{nom_tabla}': {e}"
        )
        raise