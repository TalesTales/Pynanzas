from dataclasses import asdict
import sqlite3

from pynanzas.constants import PROD_ID
from pynanzas.sql.diccionario import BD_SQL, ColumDDL, NomBD, NomTablas
from pynanzas.sql.esquemas import EsquemaMovs


def insertar_mov(
        movimiento: EsquemaMovs,
        nom_tabla_movs: NomTablas = NomTablas.MOVS,
        producto_id: str = PROD_ID,
        nom_bd: NomBD = BD_SQL
) -> None:
    from pynanzas.sql.sqlite import tabla_existe

    mov = asdict(movimiento)
    
    mov.pop('id', None)
    mov.pop('fecha_agregada', None)
    
    columnas: str = ','.join(mov.keys())
    placeholders: str = ','.join(['?'] * len(mov.keys()))
    valores: tuple = tuple(mov.values())

    with sqlite3.connect(nom_bd) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        if not tabla_existe(cursor, nom_tabla_movs):
            crear_tabla_movs(nom_tabla_movs=nom_tabla_movs, nom_bd=nom_bd)
        query: str = (f"INSERT INTO {nom_tabla_movs} "
                      f"({columnas}) "
                      f"VALUES ({placeholders})")
        cursor.execute(query, valores)
        conn.commit()  # Agregado: faltaba commit

EsquemaMovsDDL: EsquemaMovs =  EsquemaMovs(
    id = ColumDDL.INT_PK_AUTO,
    producto_id = ColumDDL.TXT_NOT_NULL,
    fecha = ColumDDL.DATE_NOT_NULL,
    tipo = ColumDDL.TXT_NOT_NULL,
    valor  = ColumDDL.REAL_NOT_NULL,
    unidades  = ColumDDL.REAL,
    valor_unidades = ColumDDL.REAL,
    fecha_agregada = ColumDDL.DATE_ACTUAL
)

def crear_tabla_movs(esquema_movs: EsquemaMovs = EsquemaMovsDDL,
                     nom_tabla_movs: NomTablas = NomTablas.MOVS,
                     nom_tabla_prods: NomTablas = NomTablas.PRODS,
                     producto_id: str = PROD_ID,
                     nom_bd: NomBD = BD_SQL) -> None:
    from pynanzas.sql.prods import crear_tabla_prods
    from pynanzas.sql.sqlite import tabla_existe

    if nom_tabla_movs == "":
        raise ValueError("crear_tabla_movs: nom_tabla_movs vacio")
    if nom_tabla_prods == "":
        raise ValueError("crear_tabla_movs: nom_tabla_prods vacio")
    if esquema_movs is None or len(esquema_movs) == 0:
        esquema_movs = EsquemaMovsDDL

    columnas_ddl: list[str] = []
    for k, v in esquema_movs.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl = (',\n'.join(columnas_ddl))
    orden_ddl += (f",\nFOREIGN KEY ({producto_id}) REFERENCES"
                  f" {nom_tabla_prods} ({producto_id})")
    try:
        with sqlite3.connect(nom_bd) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_existe(cursor, nom_tabla_prods):
                crear_tabla_prods(nom_tabla_prods=nom_tabla_prods,
                                  nom_bd=nom_bd)
            query: str = (f"CREATE TABLE IF NOT EXISTS {nom_tabla_movs} "
                          f"(\n{orden_ddl}\n);")
            print(query)  # TODO: logging
            cursor.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_movs: error sql {e}")