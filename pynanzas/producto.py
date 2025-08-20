from dataclasses import dataclass, field
from datetime import date

import numpy as np
from overrides import override
import pandas as pd
import pyxirr

from pynanzas.diccionario import (
    Liquidez,
    Moneda,
    MovsAportes,
    MovsIntereses,
    Plazo,
    Riesgo,
)

MOVS_APORTES = [m.value for m in MovsAportes]
MOVS_INTERESES = [m.value for m in MovsIntereses]


@dataclass
class ProductoFinanciero:
    producto_id: str
    nombre: str
    ticker: str
    simulado: bool
    moneda: Moneda
    riesgo: Riesgo
    liquidez: Liquidez
    plazo: Plazo
    objetivo: str
    administrador: str
    plataforma: str
    tipo_producto: str
    tipo_inversion: str
    # categoria: str
    abierto: bool = True
    asignacion: float = 0
    saldo: float = field(init=False, default=0)
    aportes: float = field(init=False, default=np.nan)
    intereses: float = field(init=False, default=np.nan)
    xirr: float | None = field(init=False, default=np.nan)

    peso: float = 0.0

    saldo_inicial: float = field(init=False, default=np.nan)
    rentabilidad_acumulada: float = field(init=False, default=np.nan)

    movs_hist: pd.DataFrame = field(init=False, default_factory=pd.DataFrame)
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
    def __str__(self) -> str:

        abierto_tag: str = "[ABIERTO]" if self.abierto else "[CERRADO]"
        string: str = (
            f"{self.nombre}: {self.ticker} | {abierto_tag} | "
            f"Plataforma: {self.plataforma}, Tipo: {self.tipo_producto}, "
            f"Riesgo: {self.riesgo}, Plazo: {self.plazo}, "
            f"Administrado por {self.administrador}"
        )
        if self.abierto:
            xirr_display = (
                f"{self.xirr:.2%}"
                if (self.xirr is not None and not np.isnan(self.xirr))
                else "N/A"
            )
            string += f"| Saldo: COP ${self.saldo:,.2f}"  # TODO: Modificar moneda
            string += f" | XIRR: {xirr_display}"
            string += (
                f" | Peso: {self.peso:.2%}"
                if (self.peso is not None and not np.isnan(self.peso))
                else "N/A"
            )
            string += (
                f" | Asignación: {self.asignacion:.2%}"
                if (self.asignacion is not np.isnan(self.asignacion))
                else "N/A"
            )
        return string

    @override
    def __repr__(self) -> str:  # TODO: Mejorar representación
        return (f"<pynanzas.producto.ProductoFinanciero: {self.producto_id} "
                f"at {hex(id(self))}>")

    def procesar_movs(self, df_movs_filtrados_prod: pd.DataFrame) -> None:
        if df_movs_filtrados_prod.empty:
            self.abierto = False
            self.movs_hist = pd.DataFrame()
            return
        self.movs_hist = df_movs_filtrados_prod.sort_values(
            by="fecha"
        ).copy()
        self.movs_hist["saldo_historico"] = (
            self.movs_hist["valor"].cumsum().round(2)# TODO: Pasarlo a SQLite
        )

        self._calcular_metricas_basicas()

        self._calcular_xirr_hist()

    def _calcular_metricas_basicas(self) -> None:
        """Calcula saldos, aportes e intereses."""
        self.saldo_inicial = self.movs_hist[
            self.movs_hist["tipo"] == "saldo_inicial"
            ]["valor"].sum()

        self.aportes = self.movs_hist[
            self.movs_hist["tipo"].isin(values=MOVS_APORTES)
        ]["valor"].sum() # TODO: Query

        self.intereses = self.movs_hist[
            self.movs_hist["tipo"].isin(values=MOVS_INTERESES)
        ]["valor"].sum()

        self.saldo = (
            self.movs_hist["saldo_historico"].iloc[-1]
            if not self.movs_hist.empty
            else 0.0
        )

        self.abierto = False if self.saldo == 0.0 else True

        self.rentabilidad_acumulada = (
                self.saldo - self.aportes - self.saldo_inicial
        )

        df_movs_reales: pd.DataFrame = self.movs_hist[ #TODO:
            # Cambiar trans por movs
            self.movs_hist["tipo"] != "saldo_inicial"
            ]

        if not df_movs_reales.empty:
            self.fecha_primera_transaccion = df_movs_reales[
                "fecha"
            ].iloc[0]
            self.fecha_ultima_transaccion = df_movs_reales[
                "fecha"
            ].iloc[-1]

    def _calcular_xirr_hist(self) -> None:
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
        if self.movs_hist.empty:
            self.movs_hist["xirr_historica"] = np.nan
            self.xirr = np.nan
            return

        xirr_historica: list[float] = []

        for i in range(len(self.movs_hist)):
            historial_hasta_fecha: pd.DataFrame = self.movs_hist.iloc[
                : i + 1
            ].copy()
            df_flujos: pd.DataFrame = historial_hasta_fecha[
                historial_hasta_fecha["tipo"].isin(MOVS_APORTES)
            ].copy()
            if df_flujos.empty:
                xirr_historica.append(np.nan)
                continue

            fechas = df_flujos["fecha"].tolist()

            valores = (-df_flujos["valor"]).tolist()  # Cambiar signo

            fecha_corte = self.movs_hist.iloc[i]["fecha"]
            valor_final = self.movs_hist.iloc[i]["saldo_historico"]

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

        self.movs_hist["xirr_historica"] = xirr_historica

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
                self.movs_hist.empty
                or "xirr_historica" not in self.movs_hist.columns
        ):
            return pd.DataFrame()
        else:
            return pd.DataFrame(self.movs_hist["xirr_historica"])
