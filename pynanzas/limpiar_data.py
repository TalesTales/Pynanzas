from pathlib import Path

import polars as pl

from pynanzas.cargar_data import cargar_csv_a_df, cargar_ddb_a_lf
from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import NomTablas


def prods_csv_a_lf(nom_tabla: NomTablas = NomTablas.PRODS,
                   dir_data: Path = DIR_DATA) -> pl.LazyFrame:
    return (cargar_csv_a_df(nom_tabla,dir_data)
                                  .with_columns(
        (pl.col("fecha_actualizacion").str.to_datetime(time_unit="ms")))
                                  .cast({"simulado": pl.Boolean,
                                         "riesgo": pl.UInt8,
                                         "liquidez": pl.UInt8,
                                         "plazo": pl.UInt8,
                                         "abierto": pl.Boolean})
                                  )


def movs_csv_a_lf(nom_tabla: NomTablas = NomTablas.MOVS,
                  dir_data: Path = DIR_DATA) -> pl.LazyFrame:
    return (cargar_csv_a_df(nom_tabla, dir_data)
                   .with_columns((pl.col("fecha").str.to_datetime()),
                                 (pl.col("fecha_agregada").str.to_datetime())
                                 ))

def prods_sql_a_lf(nom_tabla: NomTablas = NomTablas.PRODS) -> pl.LazyFrame:
    return (cargar_ddb_a_lf(nom_tabla)
            .with_columns(
        (pl.col("fecha_actualizacion").str.to_datetime(time_unit="ms")))
            .cast({"simulado": pl.Boolean,
                                         "riesgo": pl.UInt8,
                                         "liquidez": pl.UInt8,
                                         "plazo": pl.UInt8,
                                         "abierto": pl.Boolean})
            )

def movs_sql_a_lf(nom_tabla: NomTablas = NomTablas.MOVS) -> pl.LazyFrame:
    return (cargar_ddb_a_lf(nom_tabla)
            .with_columns((pl.col("fecha").str.to_datetime()),
                                 (pl.col("fecha_agregada").str.to_datetime())
                                 )
            )