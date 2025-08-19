## 1.7.0 (2025-08-19)

### Feat

- **pynanzas/init**: se ajustó para agregar mas funciones desde SQL
- **movs**: insertar_movs creada

### Fix

- esquema

## 1.6.2 (2025-08-16)

### Fix

- **sql/base**: se creó un .py llamado base que contiene la clase abstracta EsquemaBase

## 1.6.1 (2025-08-16)

### Refactor

- **sql**: se agregó un nuevo submódulo llamado sql para manejar la lógica de sqlite

## 1.6.0 (2025-08-15)

### Feat

- **sql**: se agregó la función Actualizar_tabla()

## 1.5.0 (2025-08-15)

### Feat

- **diccionario**: creado el archivo diccionario para las Enums del módulo

### Fix

- **sql**: se modificó la lógica para usar Enums
- **diccionario**: implementada toda la lógica de las Enums en diccionario
- **init**: agregado dicionario a la importacion global del modulo

### Refactor

- **producto**: Se modificó Producto para que sea compatible con las Enum
- **constants**: se movio toda la logica de constantes a diccionario

## 1.4.0 (2025-08-13)

### Feat

- **sql**: Se agregaron las clases EsquemasBase(ABC), EsquemaProds y EsquemaMovs para manejar mejor los esquemas de las tablas SQLite
- **constants**: se creó la Enum ColumDDL para tener una enumeración clara en las querys DDL de SQL

## 1.3.0 (2025-08-12)

### Feat

- **sql**: creada la clase DDLProducto y la función insertar_producto

## 1.2.2 (2025-08-12)

### Fix

- **sql**: Se ajustaron todos los parametros para que usen las constantes correctas

### Perf

- **constants**: Se agregaron las constantes BD_TEST, TABLA_PRODS, TABLA_MOVS

## 1.2.1 (2025-08-12)

### Fix

- **constants**: Se cambió la constante PROD_ID a producto_id, para que sea consistente con el SQLite
- **init**: se movió la lógica de cargar datos al notebook

## 1.2.0 (2025-08-09)

### Feat

- **sql**: crear_tabla_trans agregado

## 1.1.0 (2025-08-08)

### Feat

- **sql**: crear_tabla_prods desarrollada

## 1.0.0 (2025-08-08)

### BREAKING CHANGE

- Se va a adoptar un enfoque diferente para no manejar datos en xlsx, sino en sqlite

## 0.12.2 (2025-08-06)

### Refactor

- **analisis**: dist_riesgo ahora es una función fuera del scope de portafolio

## 0.12.1 (2025-08-05)

### Fix

- **portafolio**: balancear ahora se trunca

## 0.12.0 (2025-08-05)

### Feat

- **portafolio**: dist_riesgo ahora devuelve un pd.Series con float de saldo_total

## 0.11.0 (2025-08-05)

### Feat

- **portafolio**: se creó la función dist_riesgo

### Refactor

- **producto**: _str_ actualizado para mostrar un repr según py

## 0.10.0 (2025-08-04)

### Feat

- **portafolio**: se creó la función dist_riesgo

## 0.9.3 (2025-08-04)

### Refactor

- **producto**: _str_ actualizado para mostrar un repr según py

## 0.9.2 (2025-08-04)

### Refactor

- **pynanzas.init**: Se agregaron DF_PRODS, DF_TRANS, PRODU_ID al __all__
- **producto**: __repr__ se @override para representar mejor las instancias de ProductoFinanciero

## 0.9.1 (2025-08-04)

### Refactor

- **producto**: __str__ mejor representado

## 0.9.0 (2025-08-02)

### Feat

- **portafolio**: inicio de función dist_riesgo

### Refactor

- **portafolio**: actualizada __str__

## 0.8.0 (2025-08-01)

### Feat

- **portafolio**: saldos_porcent_hist implementado

## 0.7.0 (2025-07-31)

### Feat

- **portafolio**: Lógica de análisis del portafolio se movió a la clase Portafolio

## 0.6.0 (2025-07-31)

### Feat

- **pynanzas**: PROD_ID agragada como constante del módulo

### Fix

- **portafolio**: _trans_a_prods actualizado para no recibir un df_products sino sólo un id_de_producto: str

## 0.5.1 (2025-07-31)

### Refactor

- **analisis**: balancear_portafolio se movió a portafolio

## 0.5.0 (2025-07-31)

## 0.2.2 (2025-07-31)

### Feat

- **portafolio**: implement __str__ method for object representation

### Fix

- **portafolio**: ajusta cálculo de .total y .intereses
- **datos**: corrige typo y actualiza limpiar_datos.py

### Refactor

- centralize logic in Portafolio class for simplified analysis workflow
- **init**: move data loading logic to module initialization
- **imports**: replace wildcard imports with specific imports

## 0.2.2 (2025-07-31)

### Feat

- **portafolio**: implement __str__ method for object representation

### Fix

- **portafolio**: ajusta cálculo de .total y .intereses
- **datos**: corrige typo y actualiza limpiar_datos.py

### Refactor

- **portafolio**: balancear_portafolio movido de analisis a portafolio
- centralize logic in Portafolio class for simplified analysis workflow
- **init**: move data loading logic to module initialization
- **imports**: replace wildcard imports with specific imports
