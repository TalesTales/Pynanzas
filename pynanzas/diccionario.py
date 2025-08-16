from enum import IntEnum, StrEnum


class MovsIntereses(StrEnum):
    """Enum para tipos de movimientos de intereses."""
    INTERESES = "intereses"
    DIVIDENDOS = "dividendos"
    RENDIMIENTOS = "rendimientos"

class MovsAportes(StrEnum):
    """Enum para tipos de movimientos que son aportes."""
    TRANSFERENCIA = "transferencia"
    COMPRA = "compra"
    VENTA = "venta"
    RETIRO = "retiro"
    APERTURA = "apertura"

class MovsNoAportes(StrEnum):
    """Enum para tipos de movimientos que NO son aportes."""
    SALDO_INICIAL = "saldo_inicial"
    COMISIONES = "comisiones"
    COMISION = "comisión"
    IMPUESTO = "impuesto"
    # Movimientos de intereses
    INTERESES = "intereses"
    DIVIDENDOS = "dividendos"
    RENDIMIENTOS = "rendimientos"

class Riesgo(IntEnum):
    Nulo = 0
    Bajo = 1
    Medio = 2
    Alto = 3
    Altisimo = 4

class Liquidez(IntEnum):
    Inmediata = 4
    Alta = 3
    Media = 2
    Baja = 1
    Restringida = 0

class Plazo(IntEnum):
    Inmediato = 0
    Corto = 1
    Mediano = 2
    Largo = 5
    Pension = 10

class Moneda(StrEnum):
    COP = 'cop'
    USD = 'usd'
    GBP = 'gbp'
    EUR = 'eur'
    BTC = 'btc'