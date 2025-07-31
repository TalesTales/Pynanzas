import numpy as np
import pandas as pd

from .producto import ProductoFinanciero


class Portafolio:
    def __init__(
        self, df_productos: pd.DataFrame, df_transacciones: pd.DataFrame
    ) -> None:
        self.productos: dict[str, ProductoFinanciero] = self._crear_portafolio(
            df_productos
        )
        self._procesar_trans(
            df_productos=df_productos,
            df_transacciones=df_transacciones,
            dict_productos=self.productos,
        )
        self.total: float = self._calcular_total()
        self.intereses_total: float = self._calcular_intereses()
        self.rentabilidad_total: float = self.intereses_total / self.total

    def _crear_portafolio(
        self, df_productos: pd.DataFrame
    ) -> dict[str, ProductoFinanciero]:
        if df_productos.empty:
            raise ValueError("df_productos cannot be empty")
        else:
            productos: dict[str, ProductoFinanciero] = {}
            for producto_id, fila in df_productos.iterrows():
                nuevo_producto = ProductoFinanciero(
                    producto_id=str(producto_id),
                    ticker=fila.get("ticket", "N/A"),
                    simulado=fila.get("simulado", False),
                    nombre_completo=fila.get("nombre", "Sin Nombre"),
                    administrador=fila.get("administrador", "N/A"),
                    moneda=fila.get("moneda", "COP"),
                    plataforma=fila.get("plataforma", "N/A"),
                    tipo_de_producto=fila.get("tipo_de_producto", "N/A"),
                    liquidez=fila.get("liquidez", "N/A"),
                    tipo_de_inversion=fila.get("tipo_de_inversion", "N/A"),
                    categoria=fila.get("categoria", "N/A"),
                    objetivo=fila.get("objetivo", "N/A"),
                    riesgo=fila.get("riesgo", "N/A"),
                    plazo=fila.get("plazo", "N/A"),
                    asignacion=fila.get("asignacion", 0.0),
                )
                setattr(self, nuevo_producto.producto_id, nuevo_producto)
                productos[str(producto_id)] = nuevo_producto
            return productos

    def _procesar_trans(
        self,
        df_productos: pd.DataFrame,
        df_transacciones: pd.DataFrame,
        dict_productos: dict[str, ProductoFinanciero],
    ) -> None:
        """
        Actualiza todos los productos del portafolio con sus transacciones correspondientes.

        Args:
            df_de_productos: DataFrame con información de productos
            df_con_transacciones: DataFrame con todas las transacciones
            dict_productos: Diccionario con objetos de productos del portafolio

        Returns:
            dict: Resultado con éxito/error y detalles
        """
        try:
            if df_productos.index.name not in df_transacciones.columns:
                error_msg = f"No se encontró la columna '{
                    df_productos.index.name}'en las transacciones."
                print(f"❌ ERROR: {error_msg}")
            # productos_procesados = 0

            for producto_id, objeto_producto in dict_productos.items():
                df_filtrado_para_producto = df_transacciones[
                    df_transacciones[df_productos.index.name] == producto_id
                ]
                objeto_producto.procesar_trans(df_filtrado_para_producto)
                # productos_procesados += 1
            # print(f"Procesados{productos_procesados}")# TODO: Pasar a logging.info

        except Exception as e:
            error_msg = f"Error inesperado durante la actualización: {str(e)}"
            print(f"❌ ERROR: {error_msg}")

    def _calcular_total(self) -> float:
        saldos = np.array(
            [producto.saldo_actual for producto in self.productos.values()]
        )
        saldos_validos = saldos[~np.isnan(saldos)]
        total = np.sum(saldos_validos)
        return total

    def _calcular_intereses(self) -> float:
        interes = np.array(
            [producto.intereses for producto in self.productos.values()]
        )
        intereses_valido = interes[~np.isnan(interes)]
        total = np.sum(intereses_valido)
        return total

    def balancear(self):
        raise NotImplementedError("Este método no esta implementado.")

    def saldos_hist(self):
        raise NotImplementedError("Este método no esta implementado.")

    def saldos_porcent_hist(self):
        raise NotImplementedError("Este método no esta implementado.")


