# %%
from pynanzas import DF_PRODS, DF_TRANS, PROD_ID, Portafolio

portafolio: Portafolio = Portafolio(DF_PRODS, DF_TRANS, PROD_ID)
print(portafolio.productos.keys())

# %%
a = (portafolio.productos["FonNu"].hist_trans)

print(a)
