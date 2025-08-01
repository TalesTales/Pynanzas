"""
Funciones a desarrollar:


"""

import numpy as np
import pandas as pd

from .producto import ProductoFinanciero


def historico_acumulado(
    portafolio: dict[str, ProductoFinanciero],
    abiertos: bool = True,
    simulados: bool = False,
) -> pd.DataFrame:
    """Extrae y consolida el histórico de saldos acumulados de múltiples productos financieros.

    Recopila los datos históricos de saldos de todos los productos en el portafolio que
    cumplan con los criterios especificados. Los datos se organizan en un DataFrame donde
    cada columna representa un producto (ticker) y cada fila una fecha con el saldo
    acumulado correspondiente.

    Args:
        portafolio (dict[str, ProductoFinanciero]): Diccionario donde las claves son
            los tickers de los productos y los valores son instancias de ProductoFinanciero.
        abiertos (bool, optional): Si True, incluye solo productos abiertos. Si False,
            incluye solo productos cerrados. Si None, incluye todos independientemente
            del estado. Defaults to True.
        simulados (bool, optional): Si True, incluye solo productos simulados. Si False,
            incluye solo productos reales. Si None, incluye todos independientemente
            del tipo. Defaults to False.

    Returns:
        pd.DataFrame: DataFrame con índice de fechas y columnas nombradas por ticker.
            Cada celda contiene el saldo histórico acumulado para ese producto en esa fecha.
            Los valores faltantes se propagan hacia adelante (forward fill). Si no hay
            datos válidos, retorna un DataFrame vacío.

    Note:
        - Solo se procesan productos que tengan la columna 'saldo_historico' en su
          historial_transacciones.
        - Se eliminan automáticamente los valores NaN de saldos.
        - Si hay múltiples transacciones en la misma fecha para un producto, se toma
          el último saldo (groupby fecha + last()).
        - Los datos se ordenan cronológicamente y se aplica forward fill para completar
          valores faltantes.
        - Los saldos están en valores absolutos (moneda), no en porcentajes.

    Example:
        # >>> portafolio = {
        # ...     'CDT_001': producto_cdt,
        # ...     'ACCIONES_ECOPETROL': producto_acciones,
        # ...     'FONDO_CONSERVADOR': producto_fondo
        # ... }
        # >>> saldos_df = historico_acumulado(portafolio, abiertos=True,simulados=False)
        # >>> print(saldos_df.head())
        #             CDT_001  ACCIONES_ECOPETROL  FONDO_CONSERVADOR
        # fecha
        # 2023-01-01  1000000              500000            2000000
        # 2023-01-02  1005000              485000            2010000
        # 2023-01-03  1010000              520000            2015000
        #
        # >>> # Calcular valor total del portafolio por fecha
        # >>> valor_total = saldos_df.sum(axis=1)
        #
        # >>> # Solo productos cerrados
        # >>> saldos_cerrados = historico_acumulado(portafolio, abiertos=False)
    """
    historico_acumulado_df: pd.DataFrame = pd.DataFrame()

    for i, (ticker, producto) in enumerate(portafolio.items()):
        if abiertos is not None and abiertos != producto.abierto:
            continue

        if simulados is not None and simulados != producto.simulado:
            continue

        if (
            producto.hist_trans.empty
            or "saldo_historico" not in producto.hist_trans.columns
        ):
            continue

        producto_saldo = producto.hist_trans[
            ["fecha", "saldo_historico"]
        ].copy()
        producto_saldo = producto_saldo[
            ~producto_saldo["saldo_historico"].isna()
        ]

        if producto_saldo.empty:
            continue
        producto_saldo = producto_saldo.groupby("fecha").last()
        producto_saldo = producto_saldo.rename(
            columns={"saldo_historico": ticker}
        )

        if historico_acumulado_df.empty:
            historico_acumulado_df = producto_saldo
        else:
            historico_acumulado_df = pd.concat(
                [historico_acumulado_df, producto_saldo], axis=1
            )

    if not historico_acumulado_df.empty:
        historico_acumulado_df = historico_acumulado_df.sort_index()
        historico_acumulado_df = historico_acumulado_df.ffill()
        # último valor
    return historico_acumulado_df


def historico_porcentaje(
    portafolio: dict[str, ProductoFinanciero],
) -> pd.DataFrame:
    """Calcula el histórico de participación porcentual de cada producto en el portafolio.

    Convierte los saldos históricos absolutos en porcentajes de participación, donde cada
    fila suma exactamente 100% (1.0). Utiliza operaciones vectorizadas para calcular
    eficientemente la proporción de cada producto respecto al valor total del portafolio
    en cada fecha.

    Args:
        portafolio (dict[str, ProductoFinanciero]): Diccionario donde las claves son
            los tickers de los productos y los valores son instancias de ProductoFinanciero.
            Se aplican los filtros por defecto de historico_acumulado() (abiertos=True,
            simulados=False).

    Returns:
        pd.DataFrame: DataFrame con índice de fechas y columnas nombradas por ticker.
            Cada celda contiene la participación porcentual (0.0 a 1.0) de ese producto
            en el valor total del portafolio para esa fecha. Cada fila suma exactamente 1.0.
            Los valores NaN se reemplazan con 0.0.

    Note:
        - Esta función internamente llama a historico_acumulado() con parámetros por defecto.
        - Utiliza operaciones vectorizadas (.div() con axis=0) para máxima eficiencia.
        - Si el valor total del portafolio es 0 en alguna fecha, todos los porcentajes
          serán 0 para esa fecha.
        - Los resultados están en formato decimal (0.25 = 25%), no porcentual.

    Raises:
        ZeroDivisionError: No se produce porque .fillna(0) maneja automáticamente las
            divisiones por cero.

    Example:
        # >>> portafolio = {
        # ...  'CDT_001': producto_cdt,
        # ...  'ACCIONES': producto_acciones,
        # ...  'BONOS': producto_bonos
        # ... }
        # >>> porcentajes_df = historico_porcentaje(portafolio)
        # >>> print(porcentajes_df.head())
        # CDT_001  ACCIONES  BONOS
        # fecha
        # 2023-01-01     0.50      0.30   0.20
        # 2023-01-02     0.48      0.32   0.20
        # 2023-01-03     0.52      0.28   0.20
        #
        # >>> # Verificar que cada fila suma 1.0 (100%)
        # >>> print(porcentajes_df.sum(axis=1).head())
        # fecha
        # 2023-01-01    1.0
        # 2023-01-02    1.0
        # 2023-01-03    1.0
        #
        # >>> # Convertir a porcentajes para visualización
        # >>> porcentajes_display = porcentajes_df * 100
        #
        # >>> # Usar para gráfico de área apilado
        # >>> ax = porcentajes_df.plot(kind='area', stacked=True,
        # ...                         title='Composición del Portafolio')
    """
    historico_acumulado_df: pd.DataFrame = historico_acumulado(portafolio)

    historico_porcentaje_df: pd.DataFrame = historico_acumulado_df.div(
        historico_acumulado_df.sum(axis=1), axis=0
    ).fillna(0)

    return historico_porcentaje_df
