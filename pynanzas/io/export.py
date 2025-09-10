from datetime import datetime
import os
from pathlib import Path

import duckdb

from pynanzas.constants import DIR_BACKUP, MD_TOKEN
from pynanzas.sql.diccionario import (
    NOM_BD,
    PATH_DDB,
    NombreBD,
    NomTablas,
    PathDB,
)


def _exportar_tabla_parquet(nom_tabla: NomTablas,
                            path_db: PathDB = PATH_DDB,
                            dir_backup: Path = DIR_BACKUP) -> None:

    fecha: str = datetime.now().strftime("%y%m%d_%H%M%S")
    dir_data_fecha: Path = dir_backup / fecha
    nom_parquet = f"{nom_tabla}_{fecha}.parquet"
    os.makedirs(dir_data_fecha, exist_ok=True)
    parquet_path = os.path.join(dir_data_fecha, nom_parquet)
    try:
        with duckdb.connect(path_db) as con:
            data = con.sql(f"COPY {nom_tabla} TO '{parquet_path}' ("
                           f"FORMAT parquet);")
        print(parquet_path)
        return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def _exportar_ddb_parquet(path_db: PathDB = PATH_DDB,
                          dir_backup: Path = DIR_BACKUP) -> None:

    fecha: str = datetime.now().strftime("%y%m%d_%H%M%S")
    dir_data_fecha: Path = dir_backup / fecha
    os.makedirs(dir_data_fecha, exist_ok=True)
    try:
        with duckdb.connect(path_db) as con:
            con.sql(f"EXPORT DATABASE '{dir_data_fecha}' (FORMAT parquet);")
        print(dir_data_fecha)
        return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def exportar_remoto(md_con: duckdb.DuckDBPyConnection | None = None,
                    nombre_db: NombreBD = NombreBD.DDB,
                    path_db: PathDB = PATH_DDB,
                    md_token: str = MD_TOKEN) -> None:
    fecha = datetime.now().strftime("%y%m%d_%H%M%S")
    query = (
        f"""ATTACH '{path_db}' AS ddb_local;\n"""
        f"""CREATE OR REPLACE DATABASE {NOM_BD}_{fecha} FROM 
        ddb_local;\n""" #TODO: Ajustar mejor el acoplamiento de VERSION_DB (
        # Tal vez cambiar NombreBD.DDB para que no contenga
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
    _exportar_ddb_parquet()
    exportar_remoto()