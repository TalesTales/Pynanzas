import os
from pathlib import Path

import pandas as pd

from .constants import BASE_PATH


def cargar_datos(data_dir: str = "data", nombre_archivo: str = "Inversiones_Data.xlsx") -> dict[str, pd.DataFrame]:
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
    data_path: Path = BASE_PATH / data_dir
    archivo_path: Path = data_path / nombre_archivo
    data: dict[str, pd.DataFrame] = {}
    try:
        excel_data = pd.ExcelFile(archivo_path)
        df_transacciones_read = pd.read_excel(excel_data, sheet_name="Transacciones")
        df_diccionario_read = pd.read_excel(excel_data, sheet_name="Diccionario")
        df_productos_read = pd.read_excel(excel_data, sheet_name="Productos")
        if not df_transacciones_read.empty and not df_productos_read.empty and not df_diccionario_read.empty:  # TODO: refactor
            data = {"transacciones": df_transacciones_read, "productos": df_productos_read, "diccionario": df_diccionario_read}
            print("✅ ¡Éxito! Hojas 'Transacciones', 'Diccionario' y 'Productos' cargadas desde Excel.")
        else:
            print("Archivo cargado, pero df vacíos.")
    except FileNotFoundError:
        print(f"⚠️ No se encontró {archivo_path.name}. Buscando archivos CSV individuales...")
        try:
            archivo_csv = "Inversiones_DATA"
            df_transacciones_read = pd.read_csv(data_path / f"{archivo_csv}_Transacciones.csv")
            df_diccionario_read = pd.read_csv(data_path / f"{archivo_csv}_Diccionario.csv")
            df_productos_read = pd.read_csv(data_path / f"{archivo_csv}_Productos.csv")
            if not df_transacciones_read.empty and not df_productos_read.empty and not df_diccionario_read.empty:  # TODO: refactor
                data = {"transacciones": df_transacciones_read, "productos": df_productos_read, "diccionario": df_diccionario_read}
                print("✅ ¡Éxito! Archivos CSV cargados como alternativa.")
            else:
                print("Archivo cargado, pero df vacíos.")
        except FileNotFoundError:
            print("❌ ERROR: No se encontró el archivo Excel principal ni los CSV individuales.")
            raise
    except Exception as e:
        print(f"❌ ERROR: Ocurrió un problema al leer las hojas del archivo Excel: {e}")
        raise

    if not data_path or not os.path.exists(data_path):
        print("\n⚠️ ¡ATENCIÓN! La variable BASE_PATH no está configurada.")
    else:
        print("✅ Archivo leído exitosamente.")
    return data
