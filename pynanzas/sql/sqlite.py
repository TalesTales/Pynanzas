import sqlite3

from pynanzas.sql.diccionario import NomTablas


def tabla_existe(
        cursor: sqlite3.Cursor,
        nom_tabla: NomTablas,
) -> bool:
    query: str = ("SELECT name FROM sqlite_master WHERE type='table' AND "
                  "name=?")
    cursor.execute(query, (nom_tabla,))
    return bool(cursor.fetchall())

        
