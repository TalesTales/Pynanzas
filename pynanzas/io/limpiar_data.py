
from functools import lru_cache

import duckdb
import polars as pl

from pynanzas.duck.dicc import NomTabl, PATH_DDB, PathBD
from pynanzas.io.cargar_data import (
    _cargar_tabla_ddb_a_lf,
)


@lru_cache
def _tabla_lf(nom_tabla: NomTabl,
              path_db: PathBD = PATH_DDB,
              local_con: duckdb.DuckDBPyConnection | None = None,
              *,
              md: bool = False) -> pl.LazyFrame:
    # TOSO: Usar varias verificaciones para que si md, ddb no funcionan,
    # use parquet del backup y en últimas no arroje nada
    return _cargar_tabla_ddb_a_lf(nom_tabla, path_db, local_con, md=md)