from enum import StrEnum
import os

from pynanzas.constants import (
    DIR_DATA,
    TABLA_MOVS,
    TABLA_PRODS,
    TEST,
)


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
    PRODS = TABLA_PRODS
    MOVS = TABLA_MOVS

class PathDB(StrEnum):
    SQLITE = os.path.join(DIR_DATA, "pynanzas_bd.sqlite")
    TEST = os.path.join(DIR_DATA,"pynanzas_bd_test.sqlite")


if not TEST:
    PATH_DB: PathDB = PathDB.SQLITE
else:
    PATH_DB = PathDB.TEST
