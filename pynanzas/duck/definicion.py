from enum import StrEnum
from pathlib import Path

import duckdb

from pynanzas.cons import DIR_BACKUP
from pynanzas.duck.dicc import MOV_ID, PATH_DDB, PROD_ID, NomTabl, PathBD
from pynanzas.duck.esquemas import EsquemaMovs, EsquemaProds
from pynanzas.io.export import _exportar_ddb_parquet, _exportar_ddb_csv


class DDLDDB(StrEnum):
    VARCHAR_UNIQ = "VARCHAR NOT NULL UNIQUE"
    VARCHAR_PK = "VARCHAR PRIMARY KEY"
    VARCHAR_NULL = "VARCHAR DEFAULT NULL"
    VARCHAR_NOT_NULL = "VARCHAR NOT NULL"
    BOOLEAN_FALSE = "BOOLEAN NOT NULL DEFAULT FALSE"
    BOOLEAN_TRUE = "BOOLEAN NOT NULL DEFAULT TRUE"
    FLOAT_NULL = "FLOAT DEFAULT NULL"
    DECIMAL_NULL = "DECIMAL(9,2) DEFAULT NULL"
    DECIMAL_NOT_NULL = "DECIMAL(9,2) NOT NULL"
    DATETIME_ACTUAL = "TIMESTAMP WITH TIME ZONE DEFAULT(CURRENT_TIMESTAMP)"
    TINYINT_NOT_NULL = "UTINYINT NOT NULL"
    DATE_NOT_NULL = "DATE NOT NULL"
    MOV_ID_PK = f"USMALLINT DEFAULT(nextval('{MOV_ID}')) PRIMARY KEY"
    @staticmethod
    def txt_default(default: str) -> str:
        return f"VARCHAR NOT NULL DEFAULT '{default}'"

ProdsDDL_DDB = EsquemaProds(
    producto_id = DDLDDB.VARCHAR_PK,
    nombre = DDLDDB.VARCHAR_UNIQ,
    ticker = DDLDDB.VARCHAR_UNIQ,
    simulado = DDLDDB.BOOLEAN_FALSE,
    moneda = DDLDDB.txt_default('cop'),
    riesgo = DDLDDB.TINYINT_NOT_NULL,
    liquidez = DDLDDB.TINYINT_NOT_NULL,
    plazo = DDLDDB.TINYINT_NOT_NULL,
    objetivo = DDLDDB.VARCHAR_NULL,
    administrador = DDLDDB.VARCHAR_NULL,
    plataforma = DDLDDB.VARCHAR_NULL,
    tipo_producto = DDLDDB.VARCHAR_NULL,
    tipo_inversion = DDLDDB.VARCHAR_NULL,
    abierto = DDLDDB.BOOLEAN_TRUE,
    asignacion  = DDLDDB.FLOAT_NULL,
    saldo = DDLDDB.DECIMAL_NULL,
    aportes = DDLDDB.DECIMAL_NULL,
    intereses = DDLDDB.DECIMAL_NULL,
    xirr = DDLDDB.FLOAT_NULL,
    fecha_actualizacion = DDLDDB.DATETIME_ACTUAL
)
def _crear_tabl_prods_ddb(esquema_prods: EsquemaProds = ProdsDDL_DDB,
                          nom_tabla_prods: NomTabl = NomTabl.PRODS,
                          path_bd: PathBD = PATH_DDB,
                          local_con: duckdb.DuckDBPyConnection | None = None) \
        -> None:
    esquema_prods = ProdsDDL_DDB if len(esquema_prods) == 0 else esquema_prods

    columns_ddl: list[str] = []
    for k, v in esquema_prods.items():
        columns_ddl.append(f"{k} {v}")
    orden_ddl: str = ",\n".join(columns_ddl)
    con_interna = duckdb.connect(path_bd) if local_con is None else local_con
    try:
        query: str = f"CREATE TABLE IF NOT EXISTS {nom_tabla_prods} "
        query += f"(\n{orden_ddl}\n);"
        print(f'--------\n{query}\n--------')  # TODO: logging
        con_interna.execute(query)
        print(con_interna.sql(f"SHOW {nom_tabla_prods}").pl())
    except Exception as e:
        print(f"sql._crear_tabla_ddb_prods: error duckdb {e}")
        raise
    finally:
        if local_con is None:
            con_interna.close()

MovsDDL_DDB: EsquemaMovs =  EsquemaMovs(
    id = DDLDDB.MOV_ID_PK,
    producto_id = DDLDDB.VARCHAR_NOT_NULL,
    fecha = DDLDDB.DATE_NOT_NULL,
    tipo = DDLDDB.VARCHAR_NOT_NULL,
    valor  = DDLDDB.DECIMAL_NOT_NULL,
    unidades  = DDLDDB.FLOAT_NULL,
    valor_unidades = DDLDDB.FLOAT_NULL,
    fecha_agregada = DDLDDB.DATETIME_ACTUAL,
    saldo_hist = DDLDDB.DECIMAL_NULL,
    xirr_hist = DDLDDB.FLOAT_NULL,
)

