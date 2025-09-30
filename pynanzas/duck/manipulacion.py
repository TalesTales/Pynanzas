from dataclasses import asdict
from datetime import datetime

import duckdb

from pynanzas.duck.dicc import (
    PATH_DDB,
    PROD_ID,
    NomTabla,
    PathBD,
)
from pynanzas.duck.esquemas import EsquemaMovs
from pynanzas.io.cargar_data import (
    _cargar_tabla_ddb_a_relation,
)
from pynanzas.modelos.producto import ProductoFinanciero, fabrica_prod


def _insertar_mov_ddb(
        movimientos: list[EsquemaMovs],
        nom_tabla_movs: NomTabla = NomTabla.MOVS,
        nom_tabla_prods: NomTabla = NomTabla.PRODS,
        path_db: PathBD = PATH_DDB) -> None:
    print("Insertar movimientos\n")
    try:
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
                # print(query)
                # print(valores)
                local_con.execute(query, valores)
            for m in movimientos:
                print(m)

            commit = input('commit? s/n: ')
            if commit == 's':
                local_con.execute("COMMIT;")
                print('commit;')
                print('Actualizando')
                prods = []
                for mov in movimientos:
                    prods.append(asdict(mov)[PROD_ID])
                prods_unique = set(prods)
                local_con.execute(inicio_transaccion)
                prods = local_con.execute("select producto_id from prods;").fetchall()
                lista_prods = [row[0] for row in prods]
                for prod in prods_unique:
                    i = lista_prods.index(prod)
                    p = fabrica_prod(i,nom_tabla_prods,path_db)
                    _actualizar_prod(p,
                                     ask_commit=False,
                                     local_con=local_con)
                local_con.execute("COMMIT;")
            else:
                local_con.execute("ROLLBACK;")
                print('rollback;')
            print(_cargar_tabla_ddb_a_relation(nom_tabla_movs, path_db,
                                         local_con).select("producto_id","fecha","tipo","valor","id").order("id "
                                                          "desc").limit(len(movimientos)+3))
    except Exception as e:
        print(f"sql.insertar_mov_ddb: error sql {e}")


def fabricar_movs(nom_tabla_movs: NomTabla= NomTabla.MOVS,
                  nom_tabla_prods: NomTabla = NomTabla.PRODS,
                  path_db: PathBD = PATH_DDB) -> None:
    insertar: bool = True
    movs: list[EsquemaMovs] = []
    lista_prods: list[str] = []
    with duckdb.connect(path_db) as con:
        prods =  con.execute("select producto_id from prods;").fetchall()
        lista_prods = [row[0] for row in prods]
    while insertar:
        print(lista_prods)
        producto_id: str = input("producto_id: ")
        if producto_id.strip() not in lista_prods:
            print("Producto no encontrado")
            continue
        fecha: str = input("fecha: ")
        tipo: str = input("tipo: ")
        valor_str: str | float = input("valor: ")
        try:
            valor = float(valor_str)
        except Exception:
            print("Error en el valor")
            continue
        crear_mov: str = (f"¿Insertar: {producto_id}, {fecha}, {tipo},"
                          f" {valor}? s/n: ")
        append: str = input(crear_mov)
        if append == "s":
            mov: EsquemaMovs = EsquemaMovs(producto_id, fecha, tipo, valor)
            movs.append(mov)
            print(movs)

        insertar_otro: str = input("¿Insertar otro movimiento? s/n: ")
        if insertar_otro == "s":
            pass
        else:
            insertar = False
        print("========")
    _insertar_mov_ddb(movs, nom_tabla_movs,nom_tabla_prods, path_db)


def _actualizar_prod(prod: ProductoFinanciero,
                     local_con: duckdb.DuckDBPyConnection,
                     ask_commit: bool= True,
                     prod_id: str = PROD_ID,
                     nom_tabl_prod: NomTabla = NomTabla.PRODS,
                     ) -> None:
    query: str = (f"""UPDATE {nom_tabl_prod}
                  SET abierto = ?,
                      aportes = ?,
                      intereses = ?,
                      saldo = ?,
                      xirr = ?,
                      fecha_actualizacion = ?,
                      asignacion = ?
                  WHERE {prod_id} = ?
                  """)
    valores: tuple = (prod.abierto,
                      prod.aportes,
                      prod.intereses,
                      prod.saldo,
                      prod.xirr,
                      datetime.now(),
                      prod.asignacion,
                      prod.producto_id)
    if ask_commit:
        print(query, valores)
        commit = input("Confirmar UPDATE? s/n: ")
        if commit == "s":
            try:
                local_con.execute(query, valores)
                print(local_con.sql(f"""SELECT
                                abierto,
                                aportes,
                                intereses,
                                saldo,
                                xirr,
                                fecha_actualizacion,
                                asignacion
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
            local_con.execute(query, valores)
            print(f"Actualizado {prod.producto_id}")
        except Exception as e:
            raise e
