from datetime import datetime
import os
from pathlib import Path
import sqlite3

import duckdb
import pandas as pd

from pynanzas.constants import DIR_DATA, MD_TOKEN
from pynanzas.sql.diccionario import PATH_DDB, PATH_SQLITE, NomTablas, PathDB


def _exportar_db_parquet(nom_tabla: NomTablas,
                         path_db: PathDB = PATH_DDB,
                         data_dir: Path = DIR_DATA) -> None:

    fecha: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    nom_parquet = f"{nom_tabla}_{fecha}.parquet"

    os.makedirs(data_dir, exist_ok=True)
    parquet_path = os.path.join(data_dir, nom_parquet)
    if path_db == PATH_SQLITE:
        try:
            with sqlite3.connect(path_db) as con:
                df = pd.read_sql_query(f"SELECT * FROM {nom_tabla}",con)
                df.to_csv(parquet_path, index=False, encoding='utf-8')

            print(f"Exportado: {len(df)} filas → {parquet_path}")
            return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    elif path_db == PATH_DDB:
        try:
            with duckdb.connect(path_db) as con:
                con.sql(f"COPY {nom_tabla} TO '{nom_tabla}.parquet' (FORMAT parquet);")
            return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    return None

def guardar_md():
    print(MD_TOKEN)
    with duckdb.connect(f"md:?motherduck_token={MD_TOKEN}") as con:
        fecha = datetime.now().strftime("%y%m%d_%H%M%S")
        q = (f"""ATTACH '{PATH_DDB}' AS ddb;\n"""
             f"""CREATE OR REPLACE DATABASE pynanzas_{fecha} FROM ddb;\n""")
        print(q)
        con.sql(q)

if __name__ == '__main__':
    guardar_md()