def _crear_tabla_ddb_movs(esquema_movs: EsquemaMovs = MovsDDL_DDB,
                          nom_tabla_movs: NomTabl = NomTabl.MOVS,
                          nom_tabla_prods: NomTabl = NomTabl.PRODS,
                          prod_id: str = PROD_ID,
                          mov_id: str = MOV_ID,
                          path_bd: PathBD = PATH_DDB,
                          local_con: duckdb.DuckDBPyConnection | None = None) -> None:

    if esquema_movs is None or len(esquema_movs) == 0:
        esquema_movs = MovsDDL_DDB

    columnas_ddl: list[str] = []
    for k, v in esquema_movs.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl = (',\n'.join(columnas_ddl))
    orden_ddl += (f",\nFOREIGN KEY ({prod_id}) REFERENCES"
                  f" {nom_tabla_prods}({prod_id})")

    sec =  f"""CREATE SEQUENCE {mov_id} INCREMENT BY 1 MINVALUE 1 MAXVALUE 
    65535 NO CYCLE;"""
    con_interna = duckdb.connect(path_bd) if local_con is None else local_con
    try:
        query: str = (f"CREATE TABLE IF NOT EXISTS {nom_tabla_movs} "
                      f"(\n{orden_ddl}\n);")
        print(sec, query)
        con_interna.execute(sec)
        con_interna.execute(query)
        print(con_interna.sql(f"SHOW {nom_tabla_prods}").pl())
    except Exception as e:
        print(f"sql._crear_tabla_ddb_movs: error duckdb {e}")
        raise
    finally:
        if local_con is None:
            con_interna.close()

def _reconstruir_ddb_parquet(esquema_prods: EsquemaProds = ProdsDDL_DDB,
                            esquema_movs: EsquemaMovs = MovsDDL_DDB,
                            nom_tabla_movs: NomTabl = NomTabl.MOVS,
                            nom_tabla_prods: NomTabl = NomTabl.PRODS,
                            prod_id: str = PROD_ID,
                            mov_id: str = MOV_ID,
                            path_bd: PathBD = PATH_DDB,
                            path_parquet: Path | None = None,
                            local_con: duckdb.DuckDBPyConnection | None
                            = None):

    col_prods = list(esquema_prods.keys())
    col_prods.remove('fecha_actualizacion')
    q_insert_prods = f"""INSERT INTO {nom_tabla_prods} ({', '.join(col_prods)})
        SELECT {', '.join(col_prods)} FROM p_prods.p_prods;"""


    col_movs = list(esquema_movs.keys())
    col_movs.remove('id')
    q_insert_movs = f"""INSERT INTO {nom_tabla_movs} ({', '.join(col_movs)})
        SELECT {', '.join(col_movs)} FROM p_movs.p_movs;"""

    dirs = [d for d in DIR_BACKUP.iterdir() if d.is_dir() and "_" in d.name]
    last_dir = max(dirs, key=lambda d: d.name) if path_parquet is None else path_parquet
    last_path_prods: Path = (last_dir / (nom_tabla_prods+".parquet"))
    last_path_movs: Path = (last_dir / (nom_tabla_movs+".parquet"))

    print("Reconstruir desde", last_dir)
    con_interna = duckdb.connect(PATH_DDB) if local_con is None else local_con
    try:
        _crear_tabl_prods_ddb(esquema_prods, nom_tabla_prods, path_bd, con_interna)
        _crear_tabla_ddb_movs(esquema_movs, nom_tabla_movs, nom_tabla_prods, prod_id, mov_id, path_bd, con_interna)
        attach_p_prods = f"ATTACH '{last_path_prods}' as p_prods"
        print(attach_p_prods)
        con_interna.execute(attach_p_prods)
        print(q_insert_prods)
        con_interna.execute(q_insert_prods)
        print(con_interna.sql(f"FROM {nom_tabla_prods}").pl())
        attach_p_prods = f"ATTACH '{last_path_movs}' as p_movs"
        print(attach_p_prods)
        con_interna.execute(attach_p_prods)
        print(q_insert_movs)
        con_interna.execute(q_insert_movs)
        print(con_interna.sql(f"FROM {nom_tabla_movs}").pl())
        _exportar_ddb_parquet()
        _exportar_ddb_csv()
    except Exception as e:
        print(f"sql._crear_tabla_ddb_movs: error duckdb {e}")
        raise
    finally:
        if local_con is None:
            con_interna.close()

if __name__ == '__main__':
    _reconstruir_ddb_parquet()