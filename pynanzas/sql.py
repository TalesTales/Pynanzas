import sqlite3
from typing import Optional

from .constants import BD_SQLITE


def crear_tabla_prods(nombre_tabla: str = 'productos',
                      nombre_columnas: Optional[dict[str,str]] = None,
                      nombre_bd: str = BD_SQLITE) -> None:
    """Crea una tabla de productos financieros en una base de datos SQLite.

    Esta función permite crear una tabla con un esquema predefinido para almacenar
    información sobre productos de inversión, incluyendo características como riesgo,
    liquidez, plazo, y detalles de administración.

    Args:
        nombre_tabla: Nombre de la tabla a crear en la base de datos.
        nombre_columnas: Diccionario que define las columnas y sus tipos/restricciones
            SQL. Si no se proporciona, se utilizará un esquema predefinido para
            productos financieros. Formato: {'nombre_columna': 'TIPO_SQL RESTRICCIONES'}.
        nombre_bd: Ruta del archivo de base de datos SQLite.

    Raises:
        ValueError: Si nombre_bd o nombre_tabla están vacíos.
        sqlite3.Error: Si ocurre un error durante la creación de la tabla.

    Examples:
        Crear tabla con esquema por defecto:

            crear_tabla_prods()

        Crear tabla personalizada:

            columnas_custom = {
                "id": "INTEGER PRIMARY KEY",
                "nombre": "TEXT NOT NULL",
                "precio": "REAL"
            }
            crear_tabla_prods(nombre_tabla='mi_tabla', nombre_columnas=columnas_custom)

    Note:
        Esquema por defecto:

            "producto_id":    "TEXT NOT NULL PRIMARY KEY",

            "nombre":         "TEXT NOT NULL UNIQUE",

            "ticket":         "TEXT NOT NULL UNIQUE",

            "simulado":       "BOOLEAN NOT NULL DEFAULT FALSE",

            "moneda":         "TEXT NOT NULL DEFAULT 'cop'",

            "riesgo":         "TEXT NOT NULL",

            "liquidez":       "TEXT NOT NULL",

            "plazo":          "TEXT NOT NULL",

            "asignacion":     "REAL NOT NULL DEFAULT 0.0",

            "objetivo":       "TEXT NOT NULL",

            "administrador":  "TEXT NOT NULL",

            "plataforma":     "TEXT NOT NULL",

            "tipo_producto":  "TEXT NOT NULL",

            "tipo_inversion": "TEXT NOT NULL",

        La función utiliza CREATE TABLE IF NOT EXISTS, por lo que es segura para
        ejecutar múltiples veces. Si no se proporciona una conexión, se creará
        y cerrará automáticamente. El esquema por defecto incluye 14 columnas
        específicas para productos financieros.

    Author:
        TalesTales - Documentación creada con Claude.
    """
    if nombre_bd == '':
        raise ValueError('crear_tabla_prods: nombre_bd vacio')
    if nombre_tabla == '':
        raise ValueError('crear_tabla_prods: nombre_tabla vacio')
    if nombre_columnas is None or len(nombre_columnas) == 0:
        nombre_columnas = {
            "producto_id":    "TEXT NOT NULL PRIMARY KEY",
            "nombre":         "TEXT NOT NULL UNIQUE",
            "ticket":         "TEXT NOT NULL UNIQUE",
            "simulado":       "BOOLEAN NOT NULL DEFAULT FALSE",
            "moneda":         "TEXT NOT NULL DEFAULT 'cop'",
            "riesgo":         "TEXT NOT NULL",
            "liquidez":       "TEXT NOT NULL",
            "plazo":          "TEXT NOT NULL",
            "asignacion":     "REAL NOT NULL DEFAULT 0.0",
            "objetivo":       "TEXT NOT NULL",
            "administrador":  "TEXT NOT NULL",
            "plataforma":     "TEXT NOT NULL",
            "tipo_producto":  "TEXT NOT NULL",
            "tipo_inversion": "TEXT NOT NULL",
        }
    orden_ddl: str = ''

    ultima_k: str = next(reversed(nombre_columnas.keys()))

    for k, v in nombre_columnas.items():
        orden_ddl += f'{k} {v}'
        if k != ultima_k:
            orden_ddl += ',\n'

    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            ddl_completo: str = f"""CREATE TABLE IF NOT EXISTS {nombre_tabla} (\n{orden_ddl}\n);"""
            print(ddl_completo) #TODO: logging
            cursor.execute(ddl_completo)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_prods: error sql {e}")

def crear_tabla_trans(nombre_tabla: str = 'transacciones',
                      nombre_columnas: Optional[dict[str, str]] = None,
                      nombre_tabla_prods: str = 'productos',
                      nombre_bd: str = BD_SQLITE) -> None:
    if nombre_bd == '':
        raise ValueError('crear_tabla_trans: nombre_bd vacio')
    if nombre_tabla == '':
        raise ValueError('crear_tabla_trans: nombre_tabla vacio')
    if nombre_tabla_prods == '':
        raise ValueError('crear_tabla_trans: nombre_tabla_prods vacio')
    if nombre_columnas is None or len(nombre_columnas) == 0:
        nombre_columnas = {
            "id":            "INTEGER PRIMARY KEY AUTOINCREMENT",
            "producto_id":   "TEXT NOT NULL",
            "fecha":         "DATE NOT NULL",
            "tipo":          "TEXT NOT NULL",
            "valor":         "REAL NOT NULL",
            "unidades":      "REAL",
            "valor_uniadad": "REAL",
        }
    ultima_k: str = next(reversed(nombre_columnas.keys()))
    orden_ddl: str = ''
    for k, v in nombre_columnas.items():
        orden_ddl += f'{k} {v}'
        orden_ddl += ',\n'
    orden_ddl = orden_ddl + f"FOREIGN KEY (producto_id) REFERENCES {nombre_tabla_prods} (producto_id)"
    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not _tabla_prods_existe(cursor, nombre_bd, nombre_tabla_prods):
                crear_tabla_prods(nombre_tabla=nombre_tabla_prods,
                                  nombre_bd=nombre_bd)
            ddl_completo: str = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} (\n{orden_ddl}\n);"
            print(ddl_completo)  #TODO: logging
            cursor.execute(ddl_completo)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_trans: error sql {e}")


def _tabla_prods_existe(cursor,
                        nombre_bd: str = BD_SQLITE,
                        nombre_tabla_prods: str = 'productos',
                        ) -> bool:
    query_tabla_prods: str = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nombre_tabla_prods}'"
    cursor.execute(query_tabla_prods)
    return bool(cursor.fetchall())