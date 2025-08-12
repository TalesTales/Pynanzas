"""
Constantes utilizadas en el proyecto de análisis de inversiones.

Este módulo define constantes globales que se utilizan en todo el proyecto,
incluyendo categorías de movimientos financieros y rutas de directorios.
"""

import os
from pathlib import Path

BD_SQLITE: str = 'pynanzas_bd.sqlite'

PROD_ID: str = 'producto_id'

# Categorías de movimientos financieros
MOVIMIENTOS_INTERESES: list[str] = ["intereses", "dividendos", "rendimientos"]
MOVIMIENTOS_NO_APORTANTES: list[str] = [
    "saldo_inicial",
    "comisiones",
    "comisión",
    "impuesto",
] + MOVIMIENTOS_INTERESES
MOVIMIENTOS_APORTES: list[str] = [
    "transferencia",
    "compra",
    "venta",
    "retiro",
    "apertura",
]
try:
    directorio_base: Path = Path(__file__).resolve().parent.parent
except NameError:
    directorio_base = Path(os.getcwd()).resolve().parent

BASE_PATH: Path = directorio_base