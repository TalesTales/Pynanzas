# %%
import pandas as pd

from pynanzas import (
    Portafolio,
    cargar_datos,
    prods_raw_a_df,
    trans_raw_to_df,
)

DATA: dict[str, pd.DataFrame] = cargar_datos()
PROD_ID: str = DATA["diccionario"]["Ficha"].iloc[0].lower().replace(" ", "_")

# Limpieza de Datos
df_prods: pd.DataFrame = prods_raw_a_df(
    DATA["productos"], PROD_ID, DATA["diccionario"]
)
df_transacciones: pd.DataFrame = trans_raw_to_df(DATA["transacciones"])

portafolio: Portafolio = Portafolio(df_prods, df_transacciones)
print(portafolio.productos.keys())
# %%
portafolio.total
# print(portafolio_n.productos)
# xirr_historico: pd.DataFrame = xirr_historicas(
#     portafolio=portafolio, abiertos=None
# )
# display(xirr_historico.resample("ME").last() * 100)
# # (xirr_historico.resample('ME').last() * 100).plot()

# saldo_historico: pd.DataFrame = historico_acumulado(portafolio=portafolio)
# display(saldo_historico.resample("ME").last())  # pyright: ignore[reportUndefinedVariable]

# porcentaje_historico: pd.DataFrame = historico_porcentaje(
#     portafolio=portafolio
# )
# display(porcentaje_historico.resample("ME").last() * 100)  # pyright: ignore[reportUndefinedVariable]

# print(balancear_portafolio(portafolio, 300_000))
