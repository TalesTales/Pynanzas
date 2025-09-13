from dataclasses import asdict
from datetime import datetime

import duckdb

from pynanzas.duck.dicc import (
    PATH_DDB,
    PROD_ID,
    NomTabl,
    PathBD,
)
from pynanzas.duck.esquemas import EsquemaMovs
from pynanzas.io.cargar_data import (
    _cargar_tabla_ddb_a_relation,
)
from pynanzas.modelos.producto import ProductoFinanciero


def _insertar_mov_ddb(
        movimientos: list[EsquemaMovs],
        nom_tabla_movs: NomTabl = NomTabl.MOVS,
        path_db: PathBD = PATH_DDB,
        local_con: duckdb.DuckDBPyConnection | None = None
) -> None:
    print("Insertar movimientos\n")
    print("====")
    try:
        if local_con is None:
            with duckdb.connect(path_db) as local_con:
                inicio_transaccion: str = "BEGIN TRANSACTION;\n"
                local_con.execute(inicio_transaccion)
                print(inicio_transaccion)
                for mov in movimientos:
                    m = asdict(mov)
                    m.pop('id', None)
                    m.pop('fecha_agregada', None)
                    columnas: str = ','.join(m.keys())
                    placeholders: str = ','.join(['?'] * len(m.keys()))
                    valores: tuple = tuple(m.values())

                    query = (f"INSERT INTO {nom_tabla_movs}\n"
                              f"({columnas}) VALUES ({placeholders});\n")
                    print(query)
                    print(valores)
                    local_con.execute(query, valores)
                commit = input('commit? s/n: ')
                if commit == 's':
                    local_con.execute("COMMIT;")
                    print('commit;')
                else:
                    local_con.execute("ROLLBACK;")
                    print('rollback;')
                print(_cargar_tabla_ddb_a_relation(nom_tabla_movs, path_db,
                                             local_con).select("producto_id","fecha","tipo","valor","id").order("id "
                                                              "desc").limit(len(movimientos)+3))
        else:
            print("No conn passed")
    except Exception as e:
        print(f"sql.insertar_mov_ddb: error sql {e}")


def fabricar_movs(nom_tabla_movs: NomTabl= NomTabl.MOVS,
                  path_db: PathBD = PATH_DDB,
                  local_con: duckdb.DuckDBPyConnection | None = None) -> None:
    insertar: bool = True
    movs: list[EsquemaMovs] = []
    while insertar:
        producto_id: str = input("producto_id: ")
        fecha: str = input("fecha: ")
        tipo: str = input("tipo: ")
        valor: float = float(input("valor: "))
        crear_mov: str = (f"¿Insertar: {producto_id}, {fecha}, {tipo},"
                          f" {valor}? s/n: ")
        append: str = input(crear_mov)
        if append == "s":
            mov: EsquemaMovs = EsquemaMovs(producto_id, fecha, tipo, valor)
            movs.append(mov)
            print(movs)
        else:
            pass

        insertar_otro: str = input("¿Insertar otro movimiento? s/n: ")
        if insertar_otro == "s":
            pass
        else:
            insertar = False
        print("========")
        print("\n")
    _insertar_mov_ddb(movs, nom_tabla_movs, path_db, local_con)

def update_prod_ddb(prod: ProductoFinanciero,
                    ask_commit: bool= True,
                    prod_id: str = PROD_ID,
                    nom_tabl_prod: NomTabl = NomTabl.PRODS,
                    path_db: PathBD = PATH_DDB
                    ):
    query: str = (f"""UPDATE {nom_tabl_prod}
                  SET abierto = ?,
                      aportes = ?,
                      intereses = ?,
                      saldo = ?,
                      xirr = ?,
                      fecha_actualizacion = ?
                  WHERE {prod_id} = ?
                  """)
    valores: tuple = (prod.abierto,
                     prod.aportes,
                     prod.intereses,
                     prod.saldo,
                     prod.xirr,
                     datetime.now(),
                     prod.producto_id)
    if ask_commit:
        print(query, valores)
        commit = input("Confirmar UPDATE? s/n: ") if ask_commit else "s"
        if commit == "s":
            try:
                with duckdb.connect(path_db) as con:
                    con.execute(query, valores)
                    print(con.sql(f"""SELECT 
                                    abierto,
                                    aportes,
                                    intereses,
                                    saldo,
                                    xirr,
                                    fecha_actualizacio?
                                  FROM {nom_tabl_prod}
                                    WHERE {prod_id} 
                                    = '{prod.producto_id}'"""))
            except:
                raise
        else:
            print("Operation cancelled")
            return
    else:
        try:
            with duckdb.connect(PATH_DDB) as con:
                con.execute(query, valores)
        except Exception as e:
            raise e

if __name__ == '__main__':
    pass