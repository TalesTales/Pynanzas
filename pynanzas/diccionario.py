from enum import IntEnum, StrEnum

from pynanzas.constants import BD_SQLITE, BD_TEST, TABLA_MOVS, TABLA_PRODS


class MovsIntereses(StrEnum):
    """Enum para tipos de movimientos de intereses."""
    INTERESES = "intereses"
    DIVIDENDOS = "dividendos"
    RENDIMIENTOS = "rendimientos"

class MovsAportes(StrEnum):
    """Enum para tipos de movimientos que son aportes."""
    TRANSFERENCIA = "transferencia"
    COMPRA = "compra"
    VENTA = "venta"
    RETIRO = "retiro"
    APERTURA = "apertura"

class MovsNoAportes(StrEnum):
    """Enum para tipos de movimientos que NO son aportes."""
    SALDO_INICIAL = "saldo_inicial"
    COMISIONES = "comisiones"
    COMISION = "comisión"
    IMPUESTO = "impuesto"
    # Movimientos de intereses
    INTERESES = "intereses"
    DIVIDENDOS = "dividendos"
    RENDIMIENTOS = "rendimientos"


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


class NomTablas(StrEnum):
    PRODS = TABLA_PRODS
    MOVS = TABLA_MOVS

class NomBD(StrEnum):
    BD_SQLITE = BD_SQLITE
    BD_TEST = BD_TEST

class Riesgo(IntEnum):
    Nulo = 0
    Bajo = 1
    Medio = 2
    Alto = 3
    Altisimo = 4

class Liquidez(IntEnum):
    Inmediata = 4
    Alta = 3
    Media = 2
    Baja = 1
    Restringida = 0

class Plazo(IntEnum):
    Inmediato = 0
    Corto = 1
    Mediano = 2
    Largo = 5
    Pension = 10

class Moneda(StrEnum):
    COP = 'cop'
    USD = 'usd'
    GBP = 'gbp'
    EUR = 'eur'
    BTC = 'btc'

if __name__ == "__main__":
    for r in Riesgo:
        print(r.name, r.value)
