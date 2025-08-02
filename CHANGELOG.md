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
