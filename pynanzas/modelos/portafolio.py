

from decimal import Decimal

import duckdb
import polars as pl

from pynanzas.dicc import Liquidez, Plazo, Riesgo
from pynanzas.duck.dicc import PATH_DDB, PROD_ID, NomTabla, PathBD
from pynanzas.modelos.producto import ProductoFinanciero


def _crear_portafolio(nom_tabla_prods: NomTabla = NomTabla.PRODS,
                      path_bd: PathBD = PATH_DDB
                      ) -> dict[str, ProductoFinanciero]:
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
            FROM {nom_tabla_prods}
        """).fetchall()
    return {str(prod[0]) : ProductoFinanciero(*prod) for prod in prods}

class Portafolio:
    def __init__(self) -> None:
        self.prods: dict[str,ProductoFinanciero] = _crear_portafolio()
        for producto_id, prod in self.prods.items():
            setattr(self, producto_id, prod)
        self.prods_lz = pl.LazyFrame(prod for prod in self.prods.values())

    def __getitem__(self, key: str) -> ProductoFinanciero:
        return self.prods[key]

    def __iter__(self):
        return iter(self.prods.values())

    def __len__(self):
        return len(self.prods)

    def __getattr__(self, prod: str) -> ProductoFinanciero:
        if prod in self.prods:
            return self.prods[prod]
        raise AttributeError(f"'Portafolio' no tiene producto '{prod}'")

    def __str__(self):
        return (
            f"Portafolio: ({len(self)}) productos. COP"
            f"${self.total:,.2f}"
        )  # TODO: asegurar que total se calcule cop

    @cached_property
    def total(self) -> float:
        return sum(prod.saldo for prod in self.prods.values())

    @cached_property
    def intereses(self) -> float:
        return sum(prod.intereses for prod in self.prods.values())

    def pesos(self, *,
              riesgo: Riesgo | None = None,
              plazo: Plazo | None = None,
              liquidez: Liquidez | None = None,
              simulado: bool | None = None) -> pl.DataFrame:
        df = self.prods_pl

        if riesgo is not None:
            df = df.filter(pl.col("riesgo") == riesgo.value)
        if plazo is not None:
            df = df.filter(pl.col("plazo") == plazo.value)
        if liquidez is not None:
            df = df.filter(pl.col("liquidez") == liquidez.value)
        if simulado is not None:
            df = df.filter(pl.col("simulado") == simulado)

        total = df.select(pl.col("saldo").sum()).item()

        prod_filtrados = set(df.select("producto_id").to_series().to_list())

        return pl.DataFrame([
            {"Prod": p.producto_id,
             "Peso": int(p.saldo) / int(total),
             "Saldo": int(p.saldo)}
            for p in self.prods.values()
            if p.producto_id in prod_filtrados])

    def xirr_historicas(self):
        registros = []
        for p in self.prods.values():
            for fecha, xirr in p.xirr_hist:
                registros.append(
                    {
                        "fecha": fecha,
                        "producto_id": p.producto_id,
                        "xirr": xirr,
                    }
                )

        df = pl.DataFrame(registros)

        df = df.pivot(
            values="xirr", on="fecha", columns="producto_id"
        ).sort("fecha")

        df = df.select(pl.all().forward_fill())

        return df

    #     # Extraer la xirr desde Producto Financierto
    #     # Apendizarla en un df que sea fecha y add column producto id
    #     # ordenar por fecha
    #     # Fill null con anterior

    # def balancear(self, monto_invertir: float) -> dict[str, float]:
    #     portafolio_actual: float = self.total
    #     portafolio_futuro: float = portafolio_actual + monto_invertir
    #     portafolio = self.prods
    #     # Calcular valores objetivos para cada producto
    #     valores_actuales: dict[str, float] = {}
    #     valores_objetivo: dict[str, float] = {}
    #     diferencias: dict[str, float] = {}
    #
    #     for ticker, producto in portafolio.items():
    #         if producto.asignacion >= 0:
    #             valor_actual = producto.saldo
    #             valor_objetivo = portafolio_futuro * producto.asignacion
    #             diferencia = valor_objetivo - valor_actual
    #
    #             valores_actuales[ticker] = valor_actual
    #             valores_objetivo[ticker] = valor_objetivo
    #             diferencias[ticker] = diferencia
    #
    #             # print(f"\n{ticker}:")
    #             # print(f"  Peso actual: {producto.peso:.2%}")
    #             # print(f"  Peso objetivo: {producto.asignacion:.2%}")
    #             # print(f"  Valor actual: ${valor_actual:,.2f}")
    #             # print(f"  Valor objetivo: ${valor_objetivo:,.2f}")
    #             # print(f"  Diferencia: ${diferencia:,.2f}")
    #
    #     diferencias_positivas: dict[str, float] = {
    #         k: v for k, v in diferencias.items() if v > 0
    #     }
    #
    #     suma_diferencias_positivas: float = sum(diferencias_positivas.values())
    #
    #     distribucion: dict[str, float] = {}
    #
    #     if suma_diferencias_positivas > 0:
    #         for ticker, diferencia in diferencias_positivas.items():
    #             proporcion = diferencia / suma_diferencias_positivas
    #             monto_asignado = np.trunc(monto_invertir * proporcion)
    #             distribucion[ticker] = monto_asignado
    #     else:
    #         for ticker, producto in portafolio.items():
    #             if producto.asignacion >= 0 and not np.isnan(producto.saldo):
    #                 distribucion[ticker] = monto_invertir * producto.asignacion
    #
    #     # print("DISTRIBUCIÓN SUGERIDA DE LA NUEVA INVERSIÓN:")
    #
    #     total_distribuido: float = 0
    #     for ticker, monto in distribucion.items():
    #         if monto > 0:
    #             porcentaje = (monto / monto_invertir) * 100
    #             # print(f"{ticker}: ${monto:,.2f} ({porcentaje:.1f}%)")
    #             total_distribuido += monto
    #
    #     # print(f"\nTotal distribuido: ${total_distribuido:,.2f}")
    #     #
    #     # print("PESOS RESULTANTES DESPUÉS DE LA INVERSIÓN:")
    #
    #     for ticker, producto in portafolio.items():
    #         if producto.asignacion >= 0 and not np.isnan(producto.saldo):
    #             valor_final = valores_actuales[ticker] + distribucion.get(
    #                 ticker, 0
    #             )
    #             peso_final = valor_final / portafolio_futuro
    #             diferencia_objetivo = peso_final - producto.asignacion
    #
    #             # print(f"{ticker}:")
    #             # print(f"  Peso final: {peso_final:.2%}")
    #             # print(f"  Objetivo: {producto.asignacion:.2%}")
    #             # print(f"  Diferencia: {diferencia_objetivo:+.2%}")
    #     return distribucion
    # def saldos_hist(self) -> pl.DataFrame:
    #     portafolio = self.prods
    #     historico_acumulado_df: pd.DataFrame = pd.DataFrame()
    #
    #     for i, (ticker, producto) in enumerate(portafolio.items()):
    #         if abiertos is not None and abiertos != producto.abierto:
    #             continue
    #
    #         if simulados is not None and simulados != producto.simulado:
    #             continue
    #
    #         if (
    #             producto._movs_hist.empty
    #             or "saldo_historico" not in producto._movs_hist.columns
    #         ):
    #             continue
    #
    #         producto_saldo = producto._movs_hist[
    #             ["fecha", "saldo_historico"]
    #         ].copy()
    #         producto_saldo = producto_saldo[
    #             ~producto_saldo["saldo_historico"].isna()
    #         ]
    #
    #         if producto_saldo.empty:
    #             continue
    #         producto_saldo = producto_saldo.groupby("fecha").last()
    #         producto_saldo = producto_saldo.rename(
    #             columns={"saldo_historico": ticker}
    #         )
    #
    #         if historico_acumulado_df.empty:
    #             historico_acumulado_df = producto_saldo
    #         else:
    #             historico_acumulado_df = pd.concat(
    #                 [historico_acumulado_df, producto_saldo], axis=1
    #             )
    #
    #     if not historico_acumulado_df.empty:
    #         historico_acumulado_df = historico_acumulado_df.sort_index()
    #         historico_acumulado_df = historico_acumulado_df.ffill()
    #         # último valor
    #     return historico_acumulado_df
    #
    # def saldos_porcent_hist(
    #     self, abiertos: bool = True, simulados: bool = False
    # ) -> pd.DataFrame:
    #     saldos: pd.DataFrame = self.saldos_hist(abiertos, simulados)
    #     totales: Series[float] = self.saldos_hist(abiertos, simulados).sum(
    #         axis=1
    #     )
    #     df_saldos_porcent_hist: pd.DataFrame = saldos.div(totales, axis=0)
    #     return df_saldos_porcent_hist
    #
    # def dist_riesgo(self) -> pd.Series:  # TODO: Se puede optimizar
    #     return dist_riesgo(productos=self.prods)

if __name__ == '__main__':
    port = Portafolio()
    print(port)
    print(port.pesos(riesgo = Riesgo.Bajo, simulado=False))