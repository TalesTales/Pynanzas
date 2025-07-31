# Pyfinanzas Hoja de ruta

## En desarrollo

- [*] Desarrollar la clase Portafolio

## Backlog y parqueadero

### MIS IDEAS

- [ ] Ver la evolución histórica de mi portafolio desde enero de 2025
- [x] Ver la TIR de cada producto y poderla comparar como un DataFrame
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
- [ ] Que le diga al programa cuánto quiero en cada categoría de riesgo y que calcule cuánto debo invertir para rebalancear
- [ ] Calcular la volatilidad de cada producto
- [ ] Calcular la volatilidad de mi portafolio
- [ ] Calcular mi exposición a ciertos tipos de riesgo (riesgo país, riesgo de mercado)
- [ ] Calcular el riesgo total de mi portafolio
- [ ] Calcular métricas avanzadas como el Ratio de Sharpe
- [ ] Saber cuál es la intersección de mis activos en la vida real (ej. si un ETF que poseo ya invierte en una acción que también tengo por separado)
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
- [ ] Crear un dashboard para monitorear el rendimiento del portafolio
- [ ] Añadir capacidades de pronóstico y análisis de escenarios
- [ ] Implementar algoritmos de optimización de portafolio
- [x] Crear un `README.md` completo con la descripción del proyecto, instrucciones de instalación y ejemplos de uso
- [ ] Documentar el esquema de datos y los formatos esperados
- [ ] Crear un diccionario de datos que explique todos los términos financieros utilizados
- [ ] Documentar la arquitectura del proyecto y las decisiones de diseño
- [ ] Generar documentación de la API usando una herramienta como Sphinx
- [x] Crear una estructura de paquete de Python adecuada con archivos `__init__.py`
- [ ] Añadir tests unitarios para todos los módulos, empezando por la funcionalidad principal
- [ ] Implementar un sistema de gestión de configuración (ej. usando archivos `.env`)
- [ ] Crear una interfaz de línea de comandos (CLI) para ejecutar análisis
- [ ] Implementar un almacenamiento en base de datos en lugar de archivos CSV/Excel
- [ ] Optimizar el rendimiento de los cálculos de XIRR para grandes volúmenes de datos
- [ ] Crear contenedores de Docker para la aplicación
- [ ] Configurar integración continua (CI) para tests automáticos
