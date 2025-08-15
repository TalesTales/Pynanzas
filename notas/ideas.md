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

# Lógica dentro de la clase ProductoFinanciero que implementaré después

    """Bloque heredado de la lógica de las acciones"""

    # precio_promedio_compra: float = field(init=False, default=np.nan)
    # precio_actual_mercado: float = field(init=False, default=np.nan)
    # valor_mercado_actual: float = field(init=False, default=np.nan)
    # historial_precios: pd.DataFrame = field(init=False, default_factory=pd.DataFrame)
    # info: dict[str, str] = field(init=False, default_factory=dict)
    # # volatilidad_total: float = field(init=False, default=np.nan)  # Falta implementar
    # tasa_cambio_actual: float = field(init=False, default=1.0)

# Estructura de esquemas

Desde Claude

```
python
"""
Sistema de esquemas flexible para tablas de base de datos.
Permite usar esquemas por defecto o personalizados de manera transparente.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, List, Type
from enum import Enum
import sqlite3
from .constants import BD_SQLITE, PROD_ID, TABLA_MOVS, TABLA_PRODS


class TipoColumna(Enum):
    """Enum para tipos de columna SQL comunes."""
    INTEGER_PK = "INTEGER PRIMARY KEY"
    INTEGER_PK_AUTO = "INTEGER PRIMARY KEY AUTOINCREMENT"
    TEXT_NOT_NULL = "TEXT NOT NULL"
    TEXT_UNIQUE = "TEXT NOT NULL UNIQUE"
    TEXT_PK = "TEXT NOT NULL PRIMARY KEY"
    REAL = "REAL"
    REAL_NOT_NULL = "REAL NOT NULL"
    REAL_DEFAULT_ZERO = "REAL NOT NULL DEFAULT 0.0"
    BOOLEAN = "BOOLEAN NOT NULL DEFAULT FALSE"
    DATE = "DATE NOT NULL"
    TEXT_DEFAULT = lambda default: f"TEXT NOT NULL DEFAULT '{default}'"


class BaseSchema(ABC):
    """Clase base abstracta para esquemas de tabla."""
    
    @abstractmethod
    def get_columns(self) -> Dict[str, str]:
        """Retorna el diccionario de columnas y sus definiciones SQL."""
        pass
    
    @abstractmethod
    def get_required_columns(self) -> List[str]:
        """Retorna lista de columnas que son obligatorias."""
        pass
    
    def validate_custom_schema(self, custom_columns: Dict[str, str]) -> bool:
        """Valida que un schema personalizado tenga las columnas requeridas."""
        required = set(self.get_required_columns())
        provided = set(custom_columns.keys())
        
        missing = required - provided
        if missing:
            raise ValueError(
                f"Faltan columnas requeridas en schema personalizado: {missing}"
            )
        return True


@dataclass
class SchemaProductos(BaseSchema):
    """Schema para tabla de productos financieros."""
    
    # Columnas requeridas (core business logic)
    producto_id: str = field(default=TipoColumna.TEXT_PK.value)
    nombre: str = field(default=TipoColumna.TEXT_UNIQUE.value)
    
    # Columnas opcionales pero recomendadas
    ticket: str = field(default=TipoColumna.TEXT_UNIQUE.value)
    simulado: str = field(default=TipoColumna.BOOLEAN.value)
    moneda: str = field(default=TipoColumna.TEXT_DEFAULT('cop'))
    riesgo: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    liquidez: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    plazo: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    asignacion: str = field(default=TipoColumna.REAL_DEFAULT_ZERO.value)
    objetivo: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    administrador: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    plataforma: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    tipo_producto: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    tipo_inversion: str = field(default=TipoColumna.TEXT_NOT_NULL.value)

    def get_columns(self) -> Dict[str, str]:
        """Retorna todas las columnas como diccionario."""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }
    
    def get_required_columns(self) -> List[str]:
        """Columnas absolutamente necesarias para el funcionamiento básico."""
        return ['producto_id', 'nombre']

    def keys(self):
        return self.get_columns().keys()
    
    def items(self):
        return self.get_columns().items()
    
    def values(self):
        return self.get_columns().values()
    
    def __len__(self):
        return len(self.get_columns())


@dataclass  
class SchemaMovimientos(BaseSchema):
    """Schema para tabla de movimientos/transacciones."""
    
    # Columnas requeridas
    id: str = field(default=TipoColumna.INTEGER_PK_AUTO.value)
    fecha: str = field(default=TipoColumna.DATE.value)
    tipo: str = field(default=TipoColumna.TEXT_NOT_NULL.value)
    valor: str = field(default=TipoColumna.REAL_NOT_NULL.value)
    
    # Columnas opcionales
    unidades: str = field(default=TipoColumna.REAL.value)
    valor_unidad: str = field(default=TipoColumna.REAL.value)
    
    # El producto_id se agregará dinámicamente
    _producto_id_column: Optional[str] = field(default=None, init=False)
    _producto_id_name: str = field(default=PROD_ID, init=False)
    
    def __post_init__(self):
        """Agrega la columna de producto_id después de inicialización."""
        self._producto_id_column = TipoColumna.TEXT_NOT_NULL.value

    def get_columns(self) -> Dict[str, str]:
        """Retorna todas las columnas incluyendo el producto_id."""
        columns = {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
            if not field.name.startswith('_')
        }
        # Agregar producto_id
        columns[self._producto_id_name] = self._producto_id_column
        return columns
    
    def get_required_columns(self) -> List[str]:
        """Columnas absolutamente necesarias."""
        return ['id', self._producto_id_name, 'fecha', 'tipo', 'valor']

    def keys(self):
        return self.get_columns().keys()
    
    def items(self):
        return self.get_columns().items()
    
    def values(self):
        return self.get_columns().values()
    
    def __len__(self):
        return len(self.get_columns())


class SchemaManager:
    """Gestor de esquemas que permite usar defaults o personalizados."""
    
    @staticmethod
    def resolver_schema_productos(
        schema_personalizado: Optional[Union[Dict[str, str], SchemaProductos]] = None
    ) -> Dict[str, str]:
        """
        Resuelve el schema a usar para productos.
        
        Args:
            schema_personalizado: Puede ser None (usa default), un dict personalizado,
                                o una instancia de SchemaProductos modificada.
        
        Returns:
            Dict con las columnas y definiciones SQL finales.
        """
        if schema_personalizado is None:
            # Usar schema por defecto
            return SchemaProductos().get_columns()
        
        elif isinstance(schema_personalizado, dict):
            # Validar que el dict personalizado tenga columnas requeridas
            schema_default = SchemaProductos()
            schema_default.validate_custom_schema(schema_personalizado)
            return schema_personalizado
        
        elif isinstance(schema_personalizado, SchemaProductos):
            # Usar instancia personalizada de SchemaProductos
            return schema_personalizado.get_columns()
        
        else:
            raise TypeError(
                "schema_personalizado debe ser None, dict, o SchemaProductos"
            )

    @staticmethod
    def resolver_schema_movimientos(
        schema_personalizado: Optional[Union[Dict[str, str], SchemaMovimientos]] = None,
        producto_id_column: str = PROD_ID
    ) -> Dict[str, str]:
        """
        Resuelve el schema a usar para movimientos.
        
        Args:
            schema_personalizado: Schema personalizado o None para default.
            producto_id_column: Nombre de la columna que referencia productos.
        """
        if schema_personalizado is None:
            # Usar schema por defecto
            schema = SchemaMovimientos()
            schema._producto_id_name = producto_id_column
            schema.__post_init__()
            return schema.get_columns()
        
        elif isinstance(schema_personalizado, dict):
            # Validar dict personalizado
            schema_default = SchemaMovimientos()
            schema_default._producto_id_name = producto_id_column
            schema_default.__post_init__()
            schema_default.validate_custom_schema(schema_personalizado)
            return schema_personalizado
        
        elif isinstance(schema_personalizado, SchemaMovimientos):
            # Usar instancia personalizada
            schema_personalizado._producto_id_name = producto_id_column
            schema_personalizado.__post_init__()
            return schema_personalizado.get_columns()
        
        else:
            raise TypeError(
                "schema_personalizado debe ser None, dict, o SchemaMovimientos"
            )


# ===============================
# FUNCIONES DE CREACIÓN DE TABLAS MEJORADAS
# ===============================

def crear_tabla_prods_v2(
    tabla_prods: str = TABLA_PRODS,
    schema: Optional[Union[Dict[str, str], SchemaProductos]] = None,
    nombre_bd: str = BD_SQLITE,
) -> None:
    """
    Crea tabla de productos con schema flexible.
    
    Args:
        tabla_prods: Nombre de la tabla
        schema: Schema a usar (None=default, dict=personalizado, SchemaProductos=instancia)
        nombre_bd: Ruta de la base de datos
    
    Examples:
        # Usar schema por defecto
        crear_tabla_prods_v2()
        
        # Schema completamente personalizado
        crear_tabla_prods_v2(schema={
            'id': 'INTEGER PRIMARY KEY',
            'nombre': 'TEXT NOT NULL',
            'precio': 'REAL'
        })
        
        # Modificar schema por defecto
        schema_custom = SchemaProductos()
        schema_custom.riesgo = "INTEGER NOT NULL"  # cambiar tipo
        crear_tabla_prods_v2(schema=schema_custom)
    """
    
    if not tabla_prods.strip():
        raise ValueError("tabla_prods no puede estar vacío")
    if not nombre_bd.strip():
        raise ValueError("nombre_bd no puede estar vacío")

    # Resolver el schema a usar
    columnas = SchemaManager.resolver_schema_productos(schema)
    
    # Construir DDL
    columnas_ddl = [f"{col} {definicion}" for col, definicion in columnas.items()]
    ddl = ",\n    ".join(columnas_ddl)
    
    # Ejecutar
    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor = conn.cursor()
            query = f"""CREATE TABLE IF NOT EXISTS {tabla_prods} (
    {ddl}
);"""
            cursor.execute(query)
            conn.commit()
            print(f"✅ Tabla {tabla_prods} creada con {len(columnas)} columnas")
            
    except sqlite3.Error as e:
        print(f"❌ Error SQL: {e}")
        raise


def crear_tabla_movs_v2(
    tabla_movs: str = TABLA_MOVS,
    schema: Optional[Union[Dict[str, str], SchemaMovimientos]] = None,
    tabla_prods: str = TABLA_PRODS,
    producto_id_column: str = PROD_ID,
    nombre_bd: str = BD_SQLITE,
) -> None:
    """
    Crea tabla de movimientos con schema flexible y foreign key.
    
    Examples:
        # Default
        crear_tabla_movs_v2()
        
        # Con columnas extra
        schema_custom = SchemaMovimientos()
        schema_custom.descripcion = "TEXT"
        schema_custom.categoria = "TEXT"
        crear_tabla_movs_v2(schema=schema_custom)
    """
    
    # Validaciones
    for nombre, valor in [("tabla_movs", tabla_movs), ("tabla_prods", tabla_prods), ("nombre_bd", nombre_bd)]:
        if not valor.strip():
            raise ValueError(f"{nombre} no puede estar vacío")

    # Resolver schema
    columnas = SchemaManager.resolver_schema_movimientos(schema, producto_id_column)
    
    # Construir DDL con foreign key
    columnas_ddl = [f"{col} {definicion}" for col, definicion in columnas.items()]
    columnas_ddl.append(f"FOREIGN KEY ({producto_id_column}) REFERENCES {tabla_prods} ({producto_id_column})")
    ddl = ",\n    ".join(columnas_ddl)
    
    # Ejecutar
    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor = conn.cursor()
            
            # Asegurar que tabla productos existe
            if not _tabla_existe(cursor, tabla_prods):
                print(f"⚠️  Tabla {tabla_prods} no existe, creándola...")
                crear_tabla_prods_v2(tabla_prods=tabla_prods, nombre_bd=nombre_bd)
            
            query = f"""CREATE TABLE IF NOT EXISTS {tabla_movs} (
    {ddl}
);"""
            cursor.execute(query)
            conn.commit()
            print(f"✅ Tabla {tabla_movs} creada con {len(columnas)} columnas")
            
    except sqlite3.Error as e:
        print(f"❌ Error SQL: {e}")
        raise


def _tabla_existe(cursor: sqlite3.Cursor, nombre_tabla: str) -> bool:
    """Verifica si una tabla existe."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
    return bool(cursor.fetchall())


# ===============================
# EJEMPLOS DE USO
# ===============================

def ejemplos_uso():
    """Ejemplos de cómo usar el sistema flexible."""
    
    print("=== EJEMPLO 1: Schema por defecto ===")
    crear_tabla_prods_v2()
    crear_tabla_movs_v2()
    
    print("\n=== EJEMPLO 2: Schema completamente personalizado ===")
    schema_productos_custom = {
        'producto_id': 'TEXT PRIMARY KEY',
        'nombre': 'TEXT NOT NULL',
        'precio_actual': 'REAL',
        'fecha_creacion': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
    
    schema_movimientos_custom = {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'producto_id': 'TEXT NOT NULL',
        'fecha': 'DATE NOT NULL',
        'tipo_operacion': 'TEXT NOT NULL',
        'cantidad': 'REAL NOT NULL',
        'precio_unitario': 'REAL',
        'comision': 'REAL DEFAULT 0',
        'notas': 'TEXT'
    }
    
    crear_tabla_prods_v2("productos_custom", schema_productos_custom)
    crear_tabla_movs_v2("movimientos_custom", schema_movimientos_custom, "productos_custom")
    
    print("\n=== EJEMPLO 3: Modificar schema por defecto ===")
    schema_modificado = SchemaProductos()
    schema_modificado.riesgo = "INTEGER NOT NULL"  # cambiar a entero
    schema_modificado.fecha_creacion = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"  # agregar nueva columna
    
    crear_tabla_prods_v2("productos_modificado", schema_modificado)


if __name__ == "__main__":
    ejemplos_uso()
```