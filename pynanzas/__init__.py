import atexit

from pynanzas.duck.con import cerrar_cons
from pynanzas.duck.manipulacion import fabricar_movs
from pynanzas.modelos.producto import fabrica_prod

atexit.register(cerrar_cons)


__all__ = ["fabricar_movs",
           "fabrica_prod"]