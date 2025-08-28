import sqlite3

from pynanzas.constants import PROD_ID
from pynanzas.sql.diccionario import PATH_DB, ColumDDL, NomTablas, PathDB
from pynanzas.sql.esquemas import EsquemaMovs, EsquemaProds

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
    xirr = ColumDDL.REAL_DEFAULT_CERO,
    fecha_actualizacion = ColumDDL.DATE_ACTUAL
)

def crear_tabla_prods(esquema_prods: EsquemaProds = EsquemaProdsDDL,
                      nom_tabla_prods: NomTablas = NomTablas.PRODS,
                      path_db: PathDB = PATH_DB) -> None:
    if esquema_prods is None or len(esquema_prods) == 0:
        esquema_prods = EsquemaProdsDDL

    columnas_ddl: list[str] = []
    for k, v in esquema_prods.items():
        columnas_ddl.append(f"{k} {v}")
    orden_ddl: str = ",\n".join(columnas_ddl)

    try:
        with sqlite3.connect(path_db) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            query: str = f"CREATE TABLE IF NOT EXISTS {nom_tabla_prods} "
            query += f"(\n{orden_ddl}\n);"
            print(f'crear_tabla_prod:\n{query}')  # TODO: logging
            cursor.execute(query)
            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_prods: error sql {e}")



EsquemaMovsDDL: EsquemaMovs =  EsquemaMovs(
    id = ColumDDL.INT_PK_AUTO,
    producto_id = ColumDDL.TXT_NOT_NULL,
    fecha = ColumDDL.DATE_NOT_NULL,
    tipo = ColumDDL.TXT_NOT_NULL,
    valor  = ColumDDL.REAL_NOT_NULL,
    unidades  = ColumDDL.REAL,
    valor_unidades = ColumDDL.REAL,
    fecha_agregada = ColumDDL.DATE_ACTUAL,
    saldo_hist = ColumDDL.REAL_DEFAULT_CERO,
)

def crear_tabla_movs(esquema_movs: EsquemaMovs = EsquemaMovsDDL,
                     nom_tabla_movs: NomTablas = NomTablas.MOVS,
                     nom_tabla_prods: NomTablas = NomTablas.PRODS,
                     producto_id: str = PROD_ID,
                     path_db: PathDB = PATH_DB) -> None:
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
        with sqlite3.connect(path_db) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            if not tabla_existe(cursor, nom_tabla_prods):
                crear_tabla_prods(nom_tabla_prods=nom_tabla_prods,
                                  path_db=path_db)
            query: str = (f"CREATE TABLE IF NOT EXISTS {nom_tabla_movs} "
                          f"(\n{orden_ddl}\n);")
            print(query)  # TODO: logging
            cursor.execute(query)

            trigger_insert = f"""
                    CREATE TRIGGER IF NOT EXISTS trigger_saldo_hist_insert
                    AFTER INSERT ON {nom_tabla_movs}
                    FOR EACH ROW
                    BEGIN
                        -- Calcular saldo para el registro recién insertado
                        UPDATE {nom_tabla_movs} 
                        SET saldo_hist = ROUND((
                            SELECT SUM(m2.valor)
                            FROM {nom_tabla_movs} m2
                            WHERE m2.producto_id = NEW.producto_id
                            AND (m2.fecha < NEW.fecha 
                                 OR (m2.fecha = NEW.fecha AND m2.id <= NEW.id))
                        ), 2)
                        WHERE id = NEW.id;

                        -- Recalcular saldos para movimientos posteriores del mismo producto
                        UPDATE {nom_tabla_movs} 
                        SET saldo_hist = ROUND((
                            SELECT SUM(m3.valor)
                            FROM {nom_tabla_movs} m3
                            WHERE m3.producto_id = {nom_tabla_movs}.producto_id
                            AND (m3.fecha < {nom_tabla_movs}.fecha 
                                 OR (m3.fecha = {nom_tabla_movs}.fecha AND m3.id <= {nom_tabla_movs}.id))
                        ), 2)
                        WHERE producto_id = NEW.producto_id 
                        AND (fecha > NEW.fecha 
                             OR (fecha = NEW.fecha AND id > NEW.id));
                    END;
                    """

            trigger_update = f"""
                    CREATE TRIGGER IF NOT EXISTS trigger_saldo_hist_update
                    AFTER UPDATE OF valor ON {nom_tabla_movs}
                    FOR EACH ROW
                    BEGIN
                        -- Recalcular saldos desde la fecha del registro modificado en adelante
                        UPDATE {nom_tabla_movs} 
                        SET saldo_hist = ROUND((
                            SELECT SUM(m2.valor)
                            FROM {nom_tabla_movs} m2
                            WHERE m2.producto_id = {nom_tabla_movs}.producto_id
                            AND (m2.fecha < {nom_tabla_movs}.fecha 
                                 OR (m2.fecha = {nom_tabla_movs}.fecha AND m2.id <= {nom_tabla_movs}.id))
                        ), 2)
                        WHERE producto_id = NEW.producto_id 
                        AND (fecha >= NEW.fecha);
                    END;
                    """

            trigger_delete = f"""
                    CREATE TRIGGER IF NOT EXISTS trigger_saldo_hist_delete
                    AFTER DELETE ON {nom_tabla_movs}
                    FOR EACH ROW
                    BEGIN
                        -- Recalcular saldos para movimientos posteriores del mismo producto
                        UPDATE {nom_tabla_movs} 
                        SET saldo_hist = ROUND((
                            SELECT SUM(m2.valor)
                            FROM {nom_tabla_movs} m2
                            WHERE m2.producto_id = {nom_tabla_movs}.producto_id
                            AND (m2.fecha < {nom_tabla_movs}.fecha 
                                 OR (m2.fecha = {nom_tabla_movs}.fecha AND m2.id <= {nom_tabla_movs}.id))
                        ), 2)
                        WHERE producto_id = OLD.producto_id 
                        AND (fecha >= OLD.fecha);
                    END;
                    """
            cursor.execute(trigger_insert)
            print("✓ Trigger INSERT creado")

            cursor.execute(trigger_update)
            print("✓ Trigger UPDATE creado")

            cursor.execute(trigger_delete)
            print("✓ Trigger DELETE creado")

            conn.commit()
    except sqlite3.Error as e:
        print(f"sql.crear_tabla_movs: error sql {e}")
