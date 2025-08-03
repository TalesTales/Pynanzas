"""
Pynanzas: Un paquete para el análisis y seguimiento de portafolios de inversión.
"""

import pandas as pd

from .constants import (
    MOVIMIENTOS_APORTES,
    MOVIMIENTOS_INTERESES,
    MOVIMIENTOS_NO_APORTANTES,
)
from .data_loader import cargar_datos
from .limpiar_datos import prods_raw_a_df, trans_raw_to_df
from .portafolio import Portafolio
from .producto import ProductoFinanciero

__all__ = [
    "Portafolio",
    "ProductoFinanciero",
    "MOVIMIENTOS_APORTES",
    "MOVIMIENTOS_INTERESES",
    "MOVIMIENTOS_NO_APORTANTES",
    "PROD_ID",
]

DATOS: dict[str, pd.DataFrame] = cargar_datos()
DF_PRODS: pd.DataFrame = prods_raw_a_df(
    DATOS["productos"], DATOS["diccionario"]
)
DF_TRANS: pd.DataFrame = trans_raw_to_df(DATOS["transacciones"])
PROD_ID: str = DATOS["diccionario"]["Ficha"].iloc[0].lower().replace(" ", "_")

print("__init__:Datos cargados")
