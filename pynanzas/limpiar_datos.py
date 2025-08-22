from warnings import deprecated

import pandas as pd

from pynanzas.constants import DIR_DATA
from pynanzas.sql.diccionario import NomTablas


def prods_csv_a_df(nom_tabla: NomTablas = NomTablas.PRODS) -> pd.DataFrame:
    return pd.read_csv(DIR_DATA / (nom_tabla.value + '.csv'))

@deprecated('Se eliminará en el futuro')
def trans_raw_to_df(
    df_transacciones_raw: pd.DataFrame,
) -> pd.DataFrame:
    """
    Procesa un DataFrame crudo de transacciones y lo convierte en un DataFrame limpio y estructurado.

    La función realiza las siguientes transformaciones:
    - Normaliza los nombres de columnas (minúsculas y guiones bajos)
    - Estandariza los tipos de movimientos (minúsculas y guiones bajos)
    - Limpia y convierte los valores monetarios a formato numérico
    - Convierte las fechas a formato datetime
    - Elimina filas con datos insuficientes

    Args:
        df_transacciones_raw: pd.DataFrame de transacciones

    Returns:
        pd.DataFrame: DataFrame procesado con:
            - Nombres de columnas normalizados
            - Tipos de movimientos estandarizados
            - Valores monetarios como números (sin símbolos $ ni separadores de miles)
            - Fechas en formato datetime
            - Filas con datos insuficientes eliminadas

    Note:
        - Los valores monetarios con formato incorrecto se convierten a 0
        - Las fechas con formato incorrecto se convierten a NaT
        - Se eliminan filas que no tengan al menos 3 valores no-NA
        - No se modifican los valores de las transacciones, solo su formato
    """
    df_transacciones = df_transacciones_raw.copy()
    df_transacciones.columns = [
        col.lower().replace(" ", "_") for col in df_transacciones.columns
    ]
    df_transacciones["movimiento"] = df_transacciones["movimiento"].astype(str)
    df_transacciones["movimiento"] = [
        mov.lower().replace(" ", "_") for mov in df_transacciones["movimiento"]
    ]
    df_transacciones["valor"] = df_transacciones["valor"].astype(str)
    df_transacciones["valor"] = df_transacciones["valor"].str.replace(
        "$", "", regex=False
    )
    df_transacciones["valor"] = df_transacciones["valor"].str.replace(
        ",", "", regex=False
    )
    df_transacciones["valor"] = pd.to_numeric(
        df_transacciones["valor"], errors="coerce"
    )
    df_transacciones["valor"] = df_transacciones["valor"].fillna(0)
    df_transacciones["fecha"] = pd.to_datetime(
        df_transacciones["fecha"], errors="coerce"
    )
    df_transacciones = df_transacciones.dropna(thresh=3)
    return df_transacciones
