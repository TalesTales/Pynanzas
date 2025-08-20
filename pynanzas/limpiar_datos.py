from warnings import deprecated

import numpy as np
import pandas as pd
from pandas import CategoricalDtype

pd.set_option("future.no_silent_downcasting", True)

@deprecated('Se eliminará en el futuro')
def prods_raw_a_df(
    df_productos_raw: pd.DataFrame,
    df_diccionario_raw: pd.DataFrame,
) -> pd.DataFrame:
    """
    Procesa un DataFrame crudo de productos desde el Excel "Inversiones_DATA.xlsx" y lo convierte
    en un DataFrame estructurado con productos como filas y atributos como columnas.

    La función realiza las siguientes transformaciones:
    - Transpone la tabla para que los productos sean filas
    - Normaliza los nombres de columnas (minúsculas y guiones bajos)
    - Limpia y elimina columnas innecesarias
    - Convierte tipos de datos apropiados
    - Aplica categorías ordenadas según el diccionario de datos

    Args:
       df_productos_raw (pd.DataFrame): DataFrame crudo con los datos de productos tal como vienen del Excel.
           Se espera que tenga productos como columnas y atributos como filas.
       df_diccionario_raw (pd.DataFrame): DataFrame con el diccionario de datos que contiene el orden de las
           categorías para los atributos categóricos (riesgo, liquidez, plazos).

    Returns:
       pd.DataFrame: DataFrame procesado con:
           - Productos como filas (índice con nombre especificado)
           - Atributos como columnas con nombres normalizados
           - Tipos de datos apropiados (bool para 'simulado', numeric para 'asignacion')
           - Categorías ordenadas para atributos categóricos
           - Valores faltantes rellenados con 'N/A'

    Note:
       - La función maneja casos donde la primera fila no tiene valores únicos
       - Excluye automáticamente las columnas: 'comisión', 'composición' y valores NaN
       - Convierte 'simulado' a tipo booleano
       - Aplica orden categórico a 'riesgo', 'liquidez' y 'plazos' según el diccionario
    """
    identificador_producto: str = (
        df_diccionario_raw["Ficha"].iloc[0].lower().replace(" ", "_")
    )
    df_diccionario: pd.DataFrame = df_diccionario_raw.copy()
    if not df_productos_raw.iloc[0].is_unique:
        print("La primera fila de df_productos no tiene valores únicos!")
        columna_unica: list = list(range(len(df_productos_raw.columns)))
        fila_unica: pd.DataFrame = pd.DataFrame(
            [columna_unica], columns=df_productos_raw.columns
        )
        df_productos: pd.DataFrame = pd.concat(
            [fila_unica, df_productos_raw], ignore_index=True
        )
    else:
        df_productos = df_productos_raw.copy().set_index(
            df_productos_raw.columns[0]
        )
    df_productos = df_productos.T
    df_productos.columns = [
        str(col).lower().replace(" ", "_") for col in df_productos.columns
    ]
    columnas_a_excluir = ["comisión", "composición", np.nan]
    df_productos = df_productos.drop(
        columns=columnas_a_excluir, errors="ignore"
    )
    for col in df_productos.columns:
        if col in df_productos.columns:
            df_productos[col] = (
                df_productos[col].fillna("N/A").infer_objects(copy=False)  # pyright: ignore[reportCallIssue]
            )
    df_productos["simulado"] = (
        df_productos["simulado"].astype(int).astype(bool)
    )
    df_productos.index.name = identificador_producto
    df_productos["asignacion"] = pd.to_numeric(df_productos["asignacion"])
    columnas_categoricas = [
        "riesgo",
        "liquidez",
        "plazos",
    ]
    for atributo in columnas_categoricas:
        columna_minuscula: str = atributo.lower()
        if (
            atributo in df_diccionario.columns
            and columna_minuscula in df_productos.columns
        ):
            orden_categorias = df_diccionario[atributo].dropna().tolist()
            tipo_categorico_ordenado = CategoricalDtype(
                categories=orden_categorias, ordered=True
            )
            df_productos[columna_minuscula] = df_productos[
                columna_minuscula
            ].astype(tipo_categorico_ordenado)
    return df_productos

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
