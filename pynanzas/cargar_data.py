from pathlib import Path

import polars as pl

from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import URI, NomTablas


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
                    uri: str = URI) -> pl.LazyFrame:
    return pl.read_database_uri(f"SELECT * FROM {nom_tabla}",uri,
                                engine='adbc').lazy()