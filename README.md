# **Pynanzas**.

Un proyecto personal para analizar inversiones financieras.

El módulo usa como entrada archivos CSV o Excel con una estructura predeterminada. El archivo base lo encuentras en
/notas.

Actualmente, el módulo está migrando a SQLite para tener persistencia en la estructura de datos.

## Uso

Actualmente el módulo se uede usar dentro de un .ipynb para la visualización de xirr históricas, el balanceo de saldos,
la identificación de pesos, etc. Toda la lógica actual funciona completamente en memoria haciendo uso de pandas. El
submódulo sql está en construcción y reemplazará el cargar en memoria toda la información.

## Lógica

La unidad de análisis es la clase **ProductoFinanciero** que contiene una los siguientes atributos:

```
python
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

    abierto: bool
    peso: float
    saldo_inicial: float
    saldo_actual: float
    aportes_totales: float
    intereses: float
    rentabilidad_acumulada: float
```

Sobre esta clase se conforma la clase **Portafolio**, con los siguientes atributos:

```
python
        productos: dict[str, ProductoFinanciero]
        id_de_producto_key: str
        total: float
```

Finalmente, a cada ProductoFinanciero se le asocia un historial de transacciones, sobre el cuál se hacen los análisis y
algoritmos correspondientes.

Sobre estas estructuras se ejecutan los métodos y algoritmos de análisis. En este momento son:

- dist_riesgo: analisa el porcentaje de cada Riesgo según el total de los productos de cada uno.
- balancear: dada una cantidad int, se distribuye la misma según las asignaciones de cada ProductoFinanciero.

---

## Notas

Este es un proyecto personal. El diseño prioriza funcionalidades personales frente a las de tipo módulo público. Esto
es, si dentro del desarrollo me encuentro entre una solución sencilla para mis necesidades y una compleja que pueda
usarse tipo API, priorizaré la solución sencilla personal. Por esta razón Pynanzas puede no ser tan flexible como otras
librerías diseñadas para su uso de manera pública.
Aun así, puedes clonar este repositorio a tu gusto.
