import sqlite3

from pynanzas.sql.diccionario import ColumDDL, NomBD, NomTablas
from pynanzas.sql.esquemas import EsquemaProds

EsquemaProdsDDL: EsquemaProds = EsquemaProds(
    producto_id = ColumDDL.TXT_PK,
    nombre = ColumDDL.TXT_UNIQUE,
    ticket = ColumDDL.TXT_UNIQUE,
    simulado = ColumDDL.BOOL_FALSE,
    moneda = ColumDDL.txt_default('cop'),
    riesgo = ColumDDL.INT_DEFAULT,
    liquidez = ColumDDL.INT_DEFAULT,
    plazo = ColumDDL.INT_DEFAULT,
    asignacion = ColumDDL.REAL_DEFAULT_CERO,
    objetivo = ColumDDL.TXT_NOT_NULL,
    administrador = ColumDDL.TXT_NOT_NULL,
    plataforma = ColumDDL.TXT_NOT_NULL,
    tipo_producto = ColumDDL.TXT_NOT_NULL,
    tipo_inversion = ColumDDL.TXT_NOT_NULL,
    abierto = ColumDDL.BOOL_TRUE,
    saldo = ColumDDL.REAL_DEFAULT_CERO,
    aportes = ColumDDL.REAL_DEFAULT_CERO,
    intereses = ColumDDL.REAL_DEFAULT_CERO,
    xirr = ColumDDL.REAL_DEFAULT_CERO
)
def insertar_prod(producto: EsquemaProds,
        nom_tabla_prods: NomTablas = NomTablas.PRODS,
        nom_bd: NomBD = NomBD.BD_SQLITE
) -> None:
    from pynanzas.sql.sqlite import tabla_existe
    columnas: str = ','.join(producto.keys())
    placeholders: str = ','.join(['?'] * len(producto))
    valores = tuple(producto.values())
    try:
        with sqlite3.connect(nom_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_existe(cursor, nom_tabla_prods):
                crear_tabla_prods(nom_tabla_prods=nom_tabla_prods,
                                  nom_bd=nom_bd)
            query: str = (f"INSERT INTO {nom_tabla_prods} ({columnas}) VALUES "
                          f"({placeholders})")
            cursor.execute(query, valores)
            print(f'sql.insertar_prod:\n{query}, {valores}')  # TODO: logging
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.insertar_prod: error sql {e}")


def crear_tabla_prods(esquema_prods: EsquemaProds = EsquemaProdsDDL,
                      nom_tabla_prods: NomTablas = NomTablas.PRODS,
                      nom_bd: NomBD = NomBD.BD_SQLITE) -> None:
    if esquema_prods is None or len(esquema_prods) == 0:
        esquema_prods = EsquemaProdsDDL

    columnas_ddl: list[str] = []
    for k, v in esquema_prods.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl: str = ",\n".join(columnas_ddl)

    try:
        with sqlite3.connect(nom_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            query: str = f"CREATE TABLE IF NOT EXISTS {nom_tabla_prods} "
            query += f"(\n{orden_ddl}\n);"
            print(f'crear_tabla_prod:\n{query}')  # TODO: logging
            cursor.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_prods: error sql {e}")