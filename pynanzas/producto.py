from dataclasses import dataclass, field
from datetime import date

import numpy as np
from overrides import override
import pandas as pd
import pyxirr

from .constants import MOVIMIENTOS_APORTES, MOVIMIENTOS_INTERESES


@dataclass
class ProductoFinanciero:
    """
    Representa un único producto o activo financiero dentro del portafolio.

    v 4.0

    Esta clase encapsula toda la información y lógica relacionada con un producto
    financiero individual, incluyendo sus características, historial de transacciones,
    métricas de rendimiento y cálculos de rentabilidad.

    La clase maneja automáticamente el procesamiento de transacciones y el cálculo
    de métricas como XIRR, saldos, aportes e intereses.

    Attributes:
        producto_id (str): Identificador único del producto.
        nombre_completo (str): Nombre completo del producto financiero.
        ticker (str): Símbolo o ticker del producto.
        simulado (bool): Indica si es un producto simulado o real.
        administrador (str): Entidad que administra el producto.
        moneda (str): Moneda en la que se denomina el producto.
        plataforma (str): Plataforma donde se opera el producto.
        tipo_de_producto (str): Tipo de producto financiero.
        liquidez (str): Nivel de liquidez del producto.
        tipo_de_inversion (str): Tipo de inversión.
        categoria (str): Categoría del producto.
        objetivo (str): Objetivo de inversión.
        riesgo (str): Nivel de riesgo del producto.
        plazo (str): Plazo de inversión.
        asignacion (float): Porcentaje de asignación objetivo en el portafolio.
        abierto (bool): Indica si el producto está actualmente abierto.
        peso (float): Peso actual del producto en el portafolio.
        saldo_inicial (float): Saldo inicial del producto.
        saldo_actual (float): Saldo actual del producto.
        aportes_totales (float): Total de aportes realizados.
        intereses (float): Total de intereses generados.
        rentabilidad_acumulada (float): Rentabilidad acumulada del producto.
        historial_transacciones (pd.DataFrame): Historial completo de transacciones.
        fecha_primera_transaccion (date): Fecha de la primera transacción.
        fecha_ultima_transaccion (date): Fecha de la última transacción.
        xirr (float): Tasa interna de retorno del producto.
        es_instrumento_mercado (bool): Indica si es un instrumento de mercado.
    """

    producto_id: str
    nombre_completo: str
    ticker: str
    simulado: bool
    administrador: str
    moneda: str
    plataforma: str
    tipo_de_producto: str
    liquidez: str
    tipo_de_inversion: str
    categoria: str
    objetivo: str
    riesgo: str
    plazo: str
    asignacion: float

    abierto: bool = True
    peso: float = 0.0

    saldo_inicial: float = field(init=False, default=np.nan)
    saldo_actual: float = field(init=False, default=0)
    aportes_totales: float = field(init=False, default=np.nan)
    intereses: float = field(init=False, default=np.nan)
    rentabilidad_acumulada: float = field(init=False, default=np.nan)

    hist_trans: pd.DataFrame = field(init=False, default_factory=pd.DataFrame)
    fecha_primera_transaccion: date | None = field(init=False, default=None)
    fecha_ultima_transaccion: date | None = field(init=False, default=None)
    aportes_hist: pd.DataFrame = field(
        init=False, default_factory=pd.DataFrame
    )
    intereses_hist: pd.DataFrame = field(
        init=False, default_factory=pd.DataFrame
    )
    rentabilidad_acumulada_hist: pd.DataFrame = field(
        init=False, default_factory=pd.DataFrame
    )

    xirr: float | None = field(init=False, default=np.nan)

    es_instrumento_mercado: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        """Inicialización post-creación del objeto."""
        # Determinar si es un instrumento que se negocia en mercados secundarios
        # instrumento_mercado: list[str] = ["acción", "accion", "acciones", "ETF", "stock", "equity"]
        # self.es_instrumento_mercado = True if self.tipo_de_producto in instrumento_mercado else False
        # print(f"Inicializado el producto:{self.producto_id}") #TODO: Implementar en logging

    def __hash__(self):
        """
        Hash basado únicamente en producto_id.
        """
        return hash(self.producto_id)

    def __eq__(self, other):
        """
        Igualdad basada en producto_id.
        """
        if not isinstance(other, ProductoFinanciero):
            return False
        return self.producto_id == other.producto_id

    @override
    def __str__(self):
        """
        Genera una representación en texto del producto financiero.

        Crea una cadena de texto con información clave del producto, incluyendo su ID,
        estado (abierto/cerrado) y tipo. Si el producto está abierto, también incluye
        información financiera como saldo actual, XIRR, peso en el portafolio y
        asignación objetivo.

        Returns:
            str: Representación en texto del producto financiero con sus atributos clave.
        """
        abierto_tag = "[ABIERTO]" if self.abierto else "[CERRADO]"
        rep = (f"| Producto: {self.producto_id} | Estado: {abierto_tag} | "
               f"Tipo{self.tipo_de_producto}")
        if self.abierto:
            xirr_display = (
                f"{self.xirr:.2%}"
                if (self.xirr is not None and not np.isnan(self.xirr))
                else "N/A"
            )
            rep += f"| Saldo: COP ${self.saldo_actual:.2f}"
            rep += f" | XIRR: {xirr_display}"
            rep += (
                f" | Peso: {self.peso:.2%}"
                if (self.peso is not None and not np.isnan(self.peso))
                else "N/A"
            )
            rep += (
                f" | Asignación: {self.asignacion:.2%}"
                if (
                    self.asignacion is not None
                    and not np.isnan(self.asignacion)
                )
                else "N/A"
            )
        return rep

    def procesar_trans(self, df_transacciones_producto: pd.DataFrame) -> None:
        """Procesa todas las transacciones del producto y calcula métricas.

        Toma un DataFrame con las transacciones del producto, las ordena cronológicamente,
        calcula el saldo histórico acumulado y actualiza todas las métricas del producto
        como saldos, aportes, intereses y XIRR.

        Args:
            df_transacciones_producto (pd.DataFrame): DataFrame con las transacciones
                del producto. Debe contener al menos las columnas 'fecha' y 'valor'.

        Returns:
            None: La función actualiza los atributos del objeto directamente.

        Note:
            - Si el DataFrame está vacío, marca el producto como cerrado.
            - Ordena las transacciones por fecha antes de procesarlas.
            - Calcula el saldo histórico acumulado usando cumsum().
            - Llama a los métodos internos _calcular_metricas_basicas() y
              _calcular_xirr_historica() para actualizar todas las métricas.
        """
        if df_transacciones_producto.empty:
            self.abierto = False
            self.hist_trans = pd.DataFrame()
            return
        self.hist_trans = df_transacciones_producto.sort_values(
            by="fecha"
        ).copy()
        self.hist_trans["saldo_historico"] = (
            self.hist_trans["valor"].cumsum().round(2)
        )

        self._calcular_metricas_basicas()

        self._calcular_xirr_historica()

    def _calcular_metricas_basicas(self) -> None:
        """Calcula saldos, aportes e intereses."""
        self.saldo_inicial = self.hist_trans[
            self.hist_trans["movimiento"] == "saldo_inicial"
        ]["valor"].sum()

        self.aportes_totales = self.hist_trans[
            self.hist_trans["movimiento"].isin(values=MOVIMIENTOS_APORTES)
        ]["valor"].sum()

        self.intereses = self.hist_trans[
            self.hist_trans["movimiento"].isin(values=MOVIMIENTOS_INTERESES)
        ]["valor"].sum()

        self.saldo_actual = (
            self.hist_trans["saldo_historico"].iloc[-1]
            if not self.hist_trans.empty
            else 0.0
        )

        self.abierto = False if self.saldo_actual == 0.0 else True

        self.rentabilidad_acumulada = (
            self.saldo_actual - self.aportes_totales - self.saldo_inicial
        )

        df_movimientos_reales: pd.DataFrame = self.hist_trans[
            self.hist_trans["movimiento"] != "saldo_inicial"
        ]

        if not df_movimientos_reales.empty:
            self.fecha_primera_transaccion = df_movimientos_reales[
                "fecha"
            ].iloc[0]
            self.fecha_ultima_transaccion = df_movimientos_reales[
                "fecha"
            ].iloc[-1]

    def _calcular_xirr_historica(self) -> None:
        """Calcula la XIRR (Tasa Interna de Retorno Extendida) progresiva para cada transacción.

        Calcula la XIRR para cada punto en el tiempo del historial de transacciones,
        considerando los flujos de caja (aportes) y el valor del saldo en cada fecha.
        Esto permite obtener una serie temporal de la rentabilidad del producto.

        La XIRR se calcula utilizando la biblioteca pyxirr, que implementa el algoritmo
        de Newton-Raphson para encontrar la tasa que hace que el valor presente neto
        de los flujos de caja sea cero.

        Args:
            None: Utiliza el historial_transacciones del objeto.

        Returns:
            None: Actualiza los siguientes atributos del objeto:
                - historial_transacciones: Añade la columna "xirr_historica"
                - xirr: Establece el valor final de XIRR (último valor válido)

        Note:
            - Los aportes (MOVIMIENTOS_APORTES) se consideran como flujos de caja negativos.
            - El saldo en cada fecha se considera como flujo de caja positivo.
            - Se filtran valores inválidos de XIRR (NaN, infinitos, o fuera del rango [-10, 10]).
            - Si no hay flujos de caja o el cálculo falla, se asigna NaN.
        """
        if self.hist_trans.empty:
            self.hist_trans["xirr_historica"] = np.nan
            self.xirr = np.nan
            return

        xirr_historica: list[float] = []

        for i in range(len(self.hist_trans)):
            historial_hasta_fecha: pd.DataFrame = self.hist_trans.iloc[
                : i + 1
            ].copy()
            df_flujos: pd.DataFrame = historial_hasta_fecha[
                historial_hasta_fecha["movimiento"].isin(MOVIMIENTOS_APORTES)
            ].copy()
            if df_flujos.empty:
                xirr_historica.append(np.nan)
                continue

            fechas = df_flujos["fecha"].tolist()

            valores = (-df_flujos["valor"]).tolist()  # Cambiar signo

            fecha_corte = self.hist_trans.iloc[i]["fecha"]
            valor_final = self.hist_trans.iloc[i]["saldo_historico"]

            fechas.append(fecha_corte)
            valores.append(valor_final)

            xirr_actual: float = np.nan

            try:
                resultado: float | None = pyxirr.xirr(fechas, valores)
                if (
                    resultado is not None
                    and not np.isinf(resultado)
                    and not np.isnan(resultado)
                    and -10 < resultado < 10
                ):
                    xirr_actual = resultado
            except Exception as e:
                print(f"Error: {e} en {self.producto_id} al calcular xirr")
                print(fechas, valores)
                pass

            xirr_historica.append(xirr_actual)

        self.hist_trans["xirr_historica"] = xirr_historica

        xirr_validas: list[float] = [
            x for x in xirr_historica if not np.isnan(x)
        ]
        self.xirr = xirr_validas[-1] if xirr_validas else np.nan

    def xirr_hist(self) -> pd.DataFrame:
        """Retorna el historial de XIRR progresiva como un DataFrame.

        Extrae la columna "xirr_historica" del historial de transacciones y la devuelve
        como un DataFrame independiente. Esto facilita el análisis y visualización de
        la evolución de la rentabilidad del producto a lo largo del tiempo.

        Returns:
            pd.DataFrame: DataFrame con la columna "xirr_historica" del historial de
                transacciones. Si el historial está vacío o no contiene la columna
                "xirr_historica", devuelve un DataFrame vacío.

        Note:
            Este método es útil para acceder a los datos de XIRR histórica sin necesidad
            de manipular directamente el historial completo de transacciones.
        """
        if (
            self.hist_trans.empty
            or "xirr_historica" not in self.hist_trans.columns
        ):
            return pd.DataFrame()
        else:
            return pd.DataFrame(self.hist_trans["xirr_historica"])
