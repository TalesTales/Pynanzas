"""
Constantes utilizadas en el proyecto de análisis de inversiones.

Este módulo define constantes globales que se utilizan en todo el proyecto,
incluyendo categorías de movimientos financieros y rutas de directorios.
"""

import os
from pathlib import Path

BD_SQLITE: str = 'pynanzas_bd.sqlite'
BD_TEST: str = 'pynanzas_bd_test.sqlite'

TABLA_PRODS: str = 'productos'
TABLA_MOVS: str = 'movimientos'

PROD_ID: str = 'producto_id'

# Categorías de movimientos financieros
MOVS_INTERESES: list[str] = ["intereses", "dividendos", "rendimientos"]
MOVS_NO_APORTES: list[str] = [
    "saldo_inicial",
    "comisiones",
    "comisión",
    "impuesto",
] + MOVS_INTERESES
MOVS_APORTES: list[str] = [
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