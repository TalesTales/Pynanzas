

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
                tipo_inversion,
                asignacion
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

    def _filtro(
        self,
        abierto: bool | None  = True,
        riesgo: list[Riesgo] | None = None,
        plazo: list[Plazo] | None = None,
        liquidez: list[Liquidez] | None = None,
        simulado: bool | None = None,
    ) -> pl.LazyFrame:
        prods_lz = self.prods_lz

        if abierto is not None:
            prods_lz = (prods_lz
                        .filter(pl.col(PROD_ID).is_in([p.producto_id for p
                                                    in self.prods.values()
                                                    if p.abierto == abierto])))

        if riesgo is not None:
            valores_riesgo = [r.value for r in riesgo]
            prods_lz = prods_lz.filter(pl.col("riesgo").is_in(valores_riesgo))

        if plazo is not None:
            valores_plazo = [p.value for p in plazo]
            prods_lz = prods_lz.filter(pl.col("plazo").is_in(valores_plazo))

        if liquidez is not None:
            valores_liquidez = [l.value for l in liquidez]
            prods_lz = prods_lz.filter(pl.col("liquidez").is_in(valores_liquidez))

        if simulado is not None:
            prods_lz = prods_lz.filter(pl.col("simulado") == simulado)

        return prods_lz

    def total(self,
              *,
              abierto: bool | None  = True,
              riesgo: list[Riesgo] | None = None,
              plazo: list[Plazo] | None = None,
              liquidez: list[Liquidez] | None = None,
              simulado: bool | None = False
              ) -> float:
        prods = self._filtro(abierto, riesgo, plazo, liquidez, simulado)
        return prods.select(pl.col("saldo")).sum().collect().item()

    def intereses(self,
              *,
              abierto: bool | None = True,
              riesgo: list[Riesgo] | None = None,
              plazo: list[Plazo] | None = None,
              liquidez: list[Liquidez] | None = None,
              simulado: bool | None = False
              ) -> float:
        prods = self._filtro(abierto, riesgo, plazo, liquidez, simulado)
        intereses = [prod.intereses for prod in self.prods.values()
                     if prod.producto_id in (prods
                    .select(pl.col(PROD_ID))
                    .collect().to_series().to_list())]
        return sum(intereses)

    def pesos(self,
              *,
              abierto: bool | None = True,
              riesgo: list[Riesgo] | None = None,
              plazo: list[Plazo] | None = None,
              liquidez: list[Liquidez] | None = None,
              simulado: bool | None = False
              ) -> pl.DataFrame:
        prods = self._filtro(abierto, riesgo, plazo, liquidez, simulado)
        total = self.total(abierto = abierto, riesgo = riesgo,
                           plazo = plazo, liquidez = liquidez,
                           simulado = simulado)
        return (prods.with_columns(((pl.col("saldo").cast(Decimal)/total))
                                   .alias("peso"))
                .select(pl.col(PROD_ID), pl.col("peso"))
                .collect())

    def xirr(self,
              *,
              abierto: bool | None  = True,
              riesgo: list[Riesgo] | None = None,
              plazo: list[Plazo] | None = None,
              liquidez: list[Liquidez] | None = None,
              simulado: bool | None = False
              ) -> pl.DataFrame:
        prods = set(self._filtro(abierto, riesgo, plazo, liquidez,
                              simulado)
                    .select(pl.col(PROD_ID))
                    .collect().to_series().to_list())
        
        return pl.DataFrame({PROD_ID : p.producto_id, 'xirr' :p.xirr} for p in
                             self.prods.values()
                             if p.producto_id in prods)

    def xirr_hist(self,
                  *,
                  abierto: bool | None  = True,
                  riesgo: list[Riesgo] | None = None,
                  plazo: list[Plazo] | None = None,
                  liquidez: list[Liquidez] | None = None,
                  simulado: bool | None = False ) -> pl.DataFrame:

        prods = set(self._filtro(abierto, riesgo, plazo, liquidez,
                              simulado)
                    .select(pl.col(PROD_ID))
                    .collect().to_series().to_list())

        lista_xirr = [p.xirr_hist.rename({'xirr_hist':p.producto_id})
                      for p in self.prods.values()
                      if p.producto_id in prods]

        xirr_hist = pl.concat(lista_xirr, how='align')
        return xirr_hist

    def saldos(
        self,
        *,
        abierto: bool | None  = True,
        riesgo: list[Riesgo] | None = None,
        plazo: list[Plazo] | None = None,
        liquidez: list[Liquidez] | None = None,
        simulado: bool | None = False,
    ) -> pl.DataFrame:
        prods = set(
            self._filtro(abierto, riesgo, plazo, liquidez, simulado)
            .select(pl.col(PROD_ID))
            .collect()
            .to_series()
            .to_list()
        )

        return pl.DataFrame(
            {PROD_ID: p.producto_id, "saldo": p.saldo}
            for p in self.prods.values()
            if p.producto_id in prods
        )

    def saldo_hist(self,
                   *,
                   abierto: bool | None  = True,
                   riesgo: list[Riesgo] | None = None,
                   plazo: list[Plazo] | None = None,
                   liquidez: list[Liquidez] | None = None,
                   simulado: bool | None = False ) -> pl.DataFrame:

        prods = set(self._filtro(abierto, riesgo, plazo, liquidez,
                              simulado)
                    .select(pl.col(PROD_ID))
                    .collect().to_series().to_list())

        lista_saldo = [p.saldo_hist.rename({'saldo_hist':p.producto_id})
                      for p in self.prods.values()
                      if p.producto_id in prods]

        saldo_hist = pl.concat(lista_saldo, how='align')
        return saldo_hist

    def invertir_monto(
        self,
        monto: float,
        balancear: bool = False,
        *,
        abierto: bool | None = True,
        riesgo: list[Riesgo] | None = None,
        plazo: list[Plazo] | None = None,
        liquidez: list[Liquidez] | None = None,
        simulado: bool | None = False,
    ) -> pl.DataFrame:
        # Obtener productos filtrados
        prods = (
            self._filtro(abierto, riesgo, plazo, liquidez, simulado)
            .select(pl.col(PROD_ID), pl.col("saldo"), pl.col("asignacion"))
        ).collect()

        total = prods.select(pl.col("asignacion")).sum().item()
        pesos = self.pesos(
            abierto=abierto,
            riesgo=riesgo,
            plazo=plazo,
            liquidez=liquidez,
            simulado=simulado,
        )

        # Concatenar y calcular diferencias iniciales
        df_prods: pl.DataFrame = pl.concat(
            [prods, pesos], how="align"
        ).with_columns(
            (pl.col("asignacion") / total).alias("asignacion"),
            (pl.col("peso") - (pl.col("asignacion") / total)).alias(
                "diferencia_peso"
            ),
        )

        saldo: float = df_prods.select(pl.col("saldo")).sum().item()
        saldo_final: float = saldo + monto

        if monto == 0:
            return df_prods

        elif monto < 0:
            monto_abs = abs(monto)

            if monto_abs > saldo:
                df_prods = df_prods.with_columns(
                    (pl.col("saldo") * -1).alias("variación"),
                    pl.lit(0).alias("nuevo_saldo"),
                    pl.lit(0.0).alias("nuevo_peso"),
                )
            else:
                df_prods = df_prods.with_columns(
                    (monto * pl.col("asignacion")).round(0).alias("variación")
                )
                df_prods = df_prods.with_columns(
                    (pl.col("saldo") + pl.col("variación")).alias(
                        "nuevo_saldo"
                    )
                )
                df_prods = df_prods.with_columns(
                    (pl.col("nuevo_saldo") / pl.col("nuevo_saldo").sum())
                    .round(4)
                    .alias("nuevo_peso")
                )

            return df_prods

        else:
            if balancear:
                monto_total = saldo_final
                df_prods = df_prods.with_columns(
                    (
                        (monto_total * pl.col("asignacion")).round(0)
                        - pl.col("saldo")
                    ).alias("variación")
                )
                df_prods = df_prods.with_columns(
                    (pl.col("saldo") + pl.col("variación")).alias(
                        "nuevo_saldo"
                    )
                )
                df_prods = df_prods.with_columns(
                    (pl.col("nuevo_saldo") / pl.col("nuevo_saldo").sum())
                    .round(4)
                    .alias("nuevo_peso")
                )

            else:
                df_prods = df_prods.with_columns(
                    (saldo_final * pl.col("asignacion"))
                    .round(0)
                    .alias("saldo_objetivo")
                )
                df_prods = df_prods.with_columns(
                    (pl.col("saldo_objetivo") - pl.col("saldo")).alias(
                        "brecha"
                    )
                )

                suma_brechas = (
                    df_prods.filter(pl.col("brecha") > 0)
                    .select(pl.col("brecha"))
                    .sum()
                    .item()
                )

                if suma_brechas <= monto:
                    excedente = monto - suma_brechas
                    df_prods = df_prods.with_columns(
                        pl.when(pl.col("brecha") > 0)
                        .then(
                            pl.col("brecha")
                            + (excedente * pl.col("asignacion"))
                        )
                        .otherwise(excedente * pl.col("asignacion"))
                        .round(0)
                        .alias("inversion")
                    )

                else:
                    df_prods = df_prods.with_columns(
                        pl.when(pl.col("brecha") > 0)
                        .then(
                            (monto * pl.col("brecha") / suma_brechas).round(0)
                        )
                        .otherwise(0)
                        .alias("inversion")
                    )

                suma_inversiones = (
                    df_prods.select(pl.col("inversion")).sum().item()
                )
                diferencia_redondeo = monto - suma_inversiones

                if diferencia_redondeo != 0:
                    # Ajustar en el producto con mayor brecha positiva
                    max_brecha_filter = df_prods.filter(pl.col("brecha") > 0)

                    if len(max_brecha_filter) > 0:
                        idx_max_brecha = (
                            df_prods.with_row_index()
                            .filter(pl.col("brecha") > 0)
                            .sort("brecha", descending=True)
                            .select("index")
                            .head(1)
                            .item()
                        )

                        df_prods = df_prods.with_columns(
                            pl.when(pl.int_range(pl.len()) == idx_max_brecha)
                            .then(pl.col("inversion") + diferencia_redondeo)
                            .otherwise(pl.col("inversion"))
                            .alias("inversion")
                        )
                    else:
                        idx_max_asig = (
                            df_prods.with_row_index()
                            .sort("asignacion", descending=True)
                            .select("index")
                            .head(1)
                            .item()
                        )

                        df_prods = df_prods.with_columns(
                            pl.when(pl.int_range(pl.len()) == idx_max_asig)
                            .then(pl.col("inversion") + diferencia_redondeo)
                            .otherwise(pl.col("inversion"))
                            .alias("inversion")
                        )

                df_prods = df_prods.with_columns(
                    (pl.col("saldo") + pl.col("inversion")).alias(
                        "nuevo_saldo"
                    )
                )
                df_prods = df_prods.with_columns(
                    (pl.col("nuevo_saldo") / pl.col("nuevo_saldo").sum())
                    .round(4)
                    .alias("nuevo_peso")
                )

            return df_prods


   # diferencia entre pesos y distribucion a df
   # si valor = 0 devuelve filtro quieto

   # si valor en menos 0
   # si balanear = True
   # sumar total portafolio + monto y distribuirlo
   # else
   # distribuir monto

   # si valor es mayor a cero
   # distribuir entre los pesos
   # si balanear = True
   # sumar total portafolio + monto y distribuirlo
   # else
   # distribuir monto

   # devuelve pl.dataframe(prod_id, saldo, variacion, nuevo saldo,
    # asignacion, peso)

if __name__ == '__main__':
    port = Portafolio()
    print(port.xirr(abierto=None))
    print(port.xirr_hist(abierto=None))
    print(port.saldos(abierto=None))
    print(port.saldo_hist(abierto=None))
    print(port.pesos(abierto=None))