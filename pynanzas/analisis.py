
from typing import Optional

from numpy import empty
import pandas as pd

from pynanzas.producto import ProductoFinanciero


def dist_riesgo(productos: dict[str, ProductoFinanciero],
                saldos: Optional[dict[str, float]]  = None) -> pd.Series:
    if productos is empty:
        return pd.Series()
    if saldos is empty:
        return pd.Series()
    
    dict_dist_riesgo: dict[str, float] = {
        "Altísimo": 0,
        "Alto":     0,
        "Medio":    0,
        "Bajo":     0,
    }
    if saldos is None:
       saldos = {prod.producto_id: prod.saldo for prod in productos.values()}
    for producto in productos.values():
        if producto.riesgo in dict_dist_riesgo:
            dict_dist_riesgo[producto.riesgo] += saldos.get(
                producto.producto_id, 0)
    return pd.Series(dict_dist_riesgo, name="dist_riesgo", dtype="float")