def transacciones_a_producto(
    df_de_productos: pd.DataFrame,
    df_con_transacciones: pd.DataFrame,
    dict_productos: dict[str, ProductoFinanciero],
) -> None:
    """
    Actualiza todos los productos del portafolio con sus transacciones correspondientes.

    Args:
        df_de_productos: DataFrame con información de productos
        df_con_transacciones: DataFrame con todas las transacciones
        dict_productos: Diccionario con objetos de productos del portafolio

    Returns:
        dict: Resultado con éxito/error y detalles
    """
    try:
        if df_de_productos.index.name not in df_con_transacciones.columns:
            error_msg = f"No se encontró la columna '{
                df_de_productos.index.name}' en las transacciones."
            print(f"❌ ERROR: {error_msg}")
        productos_procesados = 0

        for id_producto, objeto_producto in dict_productos.items():
            df_filtrado_para_producto = df_con_transacciones[
                df_con_transacciones[df_de_productos.index.name] == id_producto
            ]
            objeto_producto.procesar_trans(df_filtrado_para_producto)
            productos_procesados += 1
        print(f"Procesados{productos_procesados}")

    except Exception as e:
        error_msg = f"Error inesperado durante la actualización: {str(e)}"
        print(f"❌ ERROR: {error_msg}")


def calcular_pesos(portafolio: dict[str, ProductoFinanciero]) -> float:
    total_portafolio: float = 0
    for saldo in portafolio.values():
        if not np.isnan(saldo.saldo_actual):
            total_portafolio += saldo.saldo_actual

    _producto: ProductoFinanciero
    for _producto in portafolio.values():
        if not np.isnan(_producto.saldo_actual):
            _producto.peso = _producto.saldo_actual / total_portafolio
    print(f"\nPortafolio calculado: {total_portafolio:.2f}")
    return total_portafolio


def crear_portafolio(
    df_productos: pd.DataFrame,
) -> dict[str, ProductoFinanciero]:
    """Crea un portafolio de productos financieros a partir de un DataFrame.

    Convierte cada fila del DataFrame en un objeto ProductoFinanciero y los organiza
    en un diccionario donde las claves son los identificadores de los productos.

    Args:
        df_productos (pd.DataFrame): DataFrame con información de productos financieros.
            Cada fila representa un producto y debe contener columnas con los atributos
            necesarios para crear objetos ProductoFinanciero.

    Returns:
        dict[str, ProductoFinanciero]: Diccionario donde las claves son los identificadores
            de los productos (índice del DataFrame convertido a string) y los valores son
            objetos ProductoFinanciero inicializados con los datos de cada fila.

    Note:
        - Utiliza el índice del DataFrame como identificador de producto.
        - Para atributos faltantes, utiliza valores predeterminados.
        - Imprime un mensaje de confirmación con el número de productos creados.
        - No procesa transacciones; para eso se debe llamar a transacciones_a_producto().
    """
    productos: dict[str, ProductoFinanciero] = {}
    for indice, fila in df_productos.iterrows():
        producto = ProductoFinanciero(
            producto_id=str(indice),
            ticker=fila.get("ticket", "N/A"),
            simulado=fila.get("simulado", False),
            nombre_completo=fila.get("nombre", "Sin Nombre"),
            administrador=fila.get("administrador", "N/A"),
            moneda=fila.get("moneda", "COP"),
            plataforma=fila.get("plataforma", "N/A"),
            tipo_de_producto=fila.get("tipo_de_producto", "N/A"),
            liquidez=fila.get("liquidez", "N/A"),
            tipo_de_inversion=fila.get("tipo_de_inversion", "N/A"),
            categoria=fila.get("categoria", "N/A"),
            objetivo=fila.get("objetivo", "N/A"),
            riesgo=fila.get("riesgo", "N/A"),
            plazo=fila.get("plazo", "N/A"),
            asignacion=fila.get("asignacion", 0.0),
        )
        productos[str(indice)] = producto
    print(
        f"\n✅ Portafolio creado AUTOMÁTICAMENTE con {len(productos)} productos"
    )
    return productos
