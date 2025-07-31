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

    def __str__(self):
        return f"Portafolio: ({self.productos.__len__}) productos. COP${self.total:.2f}"

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


def balancear_portafolio(
    portafolio: dict[str, ProductoFinanciero], monto_invertir: float
) -> dict[str, float]:  # TODO:
    # Agregar filtros tipo simulado, abierto, etc.
    """Calcula la distribución óptima de una nueva inversión para rebalancear un portafolio.

    Esta función analiza el portafolio actual y determina cómo distribuir una nueva
    inversión para acercar los pesos de cada producto financiero a sus asignaciones
    objetivo. Prioriza los productos que están más alejados de su peso objetivo.

    Args:
        portafolio: Diccionario donde las llaves son los tickers de los productos
            financieros y los valores son objetos ProductoFinanciero que contienen
            información sobre saldo actual, asignación objetivo y peso actual.
        monto_invertir: Monto total en pesos que se desea invertir para rebalancear
            el portafolio.

    Returns:
        Diccionario con la distribución sugerida donde las llaves son los tickers
        y los valores son los montos en pesos que se deben invertir en cada producto.
        La suma de todos los valores será igual a monto_invertir.

    Note:
        La función imprime información detallada del análisis y la distribución
        sugerida en la consola, incluyendo pesos actuales vs objetivos y los
        pesos resultantes después de la inversión.
    """

    portafolio_actual: float = calcular_pesos(portafolio)
    portafolio_futuro: float = portafolio_actual + monto_invertir

    # Calcular valores objetivos para cada producto
    valores_actuales: dict[str, float] = {}
    valores_objetivo: dict[str, float] = {}
    diferencias: dict[str, float] = {}

    for ticker, producto in portafolio.items():
        if producto.asignacion >= 0:
            valor_actual = producto.saldo_actual
            valor_objetivo = portafolio_futuro * producto.asignacion
            diferencia = valor_objetivo - valor_actual

            valores_actuales[ticker] = valor_actual
            valores_objetivo[ticker] = valor_objetivo
            diferencias[ticker] = diferencia

            print(f"\n{ticker}:")
            print(f"  Peso actual: {producto.peso:.2%}")
            print(f"  Peso objetivo: {producto.asignacion:.2%}")
            print(f"  Valor actual: ${valor_actual:,.2f}")
            print(f"  Valor objetivo: ${valor_objetivo:,.2f}")
            print(f"  Diferencia: ${diferencia:,.2f}")

    diferencias_positivas: dict[str, float] = {
        k: v for k, v in diferencias.items() if v > 0
    }

    suma_diferencias_positivas: float = sum(diferencias_positivas.values())

    distribucion: dict[str, float] = {}

    if suma_diferencias_positivas > 0:
        for ticker, diferencia in diferencias_positivas.items():
            proporcion = diferencia / suma_diferencias_positivas
            monto_asignado = monto_invertir * proporcion
            distribucion[ticker] = monto_asignado
    else:
        for ticker, producto in portafolio.items():
            if producto.asignacion >= 0 and not np.isnan(
                producto.saldo_actual
            ):
                distribucion[ticker] = monto_invertir * producto.asignacion

    print("DISTRIBUCIÓN SUGERIDA DE LA NUEVA INVERSIÓN:")

    total_distribuido: float = 0
    for ticker, monto in distribucion.items():
        if monto > 0:
            porcentaje = (monto / monto_invertir) * 100
            print(f"{ticker}: ${monto:,.2f} ({porcentaje:.1f}%)")
            total_distribuido += monto

    print(f"\nTotal distribuido: ${total_distribuido:,.2f}")

    print("PESOS RESULTANTES DESPUÉS DE LA INVERSIÓN:")

    for ticker, producto in portafolio.items():
        if producto.asignacion >= 0 and not np.isnan(producto.saldo_actual):
            valor_final = valores_actuales[ticker] + distribucion.get(
                ticker, 0
            )
            peso_final = valor_final / portafolio_futuro
            diferencia_objetivo = peso_final - producto.asignacion

            print(f"{ticker}:")
            print(f"  Peso final: {peso_final:.2%}")
            print(f"  Objetivo: {producto.asignacion:.2%}")
            print(f"  Diferencia: {diferencia_objetivo:+.2%}")
    return distribucion


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
