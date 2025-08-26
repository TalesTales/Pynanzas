from pathlib import Path

import polars as pl

from pynanzas.cargar_data import cargar_csv_a_df, cargar_sql_a_df
from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import NomTablas, PATH_DB, PathDB


def prods_csv_a_df(nom_tabla: NomTablas = NomTablas.PRODS,
                   dir_data: Path = DIR_DATA) -> pl.DataFrame:
    csv_prods_raw: pl.LazyFrame = (cargar_csv_a_df(nom_tabla,dir_data)
                                  .with_columns(
        (pl.col("fecha_actualizacion").str.to_datetime(time_unit="ms")))
                                  .cast({"simulado": pl.Boolean,
                                         "riesgo": pl.UInt8,
                                         "liquidez": pl.UInt8,
                                         "plazo": pl.UInt8,
                                         "abierto": pl.Boolean})
                                  )
    return csv_prods_raw.collect()

def movs_csv_a_df(nom_tabla: NomTablas = NomTablas.MOVS,
                  dir_data: Path = DIR_DATA) -> pl.DataFrame:
    csv_movs_raw = (cargar_csv_a_df(nom_tabla, dir_data)
                   .with_columns((pl.col("fecha").str.to_datetime()),
                                 (pl.col("fecha_agregada").str.to_datetime())
                                 ))
    return csv_movs_raw.collect()

def prods_sql_a_df(nom_tabla: NomTablas = NomTablas.PRODS,
                   nom_bd: PathDB = PATH_DB) -> pl.DataFrame:
    sql_prods_raw: pl.LazyFrame = (cargar_sql_a_df(nom_tabla,nom_bd).lazy()
                                  .with_columns(
        (pl.col("fecha_actualizacion").str.to_datetime(time_unit="ms")))
                                  .cast({"simulado": pl.Boolean,
                                         "riesgo": pl.UInt8,
                                         "liquidez": pl.UInt8,
                                         "plazo": pl.UInt8,
                                         "abierto": pl.Boolean})
                                  )
    return sql_prods_raw.collect()

if __name__ == '__main__':
    print( prods_sql_a_df().head())
    pass