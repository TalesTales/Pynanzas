from enum import StrEnum
import os

from pynanzas.cons import DIR_DATA, __version__

VERSION_DB = __version__.major
NOM_BD = f"pynanzas{VERSION_DB}"
PROD_ID: str = "producto_id"
MOV_ID: str = "mov_id"

class NomTabla(StrEnum):
    PRODS = "prods"
    MOVS = "movs"


class NombreBD(StrEnum):
    SQLITE = f"{NOM_BD}.sqlite"
    DDB = f"{NOM_BD}.db"


class PathBD(StrEnum):
    SQLITE = os.path.join(DIR_DATA, NombreBD.SQLITE)
    DDB = os.path.join(DIR_DATA, NombreBD.DDB)

PATH_SQLITE: PathBD = PathBD.SQLITE
PATH_DDB: PathBD = PathBD.DDB
URI_SQLITE: str = f"sqlite:///{PATH_SQLITE}"
URI_DDB: str = f"duckdb:///{PATH_DDB}"
