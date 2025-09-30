–# Pyfinanzas Hoja de ruta

## En Desarrollo

- [ ] El cálculo de los intereses en ProductoFinanciero es equivocado. Revisar.

## Hecho

- [ ] PRODUCTOS: Agregar holdings
- [ ] PORTAFOLIO: Balancear debe aceptar valores negativos (retiros)
- [ ] Agregar DocString a todo
- [ ] Insertar clase Movimiento
- [ ] Desarrollar una función _eq_ dentro de la clase Movimiento
- [ ] No eliminar Diccionario.csv (buscar forma de generarlo desde py o desde sqlite)
- [ ] Update o guardar los saldos hist y las xirr hist en ddb
- [x] Cada vez que se inserta un movimiento en duckdb se debe actualizar todo el duckdb.
- [x] PORTAFOLIO: Poder filtrar todas las funciones por Plataforma (!), Riesgo, Plazo, etc.
- [x] PORTAFOLIO: reescribir la clase
- [*] PRODUCTO: terminar de pasar todas las funciones a polars. (Por ahora seguir manejando todo en memoria)
    - Ya están todas las funciones escalares. Falta ahora desarrollar las históricas (Saldo y xirr) (mantener en pl(9.
      Después vemos cómo pasarlas a ddb))
- [x] Ingresar transacciones desde lo que hay ahora
- [x] Actualizar la función Insertar_movimiento para usar correctamente ddb
- [x] BUG: se crean dos atributos mov_hist y movs_hist en Producto.
- [x] BUG: -filter( no está filtrando crrectamente)
    - Si reconoce el string "" pero no el valor
- [x] Borrar la lectura de Excel de data_loader
- [x] Dejar solamente lectura de CSV
- [x] Función para exportar los datos a CSV en la carpeta correcta (.data)
- [x] BUG: Cuando se crea la tabla productos las columnas que son enumeraciones se crean como texto
- [x] Eliminar completamente la dependencia de Excel y dejar sólo lectura de CSV.
- [x] BUG: en .portafolio_transacciones_a_productos
- [x] Empezar a usar SQLite
    - [x] Empezar a usar enumeraciones
    - [x] Subir los datos de los productos a la tabla
- [x] Subir transacciones a TABLE movimientos
- [x] Actualizas DDL de TABLE productos
- [x] crear tabla de productos
- [x] Agregar: abierto, saldo, aportes, intereses, rentabilidad, ultima_tran, xirr a la TABLE productos
- [x] Actualizar el esquema de Productos
- [x] Agregar un esquema general
- [x] PORTAFOLIO: ver riesgos: Poder ver en un dict o en print por cada Riesgo, qué porcentaje de mi portafolio hay. De
- [x] BUG: administrador y tipo_inversion no reconocidos por sqlite
- [x] Desarrollar la clase Portafolio
- [x] Ver la TIR de cada producto y poderla comparar como un DataFrame
- [x] Crear un `README.md` completo con la descripción del proyecto, instrucciones de instalación y ejemplos de uso
- [x] Crear una estructura de paquete de Python adecuada con archivos `__init__.py`
- [x] Producto: str que muestre la información completa.

## Backlog y parqueadero

### MIS IDEAS

- BUG: Cuando se envía un NAN a balancear en Portafolio, se le asigna la completa totalidad del saldo
- [ ] ProductoFinanciero o portafolio: encontrar la forma de simular un pd.Dataframe o un ProductoFinanciero despues
  de "balancer" para que pueda ver la dist_riesgo antes y después, todo con filtros.
- [ ] PORTAFOLIO: De pronto la función "balancear" no se llama asi? En cualquier caso, debe tener un varificador de "
  inversión mínima", atada a una propiedad del ProductoFinanciero. Por ejemplo: en TYBA es de COP5000, pero en IBKR
  cambia dependiendo del producto. Esto haría que cuando se ejecute el algoritmo, si la asignación es menor a la
  inversión, se deba transferir esa parte a otra parte del portafolio.
- [ ] PORTAFOLIO: Agregar una función para ver el retorno mensual.
- [ ] PORTAFOLIO: Hacer el total de retorno en un df.
- [ ] Ver la evolución histórica de mi portafolio desde enero de 2025
- [ ] Calcular cuánto puedo retirar (la "regla del 4%")
- [ ] Poder clasificar por tipo de riesgo cómo ha rendido al día de hoy
- [ ] Que pueda ver en un gráfico de torta cómo está conformado hoy y compararlo con otra fecha
- [ ] Ver producto por producto un gráfico de barras por mes que indique el total de aportes y el total de intereses
- [ ] Poder imprimir una ficha técnica de cada producto
- [ ] Que calcule la comisión y el costo real de cada producto financiero
- [ ] Poder incluir fácilmente otros productos para simular o proyectar el siguiente mes
- [ ] Poder comparar un producto real con uno simulado, sobre todo ETFs
- [ ] Saber en qué sector económico estoy invirtiendo, si es posible determinarlo
- [ ] Poder ingresar productos en otras monedas y hacer seguimiento a la tasa de cambio
- [ ] Poder imprimir una ficha técnica de mi portafolio real en PDF
- [ ] Que le diga al programa cuánto quiero en cada categoría de riesgo y que calcule cuánto debo invertir para
  rebalancear
- [ ] Calcular la volatilidad de cada producto
- [ ] Calcular la volatilidad de mi portafolio
- [ ] Calcular mi exposición a ciertos tipos de riesgo (riesgo país, riesgo de mercado)
- [ ] Calcular el riesgo total de mi portafolio
- [ ] Calcular métricas avanzadas como el Ratio de Sharpe
- [ ] Saber cuál es la intersección de mis activos en la vida real (ej. si un ETF que poseo ya invierte en una acción
  que también tengo por separado)
- [ ] Saber mi coeficiente de apalancamiento
- [ ] Saber cuánto deben subir o bajar mis activos para perderlo todo

### IA IDEAS

- [ ] Arreglar los comentarios TODO en el código
- [ ] Implementar `logging` en lugar de usar `print()` para los mensajes de estado y error
- [ ] Implementar decoradores `@property` para los atributos calculados en la clase `ProductoFinanciero`
- [ ] Implementar una estrategia de manejo de errores con excepciones personalizadas
- [ ] Crear un módulo dedicado a la visualización para gráficos e informes
- [ ] Añadir soporte para categorización y etiquetado de transacciones
- [ ] Implementar la exportación de datos a varios formatos (CSV, Excel)
- [ ] Implementar la comparación del rendimiento contra índices de mercado (benchmarking)
- [ ] Añadir soporte para fuentes de datos externas (APIs de datos de mercado)
- [ ] Añadir capacidades de pronóstico y análisis de escenarios
- [ ] Implementar algoritmos de optimización de portafolio
- [ ] Documentar el esquema de datos y los formatos esperados
- [ ] Crear un diccionario de datos que explique todos los términos financieros utilizados
- [ ] Documentar la arquitectura del proyecto y las decisiones de diseño
- [ ] Generar documentación de la API usando una herramienta como Sphinx
- [ ] Añadir tests unitarios para todos los módulos, empezando por la funcionalidad principal
- [ ] Implementar un sistema de gestión de configuración (ej. usando archivos `.env`)
- [ ] Crear una interfaz de línea de comandos (CLI) para ejecutar análisis
- [x] Implementar un almacenamiento en base de datos en lugar de archivos CSV/Excel
- [ ] Optimizar el rendimiento de los cálculos de XIRR para grandes volúmenes de datos
- [ ] Crear contenedores de Docker para la aplicación
- [ ] Configurar integración continua (CI) para tests automáticos
