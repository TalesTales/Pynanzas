# %%
from pynanzas import DF_PRODS, DF_TRANS, Portafolio

portafolio: Portafolio = Portafolio(
    df_productos=DF_PRODS, df_transacciones=DF_TRANS)
print(portafolio.productos.keys())

# %%
print(str(portafolio))
