
import duckdb
import polars as pl

from pynanzas.io.cargar_data import (
    _cargar_tabla_ddb_a_lf,
)
from pynanzas.sql.diccionario import PATH_DDB, NomTablas, PathDB


def _tabla_lf(nom_tabla: NomTablas,
              path_db: PathDB = PATH_DDB,
              local_con: duckdb.DuckDBPyConnection | None = None,
              *,
              md: bool = False) -> pl.LazyFrame:
    # TOSO: Usar varias verificaciones para que si md, ddb no funcionan,
    # use parquet del backup y en últimas no arroje nada
    return _cargar_tabla_ddb_a_lf(nom_tabla, path_db, local_con, md=md)