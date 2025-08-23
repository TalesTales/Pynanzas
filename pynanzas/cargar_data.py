from pathlib import Path
import sqlite3

import pandas as pd

from pynanzas.constants import DIR_DATA, PROD_ID
from pynanzas.sql.diccionario import PATH_DB, NomTablas, PathDB


def cargar_csv_a_df(
    nom_tabla: NomTablas,
    dir_data: Path = DIR_DATA
) -> pd.DataFrame:
    try:
        if (dir_data / (nom_tabla + '.csv')).exists():
            df_read: pd.DataFrame = pd.read_csv(dir_data/(nom_tabla + '.csv'))
            if not df_read.empty:
                print(
                   f"data_loader.cargar_datos({nom_tabla}): Archivos leído "
                   f"exitosamente."
                )
            else:
                print("cargar_datos: Archivo cargado, pero df vacíos.")
        else:
            df_read = pd.DataFrame()
            print(f"data_loader.cargar_datos({nom_tabla}): no existe")
    except FileNotFoundError:
        print("data_loader.cargar_datos(): ERROR: No se encontró csv.")
        raise
    except Exception as e:
        print(f"data_loader.cargar_datos(): ERROR: {e}")
        raise
    return df_read


def tabla_sql_a_df(
    nom_tabla: NomTablas, nom_bd: PathDB = PATH_DB
) -> pd.DataFrame:
    try:
        with sqlite3.connect(nom_bd) as conn:
            query = f"SELECT * FROM {nom_tabla}"
            if nom_tabla == NomTablas.PRODS:
                df = pd.read_sql_query(query, conn, index_col=PROD_ID)
            else:
                df = pd.read_sql_query(query, conn)
            return df
    except sqlite3.Error as e:
        print(
            f"data_loader.tabla_sql_a_df: Error al leer la tabla "
            f"'{nom_tabla}': {e}"
        )
        return pd.DataFrame()