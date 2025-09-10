from datetime import datetime
import os
from pathlib import Path

import duckdb

from pynanzas.constants import DIR_DATA, MD_TOKEN
from pynanzas.sql.diccionario import PATH_DDB, NomTablas, PathDB


def _exportar_tabla_parquet(nom_tabla: NomTablas,
                            path_db: PathDB = PATH_DDB,
                            data_dir: Path = DIR_DATA) -> None:

    fecha: str = datetime.now().strftime("%y%m%d_%H%M%S")
    data_bu: Path = data_dir / "backup" / fecha
    nom_parquet = f"{nom_tabla}_{fecha}.parquet"
    os.makedirs(data_bu, exist_ok=True)
    parquet_path = os.path.join(data_bu, nom_parquet)
    try:
        with duckdb.connect(path_db) as con:
            data = con.sql(f"COPY {nom_tabla} TO '{parquet_path}' ("
                           f"FORMAT parquet);")
        print(parquet_path)
        return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def exportar_remoto(md_con: duckdb.DuckDBPyConnection | None = None,
                    path_db: PathDB = PATH_DDB,
                    md_token: str = MD_TOKEN) -> None:
    fecha = datetime.now().strftime("%y%m%d_%H%M%S")
    query = (
        f"""ATTACH '{path_db}' AS ddb_local;\n"""
        f"""CREATE OR REPLACE DATABASE pynanzas_{fecha} FROM ddb_local;\n"""
    )
    print(query)
    if md_con is None:
        with duckdb.connect(f"md:?motherduck_token={md_token}") as md_con:
            md_con.sql(query)
        return
    else:
        md_con.sql(query)
        return

if __name__ == '__main__':
    pass