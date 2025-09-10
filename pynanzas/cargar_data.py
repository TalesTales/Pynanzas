from pathlib import Path

import duckdb
import polars as pl

from pynanzas.constants import DIR_DATA, MD_GLOBAL, MD_TOKEN
from pynanzas.export import guardar_md
from pynanzas.sql.diccionario import PATH_DDB, NomTablas, PathDB


def _cargar_csv_a_lf(
    nom_tabla: NomTablas,
    dir_data: Path = DIR_DATA
) -> pl.LazyFrame:
    try:
        df_read = pl.scan_csv(dir_data/(nom_tabla + '.csv'))
        return df_read
    except FileNotFoundError:
        print("_cargar_csv_a_lf(): ERROR: No se encontró csv.")
        raise
    except Exception as e:
        print(f"_cargar_csv_a_lf(): ERROR: {e}")
        raise

def _cargar_parquet_a_lf(
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


def _synch_ddb_local_md(path_db: PathDB = PATH_DDB,
                        md_token: str  = MD_TOKEN)->None:
    tiempo_local = Path(path_db).stat().st_mtime

    md_q: str = ("SELECT name, created_ts "
                 "FROM md_information_schema.databases "
                 "WHERE name like 'pynanzas_%'"
                 "ORDER BY created_ts;")

    try:
        with duckdb.connect(f"md:?motherduck_token={md_token}") as con:
            df = con.execute(md_q).pl()
            nombre_bd_md = df.tail(1).select(pl.col("name")).item()
            tiempo_md = df.tail(1).select(pl.col("created_ts")).item().timestamp()
            if float(tiempo_md) > float(tiempo_local):
                con.sql(f"""DETACH ddb_local;"""
                        """ATTACH '{path_db}' AS ddb_local;\n"""
                        f"""CREATE OR REPLACE DATABASE ddb_local FROM
                {nombre_bd_md};\n""")
                print("ddb_md")
            else:
                guardar_md(con, path_db)
                print("ddb_local")
        return None
    except Exception as e:
        print(f"descargar_md(): ERROR: {e}")
        print("ddb_local")

def _cargar_ddb_a_lf(nom_tabla: NomTablas,
                     path_db: PathDB = PATH_DDB,
                     local_con: duckdb.DuckDBPyConnection | None = None,
                     *,
                     md: bool = False) -> pl.LazyFrame:
    global MD_GLOBAL
    print(f"md= {md}, y MD_GLOBAL= {MD_GLOBAL}")
    if md or MD_GLOBAL:
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

if __name__ == "__main__":
    print(MD_GLOBAL,_cargar_ddb_a_lf(NomTablas.PRODS).collect())