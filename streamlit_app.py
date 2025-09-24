import streamlit as st

st.title("Big Data Storage Lab")
st.write("App inicial — conecta con las capas Bronze/Silver y muestra KPIs.")

import streamlit as st
import pandas as pd
from typing import Dict, List

# Importar funciones de los módulos src
from src.transform import normalize_columns, to_silver
from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks

# -------------------------
# Configuración de la app
# -------------------------
st.set_page_config(
    page_title="Big Data Storage Lab",
    layout="wide"
)

st.title("🧪 Big Data Storage Lab")
st.markdown("Pipeline simple: **CSV heterogéneos → Bronze → Silver → KPIs**")

# -------------------------
# Sidebar: configuración
# -------------------------
st.sidebar.header("Configuración de columnas origen")
date_col = st.sidebar.text_input("Columna origen para fecha", value="fecha")
partner_col = st.sidebar.text_input("Columna origen para partner", value="cliente")
amount_col = st.sidebar.text_input("Columna origen para amount", value="importe")

mapping: Dict[str, str] = {
    date_col: "date",
    partner_col: "partner",
    amount_col: "amount",
}

# -------------------------
# Subida de archivos CSV
# -------------------------
uploaded_files = st.file_uploader(
    "Sube uno o varios CSVs",
    type=["csv"],
    accept_multiple_files=True
)

bronze_frames: List[pd.DataFrame] = []

if uploaded_files:
    for file in uploaded_files:
        try:
            # Intentar UTF-8, fallback a latin-1
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding="latin-1")

            # Normalizar columnas
            df = normalize_columns(df, mapping)

            # Añadir linaje
            df = tag_lineage(df, source_name=file.name)

            bronze_frames.append(df)

        except Exception as e:
            st.error(f"Error al procesar {file.name}: {e}")

# -------------------------
# Construcción de Bronze
# -------------------------
if bronze_frames:
    bronze = concat_bronze(bronze_frames)

    st.subheader("📊 Bronze (unificado)")
    st.dataframe(bronze.head(20))

    # Validaciones
    st.subheader("🔎 Validaciones")
    errors = basic_checks(bronze)
    if errors:
        st.error("Se encontraron errores en la validación:")
        for err in errors:
            st.write(f"- {err}")
    else:
        st.success("Validaciones OK. Se puede generar Silver.")

        # -------------------------
        # Construcción de Silver
        # -------------------------
        silver = to_silver(bronze)

        st.subheader("🥈 Silver (partner × mes)")
        st.dataframe(silver.head(20))

        # KPIs simples
        st.subheader("📈 KPIs")
        total_amount = silver["amount"].sum()
        partners_count = silver["partner"].nunique()
        months_count = silver["month"].nunique()

        col1, col2, col3 = st.columns(3)
        col1.metric("Monto total (EUR)", f"{total_amount:,.2f}")
        col2.metric("Partners únicos", partners_count)
        col3.metric("Meses analizados", months_count)

        # Bar chart: mes vs amount
        st.bar_chart(silver.set_index("month")["amount"])

        # -------------------------
        # Descarga de resultados
        # -------------------------
        st.subheader("💾 Descarga de resultados")
        bronze_csv = bronze.to_csv(index=False).encode("utf-8")
        silver_csv = silver.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar Bronze CSV",
            data=bronze_csv,
            file_name="bronze.csv",
            mime="text/csv"
        )

        st.download_button(
            label="Descargar Silver CSV",
            data=silver_csv,
            file_name="silver.csv",
            mime="text/csv"
        )
else:
    st.info("Sube archivos CSV para comenzar el flujo.")
