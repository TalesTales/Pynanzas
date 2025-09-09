from pathlib import Path

import duckdb
import polars as pl

from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import PATH_DDB, NomTablas, PathDB


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

def cargar_ddb_a_lf(nom_tabla: NomTablas,
                    path_db: PathDB = PATH_DDB) -> pl.LazyFrame:
    with duckdb.connect(path_db) as con:
        return con.execute(f"""SELECT * FROM {nom_tabla};""").pl().lazy()

if __name__ == "__main__":
    print(cargar_ddb_a_lf(NomTablas.PRODS).collect())