import os.path
from pathlib import Path

import duckdb
import polars as pl

from pynanzas.constants import DIR_DATA, MD_GLOBAL, MD_TOKEN
from pynanzas.io.export import (
    _exportar_ddb_parquet,
    exportar_remoto,
)
from pynanzas.sql.diccionario import PATH_DDB, NomTablas, PathDB


def _cargar_parquet_a_lf(#TODO: de pronto usar esto como último recurso para
        # cargar datos?
    nom_tabla: NomTablas,
    dir_data: Path = DIR_DATA
) -> pl.LazyFrame:
    try:
        df_read = pl.scan_parquet(dir_data/(nom_tabla + '.parquet'))
        return df_read
    except FileNotFoundError:
        print("_cargar_parquet_a_lf(): ERROR: No se encontró parquet.")
        raise
    except Exception as e:
        print(f"_cargar_parquet_a_lf(): ERROR: {e}")
        raise

def _cargar_parquet_a_ddb():
    raise NotImplementedError


def _synch_ddb_local_md(path_db: PathDB = PATH_DDB,
                        md_token: str  = MD_TOKEN)->None:

    md_q: str = ("SELECT name, created_ts "
                 "FROM md_information_schema.databases "
                 "WHERE name like 'pynanzas_%'"
                 "ORDER BY created_ts;")

    try:
        with duckdb.connect(f"md:?motherduck_token={md_token}") as con:
            if not os.path.exists(path_db):
                print("Descargando md y creando local")
                print(md_q)
                df = con.sql(md_q)
                nombre_bd_md = df.pl().tail(1).select(pl.col("name")).item()
                query = (f"""ATTACH '{path_db}' as ddb_local; """
                         f"""COPY FROM DATABASE {nombre_bd_md} to ddb_local; """
                         f"""CHECKPOINT ddb_local;""")
                print(query)
                con.sql(query)
            else:
                tiempo_local = Path(path_db).stat().st_mtime
                df = con.sql(md_q)
                nombre_bd_md = df.pl().tail(1).select(pl.col("name")).item()
                tiempo_md = (df.pl().tail(1).select(pl.col("created_ts"))
                                    .item().timestamp())
                if float(tiempo_md) > float(tiempo_local):
                    print("Descargando md y actualizando local")
                    _exportar_ddb_parquet()
                    con.sql(
                            f"""ATTACH '{path_db}' AS ddb_local;\n"""
                            f"""CREATE OR REPLACE DATABASE ddb_local """
                            f"""FROM {nombre_bd_md};\n"""
                            f"""DETACH ddb_local;""")
                    print("ddb_md")
                else:
                    if os.path.exists(path_db):
                        print("Subiendo md")
                        exportar_remoto(con, path_db)
                        print("ddb_local")
                    else:
                        print("ddb_local no existe")
        return None
    except Exception as e:
        print(f"exportar_remoto(): ERROR: {e}")

def _cargar_tabla_ddb_a_lf(nom_tabla: NomTablas,
                           path_db: PathDB = PATH_DDB,
                           local_con: duckdb.DuckDBPyConnection | None = None,
                           *,
                           md: bool = False) -> pl.LazyFrame:
    global MD_GLOBAL
    print(f"md= {md}, MD_GLOBAL= {MD_GLOBAL}, ddb= {os.path.exists(path_db)}")
    if md or MD_GLOBAL or not os.path.exists(path_db):
        print("sincronizando")
        _synch_ddb_local_md(path_db)
        MD_GLOBAL = False
        print(f"md= {md}, y MD_GLOBAL= {MD_GLOBAL}")
    else:
        print("local")
    if local_con:
        return local_con.execute(f"""SELECT * FROM {nom_tabla};""").pl().lazy()
    else:
        with duckdb.connect(path_db) as con:
            return con.execute(f"""SELECT * FROM {nom_tabla};""").pl().lazy()

def _cargar_tabla_ddb_a_relation(nom_tabla: NomTablas,
                                 path_db: PathDB = PATH_DDB,
                                 local_con: duckdb.DuckDBPyConnection | None = None,
                                 *,
                                 md: bool = False) -> duckdb.DuckDBPyRelation:
    global MD_GLOBAL
    print(f"md= {md}, MD_GLOBAL= {MD_GLOBAL}, ddb= {os.path.exists(path_db)}")
    if md or MD_GLOBAL or not os.path.exists(path_db):
        print("sincronizando")
        _synch_ddb_local_md(path_db)
        MD_GLOBAL = False
        print(f"md= {md}, y MD_GLOBAL= {MD_GLOBAL}")
    else:
        print("local")
    if local_con:
        return local_con.sql(f"""SELECT * FROM {nom_tabla};""")
    else:
        with duckdb.connect(path_db) as con:
            return con.sql(f"""SELECT * FROM {nom_tabla};""")

if __name__ == '__main__':
    _cargar_tabla_ddb_a_lf(NomTablas.MOVS)