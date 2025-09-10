from enum import StrEnum
import os

from pynanzas.constants import DIR_DATA
from pynanzas.version import VERSION_DB


class ColumDDL(StrEnum):
    INT_PK = "INTEGER primary key"
    INT_PK_AUTO = "INTEGER primary key AUTOINCREMENT"
    INT_DEFAULT = "INTEGER default 0"
    TXT_NOT_NULL = "TEXT not null"
    TXT_UNIQUE = "TEXT not null UNIQUE"
    TXT_PK = "TEXT not null primary key"
    REAL = "REAL"
    REAL_NOT_NULL = "REAL not null"
    REAL_DEFAULT_CERO = "REAL not null default 0.0"
    BOOL_FALSE = "BOOLEAN not null default FALSE"
    BOOL_TRUE = "BOOLEAN not null default TRUE"
    DATE = "DATE not null"
    DATE_NOT_NULL = "DATE not null"
    DATE_ACTUAL = "DATE default CURRENT_TIMESTAMP"

    @staticmethod
    def txt_default(default: str) -> str:
        """Genera un tipo TEXT not null con valor por defecto."""
        return f"TEXT not null default '{default}'"


class NomTablas(StrEnum):
    PRODS = "productos"
    MOVS = "movimientos"

class NombreBD(StrEnum):
    SQLITE = f"pynanzas{VERSION_DB}.sqlite"
    DDB = f"pynanzas{VERSION_DB}.db"

class PathDB(StrEnum):
    SQLITE = os.path.join(DIR_DATA, NombreBD.SQLITE)
    DDB = os.path.join(DIR_DATA, NombreBD.DDB)

PATH_SQLITE: PathDB = PathDB.SQLITE
PATH_DDB: PathDB = PathDB.DDB

URI_SQLITE: str = f"sqlite:///{PATH_SQLITE}"
URI_DDB: str = f"duckdb:///{PATH_DDB}"