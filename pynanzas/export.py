import os
from pathlib import Path
import sqlite3

import pandas as pd

from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import BD_SQL, NomBD, NomTablas


def exportar_sqlite_csv(nom_tabla: NomTablas,
                        nom_bd: NomBD = BD_SQL,
                        nom_csv = None,
                        data_dir: Path = DIR_DATA):
    os.makedirs(data_dir, exist_ok=True)

    if not nom_csv:
        nom_csv = f"{nom_tabla}.csv"

    csv_path = os.path.join(data_dir, nom_csv)

    try:
        with sqlite3.connect(nom_bd) as con:
            df = pd.read_sql_query(f"SELECT * FROM {nom_tabla}",con)
            df.to_csv(csv_path, index=False, encoding='utf-8')

        print(f"Exportado: {len(df)} filas → {csv_path}")
        return csv_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None
