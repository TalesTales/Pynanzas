from dataclasses import dataclass
import sqlite3
from typing import Any, ItemsView, KeysView, Optional, ValuesView

from .constants import BD_SQLITE, PROD_ID, TABLA_MOVS, TABLA_PRODS


@dataclass
class DDLProducto:
    producto_id: str ="TEXT NOT NULL PRIMARY KEY"
    nombre: str = "TEXT NOT NULL UNIQUE"
    ticket: str ="TEXT NOT NULL UNIQUE"
    simulado: bool | str ="BOOLEAN NOT NULL DEFAULT FALSE"
    moneda: str ="TEXT NOT NULL DEFAULT 'cop'"
    riesgo: str = "TEXT NOT NULL"
    liquidez: str = "TEXT NOT NULL"
    plazo: str  = "TEXT NOT NULL"
    asignacion: float | str =  "REAL NOT NULL DEFAULT 0.0"
    objetivo: str  = "TEXT NOT NULL"
    administrador: str = "TEXT NOT NULL"
    plataforma: str = "TEXT NOT NULL"
    tipo_producto: str = "TEXT NOT NULL"
    tipo_inversion:str = "TEXT NOT NULL"

    def __len__(self) -> int:
        return len(self.__dict__)

    def keys(self) -> KeysView[str]:
        return self.__dict__.keys()

    def items(self) -> ItemsView[str, Any]:
        return self.__dict__.items()

    def values(self) -> ValuesView[Any]:
        return self.__dict__.values()
    
def crear_tabla_prods(
    tabla_prods: str = TABLA_PRODS,
    nombre_columnas: Optional[dict[str, str] | DDLProducto] = None,
    nombre_bd: str = BD_SQLITE,
) -> None:
    """Crea una tabla de productos financieros en una base de datos SQLite.

    Esta función permite crear una tabla con un esquema predefinido para almacenar
    información sobre productos de inversión, incluyendo características como riesgo,
    liquidez, plazo, y detalles de administración.

    Args:
        tabla_prods: Nombre de la tabla a crear en la base de datos.
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
    if nombre_bd == "":
        raise ValueError("crear_tabla_prods: nombre_bd vacio")
    if tabla_prods == "":
        raise ValueError("crear_tabla_prods: nombre_tabla vacio")
    if nombre_columnas is None or len(nombre_columnas) == 0:
        nombre_columnas = DDLProducto()
    columnas_ddl: list[str] = []
    for k, v in nombre_columnas.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl: str = ",\n".join(columnas_ddl)

    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            query: str = f"""CREATE TABLE IF NOT EXISTS {tabla_prods}
            (\n{orden_ddl}\n);"""
            print(f'crear_tabla_prod:\n{query}')  # TODO: logging
            cursor.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_prods: error sql {e}")


def crear_tabla_movs(
    nombre_tabla: str = TABLA_MOVS,
    nombre_columnas: Optional[dict[str, str]] = None,
    nombre_tabla_prods: str = TABLA_PRODS,
    producto_id: str = PROD_ID,
    nombre_bd: str = BD_SQLITE,
) -> None:
    if nombre_bd == "":
        raise ValueError("crear_tabla_movs: nombre_bd vacio")
    if nombre_tabla == "":
        raise ValueError("crear_tabla_movs: nombre_tabla vacio")
    if nombre_tabla_prods == "":
        raise ValueError("crear_tabla_movs: nombre_tabla_prods vacio")
    if nombre_columnas is None or len(nombre_columnas) == 0:
        nombre_columnas = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            producto_id: "TEXT NOT NULL",
            "fecha": "DATE NOT NULL",
            "tipo": "TEXT NOT NULL",
            "valor": "REAL NOT NULL",
            "unidades": "REAL",
            "valor_unidad": "REAL",
        }
    orden_ddl: str = ""
    for k, v in nombre_columnas.items():
        orden_ddl += f"{k} {v}"
        orden_ddl += ",\n"
    orden_ddl = (
        orden_ddl
        + f"""FOREIGN KEY ({producto_id}) REFERENCES
    {nombre_tabla_prods} ({producto_id})"""
    )
    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_prods_existe(cursor, nombre_tabla_prods):
                crear_tabla_prods(
                    tabla_prods=nombre_tabla_prods, nombre_bd=nombre_bd
                )
            ddl_completo: str = f"""CREATE TABLE IF NOT EXISTS {nombre_tabla}
            (\n{orden_ddl}\n);"""
            print(ddl_completo)  # TODO: logging
            cursor.execute(ddl_completo)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_movs: error sql {e}")


def tabla_prods_existe(
    cursor,
    nombre_tabla_prods: str = TABLA_PRODS,
) -> bool:
    query_tabla_prods: str = f"""SELECT name FROM sqlite_master WHERE
    type='table' AND name='{nombre_tabla_prods}'"""
    cursor.execute(query_tabla_prods)
    return bool(cursor.fetchall())

def insertar_prod(
    producto: dict[str, Any] | DDLProducto,
    tabla_prods: str = TABLA_PRODS,
    nombre_bd: str = BD_SQLITE
)->None:
    columnas: str = ','.join(producto.keys())
    placeholders: str = ','.join(['?'] * len(producto))
    valores = tuple(producto.values())
    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_prods_existe(cursor, tabla_prods):
                crear_tabla_prods(
                    tabla_prods=tabla_prods, nombre_bd=nombre_bd
                )
            query: str = f"""INSERT INTO {tabla_prods} ({columnas}) VALUES
            (\n{placeholders}\n);"""
            cursor.execute(query, valores)
            print(f'sql.insertar_prod:\n{query},{valores}')  # TODO: logging
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.insertar_prod: error sql {e}")