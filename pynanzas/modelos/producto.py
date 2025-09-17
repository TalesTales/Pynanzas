from dataclasses import dataclass, field
from functools import cached_property

import duckdb
from overrides import override
import polars as pl
import pyxirr

from pynanzas.dicc import (
    Liquidez,
    Moneda,
    MovsAportes,
    MovsIntereses,
    Plazo,
    Riesgo,
)
from pynanzas.duck.dicc import PATH_DDB, PROD_ID, NomTabl, PathBD
from pynanzas.io.limpiar_data import _tabla_lf


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
    asignacion: float = 0
    saldo_inicial: float  = field(init = False, default = 0)

    def __hash__(self):
        return hash(self.producto_id)

    def __eq__(self, other):
        if not isinstance(other, ProductoFinanciero):
            return False
        return self.producto_id == other.producto_id

    @override
    def __repr__(self) -> str:
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
        return self._movs_hist.collect().with_columns(self.xirr_hist)

    @cached_property
    def _movs_hist(self)-> pl.LazyFrame:
        return (_tabla_lf(NomTabl.MOVS)
                .filter(pl.col(PROD_ID) == self.producto_id)
                .sort("fecha")
                .with_columns((pl.col("valor").cum_sum()).alias("saldo_hist")))

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
        return (self._movs_hist.select(pl.col("valor"))
                .sum().collect().item())

    @cached_property
    def saldo_hist(self) -> pl.DataFrame:
        return (self._movs_hist
                .select(pl.col('fecha'), pl.col('saldo_hist'))
                .collect())

    @cached_property
    def abierto(self) -> bool:
        if self.saldo <= 0 or None:
            return False
        else:
            return True

    @cached_property
    def rent_acum (self) -> float:
        return float(self.saldo) - float(self.aportes)

    @cached_property
    def xirr(self) -> float | None:
        df_flujos: pl.LazyFrame = (self._movs_hist
                .filter(pl.col("tipo").is_in([m.value for m in MovsAportes])))

        fechas: list = (df_flujos.select(pl.col("fecha"))
                             .collect().to_series().to_list())
        valores: list[float] = (df_flujos.select(-pl.col("valor"))
                          .collect().to_series().to_list())
        saldo: float = self._movs_hist.select(pl.col("valor")).sum().collect().item()
        fechas.append(fechas[-1])
        valores.append(saldo)
        try:
            return pyxirr.xirr(fechas, valores)
        except Exception as e:
            print(f"Error: {e} en {self.producto_id} al calcular xirr")
            print(fechas, valores)
            pass

    @cached_property
    def xirr_hist(self) -> pl.Series:
        movs_hist = self._movs_hist.collect()
        valores: list[float] = []
        xirr_hist: list[float|None] = []
        fechas_xirr = []
        valores_xirr = []
        for mov in movs_hist.rows(named=True):
            valores.append(mov["valor"])
            saldo = sum(valores)
            if mov['tipo'] in [m.value for m in MovsAportes]:
                try:
                    fechas_xirr.append(mov["fecha"])
                    valores_xirr.append(mov["valor"] * -1)
                    
                    fechas_xirr.append(mov["fecha"])
                    valores_xirr.append(saldo)
                    xirr_hist.append(pyxirr.xirr(fechas_xirr, valores_xirr))
                    fechas_xirr.pop(-1)
                    valores_xirr.pop(-1)
                except Exception as e:
                    print(f"Error: {e} en {self.producto_id} al calcular xirr")
            else:
                if len(xirr_hist) > 0:
                    xirr_hist.append(xirr_hist[-1])
                else:
                    xirr_hist.append(None)
        return pl.Series(xirr_hist).rename("xirr_hist")

    def _reset_cache(self) -> None:
        for attr in list(self.__dict__):
            if isinstance(getattr(type(self), attr, None), cached_property):
                self.__dict__.pop(attr, None)


def fabrica_prod(i,
                 nom_tabl_prods: NomTabl = NomTabl.PRODS,
                 path_bd: PathBD = PATH_DDB):
    with duckdb.connect(path_bd) as con:
        prods = con.sql(f"""
            SELECT
                producto_id,
                nombre,
                ticker,
                simulado,
                moneda,
                riesgo,
                liquidez,
                plazo,
                objetivo,
                administrador,
                plataforma,
                tipo_producto,
                tipo_inversion
            FROM {nom_tabl_prods}
        """).fetchall()
        return ProductoFinanciero(*prods[i])