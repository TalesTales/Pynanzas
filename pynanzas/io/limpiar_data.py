from pathlib import Path

import duckdb
import polars as pl

from pynanzas.cargar_data import _cargar_csv_a_lf, _cargar_ddb_a_lf
from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import PATH_DDB, NomTablas, PathDB


def _prods_csv_a_lf(nom_tabla: NomTablas = NomTablas.PRODS,
                    dir_data: Path = DIR_DATA) -> pl.LazyFrame:
    return (_cargar_csv_a_lf(nom_tabla, dir_data)
            .with_columns(
        (pl.col("fecha_actualizacion").str.to_datetime(time_unit="ms")))
            .cast({"simulado": pl.Boolean,
                                         "riesgo": pl.UInt8,
                                         "liquidez": pl.UInt8,
                                         "plazo": pl.UInt8,
                                         "abierto": pl.Boolean})
            )


def _movs_csv_a_lf(nom_tabla: NomTablas = NomTablas.MOVS,
                   dir_data: Path = DIR_DATA) -> pl.LazyFrame:
    return (_cargar_csv_a_lf(nom_tabla, dir_data)
            .with_columns((pl.col("fecha").str.to_datetime()),
                                 (pl.col("fecha_agregada").str.to_datetime())
                                 ))

def _tabla_ddb_lf(nom_tabla: NomTablas,
                  path_db: PathDB = PATH_DDB,
                  local_con: duckdb.DuckDBPyConnection | None = None,
                  *,
                  md: bool = False) -> pl.LazyFrame:
    return _cargar_ddb_a_lf(nom_tabla, path_db, local_con, md=md)