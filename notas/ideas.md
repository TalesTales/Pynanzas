# Lógica de TRM y tasa de camibio

```Python
def obtener_trm() -> float:
    """Obtiene la Tasa Representativa del Mercado actual en COP."""
    trm: float = 4400
    data_usd: pd.DataFrame = yf.Ticker("USDCOP=X").history(period="5d")
    if not data_usd.empty:
        trm = float(data_usd["Close"].iloc[-1])
        print(f"TRM: desde yfinance COP ${trm:.2f}")
        para
        el
        Jupyter
        return trm
    else:
        # Fallback: usar una tasa fija si no se puede obtener
        print(f"TRM: desde tasa fija COP ${obtener_trm():.2f}")
        para
        el
        Jupyter
        return trm


TRM: float = obtener_trm()


def obtener_tasa_cambio(ticket: Ticker | str) -> float:
    """Obtiene la tasa de cambio actual de la moneda a COP."""
    ticket.upper() if isinstance(ticket, str) else ticket
    tasa_cambio_actual: float = 1
    if ticket == "COP":
        return tasa_cambio_actual

    trm: float = obtener_trm()
    if ticket == "USD":
        return trm

    elif ticket == "BTC":
        Para
        Bitcoin
        a
        COP(vía
        USD)
        ticker_btc_usd: Ticker = yf.Ticker("BTC-USD")
        btc_usd: pd.DataFrame = ticker_btc_usd.history(period="5d")

        if not btc_usd.empty:
            tasa_cambio_actual = float(btc_usd["Close"].iloc[-1]) * trm
        else:
            tasa_cambio_actual = trm
            Valor
            aproximado
        return tasa_cambio_actual
    else:
        Para
        otra
        a
        COP(vía
        USD)
        symbol: str = str(ticket) + "USD=X"
        ticker_moneda_usd: Ticker = yf.Ticker(ticker=symbol)
        moneda_usd: pd.DataFrame = ticker_moneda_usd.history(period="5d")

        if not moneda_usd.empty:
            tasa_cambio_actual = float(moneda_usd["Close"].iloc[-1]) * trm
        else:
            tasa_cambio_actual = trm
        return tasa_cambio_actual


def obtener_precio_actual_mercado(ticker: str, period: str = "1d") -> float:
    """Obtiene el precio actual del instrumento (acción/ETF) desde yfinance."""
    try:
        ticket: Ticker = yf.Ticker(ticker)
        history: pd.DataFrame = ticket.history(period)

        if not history.empty:
            precio_actual_mercado: float = float(history["Close"].iloc[-1])
            return precio_actual_mercado
        else:
            print(f"⚠️ No se pudo obtener precio actual para {ticker}")
            return np.nan
    except Exception as e:
        print(f"❌ Error obteniendo precio para {ticker}: {e}")
        return np.nan


print(obtener_precio_actual_mercado(ticker="AAPL"))


def obtener_precio_historico_mercado(ticker: str, period: str = "1y") -> float:
    """Obtiene el precio actual del instrumento (acción/ETF) desde yfinance."""
    try:
        ticket: Ticker = yf.Ticker(ticker)
        history: pd.DataFrame = ticket.history(period)

        if not history.empty:
            precio_actual_mercado: float = float(history["Close"].iloc[-1])
            return precio_actual_mercado
        else:
            print(f"⚠️ No se pudo obtener precio actual para {ticker}")
            return np.nan
    except Exception as e:
        print(f"❌ Error obteniendo precio para {ticker}: {e}")
        return np.nan


print(yf.scrapers.funds.FundsData("top_holdings", "QTUM"))
```