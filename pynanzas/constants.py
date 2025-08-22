import os
from pathlib import Path

TEST = False

TABLA_PRODS: str = "productos"
TABLA_MOVS: str = "movimientos"
TABLA_DICC: str = "diccionario"

PROD_ID: str = "producto_id"

try:
    dir_base: Path = Path(__file__).resolve().parent.parent
except NameError:
    dir_base = Path(os.getcwd()).resolve().parent

if not (dir_base / "pynanzas").exists():
    dir_actual = Path(os.getcwd()).resolve()
    while dir_actual != dir_actual.parent:
        if (dir_actual / "pynanzas").exists():
            dir_base = dir_actual
            break
        dir_actual = dir_actual.parent

DIR_BASE: Path = dir_base
DIR_DATA: Path = DIR_BASE / "data"
