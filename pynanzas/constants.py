import os
from pathlib import Path

BD_SQLITE: str = 'pynanzas_bd.sqlite'
BD_TEST: str = 'pynanzas_bd_test.sqlite'

TABLA_PRODS: str = 'productos'
TABLA_MOVS: str = 'movimientos'

PROD_ID: str = 'producto_id'

try:
    directorio_base: Path = Path(__file__).resolve().parent.parent
except NameError:
    directorio_base = Path(os.getcwd()).resolve().parent

BASE_PATH: Path = directorio_base