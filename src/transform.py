# transform.py
# Módulo de normalización y transformaciones hacia Bronze/Silver

def normalize_columns(df):
    """
    Normaliza nombres de columnas (minúsculas, sin espacios).
    """
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

import pandas as pd
from typing import Dict

def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Renombra columnas según un mapping origen→canónico
    y normaliza los campos: date, partner, amount.
    - mapping ejemplo: {"fecha": "date", "cliente": "partner", "importe_eur": "amount"}
    """
    # Renombrar columnas
    df = df.rename(columns=mapping)

    # Normalizar fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", infer_datetime_format=True).dt.date

    # Normalizar partner
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip().str.lower()

    # Normalizar amount
    if "amount" in df.columns:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(".", "", regex=False)   # quitar separador de miles europeo
            .str.replace(",", ".", regex=False)  # convertir coma decimal a punto
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega los datos de bronze → silver:
    - Group by partner + month
    - Suma de amount
    - month como timestamp (primer día del mes)
    """
    if not {"date", "partner", "amount"}.issubset(bronze.columns):
        raise ValueError("Bronze DataFrame debe tener columnas canónicas: date, partner, amount")

    bronze = bronze.copy()
    bronze["date"] = pd.to_datetime(bronze["date"], errors="coerce")
    bronze["month"] = bronze["date"].dt.to_period("M").dt.to_timestamp()

    silver = (
        bronze.groupby(["partner", "month"], as_index=False)["amount"]
        .sum(min_count=1)
    )
    return silver
