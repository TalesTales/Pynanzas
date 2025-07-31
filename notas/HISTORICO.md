# Changelog

# Repo Privado

## V1.0

### V1.0 8 de julio de 2025

- Se desimplementó la tasa de cambio y todo lo relacionado con yfinance

### V 1.0.1

Se pueden ver las XIRR.
Se puede analizar cuánto debo asignar al portafolio para balancear los pesos

## V1.5

### V 1.5 19 julio 2025

Pase todo a módulos de Py y el Jupyter solo ejecuta.

### V 1.6

Revise las funciones de Claude. Deje solo la de Balanceo. La de graficación la
deje que devuelva un dict o DF.

# Repo Público

## V 0.2.x

- Reconstrucción del repositorio para ser público.
- Nombre del repositorio: **Pynanzas**

### 0.2.0

Se reconstruyó el repositorio completamente para hacer público el desarrollo.

### 0.2.1

Portafolio.py: Se ajustaron lógicas internas para calcular .total y .intereses

### 0.2.2

main.py: (en .gitignore) Se organizó la lógica para que solamente sea importar la clase Portafolio y avanzar en el análisis.

resumen_ideavim.md: eliminado

task.md: reestructurado

**init**.py:

- Nuevo DOCSTRING
- Importación específica (no se usa from x import \*)
- Se movió la lógica de cargar_datos() a init para que carguen automáticamente cuando el módulo se cargue en main.py

portafolio.py: se definió **str**
