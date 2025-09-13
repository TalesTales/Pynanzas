from contextlib import contextmanager
import os

from dotenv import load_dotenv
import duckdb

from pynanzas.duck.dicc import PATH_DDB, PathBD

CON_LOCAL = None
CON_MD = None

load_dotenv()

MD_TOKEN: str = os.getenv("MD_TOKEN", "")
MD_GLOBAL: bool = False

def abrir_con_local_lectura(path_bd: PathBD = PATH_DDB) -> duckdb.DuckDBPyConnection:
    global CON_LOCAL
    if CON_LOCAL is None:
        CON_LOCAL = duckdb.connect(path_bd, read_only=True)
        print("🔗 Local connection opened")
    return CON_LOCAL

def abrir_con_md_lectura(md_token: str = MD_TOKEN) -> duckdb.DuckDBPyConnection:
    global CON_MD
    if CON_MD is None:
        CON_MD = duckdb.connect(f"md:?motherduck_token={md_token}", read_only=True)
        print("🔗 MD connection opened")
    return CON_MD

def cerrar_cons():
    global CON_LOCAL, CON_MD
    if CON_LOCAL:
        CON_LOCAL.close()
        CON_LOCAL = None
        print("❌ Local connection closed")
    if CON_MD:
        CON_MD.close()
        CON_MD = None
        print("❌ MD connection closed")
    print("cerrar cons ok")

@contextmanager
def local_cm_escritura(path_ddb: PathBD = PATH_DDB):
    con = duckdb.connect(path_ddb)
    try:
        print("🔗 Local context connection opened")
        yield con
    finally:
        con.close()
        print("❌ Local context connection closed")

@contextmanager
def md_cm(md_token: str = MD_TOKEN):
    con = duckdb.connect(f"md:?motherduck_token={md_token}")
    try:
        print("🔗 MD context connection opened")
        yield con
    finally:
        con.close()
        print("❌ MD context connection closed")