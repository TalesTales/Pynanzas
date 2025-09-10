from dataclasses import dataclass, field
from functools import cached_property

from overrides import override
import polars as pl

from pynanzas.constants import PROD_ID
from pynanzas.diccionario import (
    Liquidez,
    Moneda,
    MovsAportes,
    MovsIntereses,
    Plazo,
    Riesgo,
)
from pynanzas.io.limpiar_data import _tabla_lf
from pynanzas.sql.diccionario import NomTablas


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
    abierto: bool = True
    asignacion: float = 0
    xirr: float | None = field(init = False, default = None)

    saldo_inicial: float  = field(init = False, default = 0)

    def __post_init__(self) -> None:
        self.abierto = False if self.saldo <= 0.0 else True

    def __hash__(self):
        return hash(self.producto_id)

    def __eq__(self, other):
        if not isinstance(other, ProductoFinanciero):
            return False
        return self.producto_id == other.producto_id

    @override
    def __repr__(self) -> str:  # TODO: Mejorar representación
        return (f"<pynanzas.producto.ProductoFinanciero: {self.producto_id} "
                f"en {hex(id(self))}>")

    @override
    def __str__(self) -> str:
        abierto_tag: str = "[ABIERTO]" if self.abierto else "[CERRADO]"
        string: str = (
            f"{self.nombre}: {self.ticker} | {abierto_tag} |")
        if self.abierto:
            xirr_display = (
                f"{self.xirr:.2%}"
                if (self.xirr is not None)
                else "N/A"
            )
            string += f"\nSaldo: COP ${self.saldo:,.2f}"  # TODO: Modificar moneda
            string += f" | XIRR: {xirr_display}"
            string += (
                f" | Asignación: {self.asignacion:.2%}"
                if (self.asignacion is not None)
                else "N/A"
            )
        string +=(f"\nPlataforma: {self.plataforma}, Tipo: {self.tipo_producto}, "
            f"\nAdministrado por {self.administrador}"
            f"\nRiesgo: {Riesgo(self.riesgo).name}, Plazo: "
                  f"{Plazo(self.plazo).name}"
        )
        return string

    @cached_property
    def movs_hist(self)-> pl.DataFrame:
        return self._movs_hist.collect()

    @cached_property
    def _movs_hist(self)-> pl.LazyFrame:
        return _tabla_lf(NomTablas.MOVS).filter(pl.col(PROD_ID) ==
                                                self.producto_id)
        self._calcular_metricas_basicas()
        # self._calcular_xirr_hist()

    @cached_property
    def aportes(self) -> float:
        return (self._movs_hist.filter(
        pl.col("tipo").is_in([m.value for m in MovsAportes]))
                    .select(pl.col("valor").sum().round(2))
                    .collect().item())

    @cached_property
    def intereses (self) -> float:
        return (self._movs_hist
                .filter(pl.col("tipo").is_in([m.value for m in MovsIntereses]))
                .select(pl.col("valor").sum()).collect().item())

    @cached_property
    def saldo(self) -> float:
        return (self._movs_hist.select(pl.col("saldo_hist"))
                .last().collect().item())

    @cached_property
    def rent_acum (self) -> float:
        return float(self.saldo) - float(self.aportes)

    #
    # def _calcular_xirr_hist(self) -> None:
    #     if self.movs_hist.empty:
    #         self.movs_hist["xirr_historica"] = np.nan
    #         self.xirr = np.nan
    #         return
    #
    #     xirr_historica: list[float] = []
    #
    #     for i in range(len(self.movs_hist)):
    #         historial_hasta_fecha: pd.DataFrame = self.movs_hist.iloc[
    #             : i + 1
    #         ].copy()
    #         df_flujos: pd.DataFrame = historial_hasta_fecha[
    #             historial_hasta_fecha["tipo"].isin(MOVS_APORTES)
    #         ].copy()
    #         if df_flujos.empty:
    #             xirr_historica.append(np.nan)
    #             continue
    #
    #         fechas = df_flujos["fecha"].tolist()
    #
    #         valores = (-df_flujos["valor"]).tolist()  # Cambiar signo
    #
    #         fecha_corte = self.movs_hist.iloc[i]["fecha"]
    #         valor_final = self.movs_hist.iloc[i]["saldo_historico"]
    #
    #         fechas.append(fecha_corte)
    #         valores.append(valor_final)
    #
    #         xirr_actual: float = np.nan
    #
    #         try:
    #             resultado: float | None = pyxirr.xirr(fechas, valores)
    #             if (
    #                     resultado is not None
    #                     and not np.isinf(resultado)
    #                     and not np.isnan(resultado)
    #                     and -10 < resultado < 10
    #             ):
    #                 xirr_actual = resultado
    #         except Exception as e:
    #             print(f"Error: {e} en {self.producto_id} al calcular xirr")
    #             print(fechas, valores)
    #             pass
    #
    #         xirr_historica.append(xirr_actual)
    #
    #     self.movs_hist["xirr_historica"] = xirr_historica
    #
    #     xirr_validas: list[float] = [
    #         x for x in xirr_historica if not np.isnan(x)
    #     ]
    #     self.xirr = xirr_validas[-1] if xirr_validas else np.nan
    #
    # def xirr_hist(self) -> pd.DataFrame:
    #     """Retorna el historial de XIRR progresiva como un DataFrame.
    #
    #     Extrae la columna "xirr_historica" del historial de transacciones y la devuelve
    #     como un DataFrame independiente. Esto facilita el análisis y visualización de
    #     la evolución de la rentabilidad del producto a lo largo del tiempo.
    #
    #     Returns:
    #         pd.DataFrame: DataFrame con la columna "xirr_historica" del historial de
    #             transacciones. Si el historial está vacío o no contiene la columna
    #             "xirr_historica", devuelve un DataFrame vacío.
    #
    #     Note:
    #         Este método es útil para acceder a los datos de XIRR histórica sin necesidad
    #         de manipular directamente el historial completo de transacciones.
    #     """
    #     if (
    #             self.movs_hist.empty
    #             or "xirr_historica" not in self.movs_hist.columns
    #     ):
    #         return pd.DataFrame()
    #     else:
    #         return pd.DataFrame(self.movs_hist["xirr_historica"])
