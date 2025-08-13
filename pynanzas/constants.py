from enum import StrEnum
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

# Enumeraciones

class ColumDDL(StrEnum):
    """Enum para tipos de columna SQL comunes."""
    INT_PK = "INTEGER PRIMARY KEY"
    INT_PK_AUTO = "INTEGER PRIMARY KEY AUTOINCREMENT"
    TXT_NOT_NULL = "TEXT NOT NULL"
    TXT_UNIQUE = "TEXT NOT NULL UNIQUE"
    TXT_PK = "TEXT NOT NULL PRIMARY KEY"
    REAL = "REAL"
    REAL_NOT_NULL = "REAL NOT NULL"
    REAL_DEFAULT_CERO = "REAL NOT NULL DEFAULT 0.0"
    BOOL_FALSE = "BOOLEAN NOT NULL DEFAULT FALSE"
    BOOL_TRUE = "BOOLEAN NOT NULL DEFAULT TRUE"
    DATE = "DATE NOT NULL"
    DATE_NOT_NULL = "DATE NOT NULL"
    DATE_ACTUAL = "DATE DEFAULT CURRENT_TIMESTAMP"
    @staticmethod
    def txt_default(default: str) -> str:
        """Genera un tipo TEXT NOT NULL con valor por defecto."""
        return f"TEXT NOT NULL DEFAULT '{default}'"

