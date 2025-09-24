# 🛡️ Lineamientos de Gobernanza de Datos

- Control de versiones: GitHub
- Clasificación de datos: públicos / sensibles / restringidos
- Seguridad: no subir datos sensibles al repo
- Ciclo de vida: ingesta → bronze → silver → gold

# 🛡️ Lineamientos de Gobernanza de Datos

Este documento define las políticas mínimas para garantizar la calidad, seguridad y trazabilidad de los datos dentro del laboratorio.

---

## 1. Origen y Linaje
- Cada dataset debe documentar su **fuente de origen** (URL, repositorio open data, sistema fuente).  
- Se debe mantener un **registro de transformaciones**:  
  - `raw` → datos tal cual.  
  - `bronze` → limpieza mínima (formato homogéneo).  
  - `silver` → normalización canónica.  
  - `gold` → KPIs listos para consumo.  
- El linaje debe quedar reflejado en los notebooks o scripts (logging + README).

---

## 2. Validaciones Mínimas
- Formato de fecha válido (`YYYY-MM-DD`).  
- Columnas obligatorias presentes (`date`, `partner`, `amount`).  
- `amount` numérico y no nulo.  
- Sin duplicados exactos en `silver`.  
- Reglas de negocio documentadas (ej. montos negativos admitidos o no).  

---

## 3. Política de Mínimos Privilegios
- Cada colaborador debe tener **solo los permisos necesarios**:  
  - Lectura → todos los datasets públicos.  
  - Escritura → limitada a su área de trabajo (branch, carpeta).  
  - Producción (deploy Streamlit) → restringido a roles designados.  

---

## 4. Trazabilidad
- Todo dataset procesado debe poder **reconstruirse** a partir de su fuente `raw`.  
- Se recomienda usar **logs** o **metadatos** (ej. `processed_at`, `source_file`, `row_count`) para auditar transformaciones.  
- Cada commit en GitHub debe vincularse a un cambio en el flujo (ej. `ingesta`, `validación`, `normalización`).  

---

## 5. Roles
- **Data Engineer**: diseña y mantiene pipelines de ingesta y transformación.  
- **Data Steward**: vela por la calidad de datos, validaciones y diccionario.  
- **Data Analyst**: construye KPIs y visualizaciones en Streamlit.  
- **Owner/Administrador**: define políticas de seguridad y despliegue.  

---
