"""
Pynanzas: Un paquete para el análisis y seguimiento de portafolios de inversión.
"""
from pathlib import Path
import os
import pandas as pd

from .constants import (MOVIMIENTOS_APORTES,
                        MOVIMIENTOS_INTERESES, MOVIMIENTOS_NO_APORTANTES)
from .data_loader import cargar_datos
from .limpiar_datos import prods_raw_a_df, trans_raw_to_df
from .portafolio import Portafolio
from .producto import ProductoFinanciero

__all__ = ["Portafolio", "ProductoFinanciero", "MOVIMIENTOS_APORTES",
           "MOVIMIENTOS_INTERESES", "MOVIMIENTOS_NO_APORTANTES"]

DATOS: dict[str, pd.DataFrame] = cargar_datos()
DF_PRODS: pd.DataFrame = prods_raw_a_df(
    DATOS["productos"], DATOS["diccionario"])
DF_TRANS: pd.DataFrame = trans_raw_to_df(DATOS["transacciones"])
print("Datos cargados")
