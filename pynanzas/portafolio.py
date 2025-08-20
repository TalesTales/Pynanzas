import numpy as np
import pandas as pd
from pandas import Series

from pynanzas.analisis import dist_riesgo
from pynanzas.constants import PROD_ID
from pynanzas.producto import ProductoFinanciero


class Portafolio:
    def __init__(
            self,
            df_productos: pd.DataFrame,
            df_transacciones: pd.DataFrame,
            id_de_producto_key: str,
    ) -> None:
        self.productos: dict[str, ProductoFinanciero] = self._crear_portafolio(
            df_productos
        )
        self.id_de_producto_key: str = id_de_producto_key
        self._trans_a_prods(
            df_transacciones=df_transacciones,
            dict_productos=self.productos,
        )
        self.total: float = self._calcular_total()
        self.intereses_total: float = self._calcular_intereses()
        self._calcular_pesos()

    def __str__(self):
        return (
            f"Portafolio: ({len(self.productos)}) productos. COP"
            f"${self.total:,.2f}"
        )  # TODO: asegurar que total se calcule cop

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
                print(
                    f"Portafolio._crear_portafolio. Creado: {producto_id}"
                )  # Test
                productos[str(producto_id)] = nuevo_producto
            return productos

    @staticmethod
    def _trans_a_prods(
            df_transacciones: pd.DataFrame,
            dict_productos: dict[str, ProductoFinanciero],
    ) -> None:
        try:
            for producto_id, objeto_producto in dict_productos.items():
                df_filtrado_para_producto = df_transacciones[
                    df_transacciones[PROD_ID] == producto_id
                    ]
                objeto_producto.procesar_trans(df_filtrado_para_producto)
        except Exception as e:
            error_msg = f"Error inesperado durante la actualización: {str(e)}"
            print(f"Portafolio._trans_a_productos() -> ERROR: {error_msg}")

    def _calcular_total(self) -> float:
        saldos = np.array(
            [
                producto.saldo_actual
                for producto in self.productos.values()
                if producto.moneda == "COP"
            ]
        )
        saldos_validos = saldos[~np.isnan(saldos)]

        total: float = np.sum(saldos_validos)
        return total

    def _calcular_intereses(self) -> float:
        interes = np.array(
            [
                producto.intereses
                for producto in self.productos.values()
                if producto.moneda == "COP"
            ]
        )
        intereses_validos = interes[~np.isnan(interes)]
        total = np.sum(intereses_validos)
        return total

    def _calcular_pesos(self) -> None:
        producto: ProductoFinanciero
        try:
            for producto in self.productos.values():
                if not np.isnan(producto.saldo_actual):
                    producto.peso = producto.saldo_actual / self.total
        except Exception as e:
            print(f"E: Portafolio._calcular_pesos. -> {e}")

    def balancear(self, monto_invertir: float) -> dict[str, float]:
        portafolio_actual: float = self.total
        portafolio_futuro: float = portafolio_actual + monto_invertir
        portafolio = self.productos
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

                # print(f"\n{ticker}:")
                # print(f"  Peso actual: {producto.peso:.2%}")
                # print(f"  Peso objetivo: {producto.asignacion:.2%}")
                # print(f"  Valor actual: ${valor_actual:,.2f}")
                # print(f"  Valor objetivo: ${valor_objetivo:,.2f}")
                # print(f"  Diferencia: ${diferencia:,.2f}")

        diferencias_positivas: dict[str, float] = {
            k: v for k, v in diferencias.items() if v > 0
        }

        suma_diferencias_positivas: float = sum(diferencias_positivas.values())

        distribucion: dict[str, float] = {}

        if suma_diferencias_positivas > 0:
            for ticker, diferencia in diferencias_positivas.items():
                proporcion = diferencia / suma_diferencias_positivas
                monto_asignado = np.trunc(monto_invertir * proporcion)
                distribucion[ticker] = monto_asignado
        else:
            for ticker, producto in portafolio.items():
                if producto.asignacion >= 0 and not np.isnan(
                        producto.saldo_actual
                ):
                    distribucion[ticker] = monto_invertir * producto.asignacion

        # print("DISTRIBUCIÓN SUGERIDA DE LA NUEVA INVERSIÓN:")

        total_distribuido: float = 0
        for ticker, monto in distribucion.items():
            if monto > 0:
                porcentaje = (monto / monto_invertir) * 100
                # print(f"{ticker}: ${monto:,.2f} ({porcentaje:.1f}%)")
                total_distribuido += monto

        # print(f"\nTotal distribuido: ${total_distribuido:,.2f}")
        #
        # print("PESOS RESULTANTES DESPUÉS DE LA INVERSIÓN:")

        for ticker, producto in portafolio.items():
            if producto.asignacion >= 0 and not np.isnan(
                    producto.saldo_actual
            ):
                valor_final = valores_actuales[ticker] + distribucion.get(
                    ticker, 0
                )
                peso_final = valor_final / portafolio_futuro
                diferencia_objetivo = peso_final - producto.asignacion

                # print(f"{ticker}:")
                # print(f"  Peso final: {peso_final:.2%}")
                # print(f"  Objetivo: {producto.asignacion:.2%}")
                # print(f"  Diferencia: {diferencia_objetivo:+.2%}")
        return distribucion

    def xirr_historicas(
            self,
            abiertos: bool | None = True,
            simulados: bool | None = False,
    ) -> pd.DataFrame:
        portafolio: dict[str, ProductoFinanciero] = self.productos
        xirr_historicas_df: pd.DataFrame = pd.DataFrame()

        for i, (ticker, producto) in enumerate(portafolio.items()):
            if abiertos is not None and abiertos != producto.abierto:
                continue

            if simulados is not None and simulados != producto.simulado:
                continue

            if (
                    producto.hist_trans.empty
                    or "xirr_historica" not in producto.hist_trans.columns
            ):
                continue

            producto_xirr = producto.hist_trans[
                ["fecha", "xirr_historica"]
            ].copy()
            producto_xirr = producto_xirr[
                ~producto_xirr["xirr_historica"].isna()
            ]

            if producto_xirr.empty:
                continue
            producto_xirr = producto_xirr.groupby("fecha").last()
            # producto_xirr = producto_xirr.set_index("fecha")
            producto_xirr = producto_xirr.rename(
                columns={"xirr_historica": ticker}
            )

            if xirr_historicas_df.empty:
                xirr_historicas_df = producto_xirr
            else:
                xirr_historicas_df = pd.concat(
                    [xirr_historicas_df, producto_xirr], axis=1
                )

        if not xirr_historicas_df.empty:
            xirr_historicas_df = xirr_historicas_df.sort_index()
            xirr_historicas_df = xirr_historicas_df.ffill()
            # último valor
        return xirr_historicas_df

    def saldos_hist(
            self, abiertos: bool = True, simulados: bool = False
    ) -> pd.DataFrame:
        portafolio = self.productos
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

    def saldos_porcent_hist(
            self, abiertos: bool = True, simulados: bool = False
    ) -> pd.DataFrame:
        saldos: pd.DataFrame = self.saldos_hist(abiertos, simulados)
        totales: Series[float] = self.saldos_hist(abiertos, simulados).sum(
            axis=1
        )
        df_saldos_porcent_hist: pd.DataFrame = saldos.div(totales, axis=0)
        return df_saldos_porcent_hist

    def dist_riesgo(self) -> pd.Series:#TODO: Se puede optimizar
        return dist_riesgo(productos=self.productos)
