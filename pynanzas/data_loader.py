import os
from pathlib import Path
import sqlite3
from warnings import deprecated

import pandas as pd

from pynanzas.constants import PROD_ID, DIR_DATA
from pynanzas.sql.diccionario import BD_SQL, NomBD, NomTablas

from collections import namedtuple
from typing import NamedTuple


def cargar_csv(
    dir_data: Path = DIR_DATA,
    nom_tablas: tuple[NomTablas, ...] = tuple(NomTablas),
) -> tuple:
    nom_tablas_str: list[str] = [nom.value for nom in NomTablas]
    data = namedtuple("data", nom_tablas_str)
    try:
        df_list: list[pd.DataFrame] = []
        for nom_tabla in nom_tablas_str:
            df_read: pd.DataFrame = pd.read_csv(
                DIR_DATA / (nom_tabla + ".csv")
            )
            if not df_read.empty:
                df_list.append(df_read)
            else:
                print("cargar_datos: Archivo cargado, pero df vacíos.")
        print("data_loader.cargar_datos(): Archivos leído exitosamente.")
        data = data(*df_list)
    except FileNotFoundError:
        print("data_loader.cargar_datos(): ERROR: No se encontró el CSV.")
        raise
    except Exception as e:
        print(f"data_loader.cargar_datos(): ERROR: {e}")
        raise
    return data


def tabla_sql_a_df(
    nom_tabla: NomTablas, nom_bd: NomBD = BD_SQL
) -> pd.DataFrame:
    try:
        with sqlite3.connect(nom_bd) as conn:
            query = f"SELECT * FROM {nom_tabla}"
            if nom_tabla == NomTablas.PRODS:
                df = pd.read_sql_query(query, conn, index_col=PROD_ID)
            else:
                df = pd.read_sql_query(query, conn)
            return df
    except sqlite3.Error as e:
        print(
            f"data_loader.tabla_sql_a_df: Error al leer la tabla "
            f"'{nom_tabla}': {e}"
        )
        return pd.DataFrame()


def init_once(nom_bd: NomBD = BD_SQL) -> None:
    from pynanzas.diccionario import Liquidez, Plazo, Riesgo
    from pynanzas.limpiar_datos import prods_raw_a_df, trans_raw_to_df
    from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds
    from pynanzas.sql.movs import insertar_mov
    from pynanzas.sql.prods import insertar_prod

    datos: dict[str, pd.DataFrame] = cargar_csv()
    df_prods: pd.DataFrame = prods_raw_a_df(
        datos["productos"], datos["diccionario"]
    )
    df_trans: pd.DataFrame = trans_raw_to_df(datos["transacciones"])
    for i in df_prods.index:
        print(i)
        prod = EsquemaProds(
            i,
            df_prods.loc[i]["nombre"],
            df_prods.loc[i]["ticket"],
            bool(df_prods.loc[i]["simulado"]),
            str(df_prods.loc[i]["moneda"]).lower(),
            Riesgo[df_prods.loc[i]["riesgo"]],
            Liquidez[df_prods.loc[i]["liquidez"]],
            Plazo[df_prods.loc[i]["plazo"]],
            df_prods.loc[i]["objetivo"],
            df_prods.loc[i]["administrador"],
            df_prods.loc[i]["plataforma"],
            df_prods.loc[i]["tipo_de_producto"],
            df_prods.loc[i]["tipo_de_inversion"],
        )
        insertar_prod(prod, nom_bd=nom_bd)

    for m in df_trans.index:
        mov = EsquemaMovs(
            df_trans.loc[m]["producto_id"],
            df_trans.loc[m]["fecha"].to_pydatetime(),
            df_trans.loc[m]["movimiento"],
            df_trans.loc[m]["valor"],
            df_trans.loc[m]["unidades"],
            df_trans.loc[m]["precio_de_la_unidad"],
        )
        insertar_mov(mov, nom_bd=nom_bd)
