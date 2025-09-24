# 📖 Diccionario de Datos

Este documento describe cada campo de los datasets, su tipo de dato y reglas de negocio asociadas.

| Campo        | Tipo       | Descripción                          |
|--------------|------------|--------------------------------------|
| ejemplo_id   | int        | Identificador único del registro     |
| fecha_evento | date       | Fecha en formato ISO (YYYY-MM-DD)    |

# 📖 Diccionario de Datos Canónico

Este documento define el **esquema canónico** utilizado en el laboratorio para normalizar datasets heterogéneos.

---

## Esquema Canónico

| Campo   | Tipo      | Formato/Regla                  | Descripción                                |
|---------|-----------|--------------------------------|--------------------------------------------|
| date    | date      | ISO 8601 (YYYY-MM-DD)          | Fecha del registro (ej. transacción, evento)|
| partner | string    | Texto libre (normalizado a minúsculas) | Nombre de socio/cliente/proveedor |
| amount  | float EUR | Decimal con punto como separador | Monto económico en euros                   |

---

## Mapeos Origen → Canónico

Ejemplos típicos de cómo distintos orígenes se transforman al esquema canónico:

| Origen (campo bruto) | Origen (ejemplo valor) | Canónico (`date`) | Canónico (`partner`) | Canónico (`amount`) |
|-----------------------|------------------------|-------------------|----------------------|---------------------|
| `fecha`              | `12/03/2023`          | `2023-03-12`      | —                    | —                   |
| `cliente`            | `ACME S.A.`           | —                 | `acme s.a.`          | —                   |
| `importe_eur`        | `1.200,50`            | —                 | —                    | `1200.50`           |
| `transaction_date`   | `2023-07-01`          | `2023-07-01`      | —                    | —                   |
| `vendor_name`        | `MegaCorp`            | —                 | `megacorp`           | —                   |
| `amount`             | `750.00`              | —                 | —                    | `750.00`            |

---

## Reglas de Normalización

- **Fechas**: convertir todo a `YYYY-MM-DD`.  
- **Partner**: transformar a minúsculas, eliminar espacios duplicados.  
- **Amount**:  
  - Asegurar tipo `float`.  
  - Reemplazar comas `,` por puntos `.` como separador decimal.  
  - Expresado siempre en **EUR**.  

