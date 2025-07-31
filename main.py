# %%
import pandas as pd

from pynanzas import (
    Portafolio,
    cargar_datos,
    prods_raw_a_df,
    trans_raw_to_df,
)

datos: dict[str, pd.DataFrame] = cargar_datos()
df_prods: pd.DataFrame = prods_raw_a_df(
    datos["productos"], datos["diccionario"])
df_transacciones: pd.DataFrame = trans_raw_to_df(datos["transacciones"])

portafolio: Portafolio = Portafolio(df_prods, df_transacciones)
print(portafolio.productos.keys())
