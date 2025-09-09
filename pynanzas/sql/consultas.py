
import polars as pl

from pynanzas.sql.diccionario import NomTablas, URI_SQLITE


def movs_filtrados_prod(producto_id: str,
                        nom_tabla_movs: NomTablas = NomTablas.MOVS,
                        uri: str = URI_SQLITE) -> (
        pl.LazyFrame):
    query = (f"SELECT * "
             f"FROM '{nom_tabla_movs}'"
             f"WHERE producto_id = ?")
    return pl.read_database_uri(query,
                                uri,
                                engine='adbc',
                                execute_options={"parameters": [producto_id]}
                                ).lazy()
if __name__ == "__main__":
    print(movs_filtrados_prod("FonNu").collect())
    a = movs_filtrados_prod("FonNu")
