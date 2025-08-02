"""
Constantes utilizadas en el proyecto de análisis de inversiones.

Este módulo define constantes globales que se utilizan en todo el proyecto,
incluyendo categorías de movimientos financieros y rutas de directorios.
"""

import os
from pathlib import Path

# Categorías de movimientos financieros
MOVIMIENTOS_INTERESES: list[str] = ["intereses", "dividendos", "rendimientos"]
"""
Lista de tipos de movimientos relacionados con intereses y rendimientos.

Estos movimientos representan ganancias pasivas generadas por los productos financieros
sin aportes adicionales del inversionista.
"""

MOVIMIENTOS_NO_APORTANTES: list[str] = [
    "saldo_inicial",
    "comisiones",
    "comisión",
    "impuesto",
] + MOVIMIENTOS_INTERESES
"""
Lista de tipos de movimientos que no constituyen aportes directos del inversionista.

Incluye movimientos como saldos iniciales, comisiones, impuestos y los movimientos
de intereses definidos en MOVIMIENTOS_INTERESES.
"""

MOVIMIENTOS_APORTES: list[str] = [
    "transferencia",
    "compra",
    "venta",
    "retiro",
    "apertura",
]
"""
Lista de tipos de movimientos que representan aportes o retiros directos del inversionista.

Estos movimientos implican un flujo de efectivo directo entre el inversionista y el
producto financiero, como transferencias, compras, ventas, retiros o aperturas.
"""

# Configuración de rutas
try:
    directorio_base: Path = Path(__file__).resolve().parent.parent
except NameError:
    directorio_base = Path(os.getcwd()).resolve().parent

BASE_PATH: Path = directorio_base
"""
Ruta base del proyecto.

Se determina automáticamente basándose en la ubicación del archivo actual o,
si no es posible, en el directorio de trabajo actual.
"""
