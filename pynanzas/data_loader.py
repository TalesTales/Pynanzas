import os
from pathlib import Path
import sqlite3
from warnings import deprecated

import pandas as pd

from pynanzas.constants import DIR_BASE, PROD_ID
from pynanzas.sql.diccionario import BD_SQL, NomBD, NomTablas


@deprecated('Se eliminará en el futuro')
def cargar_datos(
    data_dir: str = "data", nombre_archivo: str = "Inversiones_Data.xlsx"
) -> dict[str, pd.DataFrame]:
    """Carga datos de inversiones desde archivo Excel o CSV como alternativa.

    Intenta cargar datos desde un archivo Excel con hojas específicas. Si el archivo
    Excel no se encuentra, busca archivos CSV individuales como alternativa.
    Los datos deben estar ubicados en el directorio /data.

    Args:
        data_dir (str): Directorio donde se encuentran los archivos de datos.
            Por defecto es "data".
        nombre_archivo (str): Nombre del archivo Excel principal a cargar.
            Por defecto es "Inversiones_Data.xlsx".

    Returns:
        dict[str, pd.DataFrame]: Diccionario con los DataFrames cargados,
            conteniendo las claves:
            - "transacciones": DataFrame con datos de transacciones
            - "productos": DataFrame con datos de productos
            - "diccionario": DataFrame con diccionario de datos

    Raises:
        FileNotFoundError: Si no se encuentra ni el archivo Excel ni los CSV alternativos.
        Exception: Si ocurre un error al leer las hojas del archivo Excel.

    Note:
        Se espera un archivo Excel con las hojas "Transacciones", "Diccionario"
        y "Productos". Si no se encuentra el Excel, busca archivos CSV individuales
        con el patrón "Inversiones_DATA_[NombreHoja].csv".
    """
    data_path: Path = DIR_BASE / data_dir
    archivo_path: Path = data_path / nombre_archivo
    data: dict[str, pd.DataFrame] = {}
    try:
        excel_data = pd.ExcelFile(archivo_path)
        df_transacciones_read = pd.read_excel(
            excel_data, sheet_name="Transacciones"
        )
        df_diccionario_read = pd.read_excel(
            excel_data, sheet_name="Diccionario"
        )
        df_productos_read = pd.read_excel(excel_data, sheet_name="Productos")
        if (
            not df_transacciones_read.empty
            and not df_productos_read.empty
            and not df_diccionario_read.empty
        ):  # TODO: refactor
            data = {
                "transacciones": df_transacciones_read,
                "productos": df_productos_read,
                "diccionario": df_diccionario_read,
            }
            print(
                 "cargar_datos: Hojas 'Transacciones', 'Diccionario' y "
                 "'Productos' cargadas desde Excel."
            )
        else:
            print("cargar_datos: Archivo cargado, pero df vacíos.")
    except FileNotFoundError:
        print(
            f"cargar_datos:⚠️ No se encontró {
                archivo_path.name
            }. Buscando archivos CSV individuales..."
        )
        try:
            archivo_csv = "Inversiones_DATA"
            df_transacciones_read = pd.read_csv(
                data_path / f"{archivo_csv}_Transacciones.csv"
            )
            df_diccionario_read = pd.read_csv(
                data_path / f"{archivo_csv}_Diccionario.csv"
            )
            df_productos_read = pd.read_csv(
                data_path / f"{archivo_csv}_Productos.csv"
            )
            if (
                not df_transacciones_read.empty
                and not df_productos_read.empty
                and not df_diccionario_read.empty
            ):  # TODO: refactor
                data = {
                    "transacciones": df_transacciones_read,
                    "productos": df_productos_read,
                    "diccionario": df_diccionario_read,
                }
                print("cargar_datos: Archivos CSV cargados.")
            else:
                print("cargar_datos: Archivo cargado, pero df vacíos.")
        except FileNotFoundError:
            print(
                "cargar_datos: ERROR: No se encontró el archivo Excel principal ni los CSV individuales."
            )
            raise
    except Exception as e:
        print(
            f"cargar_datos: ERROR: Ocurrió un problema al leer las hojas del archivo Excel: {e}"
        )
        raise

    if not data_path or not os.path.exists(data_path):
        print("\ncargar_datos:️ ¡ATENCIÓN! La variable BASE_PATH no está configurada.")
    else:
        print("cargar_datos: Archivo leído exitosamente.")
    return data

def tabla_sql_a_df(
    nom_tabla: NomTablas,
    nom_bd: NomBD = BD_SQL
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
        print(f"data_loader.tabla_sql_a_df: Error al leer la tabla "
              f"'{nom_tabla}': {e}")
        return pd.DataFrame()

def init_once(nom_bd: NomBD = BD_SQL)-> None:
    
    from pynanzas.diccionario import Liquidez, Plazo, Riesgo
    from pynanzas.limpiar_datos import prods_raw_a_df, trans_raw_to_df
    from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds
    from pynanzas.sql.movs import insertar_mov
    from pynanzas.sql.prods import insertar_prod

    datos: dict[str, pd.DataFrame] = cargar_datos()
    df_prods: pd.DataFrame = prods_raw_a_df(
        datos["productos"], datos["diccionario"]
    )
    df_trans: pd.DataFrame = trans_raw_to_df(datos["transacciones"])
    for i in df_prods.index:
        print(i)
        prod = EsquemaProds(i,
                            df_prods.loc[i]['nombre'],
                            df_prods.loc[i]['ticket'],
                            bool(df_prods.loc[i]['simulado']),
                            str(df_prods.loc[i]['moneda']).lower(),
                            Riesgo[df_prods.loc[i]['riesgo']],
                            Liquidez[df_prods.loc[i]['liquidez']],
                            Plazo[df_prods.loc[i]['plazo']],
                            df_prods.loc[i]['objetivo'],
                            df_prods.loc[i]['administrador'],
                            df_prods.loc[i]['plataforma'],
                            df_prods.loc[i]['tipo_de_producto'],
                            df_prods.loc[i]['tipo_de_inversion'])
        insertar_prod(prod, nom_bd=nom_bd)

    for m in df_trans.index:
        mov = EsquemaMovs(
            df_trans.loc[m]['producto_id'],
            df_trans.loc[m]['fecha'].to_pydatetime(),
            df_trans.loc[m]['movimiento'],
            df_trans.loc[m]['valor'],
            df_trans.loc[m]['unidades'],
            df_trans.loc[m]['precio_de_la_unidad'],
        )
        insertar_mov(mov, nom_bd=nom_bd)