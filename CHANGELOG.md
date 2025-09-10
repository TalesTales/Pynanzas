## 3.2.2 (2025-09-10)

### Fix

- **export**: Se ajustó el nombre de la BD en MD:

## 3.2.1 (2025-09-10)

### Fix

- **version**: se ajustó la VERSION_DDB para que sólo use el primer número de la versión

## 3.2.0 (2025-09-10)

### Feat

- **export**: se agregó la función de exportar ddb a parquet

## 3.1.1 (2025-09-10)

### Fix

- **_cargar_data**: Se corrigió la lógica del flujo de control de cargar data

## 3.1.0 (2025-09-09)

### Feat

- **all**: ahora todo usa duckdb

## 3.0.0 (2025-09-09)

### Feat

- **manipulación**: se agregó función copiar de SQL a DuckDB
- **definicion**: se agregaron funciones de DDL a DuckDB
- **export**: se agregó la opción de usar export a md
- **constantns**: Se agregó MD_TOKEN para usar md:
- **cargar_data**: Se cambió la función de cargar Data de SQLite a DuckDB

### Refactor

- **limpiar_data**: se actualizó el uso de la función cargar_data

## 2.1.2 (2025-09-07)

### Refactor

- **ProductoFinanciero**: Se ajustaron las funciones básicas para usar polars
- **movs_filtrador_prod**: Se re escribió para usar polars

## 2.1.1 (2025-08-28)

### Fix

- **sql/esquemas**: Se agregagó "saldo_hist" al esquema de Mov
- **sql**: todo el pipeline de cargar -> limpiar data ahora devuelve sólo pl.LazyFrames

### Refactor

- **sql/diccionario**: Se agregó la constante URI para poder usar las funciones de polars que hacen uso de una URI

## 2.1.0 (2025-08-26)

### Feat

- **limpiar_data**: Se re-implementó prods_csv_a_df, movs_csv_a_df, prods_sql_a_df y usando LazyFrame y DataFrame desde polars
- **cargar_data**: se empezó a usar scan_csv y read_database desde polars para cargar los datos

## 2.0.0 (2025-08-25)

### Feat

- **Se-agregó-Polars-a-Pynanzas**: Se empezará la migración a Polars

### Fix

- **sql/dicc**: se eliminó un type hint erróneo

### Refactor

- **misc**: cambios menores
- **sql**: reorganizada la manera en la que se dividen las responsabilidades en los .py del submódulo sql

## 1.13.0 (2025-08-23)

### Feat

- **sqlite**: se agregó la función _reset_sql_desde_csv
- **limpiar_data**: Se organizaron las funciones para limpiar los csv y volverlos df funcionales
- **cargar_data**: se cambió el nombre del módulo y se agregó la funcón cargar_csv_a_df y tabla_sql_a_df

### Fix

- **pynanzas**: Se cambió el nombre de Nom_BD a path_db para ser consistente entre el nombre y el contenido
- **sql/esquemas**: se ajustaron los tipos de los esquemas para que puedieran integrarse con cargar_data y limpiar_data
- **sql/diccionario**: se eliminó TABLA_DICC. Innecesaria
- **data_loader**: cambiada función prods_raw_a_df por prods_csv_a_df

## 1.12.0 (2025-08-22)

### Feat

- **data_loader**: Se eliminó la función cargar_datos() y se reemplazó por cargar_csv()

## 1.11.0 (2025-08-21)

### Feat

- **export**: nuevo módulo para exportar a archivos

## 1.10.2 (2025-08-21)

### Fix

- **portafolio**: se corrigió un error en calcular intereses donde no se enconraba "COP" porque ahora las monedas se gestionan con Moneda.COP

## 1.10.1 (2025-08-21)

### Fix

- **sql**: se corrigió un error que ubicaba de manera equivocada el directorio base del main.

## 1.10.0 (2025-08-20)

### Feat

- **BD_SQL**: Se agregó una cosntante que depende de si el entorno es de pruebas o no

## 1.9.0 (2025-08-19)

### Feat

- **sql-consultas**: se agregó un nuevo .py al sub´modulo sql

### Fix

- **portafolio**: saldo total daba cero, pero no se puede dividir por cero

## 1.8.1 (2025-08-19)

### Fix

- **sql/prods**: Corregido un error del DDL de la tabla productos que ordenaba la creación de las columnas Riesgo, Plazo y Liquidez como si fueran texto, pero deben crearse siendo ints

## 1.8.0 (2025-08-19)

### Feat

- **data_loader**: agrega la función tabla_sql_a_df para conectar al lógica de negocio anterior con la persistencia en SQL

## 1.7.1 (2025-08-19)

### Fix

- **sql/movs**: se eliminan las claves "id" y "fecha_agregada" para que SQLite las maneje correctamente

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
