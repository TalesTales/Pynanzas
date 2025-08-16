from enum import StrEnum

from pynanzas.constants import BD_SQLITE, BD_TEST, TABLA_MOVS, TABLA_PRODS


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
