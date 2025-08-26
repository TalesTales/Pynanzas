#%%
from dataclasses import asdict

import pandas as pd

from pynanzas.cargar_data import cargar_csv_a_df
from pynanzas.constants import PROD_ID
from pynanzas.sql.diccionario import NomTablas
from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds

ESQUEMA_PRODS_DF = EsquemaProds(
    'string','string','string','boolean','string','category','category',
    'category','string', 'string','string', 'string','string','boolean',
    'float32','float32','float32','float32','float32','datetime64[s]')

def prods_csv_a_df(nom_tabla: NomTablas = NomTablas.PRODS,
                   esquema: EsquemaProds = ESQUEMA_PRODS_DF) -> pd.DataFrame:
    df_prods_raw: pd.DataFrame = cargar_csv_a_df(nom_tabla)
    df_prods_raw.drop_duplicates(inplace=True)
    df_prods = df_prods_raw.astype(asdict(esquema))
    df_prods.dropna(inplace=True)
    df_prods.set_index(PROD_ID, inplace=True)
    return df_prods

ESQUEMA_MOVS_DF = EsquemaMovs(
    'string','datetime64[s]','string','float64','float64','float64',
    'int64','datetime64[ns]')

def movs_csv_a_df(nom_tabla: NomTablas = NomTablas.MOVS,
                  esquema: EsquemaMovs = ESQUEMA_MOVS_DF) -> pd.DataFrame:
    df_movs_raw: pd.DataFrame = cargar_csv_a_df(nom_tabla)
    df_movs = df_movs_raw.astype(asdict(esquema))
    df_movs.drop_duplicates(inplace=True)
    df_movs.set_index('id', inplace=True, drop=True)
    return df_movs